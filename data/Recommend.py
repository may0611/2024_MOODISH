import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import re

def extract_ingredients(ingredient_str):

    #집에 대부분 있을것 같은 재료 제외
    common_ingredients = {'소금', '후추', '식용유', '참깨', '물',
                          '올리브유','간장','설탕','참기름','다진마늘','물엿','고추장','고춧가루'}
    
    # 대괄호 안의 내용 제거 및 '|'로 분리
    parts = re.split(r'\[.*?\]|\|', ingredient_str)
    # 각 부분에서 마지막 단어 제거
    cleaned_parts = [
        ' '.join(part.split()[:-1])  # 마지막 단어 제거
        for part in parts if part.strip()  # 빈 문자열 제거
    ]
    # 기본 재료 제거
    result = [
        item for item in ' '.join(cleaned_parts).split() 
        if item not in common_ingredients
    ]
    return ' '.join(result).strip()

def extract_time(time_str):
    if '2시간이상' in time_str:
        return 120
    
    match = re.search(r'(\d+)', time_str)
    if match:
        return int(match.group(1))
    return 0  # 값이 없으면 0을 반환


def Recommend_Function(user_preferences):
    file_path = 'recipe_data.csv'
    data = pd.read_csv(file_path)

    data['ingredient'] = data['ingredient'].apply(extract_ingredients)
    data['time'] = data['time'].apply(extract_time)

    user_time_limit = extract_time(user_preferences['time'])
    user_difficulty = user_preferences['difficult']

    #시간과 난이도 필터링
    data = data[data['time'] <= user_time_limit]
    if user_difficulty != '아무나':
        data = data[data['difficult'] == user_difficulty]

    #벡터화
    vectorizer = TfidfVectorizer()
    vectorizer.fit(data['ingredient'])
    user_ingredients_vector = vectorizer.transform([user_preferences['Ingredient']])


    #재료
    text_features = vectorizer.fit_transform(data['ingredient']).toarray()
    ingredient_similarity = cosine_similarity(user_ingredients_vector, text_features).flatten()


    #감정
    scaler = MinMaxScaler()
    numeric_features = scaler.fit_transform(data[['happy', 'board', 'tired','stress','sad']])

    user_emotion_vector = np.array([user_preferences['happy'], user_preferences['board'], 
                                    user_preferences['tired'], user_preferences['stress'], 
                                    user_preferences['sad']]).reshape(1, -1)

    user_emotion_vector_df = pd.DataFrame(user_emotion_vector, columns=['happy', 'board', 'tired', 'stress', 'sad'])
    user_emotion_vector_scaled = scaler.transform(user_emotion_vector_df)
    emotion_similarity = cosine_similarity(user_emotion_vector_scaled, numeric_features).flatten()


    # 최종 점수 계산
    final_similarity = (0.8 * ingredient_similarity + 0.2 * emotion_similarity)


    data['similarity_score'] = final_similarity
    recommended_recipes = data.sort_values(by='similarity_score', ascending=False)

    return (recommended_recipes[['id', 'name', 'similarity_score']].head(5))

#SVD (유저 데이터가 없어서 지금은 대기)

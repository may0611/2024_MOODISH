import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import re
from scipy.sparse.linalg import svds
from sklearn.metrics import root_mean_squared_error
from pymongo import MongoClient

def extract_ingredients(ingredient_str):

    #집에 대부분 있을것 같은 재료 제외 //조미료
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


def MakeSVDMatrix(recipe_ids,userListed,ratingName):
    user_recipe_matrix = pd.DataFrame(np.nan, index=[user["username"] for user in userListed], columns=recipe_ids)



    for user in userListed:
        username = user["username"]
        rating_str = user.get(ratingName, "")
    
        if not rating_str:
            continue
    
        rating_pairs = rating_str.split("|")
        for pair in rating_pairs:
            try:
                recipe_id_str, rating_value_str = pair.split(":")
                recipe_id = int(recipe_id_str)
                rating_value = int(rating_value_str)

                if recipe_id in recipe_ids:
                    user_recipe_matrix.at[username, recipe_id] = rating_value
            except ValueError:
                pass  # 잘못된 형식 무시

    return user_recipe_matrix



"""EX
UpdateRating("yoon","1234","RatingBored","5")
#유저 아이디(str), 레시피아이디(str), 선택한 감정(str << column이름), 레이팅 점수(int)로 db에 업데이트
"""
def UpdateRating(userid, recipeid, ratingType, ratingNum):
    uri = "mongodb+srv://moodish:U3Z1O83eGzTPQbrb@cluster0.n5s1q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    db = client["test"]
    collection = db["users"]

    user = collection.find_one({"username": userid}, {"_id": 0, ratingType: 1})

    ratingSTR = recipeid + ":" +  ratingNum

    #userid 없음 << 아마 버그
    if user is None:
        return
    
    #rating없음
    elif ratingType not in user or not user[ratingType]:
        #새로운 rating
        collection.update_one(
        {"username": userid},
        {"$set": {ratingType: ratingSTR}}
        )


    #rating 있음
    else:
        existing_rating = user.get(ratingType)

        rating_dict = {}
        if existing_rating:
            for pair in existing_rating.split("|"):
                if ":" in pair:
                    rid, rvalue = pair.split(":")
                    rating_dict[rid] = rvalue

        # 새 rating으로 갱신 (기존에 있던 값은 덮어쓰기됨)
        rating_dict[str(recipeid)] = str(ratingNum)
        updated_rating = "|".join([f"{rid}:{rvalue}" for rid, rvalue in rating_dict.items()])

        collection.update_one(
        {"username": userid},
        {"$set": {ratingType: updated_rating}}
        )

            

def ValidationSVD(selected_recipes,data):
    recipe_ids = selected_recipes['id'].values


    #EX)  <<<각 감정의 rating정보만 가져와서 그걸 rating값으로 이용 (추가예정)
    num_users = 100
    user_ids = list(range(num_users))


    np.random.seed(42)  # 재현성을 위해 랜덤 고정
    values = [np.nan, 1, 2, 3, 4, 5]
    probabilities = [0.9, 0.02, 0.02, 0.02, 0.02, 0.02]

    rating_matrix = np.random.choice(values, size=(len(user_ids), len(recipe_ids)), p=probabilities)
    user_recipe_matrix = pd.DataFrame(rating_matrix, index=user_ids, columns=recipe_ids)

    non_nan_indices = np.argwhere(~np.isnan(user_recipe_matrix.values))
    train_indices, test_indices = train_test_split(non_nan_indices, test_size=0.2, random_state=42)

    # 데이터프레임으로
    user_recipe_matrix = pd.DataFrame(rating_matrix, index=user_ids, columns=recipe_ids)


    train_matrix = user_recipe_matrix.copy()
    for i, j in test_indices:
        train_matrix.iat[i, j] = np.nan
    
    #NAN값은 평균으로
    user_means = user_recipe_matrix.mean(axis=1)  # 각 유저별 평균 계산
    user_recipe_matrix_filled = user_recipe_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

    # SVD 분해
    U, sigma, Vt = svds(user_recipe_matrix_filled.values.astype(float), k=50)

    # 시그마를 대각 행렬로 변환
    sigma = np.diag(sigma)

    # 예측 평점 복구
    predicted_ratings = np.dot(np.dot(U, sigma), Vt)

    
    predicted_df = pd.DataFrame(predicted_ratings, index=user_recipe_matrix.index, columns=user_recipe_matrix.columns)
    #predicted_df += user_means.values.reshape(-1, 1)
    

    #User_id는 user_preferenced의 column으로 있다고 가정
    #점수 계산
    user_svd_scores = predicted_df.loc[user_preferences['user_id']]
    user_svd_scores = user_svd_scores.reset_index()
    user_svd_scores = user_svd_scores.rename(columns={'index': 'id'})
    
    data = data.join(user_svd_scores.set_index('id'), on='id', rsuffix='_svd')

    data = data.fillna(0)

    data.rename(columns={user_preferences['user_id']: "SVD_Score"}, inplace=True)


    actual_ratings = user_recipe_matrix.values.flatten()
    print(user_recipe_matrix)
    print(predicted_df)

    # 예측된 평점
    predicted_ratings_flat = predicted_df.values.flatten()


    # RMSE 계산
    actual = []
    predicted = []
    for i, j in test_indices:
        actual.append(user_recipe_matrix.iat[i, j])
        predicted.append(predicted_df.iat[i, j])

    # RMSE 계산
    rmse = root_mean_squared_error(actual, predicted)
    print("SVD RMSE:", rmse)

    

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
    final_similarity = (0.85 * ingredient_similarity + 0.15 * emotion_similarity)
    
    data['similarity_score'] = final_similarity
    recommended_recipes = data.sort_values(by='similarity_score', ascending=False)

    #return (recommended_recipes[['id', 'name', 'similarity_score']].head(100))


                            #SVD

    #User_Data from Database
    uri = "mongodb+srv://moodish:U3Z1O83eGzTPQbrb@cluster0.n5s1q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    db = client["test"]
    collection = db["users"]
    
    leastNum = 10
            #rating없거나 1개인 유저 제거했는데 N명 이하면 svd진행x
    if collection.count_documents({}) < leastNum:
        return (recommended_recipes[['id', 'name', 'similarity_score']].head(5))
    
    #Processing with UserData and ContentBased
    selected_recipes = recommended_recipes[['id', 'name', 'similarity_score']].head(100)
    recipe_ids = selected_recipes['id'].values


    #성능 검사 (실제 작동에서는 사용x)
    #ValidationSVD(recommended_recipes[['id', 'name', 'similarity_score']].head(100),data)

    """EX
    userListed = [
        {"username": "a", "rating": "6911692:5|1800072:4"},
        {"username": "b", "rating": "1800072:3|4937173:5"},
        {"username": "c", "rating": "4973173:2"},
        {"username": "d", "rating": "6911692:2|1800072:4"},
        {"username": "e", "rating": "4973173:5"},
        {"username": "f", "rating": ""},
    ]
    """

    #이후 새 column 생기면 마저 작성
    #감정에 따라 다른 데이터 불러오기
    if user_preferences['happy'] == 1:
        userListed = list(collection.find({}, {"_id": 0, "username": 1, "RatingHappy":1}))
        user_recipe_matrix = MakeSVDMatrix(recipe_ids,userListed,"RatingHappy")
        
    elif user_preferences['board'] == 1:
        userListed = list(collection.find({}, {"_id": 0, "username": 1, "RatingBored": 1}))
        user_recipe_matrix = MakeSVDMatrix(recipe_ids,userListed,"RatingBored")
        
    elif user_preferences['tired'] == 1:
        userListed = list(collection.find({}, {"_id": 0, "username": 1, "RatingTired": 1}))
        user_recipe_matrix = MakeSVDMatrix(recipe_ids,userListed,"RatingTired")    
    elif user_preferences['stress'] == 1:
        userListed = list(collection.find({}, {"_id": 0, "username": 1, "RatingStress": 1}))
        user_recipe_matrix = MakeSVDMatrix(recipe_ids,userListed,"RatingStress")    
    else:
        userListed = list(collection.find({}, {"_id": 0, "username": 1, "RatingSad": 1}))
        user_recipe_matrix = MakeSVDMatrix(recipe_ids,userListed,"RatingSad")



    #NAN값은 평균으로 (평균이니 rating값이 없거나 1개인 사람 제거)
    rating_counts = user_recipe_matrix.notna().sum(axis=1)
    valid_users = rating_counts[rating_counts >= 2].index
    user_recipe_matrix = user_recipe_matrix.loc[valid_users]
    user_recipe_matrix = user_recipe_matrix.dropna(how='all')


            #rating없거나 1개인 유저 제거했는데 N명 이하면 svd진행x
    if user_recipe_matrix.shape[0] < leastNum:
        return (recommended_recipes[['id', 'name', 'similarity_score']].head(5))

            #user가 rating한 개수 자체가 2개가 안되서 제거 된 경우에도 svd진행 x
    if user_preferences["user_id"] not in user_recipe_matrix.index:
        return (recommended_recipes[['id', 'name', 'similarity_score']].head(5))
        

    user_means = user_recipe_matrix.mean(axis=1)  # 각 유저별 평균 계산
    user_recipe_matrix_filled = user_recipe_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

    # SVD 분해
    U, sigma, Vt = svds(user_recipe_matrix_filled.values.astype(float), k=int(user_recipe_matrix.shape[0]/2))

    # 시그마를 대각 행렬로 변환
    sigma = np.diag(sigma)

    # 예측 평점 복구
    predicted_ratings = np.dot(np.dot(U, sigma), Vt)

    
    predicted_df = pd.DataFrame(predicted_ratings, index=user_recipe_matrix.index, columns=user_recipe_matrix.columns)
    print(predicted_df)

    #User_id는 user_preferenced의 column으로 있다고 가정
    #점수 계산
    user_svd_scores = predicted_df.loc[user_preferences['user_id']]
    user_svd_scores = user_svd_scores.reset_index()
    user_svd_scores = user_svd_scores.rename(columns={'index': 'id'})
    
    data = data.join(user_svd_scores.set_index('id'), on='id', rsuffix='_svd')

    data = data.fillna(0)

    data.rename(columns={user_preferences['user_id']: "SVD_Score"}, inplace=True)


    actual_ratings = user_recipe_matrix.values.flatten()

    # 예측된 평점
    predicted_ratings_flat = predicted_df.values.flatten()


    #값을 MIN-MAX 스케일링으로 0~1 사이 값으로 만듦
    scaler = MinMaxScaler()

    data["SVD_Score"] = scaler.fit_transform(data["SVD_Score"].to_numpy().reshape(-1, 1)).flatten()

    
    data['combined_similarity_score'] = (0.85 * data['similarity_score']) + (0.15 * data["SVD_Score"])


    recommended_recipes = data.sort_values(by='combined_similarity_score', ascending=False)

    return recommended_recipes[['id', 'name', 'combined_similarity_score']].head(5)





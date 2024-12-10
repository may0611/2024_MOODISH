import pandas as pd
from konlpy.tag import Okt
import re

okt = Okt()

# 명사 추출 함수
def extract_nouns(text):
    # 제거할 단어 목록 정의
    remove_words = ['적당', '량', '움큼', '꼬짐', '쪽', '약간', '외', '재료']
    
    # 숫자, 단위, 불필요한 단어들을 제거하는 정규 표현식
    text = re.sub(r'[\d\(\)\[\]|\|개장컵TCR]+', '', text)
    
    # 불필요한 단어 제거
    for word in remove_words:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text)  # \b는 단어 경계를 의미
    
    # 명사 추출
    nouns = okt.nouns(text)
    
    # 명사만 공백으로 이어서 반환
    return ' '.join(nouns).strip()  # 앞뒤 공백 제거

# CSV 파일에서 데이터 읽기
data = pd.read_csv('scanning_receipt/recipe_data.csv')

# 'ingredient' 컬럼에서 명사 추출
data['nouns'] = data['ingredient'].apply(extract_nouns)

# 제거 후 명사만 추출된 데이터만 출력
print(data['nouns'].head())

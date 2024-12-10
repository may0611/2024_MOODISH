#재료 리스트 만들기

import pandas as pd
from konlpy.tag import Okt
import re

okt = Okt()

# 재료 처리 함수
def extract_ingredients(ingredient_str):
    # 집에 대부분 있을 것 같은 재료 제외
    common_ingredients = {'소금', '후추', '식용유', '참깨', '물',
                          '올리브유','간장','설탕','참기름','다진마늘','물엿','고추장','고춧가루'}
    
    # 대괄호 안의 내용 제거 및 '|'로 분리
    parts = re.split(r'\[.*?\]|\|', ingredient_str)
    ingredient_str = re.sub(r'\(.*?\)', '', ingredient_str)  # 소괄호 제거
    
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
    
    return '\n'.join(result).strip()

# CSV 파일에서 데이터 읽기
data = pd.read_csv('scanning_receipt/recipe_data.csv')

# 재료 정리
data['ingredient'] = data['ingredient'].apply(extract_ingredients)

# 결과를 txt 파일로 저장
with open('finalIngredientsList.txt', 'w', encoding='utf-8') as f:
    for line in data['ingredient']:
        f.write(line + '\n')

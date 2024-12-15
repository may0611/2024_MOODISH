import pytesseract
from PIL import Image
from konlpy.tag import Okt

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# 식재료 목록 로드 (프로그램 시작 시 한 번만 실행)
def load_ingredients(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

# 프로그램 시작 시 식재료 리스트를 로드
INGREDIENTS_LIST = load_ingredients('scanning_receipt/finalIngredientsList.txt')

# 식재료 추출 함수
def extract_ingredients(image_path):
    # 이미지 로드
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='kor')

    # 한국어 형태소 분석
    okt = Okt()
    words = [word for word, pos in okt.pos(text) if pos == 'Noun']

    # 추출된 식재료 필터링
    extracted_ingredients = [word for word in words if word in INGREDIENTS_LIST]

    # 중복 제거 및 정리
    unique_ingredients = []
    for ingredient in extracted_ingredients:
        clean_ingredient = ingredient.strip()
        if clean_ingredient and clean_ingredient not in unique_ingredients:
            unique_ingredients.append(clean_ingredient)

    return unique_ingredients

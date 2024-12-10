import pytesseract
from PIL import Image
from konlpy.tag import Okt

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# 이미지 로드
image = Image.open('scanning_receipt/image/receipt1.png')

# OCR을 사용하여 텍스트 추출
text = pytesseract.image_to_string(image, lang='kor')

# ingredients.txt 파일에서 식재료 목록 읽기
def load_ingredients(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

# 파일에서 식재료 목록을 읽어옴
ingredients_list = load_ingredients('scanning_receipt/finalIngredientsList.txt')

# 한국어 형태소 분석
okt = Okt()
words = [word for word, pos in okt.pos(text) if pos == 'Noun']
# 추출된 식재료 필터링
extracted_ingredients = [word for word in words if word in ingredients_list]

# 중복 제거 (순서 유지) 및 불필요한 공백, 특수문자 제거
unique_ingredients = []
for ingredient in extracted_ingredients:
    clean_ingredient = ingredient.strip()  # 공백 제거
    # 특수문자, 숫자 등 불필요한 단어를 제거 (여기서는 한글과 공백만 허용)
    if clean_ingredient and clean_ingredient not in unique_ingredients:
        unique_ingredients.append(clean_ingredient)



print("추출된 식재료:", extracted_ingredients)
print(text)

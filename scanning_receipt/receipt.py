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
ingredients_list = load_ingredients('scanning_receipt/listOfIngredients.txt')

# 한국어 형태소 분석
okt = Okt()
words = [word for word, pos in okt.pos(text) if pos == 'Noun']

# 추출된 식재료 필터링
extracted_ingredients = [word for word in words if word in ingredients_list]

# 추출된 식재료 출력
print("추출된 식재료:", extracted_ingredients)
print(text)

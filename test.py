#기본 영수증 텍스트화 시키기
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

a = Image.open('./image/receipt1.png')

result=pytesseract.image_to_string(a, lang='kor')
print(result) 
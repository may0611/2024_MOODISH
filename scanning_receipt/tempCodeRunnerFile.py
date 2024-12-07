# 파일 읽기
with open('ingredients.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 쉼표 제거 및 단어 처리
unique_words = set()
for line in lines:
    line = line.replace(',', '')  # 기존 쉼표 제거
    words = line.split()          # 공백 기준으로 단어 나누기
    unique_words.update(words)    # 중복 제거를 위해 set에 추가

# 중복 제거된 단어를 정렬하고 줄바꿈 처리
formatted_words = '\n'.join(sorted(unique_words))  # 정렬된 단어를 \n으로 연결

# 결과를 새로운 파일에 저장
with open('listOfIngredients.txt', 'w', encoding='utf-8') as file:
    file.write(formatted_words)

print("변환 완료! 'listOfIngredients.txt'에 저장되었습니다.")

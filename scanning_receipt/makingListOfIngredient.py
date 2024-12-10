# txt 파일에서 중복 제거

import re
def remove_duplicates(input_file, output_file):
    try:
        # 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 중복 제거 및 소괄호 제거
        unique_lines = set(
            re.sub(r'\(.*?\)', '', line).strip()  # 소괄호와 그 안의 내용 제거
            for line in lines
        )
        # 중복 제거 및 정렬 (선택 사항)
        unique_lines = set(line.strip() for line in lines)

        # 결과 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(unique_lines))
        
        print(f"중복 제거 완료! 결과는 '{output_file}'에 저장되었습니다.")
    
    except FileNotFoundError:
        print(f"파일 '{input_file}'을(를) 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 사용 예시
input_file = 'scanning_receipt/IngredientsList.txt'  # 중복을 제거할 파일
output_file = 'scanning_receipt/finalIngredientsList.txt'  # 결과 파일
remove_duplicates(input_file, output_file)

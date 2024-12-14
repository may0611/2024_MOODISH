import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def food_info(name):
    '''
    This function gives you food information for the given input.

    PARAMETERS
        - name(str): name of Korean food in Korean ex) food_info("김치찌개")
    RETURN
        - img_url(str): Image URL of the selected image
    '''

    url = f"https://www.10000recipe.com/recipe/list.html?q={name}"  # 음식 이름을 기반으로 검색 URL 설정
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')  # HTML 파싱
    else:
        print("HTTP response error:", response.status_code)
        return None

    # 모든 이미지 태그 찾기
    img_tags = soup.find_all('img')  # 모든 <img> 태그 찾기

    if len(img_tags) >= 15:  # 이미지가 15개 이상 있는지 확인
        # 기본적으로 15번째 이미지 선택
        img_tag = img_tags[14]
        img_url = img_tag.get('src')

        # 이미지 이름 추출
        img_name = img_tag.get('src', '').split('/')[-1]

        # 이미지 이름에 'icon_vod'가 포함되어 있으면 16번째 이미지 선택
        if 'icon_vod' in img_name and len(img_tags) >= 16:
            print("Skipping 15th image due to 'icon_vod' in name. Trying 16th image.")
            img_tag = img_tags[15]
            img_url = img_tag.get('src')

        if img_url:
            # 이미지 URL이 상대경로일 경우, 절대경로로 변경
            img_url = urljoin(url, img_url)
            return img_url
        else:
            print("No valid image URL found.")
            return None
    else:
        print("There are fewer than 15 images on the page.")
        return None

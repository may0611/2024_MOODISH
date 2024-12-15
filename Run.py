import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from data import Recommend
from fer import test_fer
from scanning_receipt import receipt
from PIL import Image
import io


#cd pra , npm start


app = Flask(__name__)
CORS(app)

#user_input 예시
user_preferences = {
    'Ingredient': '',
    'time': '120', #최소 5
    'difficult': '아무나',#초급 중급 고급 아무나
    'happy' : 1,
    'board' : 0,
    'tired' : 0,
    'stress' : 0,
    'sad' : 0,
}

def Emotion(img):
    if img is None:
        return {"error": "이미지를 불러오지 못했습니다. 경로를 확인하세요."}, 400

    detector = FER()
    results = detector.detect_emotions(img)

    if not results:
        return {"error": "얼굴을 탐지하지 못했거나 감정을 분석하지 못했습니다."}, 404

    response = []
    for face in results:
        response.append({
            "box": face['box'],
            "emotions": face['emotions']
        })

    return response, 200

#추천 시스템
@app.route('/recommend', methods=['POST'])
def recommend_data():
    data = request.get_json()  # 클라이언트에서 보낸 JSON 데이터 받기
    user_input_ingre = data.get('userInput')  # 사용자가 보낸 입력값 받기
    user_input_time = data.get('userInput_time')
    user_input_diffi = data.get('userInput_diffi')

    
    user_preferences['Ingredient'] = user_input_ingre
    user_preferences['time'] = user_input_time
    user_preferences['difficult'] = user_input_diffi

    result = Recommend.Recommend_Function(user_preferences)

    joined_string = '|'.join(result['name'].astype(str))
    print(joined_string)
    print("request check")
    return jsonify({'result': joined_string})
#감정 분석
@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    try:
        # 요청 로그 출력
        print("Request received at /analyze_emotion")

        # 이미지 파일이 요청에 포함되었는지 확인
        if 'image' not in request.files:
            return jsonify({"error": "이미지를 업로드하세요."}), 400

        file = request.files['image']
        print("Image received:", file.filename)

        # 이미지를 OpenCV 형식으로 디코딩
        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        print("Image decoded successfully")

        # 감정 분석 수행
        results, status_code = Emotion(img)

        # 감정 매핑 정의
        emotion_mapping = {
            'happy': 'happy',
            'sad': 'sad',
            'angry': 'anger/stress',
            'fear': 'anger/stress',
            'neutral': 'bored',
            'disgust': 'fatigue'
        }

        # 리스트 형태 결과 처리
        if isinstance(results, list) and len(results) > 0:
            # 첫 번째 객체 가져오기 (여러 객체가 있을 경우 로직 조정 필요)
            primary_result = results[0]
            emotions = primary_result.get('emotions', {})

            # 가장 높은 확률의 감정을 추출
            dominant_emotion = max(emotions, key=emotions.get)

            # 매핑 적용
            mapped_results = {
                "emotion": emotion_mapping.get(dominant_emotion, "unknown"),
            }
        else:
            return jsonify({"error": "감정 분석 결과를 처리할 수 없습니다."}), 500

        print("Mapped emotion results:", mapped_results)

        return jsonify(mapped_results), status_code

    except Exception as e:
        # 예외 발생 시 전체 에러 메시지를 출력
        print("Error occurred:", str(e))
        return jsonify({"error": f"서버 에러: {str(e)}"}), 500

# 영수증 처리 (receiptForFlask.py 활용) API 엔드포인트
@app.route('/receipt', methods=['POST'])
def receipt_data():
    # 클라이언트에서 전송된 영수증 이미지 파일 가져오기
    file = request.files['image']  # 'image'라는 필드에서 파일 받기

    # 이미지 데이터를 임시 파일로 저장하지 않고 메모리 내에서 처리
    image = Image.open(io.BytesIO(file.read()))  # 받은 파일을 BytesIO로 감싸서 Image로 로드

    # receiptForFlask.py의 receipt 함수 호출
    ingredients_list_path = './scanning_receipt/finalIngredientsList.txt'  # 식재료 리스트 파일 경로
    extracted_ingredients = process_receipt(image, ingredients_list_path)  # 식재료 추출 함수 호출

    # 결과를 JSON 형식으로 반환
    return jsonify({"ingredients": extracted_ingredients})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port = 5000)

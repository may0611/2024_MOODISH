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
@app.route('/emtion', methods=['POST'])
def emtion_data():
    data = request.get_json()  # 이미지 형태 (json아닐수도 있음)

    result = test_fer.Emotion(data)

    result2 = result['emotions']

    return jsonify({'emotion': result2}) # return type에 따라 추후 변경

@app.route('/receipt', methods=['POST'])
def receipt_data():
    # 클라이언트에서 보낸 영수증 이미지 받기
    file = request.files['receipt']  # 'receipt'라는 필드에서 파일 받기
    user_input = request.form['userInput']
    user_input_time = request.form['userInput_time']
    user_input_diffi = request.form['userInput_diffi']
    
    # 이미지를 Image 객체로 변환 (PIL 사용)
    image = Image.open(io.BytesIO(file.read()))  # 받은 파일을 BytesIO로 감싸서 Image로 로드

    # 이미지 처리 및 영수증 인식 함수 호출
    result = receipt.receipt_function(image)  # receipt_function에 이미지 전달

    # 결과 반환
    return jsonify({'receipt': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port = 5000)

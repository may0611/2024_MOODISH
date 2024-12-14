import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from data import Recommend
from fer import test_fer
from scanning_receipt import receipt


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

#영수증 인식
@app.route('/receipt', methods=['POST'])
def receipt_data():
    data = request.get_json()  # 이미지 형태 (json아닐수도 있음)

    result = receipt.receipt_function(data)

    return jsonify({'receipt': result}) # return type에 따라 추후 변경

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port = 5000)

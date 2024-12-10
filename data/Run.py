import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import Recommend


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


@app.route('/process', methods=['POST'])
def process_data():
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port = 5000)

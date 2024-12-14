import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from food_img import info


#cd pra , npm start


app = Flask(__name__)
CORS(app)


#사진 이미지 반환
@app.route('/foodImg', methods=['POST'])
def receipt_data():
    data = request.get_json()  #음식 이름
    foodName_get = data.get('foodName')

    res = info.food_info(foodName_get)

    return jsonify({'img_link': res}) # return type에 따라 추후 변경


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port = 5000)

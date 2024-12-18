from datetime import datetime
import os
import subprocess
import json
try:
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI
except:
    os.system('python -m pip install flask')
    os.system('python -m pip install openai')
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI

from analysis_words import ValidateTheEmoGrade
from chance60 import Chance60Service
import random


app = Flask(__name__)

# 設置您的 OpenAI API 密鑰
api_key = "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"

GPT = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('draw_straws.html',  error=None)

@app.route('/ipismysecretandmyaddress')
def ip():
    # 執行命令並捕獲輸出
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
    # 輸出命令執行結果的標準輸出
    print(result.stdout)
    # text = json.dumps(result.stdout)
    return result.stdout

@app.route('/draw_straws', methods=['POST'])
def draw_straws():

    problemSituation = request.json.get('problemSituation')
    if not problemSituation:
        return jsonify({'signPoems': '無事所求，不必問，自有安排，自有分配。'})

    # 使用當天的日期和基數生成隨機種子，以確保每天的運氣是不同的
    random.seed(int(datetime.now().timestamp()))
    
    # 生成一個0到100之間的隨機數，作為運氣指數
    luck_index = random.randint(1, 65)

    # 從future_telling.db取得資料,亂數取出一筆籤詩
    lots = Chance60Service()
    signPoems = lots.GetCardById(luck_index)
    return jsonify({'signPoems': signPoems[1]})

@app.route('/explain', methods=['POST'])
def explain():
    problemSituation = request.json.get('problemSituation')
    signPoems = request.json.get('signPoems')

    if signPoems:
        # 使用 OpenAI API 生成文章大綱
        explain_response = GPT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個命理大師，專門解釋籤詩的含義。"},
                {"role": "user", "content": f"我想詢問:\n\n{problemSituation}。" + f"我抽到的籤詩是:\n\n{signPoems}" + "。以上，請專注在回答從這個籤詩看我想詢問的事項，是好還是壞，請大師幫我說明一下，謝謝。"}
            ]
        )
        explain = explain_response.choices[0].message.content

    # 存入資料庫
    lots = Chance60Service()
    lots.InsertRecord(problemSituation, signPoems, explain)

    return jsonify({'explain': explain})


if __name__ == '__main__':
    app.run()
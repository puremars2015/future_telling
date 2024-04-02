from datetime import datetime
import os
try:
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI
except:
    os.system('pip install flask')
    os.system('pip install openai')
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

@app.route('/draw_straws', methods=['POST'])
def draw_straws():
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
                {"role": "user", "content": f"我想詢問:\n\n{problemSituation}。" + f"我抽到的籤詩是:\n\n{signPoems}" + "請大師幫我說明一下，謝謝。"}
            ]
        )
        explain = explain_response.choices[0].message.content


    return jsonify({'explain': explain})


@app.route('/uploadpage')
def uploadpage():
    return render_template('upload.html',  error=None)


@app.route('/submit_article', methods=['POST'])
def submit_article():
    article_text = request.json.get('article')
    if article_text:
        # 使用 OpenAI API 生成文章大綱
        outline_response = GPT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個文章大綱生成助手。"},
                {"role": "user", "content": f"生成以下文章的大綱:\n\n{article_text}"}
            ]
        )
        outline = outline_response.choices[0].message.content

        # 使用 OpenAI API 分析文章情緒
        sentiment_response = GPT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個文章情緒分析助手,專門分析文章對股市未來狀況的樂觀或悲觀程度。"},
                {"role": "user", "content": f"分析以下文章對股市未來狀況的情緒:\n\n{article_text}"}
            ]
        )
        sentiment = sentiment_response.choices[0].message.content

        # 使用 OpenAI API 根據情緒分析給予打分
        score_response = GPT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個情緒打分助手,根據給定的情緒分析,給予一個 -100 到 100 分的打分,其中 0 分代表持平、100 分代表極端樂觀、-100 分代表極端悲觀。"},
                {"role": "user", "content": f"根據以下情緒分析,給予一個 -100 到 100 分的打分:\n\n{sentiment}"}
            ]
        )
        score = score_response.choices[0].message.content
        
        ntuscore = ValidateTheEmoGrade(sentiment)

        # 返回生成的文章大綱、情緒分析和打分結果
        return jsonify({'outline': outline, 'sentiment': sentiment, 'score': score, 'ntuscore': ntuscore})
    else:
        return jsonify({'error': 'No article text provided'}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # 定義上傳路徑
        upload_folder = 'uploads'
        # 檢查目錄是否存在，不存在則創建
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        # 在指定路徑保存檔案
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        return '檔案上傳成功!'
    else:
        return '沒有上傳檔案'


if __name__ == '__main__':
    app.run(debug=True)
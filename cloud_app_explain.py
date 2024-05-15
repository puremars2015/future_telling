import functions_framework
from datetime import datetime
import os
try:
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI
except:
    os.system('python -m pip install flask')
    os.system('python -m pip install openai')
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI

@functions_framework.http
def explain(request):

    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    problemSituation = request.json.get('problemSituation')
    signPoems = request.json.get('signPoems')

    api_key = "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"
    GPT = OpenAI(api_key=api_key)

    try:
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
    except : 
        explain = 'GPT fail'


    # 存入資料庫
    # lots = Chance60Service()
    # lots.InsertRecord(problemSituation, signPoems, explain)

    return (jsonify({'explain': explain}), 200, headers)


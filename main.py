import os
try:
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI
    import redis
except:
    os.system('pip install flask')
    os.system('pip install openai')
    os.system('pip install redis')
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI
    import redis




app = Flask(__name__)


# 連接到Redis
r = redis.Redis(host='localhost', port=6379, db=0)


# 設置您的 OpenAI API 密鑰
api_key = "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"

GPT = OpenAI(api_key=api_key)

# 登入頁面
@app.route('/')
def index():
    return render_template('index.html',  error=None)

# 登入api
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 從Redis獲取用戶密碼
    stored_password = r.get(email)

    # 檢查用戶名和密碼
    if stored_password and stored_password.decode() == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
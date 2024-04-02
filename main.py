import os
import hashlib

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

# 生成密碼的鹽值
SALT = os.urandom(32)

# 設置您的 OpenAI API 密鑰
api_key = "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"

GPT = OpenAI(api_key=api_key)

def hash_password(password, salt=SALT):
    """使用SHA-256哈希和鹽值對密碼進行哈希"""
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pw_hash.hex()

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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 檢查用戶是否已存在
    if r.exists(email):
        return jsonify({'message': 'User already exists'}), 400

    # 哈希密碼並存儲到Redis
    hashed_password = hash_password(password)
    r.set(email, hashed_password)

    return jsonify({'message': 'Registration successful'}), 201


if __name__ == '__main__':
    app.run(debug=True)
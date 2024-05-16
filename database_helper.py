import sqlite3

# config
databasePath = 'database/memory.db'

def init_db():
    conn = sqlite3.connect(databasePath)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, userId TEXT, role TEXT, context TEXT, createTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def query_command(sql):
    conn = sqlite3.connect(databasePath)
    c = conn.cursor()
    c.execute(sql)
    data = c.fetchall()
    conn.commit()
    conn.close()
    return

def save_context(userId, role, context):
    conn = sqlite3.connect(databasePath)
    c = conn.cursor()
    c.execute("INSERT INTO memory (userId, role, context) VALUES (?, ?, ?)", (userId, role, context))
    conn.commit()
    conn.close()

def load_context(userId):
    conn = sqlite3.connect(databasePath)
    c = conn.cursor()
    c.execute(f"SELECT role, context FROM memory WHERE userId = '{userId}' ORDER BY id")
    data = c.fetchall()
    conn.close()
    # 將資料轉換為所需格式
    converted_data = [{"role": role, "content": content} for role, content in data]
    return converted_data

# 初始化數據庫
init_db()

# 保存上下文
# save_context("User asked about API memory methods.")

# 加載最近的上下文
# recent_context = load_context()

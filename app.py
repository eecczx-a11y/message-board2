from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3
import os
import datetime

app = Flask(__name__)
app.secret_key = "secret_key"

# 数据库路径，保证在 Render 部署时也能找到
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "notice.db")

def init_db():
    """初始化数据库表"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ⭐ 在全局初始化数据库，保证 gunicorn 启动时也会执行
init_db()

@app.route('/')
def home():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template("index.html", messages=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    msg = request.form['message']
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, message, time) VALUES (?, ?, ?)", (name, msg, now))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/api/messages')
def api():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    # 本地调试用
    app.run(debug=True)

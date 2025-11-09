from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3, os, datetime

app = Flask(__name__)
app.secret_key = "secret_key"

# 使用绝对路径，保证 Render 容器中能找到
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "notice.db")

# 初始化数据库和表
def init_db():
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

# 确保数据库初始化在启动时就执行
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

# 生产环境用 Gunicorn，不走 __main__，但本地调试可用
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3, os, datetime

app = Flask(__name__)
app.secret_key = "secret_key"

DB = "notice.db"

# 全局初始化数据库，Render启动时会执行
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, message TEXT, time TEXT)''')
    conn.commit()
    conn.close()

# 在全局直接调用
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

# __main__ 仅用于本地调试
if __name__ == "__main__":
    app.run(debug=True)


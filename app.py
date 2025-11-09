from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_FILE = "data.txt"
MAX_SIZE_MB = 100  # 最大100MB


def get_file_size_mb():
    if not os.path.exists(DATA_FILE):
        return 0
    return os.path.getsize(DATA_FILE) / (1024 * 1024)


def trim_file_if_too_big():
    """当文件超过100MB时，删除最早50%的内容"""
    if get_file_size_mb() > MAX_SIZE_MB:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        mid = len(lines) // 2
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines[mid:])


@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "匿名")
        message = request.form.get("message", "").strip()
        if message:
            with open(DATA_FILE, "a", encoding="utf-8") as f:
                f.write(f"{name}: {message}\n")
            trim_file_if_too_big()
        return redirect(url_for("index"))

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            messages = f.readlines()
    else:
        messages = []

    return render_template("index.html", messages=reversed(messages))


# ✅ 可选：Render健康检查接口
@app.route("/health")
def health_check():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

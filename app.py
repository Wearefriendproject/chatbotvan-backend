from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Dán API key thật của bạn vào đây
GROQ_API_KEY = "AIzaSyA7wDPBfltxUWBO5DLjWPsDWHi37TLzW-U"
GROQ_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent
"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama-3.1-8b-instant",  # ✅ model có thật
        "messages": [
            {"role": "system", "content": "Bạn là chatbot giúp người dùng phân tích bài văn: nêu rõ ưu điểm và nhược điểm cụ thể bằng tiếng Việt."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,  # ✅ Bắt buộc thêm
        "max_tokens": 512     # ✅ Giới hạn độ dài trả lời
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()  # nếu lỗi sẽ nhảy xuống except
        result = response.json()

        # Lấy nội dung phản hồi
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        print("❌ Lỗi khi gọi API:", e)
        return jsonify({"reply": "⚠️ Lỗi khi gọi AI: " + str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)





from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Dán API key của Gemini vào
GEMINI_API_KEY = "AIzaSyA7wDPBfltxUWBO5DLjWPsDWHi37TLzW-U"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY  # ✅ Gemini dùng header này, KHÔNG dùng Bearer
    }

    # ✅ Format dành cho Gemini (không có role, chỉ có "contents")
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Bạn là chatbot giúp người dùng phân tích bài văn: "
                            "nêu rõ ưu điểm và nhược điểm cụ thể bằng tiếng Việt.\n\n"
                            f"Văn bản người dùng gửi: {user_input}"
                        )
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        # ✅ Đường dẫn dữ liệu phản hồi của Gemini
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        print("❌ Lỗi khi gọi API:", e)
        return jsonify({"reply": f"⚠️ Lỗi khi gọi Gemini API: {str(e)}"}), 500
    except Exception as e:
        print("⚠️ Lỗi xử lý phản hồi:", e)
        return jsonify({"reply": "Không thể xử lý phản hồi từ Gemini."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

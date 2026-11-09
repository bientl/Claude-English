"""Bước 1 – Messages API (Domain D2).

Vì sao cần backend Python dù app là HTML?
  API key KHÔNG được để trong trình duyệt (ai cũng xem được bằng F12).
  Trình duyệt gọi /api/explain của server này, server mới giữ key và gọi Anthropic.
  (Đây cũng là một ý của D7 – Security: không lộ secret ở client.)

Chạy:
  pip install -r requirements.txt
  $env:ANTHROPIC_API_KEY = "sk-ant-..."      # PowerShell
  python server.py
  mở http://127.0.0.1:5000
"""
import anthropic
from flask import Flask, jsonify, request, send_from_directory

# Client tự đọc biến môi trường ANTHROPIC_API_KEY.
# SDK tự gửi 3 header bắt buộc: x-api-key, anthropic-version, content-type.
# SDK cũng đã có sẵn max_retries (mặc định 2) và timeout – retry 429/5xx tự động.
client = anthropic.Anthropic()

# Haiku: nhanh và rẻ, đủ cho việc giải nghĩa từ (D5: chọn model theo tác vụ).
MODEL = "claude-haiku-5-5"

# System prompt là tham số `system` RIÊNG, không nằm trong `messages` (bẫy thi D2).
SYSTEM_PROMPT = (
    "Bạn là gia sư tiếng Anh cho người Việt. Với mỗi từ hoặc cụm từ người dùng gửi, "
    "trả lời ngắn gọn bằng tiếng Việt: loại từ, nghĩa, phiên âm, và 2 câu ví dụ tiếng Anh "
    "kèm bản dịch."
)

app = Flask(__name__, static_folder="static")


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/explain")
def explain():
    word = (request.get_json(silent=True) or {}).get("word", "").strip()
    if not word:
        return jsonify(error="Thiếu từ cần giải nghĩa"), 400

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,  # BẮT BUỘC với Messages API
            system=SYSTEM_PROMPT,
            # messages: role user/assistant xen kẽ; content có thể là chuỗi hoặc list content block
            messages=[{"role": "user", "content": word}],
        )
    except anthropic.APIStatusError as e:
        # 4xx (trừ 429) là lỗi request -> sửa request, không retry.
        return jsonify(error=f"Lỗi API {e.status_code}: {e.message}"), 502
    except anthropic.APIConnectionError:
        return jsonify(error="Không kết nối được tới API"), 502

    # response.content là LIST content block; block text có thuộc tính .text
    text = "".join(b.text for b in response.content if b.type == "text")

    return jsonify(
        text=text,
        # stop_reason: end_turn = xong; max_tokens = bị cắt (không phải lỗi!)
        stop_reason=response.stop_reason,
        # usage: dùng để theo dõi chi phí; còn cache_creation/cache_read khi bật caching
        usage={
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    )


if __name__ == "__main__":
    app.run(debug=True)

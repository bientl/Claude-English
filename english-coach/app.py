"""English Coach: backend Flask.

Vì sao cần backend Python dù app là trang web?
  [D7] API key KHÔNG được để trong trình duyệt (ai cũng xem được bằng F12).
  Trình duyệt chỉ gọi các route /api/... của server này. Server mới giữ key và gọi Anthropic.

Chạy (từ thư mục english-coach/):
  python app.py
  mở http://127.0.0.1:5000
"""
import os
import sys

import anthropic
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

# Terminal Windows mặc định dùng cp1252, print tiếng Việt sẽ lỗi UnicodeEncodeError.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# [D7] Đọc ANTHROPIC_API_KEY và CLAUDE_MODEL từ file .env (không hard-code key trong code).
# load_dotenv() KHÔNG ghi đè biến môi trường đã có sẵn.
load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    # [D7] Chỉ báo là thiếu key, tuyệt đối không in giá trị key ra log.
    print("CẢNH BÁO: chưa có ANTHROPIC_API_KEY. Hãy tạo file .env từ .env.example.")

# [D5] Model đọc từ biến môi trường, mặc định Haiku (nhanh, rẻ).
MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")

# Client tự đọc ANTHROPIC_API_KEY từ biến môi trường.
# Bước 1 sẽ chuyển phần này sang client.py, ghi rõ max_retries và timeout.
client = anthropic.Anthropic()

# Các chế độ của app. Trang web dựng menu từ danh sách này.
# done=False nghĩa là chưa làm: route của chế độ đó trả "chưa làm".
MODES = [
    {"id": "explain", "name": "Giải nghĩa từ (bản thử)", "domains": "D2", "done": True},
    {"id": "chat", "name": "Hội thoại (streaming)", "domains": "D2, D6", "done": False},
    {"id": "grammar", "name": "Sửa ngữ pháp (JSON)", "domains": "D2, D6", "done": False},
    {"id": "reading", "name": "Bài đọc (prompt caching)", "domains": "D5", "done": False},
    {"id": "vocab", "name": "Tra từ (tool use)", "domains": "D8, D1", "done": False},
    {"id": "essay", "name": "Chấm bài viết (workflow)", "domains": "D1, D5", "done": False},
]

app = Flask(__name__, static_folder="static")


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/modes")
def list_modes():
    return jsonify(modes=MODES, model=MODEL)


@app.post("/api/explain")
def explain():
    """Bản thử từ commit đầu. Bước 1 sẽ viết lại bằng call_claude() trong client.py."""
    word = (request.get_json(silent=True) or {}).get("word", "").strip()
    if not word:
        return jsonify(error="Thiếu từ cần giải nghĩa"), 400

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,  # [D2] BẮT BUỘC với Messages API
            # [D2] system là tham số RIÊNG, không nằm trong messages
            system=(
                "Bạn là gia sư tiếng Anh cho người Việt. Với mỗi từ hoặc cụm từ người dùng gửi, "
                "trả lời ngắn gọn bằng tiếng Việt: loại từ, nghĩa, phiên âm, và 2 câu ví dụ "
                "tiếng Anh kèm bản dịch."
            ),
            messages=[{"role": "user", "content": word}],
        )
    except anthropic.APIStatusError as e:
        return jsonify(error=f"Lỗi API {e.status_code}: {e.message}"), 502
    except anthropic.APIConnectionError:
        return jsonify(error="Không kết nối được tới API"), 502

    # [D2] response.content là LIST content block; chỉ lấy các block text
    text = "".join(b.text for b in response.content if b.type == "text")
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    print(f"[explain] stop_reason={response.stop_reason} usage={usage}")
    return jsonify(text=text, stop_reason=response.stop_reason, usage=usage)


@app.post("/api/<mode_id>")
def not_done(mode_id):
    # Route chung cho các chế độ chưa làm (Flask ưu tiên route /api/explain cụ thể ở trên).
    return jsonify(error=f"Chế độ '{mode_id}' chưa làm."), 501


if __name__ == "__main__":
    app.run(debug=True)

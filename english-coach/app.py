"""English Coach: backend Flask.

Vì sao cần backend Python dù app là trang web?
  [D7] API key KHÔNG được để trong trình duyệt (ai cũng xem được bằng F12).
  Trình duyệt chỉ gọi các route /api/... của server này. Server mới giữ key và gọi Anthropic.

Chạy (từ thư mục english-coach/):
  python app.py
  mở http://127.0.0.1:5000
"""
import os

from flask import Flask, jsonify, request, send_from_directory

# client.py đã load .env, ép stdout UTF-8, và gọi API bằng HTTP thô (không SDK).
from client import ApiError, ConnectionFailed, MODEL, call_claude, get_text, stop_reason_notice, usage_dict

if not os.environ.get("ANTHROPIC_API_KEY"):
    # [D7] Chỉ báo là thiếu key, tuyệt đối không in giá trị key ra log.
    print("CẢNH BÁO: chưa có ANTHROPIC_API_KEY. Hãy tạo file .env từ .env.example.")

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
    """Giải nghĩa từ, gọi Claude qua call_claude() (client.py)."""
    word = (request.get_json(silent=True) or {}).get("word", "").strip()
    if not word:
        return jsonify(error="Thiếu từ cần giải nghĩa"), 400

    try:
        # [D2] call_claude tự log stop_reason + usage ra terminal
        response = call_claude(
            system=(
                "Bạn là gia sư tiếng Anh cho người Việt. Với mỗi từ hoặc cụm từ người dùng gửi, "
                "trả lời ngắn gọn bằng tiếng Việt: loại từ, nghĩa, phiên âm, và 2 câu ví dụ "
                "tiếng Anh kèm bản dịch."
            ),
            messages=[{"role": "user", "content": word}],
            max_tokens=500,
        )
    except ApiError as e:
        return jsonify(error=f"Lỗi API {e.status_code} ({e.error_type}): {e.message}"), 502
    except ConnectionFailed as e:
        return jsonify(error=str(e)), 502

    return jsonify(
        text=get_text(response),
        stop_reason=response["stop_reason"],
        notice=stop_reason_notice(response),
        usage=usage_dict(response),
    )


@app.post("/api/<mode_id>")
def not_done(mode_id):
    # Route chung cho các chế độ chưa làm (Flask ưu tiên route /api/explain cụ thể ở trên).
    return jsonify(error=f"Chế độ '{mode_id}' chưa làm."), 501


if __name__ == "__main__":
    # [D7] Bind tường minh 127.0.0.1: chỉ máy này truy cập được, không lộ ra mạng LAN.
    app.run(host="127.0.0.1", port=5000, debug=True)

# Lịch sử dự án English Coach

Mỗi lần tổng hợp thêm một mục mới **ở trên cùng**, ghi timestamp (giờ Việt Nam, +07:00).

---

## 2026-11-11 17:46 (+07:00): kế hoạch mới + Bước 0

**Kế hoạch (CLAUDE.md)**
- Thêm mục 0 "Trạng thái repo hiện tại" để phiên sau biết code đang ở đâu, cách chạy, và tài liệu trong `Document/`.
- Người dùng chốt ba quyết định:
  - App là **web có UI căn bản** (Flask + một trang HTML, JS thuần), không làm CLI.
  - Toàn bộ code đặt trong thư mục con **`english-coach/`**. CLAUDE.md và `Document/` vẫn ở gốc repo.
  - Thêm `pause_turn` vào danh sách `stop_reason` ở Bước 1.
- Sửa các mục 2, 3, 4, Bước 0 và Bước 2 của CLAUDE.md cho khớp: "in ra" nghĩa là hiện trên web và log ra terminal; stream đi từ Flask xuống trình duyệt; lịch sử chat giữ ở trình duyệt.

**Bước 0: dựng khung dự án [D7, D5]**
- `git mv` code cũ vào `english-coach/`: `server.py` thành `app.py`, cùng với `static/` và `requirements.txt`.
- `app.py`: đọc `.env` bằng `python-dotenv`, model lấy từ `CLAUDE_MODEL` (mặc định `claude-haiku-5-5`). Danh sách `MODES` quyết định menu trên web (`GET /api/modes`). Chế độ chưa làm trả 501 "chưa làm". Chế độ "Giải nghĩa từ" cũ vẫn giữ, Bước 1 sẽ viết lại.
- `static/index.html`: menu 6 chế độ, chế độ chưa làm hiện "Chưa làm.".
- Tạo `.env.example`, `NOTES_LOI_SAI.md`, `requirements.txt` (thêm `python-dotenv`), các thư mục `modes/`, `security/`, `data/`, `experiments/`.
- Tạo venv `english-coach/.venv`, cài `anthropic` 2.8.0, `flask`, `python-dotenv`.
- **Lỗi gặp phải:** terminal Windows dùng cp1252 nên `print` tiếng Việt crash (`UnicodeEncodeError`). Sửa bằng `sys.stdout.reconfigure(encoding="utf-8")`.
- **Kiểm tra:** dùng `app.test_client()` (không gọi API thật). `GET /` 200, `GET /api/modes` trả đủ 6 chế độ, `POST /api/chat` 501, `POST /api/explain` khi thiếu từ trả 400.

**Đang chờ**
- Người dùng tạo `.env`, chạy `python app.py`, xác nhận thấy menu và gọi thử API.
- Người dùng trả lời 3 câu trắc nghiệm của Bước 0 (D7: giữ key ở backend, xử lý key bị lộ; D5: đọc model từ cấu hình).
- Chưa commit thay đổi của phiên này.

---

## 2026-11-09 23:57 (+07:00): commit đầu tiên (437528c)

- App Flask giải nghĩa từ bằng Messages API (`server.py`, `static/index.html`): trả về `text`, `stop_reason`, `usage`.
- Thêm tài liệu ôn thi trong `Document/`: note 8 domain, cẩm nang kiến thức, đề thi bản tiếng Việt.
- Timestamp lấy từ thời điểm commit.

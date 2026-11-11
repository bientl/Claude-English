# Lịch sử dự án English Coach

Mỗi lần tổng hợp thêm một mục mới **ở trên cùng**, ghi timestamp (giờ Việt Nam, +07:00).

---

## 2026-11-12 00:14 (+07:00): Bước 1 làm dở, chuyển `client.py` sang HTTP thô (không SDK)

**Quy tắc mới (CLAUDE.md mục 2):** người dùng tự viết code. Agent chỉ được tạo/sửa file khi người dùng nói rõ "viết đi", "sửa đi" cho đúng việc đó. Lệnh chung như "làm Bước X" không tính.

**Quyết định của người dùng:** tự viết phần gọi API **không dùng anthropic SDK** để hiểu cơ chế bên dưới.
- `english-coach/client_sdk.py`: bản dùng SDK, giữ lại để đối chiếu. Đặt tên gạch dưới vì tên có gạch ngang thì Python không `import` được.
- `english-coach/client.py`: viết lại bằng `urllib`, không phụ thuộc `anthropic`.
  - `_post()` gửi `POST https://api.anthropic.com/v1/messages` với 3 header `x-api-key`, `anthropic-version: 2023-06-01`, `content-type`.
  - `response` là dict JSON gốc (`response["stop_reason"]`, không còn `response.stop_reason`).
  - Hai exception tự định nghĩa: `ApiError` (có `status_code`, `error_type`, `request_id`) cho lỗi HTTP, `ConnectionFailed` cho lỗi mạng/timeout/thiếu key.
  - **Không còn retry tự động** (SDK từng tự retry 429, 5xx). Retry sẽ tự viết ở Bước 4.
  - Vẫn giữ: ép UTF-8, đọc `MODEL` từ `CLAUDE_MODEL`, vòng lặp `pause_turn` (tối đa 5 lần), xử lý đủ 7 `stop_reason`.
- `english-coach/app.py`: bỏ `import anthropic`, bắt `ApiError`/`ConnectionFailed`, đọc `response["stop_reason"]`. Flask bind tường minh `host="127.0.0.1", port=5000`.

**Kiến thức đã học trong phiên**
- [D2] `max_tokens` là tham số bắt buộc, thiếu thì API trả 400.
- [D2] `stop_reason == "max_tokens"` là HTTP 200, không phải lỗi. `usage` và `stop_reason` do API trả về.
- [D2] 401 không retry vì request giữ nguyên thì vẫn lỗi. SDK chỉ retry lỗi kết nối, timeout, 408, 409, 429, 5xx.
- [D7] Key nằm ở backend, trình duyệt chỉ gọi `/api/...`.
- Python căn bản cho người đã biết .NET: `import`, `os.environ.get`, `load_dotenv`, class kế thừa `Exception`.

**Lỗi gặp phải:** `'dict' object has no attribute 'stop_reason'`. Nguyên nhân là hai bản `app.py` chạy song song trên cổng 5000, bản cũ còn giữ code cũ trong bộ nhớ. Sửa bằng cách tắt hết tiến trình Python rồi chạy lại một bản.

**Kiểm tra:** dùng mock `client._post` với `app.test_client()` cho ba trường hợp (thành công kèm `max_tokens`, lỗi 401, lỗi kết nối). Cả ba đúng. Người dùng chạy thử chế độ "Giải nghĩa từ" trên web, gặp lỗi ở trên. Chưa xác nhận lại sau khi chạy một bản duy nhất.

**Còn thiếu của Bước 1** (người dùng tự code):
- Đọc `request-id` và header `anthropic-ratelimit-*-remaining` từ `res.headers`.
- Đo latency (ms).
- Hàm `count_tokens()` (Token Counting API) và hiện "ước tính X / thực tế Y token" trên trang.
- Trả đủ các thông tin trên về `static/index.html`.

**Đang chờ**
- Câu hỏi đoán trước: người dùng đã trả lời 3 câu (thiếu `max_tokens`: sai; `max_tokens=20`: đúng một nửa; sai key có retry không: đúng). Ghi vào `NOTES_LOI_SAI.md` sau khi xong Bước 1.
- 3 câu trắc nghiệm của Bước 1 chưa ra.

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

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# English Coach: app học tiếng Anh dùng Claude API (dự án ôn thi CCDV-F)

> **Gửi agent trong VS Code:** đọc hết file này trước khi viết code.
> Dự án này **không** nhằm làm ra một app đẹp. Mục tiêu là giúp người dùng **đậu kỳ thi Claude Certified Developer – Foundations (CCDV-F) vào ngày 30/11/2026**. Mỗi tính năng là một bài lab để luyện một phần kiến thức trong đề thi.

## 0. Trạng thái repo hiện tại (cập nhật mục này sau mỗi bước)

**Đã chốt với người dùng (11/11):** app là web có UI căn bản (Flask + một trang HTML), code đặt trong thư mục con `english-coach/`.

**Đã xong:** Bước 0 (11/11).
- `english-coach/app.py`: Flask, đọc `.env` bằng `python-dotenv`. Danh sách `MODES` là nguồn duy nhất cho menu (trang web lấy qua `GET /api/modes`). Chế độ chưa làm rơi vào route chung `POST /api/<mode_id>` → 501 "chưa làm".
- Chế độ `explain` (giải nghĩa từ) là bản thử từ commit đầu, gọi thẳng `client.messages.create`. Bước 1 sẽ viết lại nó bằng `call_claude()` trong `client.py`.
- `app.py` ép stdout/stderr sang UTF-8 vì terminal Windows mặc định cp1252 làm `print` tiếng Việt crash. Script mới nào có `print` tiếng Việt (ví dụ `break_things.py`) cũng cần làm vậy.

**Tiếp theo:** Bước 1.

Chạy (PowerShell, từ thư mục `english-coach/`):
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # rồi điền ANTHROPIC_API_KEY
python app.py               # mở http://127.0.0.1:5000
```
Kiểm tra route mà không gọi API thật: dùng `app.test_client()` của Flask. Repo chưa có bộ test, lint hay build. `experiments/break_things.py` (Bước 4) sẽ là nơi test bằng mock.

**Tài liệu ôn thi trong `Document/`** (tiếng Việt):
- `CCDV-F_Note_8_Domain.md`: note nhanh 8 domain. Đọc file này trước khi soạn câu hỏi trắc nghiệm.
- `CCDV-F_Cam_Nang_Kien_Thuc.html` (~450 KB) và `CCDV-F_De_Thi_Tieng_Viet.html` (~640 KB): file lớn, dùng grep thay vì đọc cả file. Đề thi thử dùng để tham khảo cách ra câu hỏi và bẫy.

---

## 1. Bối cảnh

- **Người dùng** đang tự học để thi CCDV-F. Đề có 53 câu trắc nghiệm, thời gian 120 phút, closed-book, cần từ 720/1000 điểm để đậu.
- **Trọng số các domain:**

  | Domain | Nội dung | Trọng số |
  |---|---|---|
  | D2 | Applications & Integration (Messages API, streaming, lỗi, retry, batch, files…) | 33,1% |
  | D5 | Model selection, cost/latency, prompt caching, extended thinking | 16,8% |
  | D1 | Agent/workflow patterns, stopping criteria, subagents | 14,7% |
  | D6 | Prompt engineering, context engineering | 11,0% |
  | D8 | Tool use, MCP | 10,6% |
  | D7 | Security, prompt injection, least privilege | 8,1% |
  | D3 | Claude Code | 3,1% |
  | D4 | Evals | 2,6% |

- **Cách học:** xen kẽ. Người dùng học lý thuyết một chủ đề, làm tính năng tương ứng trong app, rồi làm câu hỏi trắc nghiệm của domain đó. **Từ 26/11 thì ngừng code, chỉ ôn và làm đề thi thử.**

## 2. Cách agent làm việc

1. **Làm từng bước một.** Mỗi bước phải chạy được và được người dùng xác nhận rồi mới sang bước tiếp. Không dựng cả dự án trong một lần.
2. **Code đơn giản, dễ đọc.** Comment bằng **tiếng Việt** và gắn tag domain, ví dụ `# [D2] xử lý stop_reason`.
3. **Mục đích là dạy, không chỉ làm hộ.** Sau mỗi bước:
   - Giải thích ngắn (5–10 dòng) những gì vừa quan sát được và vì sao nó quan trọng cho đề thi.
   - Đưa ra **3 câu hỏi trắc nghiệm** kiểu đề thi về đúng phần vừa làm (4 đáp án, mỗi câu có một cái bẫy hay gặp). Chờ người dùng trả lời rồi mới chấm.
   - Ghi những câu người dùng làm sai vào `NOTES_LOI_SAI.md`, kèm domain, lý do sai và quy tắc rút ra.
   - Tổng hợp những gì đã làm vào `HISTORY.md` ở gốc repo. Thêm mục mới **ở trên cùng**, tiêu đề có timestamp lấy bằng lệnh `date` (giờ +07:00), không đoán giờ.
4. **Kiến thức của agent có thể đã cũ.** Trước khi dùng tham số nào, kiểm tra lại docs chính thức tại https://docs.claude.com, đặc biệt là:
   - Tên model.
   - Cú pháp structured outputs.
   - `cache_control` và ngưỡng token tối thiểu để cache.
   - Các giá trị `stop_reason`.
   - Lỗi nào SDK tự retry.

   Thấy chỗ nào khác với file này thì theo docs, và báo cho người dùng biết.
5. **Kiểm soát chi phí.** Mặc định dùng `claude-haiku-5-5`, `max_tokens` từ 300 đến 800. Không gọi API trong vòng lặp vô hạn. Lỗi 429 và 5xx chỉ test bằng mock.
6. **Không mở rộng phạm vi.** Web UI chỉ ở mức căn bản: một trang HTML, JS thuần, không framework frontend, không build step. Không làm database hay đăng nhập. Không thêm thư viện ngoài `anthropic`, `python-dotenv` và `flask` khi không thật cần. Tính năng nào không giúp luyện domain nào thì để sau ngày 30/11.

## 3. Ràng buộc kỹ thuật

- Python 3.10 trở lên, dùng SDK chính thức `anthropic`.
- Giao diện là web căn bản: backend Flask (`app.py`) giữ key và gọi API, mỗi chế độ là một route `/api/...`; frontend là `static/index.html` gọi các route đó bằng `fetch`.
- Ở các bước dưới, "in ra" nghĩa là **hiện trên trang web** (để người dùng quan sát `stop_reason`, usage, cache hit/miss…) **và** log ra terminal chạy Flask.
- `experiments/break_things.py` vẫn là script chạy trong terminal, không cần UI.
- Model đọc từ biến môi trường `CLAUDE_MODEL`, mặc định `claude-haiku-5-5`, có thể đổi sang `claude-sonnet-5-5`.
- **[D7] API key** chỉ đọc từ `.env` hoặc biến môi trường. Không hard-code, không in key ra log. `.env` phải có trong `.gitignore`.

## 4. Cấu trúc thư mục

CLAUDE.md và `Document/` nằm ở thư mục gốc repo. Toàn bộ code nằm trong `english-coach/`, chạy lệnh từ thư mục đó.

```
<gốc repo>/
├── CLAUDE.md               # file này
├── .gitignore              # có .env, .venv, __pycache__
├── Document/               # tài liệu ôn thi
└── english-coach/
    ├── NOTES_LOI_SAI.md        # sổ lỗi sai khi làm câu hỏi
    ├── .env.example            # ANTHROPIC_API_KEY=, CLAUDE_MODEL=
    ├── requirements.txt        # anthropic, python-dotenv, flask
    ├── README.md               # cách chạy + bảng ánh xạ domain + câu hỏi tự kiểm tra
    ├── app.py                  # Flask: route trang chủ + một route /api/... cho mỗi chế độ
    ├── static/index.html       # UI căn bản: menu chọn chế độ, ô nhập, khung kết quả + khung usage
    ├── client.py               # client, call_claude() có log usage và xử lý stop_reason
    ├── modes/
    │   ├── chat.py             # hội thoại có streaming            [D2, D6]
    │   ├── grammar.py          # sửa ngữ pháp, output JSON         [D2, D6]
    │   ├── reading.py          # bài đọc dài + prompt caching      [D5]
    │   ├── vocab_tool.py       # tool use lookup_word              [D8, D1]
    │   └── essay.py            # chấm bài viết, evaluator-optimizer + routing  [D1, D5]
    ├── security/
    │   └── guard.py            # lọc input, chống prompt injection [D7]
    ├── data/
    │   ├── reading_passage.txt # đủ dài để vượt ngưỡng cache tối thiểu
    │   └── dictionary.json     # từ điển mini cho tool
    └── experiments/
        └── break_things.py     # cố tình gây lỗi để quan sát       [D2]
```

Logic gọi Claude nằm trong `modes/*.py` và không phụ thuộc Flask. `app.py` chỉ nhận request, gọi hàm trong `modes/` rồi trả JSON (hoặc stream) về trình duyệt.

## 5. Lộ trình theo ngày thi

| Giai đoạn | Ngày | Bước làm | Domain |
|---|---|---|---|
| 1 | 11–13/11 | Bước 0, 1, 2, 4 | D2 |
| 1 | 14–16/11 | Bước 3, 5 | D2, D6, D5 |
| 2 | 17–19/11 | Bước 6 | D8, D1 |
| 2 | 20–22/11 | Bước 7 | D1, D5, D6 |
| 3 | 23–25/11 | Bước 8 (bước 9 nếu còn thời gian), viết README | D7, D2 |
| — | 26–30/11 | **Ngừng code.** Chỉ ôn sổ lỗi và làm đề thi thử | — |

**Buổi đầu tiên chỉ làm Bước 0, 1, 2 và 4.** Đây là phần D2, nặng nhất trong đề.

---

## 6. Chi tiết từng bước

### Bước 0: dựng khung dự án
- Tạo `english-coach/` và các thư mục con, `.env.example`, `requirements.txt`, file `NOTES_LOI_SAI.md` rỗng. Cập nhật `.gitignore` ở gốc repo.
- Chuyển `server.py` thành `english-coach/app.py` (Flask, đọc key bằng `python-dotenv`), chuyển `static/` vào `english-coach/`. Xoá bản cũ ở gốc repo.
- Trang web có menu các chế độ. Chế độ nào chưa làm thì hiện "chưa làm".
- Hướng dẫn người dùng tạo venv, cài thư viện, điền key vào `.env`.
- **Xong khi:** `python app.py` chạy, mở http://127.0.0.1:5000 thấy được menu.

### Bước 1: `client.py`, gọi API cơ bản [D2]
- Tạo `anthropic.Anthropic()` với `max_retries` và `timeout` ghi tường minh. Comment giải thích SDK tự retry những lỗi nào (kiểm tra docs).
- Viết hàm `call_claude(system, messages, **kwargs)`. Sau mỗi lần gọi, in ra:
  - `stop_reason`.
  - `usage.input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`.
- Xử lý từng giá trị `stop_reason`:
  - `end_turn`: bình thường.
  - `max_tokens`: cảnh báo "output bị cắt".
  - `stop_sequence`: in ra chuỗi dừng đã gặp.
  - `tool_use`: trả về cho bên gọi xử lý.
  - `pause_turn`: server tool (ví dụ web search) đang chạy dở. Gửi lại response đó trong `messages` để model chạy tiếp. Không phải lỗi, không phải output bị cắt.
  - `refusal`: báo cho người dùng là model từ chối.
- Comment giải thích hai điều:
  - `system` là tham số riêng, không nằm trong `messages`.
  - Role user/assistant xen kẽ nhau, message đầu tiên là `user`.
- **Xong khi:** gửi "Hello" thì thấy câu trả lời, `stop_reason` và usage được in ra.

### Bước 2: `modes/chat.py`, hội thoại có streaming [D2, D6]
- System prompt cho model vai giáo viên tiếng Anh thân thiện. Cấp độ học viên (A2/B1/B2) do người dùng chọn.
- Giữ lịch sử trong list `messages` và gửi lại toàn bộ mỗi lượt. Comment giải thích: API **stateless**, model không tự nhớ.
- Lịch sử `messages` giữ ở trình duyệt (biến JS) và gửi kèm mỗi request. Server không lưu state, giống chính API.
- Dùng `client.messages.stream(...)` ở backend. Flask trả về streaming response, chuyển tiếp từng đoạn text xuống trình duyệt. Trình duyệt đọc bằng `fetch` + `response.body.getReader()` và nối chữ vào trang ngay khi về. Khi stream xong thì lấy final message, gửi usage và `stop_reason` ở cuối.
- Comment liệt kê thứ tự event SSE: `message_start` → `content_block_start` → `content_block_delta` → `content_block_stop` → `message_delta` → `message_stop`. Ghi chú `usage` và `stop_reason` cuối cùng nằm ở `message_delta`.
- **Xong khi:** chat được nhiều lượt, chữ hiện dần ra, model nhớ nội dung các lượt trước.

### Bước 3: `modes/grammar.py`, sửa ngữ pháp và trả JSON [D2, D6]
- Output bắt buộc là JSON gồm:
  - `original`
  - `corrected`
  - `errors[]`, mỗi phần tử có `type` và `explanation_vi`
  - `score` (0–10)
- Ưu tiên **structured outputs** (JSON schema) nếu docs hiện tại hỗ trợ model đang dùng. Nếu không, dùng phương án dự phòng: prompt có XML tags (`<sentence>`, `<format>`) và 2–3 ví dụ few-shot, rồi `json.loads` và validate lại.
- Parse lỗi thì báo rõ ràng, không để chương trình crash.
- **Xong khi:** thử 5 câu, cả 5 đều ra JSON hợp lệ.

### Bước 4: `experiments/break_things.py`, cố tình gây lỗi [D2]
Mỗi thí nghiệm in kết quả kèm giải thích tiếng Việt:
1. Sai API key → 401. Giải thích vì sao **không** retry.
2. Request sai định dạng (thiếu `max_tokens`, sai role…) → 400. Giải thích vì sao **không** retry.
3. Đặt `max_tokens=20` cho một câu hỏi dài → `stop_reason == "max_tokens"`.
4. Tự viết `retry_with_backoff()`, với `max_retries=0` để tắt retry của SDK:
   - Chỉ retry khi gặp 429, 500, 529 hoặc lỗi kết nối/timeout.
   - Dùng exponential backoff + jitter, có giới hạn số lần thử.
   - Tôn trọng header `retry-after` nếu có.
   - Test bằng **mock exception**, không spam API thật.
5. In bảng tóm tắt: mã lỗi → nghĩa → có retry không → vì sao.
- **Xong khi:** cả 5 mục chạy được và in ra kết luận.

### Bước 5: `modes/reading.py`, prompt caching [D5]
- Đặt bài đọc dài vào system prompt, `cache_control` đặt ở cuối khối đó. Bài đọc phải vượt ngưỡng cache tối thiểu của model (kiểm tra docs).
- Người dùng hỏi nhiều câu về bài đọc. Mỗi lần gọi in rõ **CACHE MISS** (`cache_creation_input_tokens > 0`) hoặc **CACHE HIT** (`cache_read_input_tokens > 0`).
- Thí nghiệm phá cache: chèn timestamp vào **đầu** system prompt để thấy cache miss. Comment giải thích thứ tự prefix **tools → system → messages**: đổi chỗ nào thì toàn bộ phần phía sau mất cache. Ghi thêm TTL mặc định của cache.
- In chi phí ước tính lúc cache hit so với không cache.
- **Xong khi:** lần gọi thứ 2 là cache hit, và chèn timestamp thì ra cache miss.

### Bước 6: `modes/vocab_tool.py`, tool use [D8, D1]
- Tool `lookup_word`, `input_schema` có trường `word` (string). Description ghi rõ khi nào nên dùng tool.
- Vòng lặp tool use:
  1. Gọi API kèm tools.
  2. Nếu `stop_reason == "tool_use"`, chạy hàm tra `data/dictionary.json`.
  3. Gửi lại `tool_result` với `tool_use_id` khớp, nằm trong message role **user**.
  4. Lặp đến khi ra `end_turn`, tối đa 5 vòng. Đây là stopping criteria của D1.
- Từ không có trong từ điển: trả `tool_result` với `is_error: true` và thông báo rõ ràng.
- Model gọi nhiều tool trong một lượt: trả **tất cả** `tool_result` trong **cùng một** user message.
- Thêm cờ để thử các giá trị `tool_choice`: `auto`, `any`, `{"type":"tool","name":"lookup_word"}`, `none`. In ra hành vi của từng giá trị.
- **Xong khi:** hỏi "What does 'resilient' mean and use 'ubiquitous' in a sentence" thì model gọi tool 2 lần rồi trả lời hoàn chỉnh.

### Bước 7: `modes/essay.py`, chấm bài viết [D1, D5, D6]
- **Routing:** bài ngắn hơn 80 từ dùng Haiku, dài hơn dùng Sonnet. In model đã chọn và lý do.
- **Evaluator-optimizer:**
  - Bước "sửa" viết lại đoạn văn.
  - Bước "chấm" đánh giá theo rubric (grammar, vocabulary, coherence) và trả JSON.
  - Điểm dưới ngưỡng thì gửi feedback cho bước "sửa", tối đa 2 vòng.
- Prompt dùng XML tags, rubric rõ ràng, có một ví dụ few-shot.
- Comment so sánh: vì sao đây là **workflow** chứ không phải **agent**, và khi nào mới cần đến agent.
- **Xong khi:** chạy với một đoạn văn có lỗi, thấy điểm tăng qua các vòng.

### Bước 8: `security/guard.py`, bảo mật [D7]
- Kiểm tra input trước khi gửi model: giới hạn độ dài, phát hiện mẫu kiểu "ignore previous instructions".
- Comment ghi rõ: chỉ lọc bằng prompt là **không đủ**. Cần thêm kiểm soát deterministic ở backend: validate output, coi output của model là untrusted, không cho model quyền thực hiện hành động nguy hiểm.
- Thử **indirect injection**: chèn một câu lệnh độc vào `reading_passage.txt` rồi xem model có làm theo không. Ghi lại cách giảm thiểu.
- **Xong khi:** demo được một ca bị chặn, một ca indirect injection, và có comment giải thích defense in depth.

### Bước 9 (tuỳ chọn): Message Batches [D2]
- Gửi batch 10 câu cần sửa ngữ pháp, poll trạng thái, rồi đọc kết quả.
- Comment giải thích:
  - Batch rẻ hơn khoảng 50%.
  - Chạy bất đồng bộ, tối đa 24 giờ.
  - Không dùng cho tác vụ realtime.

---

## 7. Bàn giao cuối (trước 26/11)

`README.md` cần có:
1. Lệnh cài đặt và chạy từng chế độ.
2. **Bảng ánh xạ** gồm các cột: tính năng, file/hàm, domain, kiến thức luyện được.
3. **Câu hỏi tự kiểm tra:** 15–20 câu ngắn về những gì đã quan sát. Ví dụ:
   - Vì sao 401 không retry?
   - Field nào chứng minh cache hit?
   - `tool_result` nằm trong role nào?
   - Khi nào dùng workflow thay vì agent?

## 8. Quy tắc làm bài thi (nhắc lại khi giải thích)
1. Đáp án đúng thường là cơ chế **deterministic** (hook, validation, gate ở backend), không phải "nhắc model trong prompt".
2. Chọn giải pháp đơn giản nhất đủ giải quyết vấn đề: workflow trước agent.
3. Chỉ retry lỗi tạm thời (429, 5xx, 529, timeout). Không retry lỗi do request (400, 401, 403, 404, 413).

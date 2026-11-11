# Chương trình học và ôn thi CCDV-F từ A đến Z
*(11/11 – 30/11/2026)*

> Một file duy nhất để theo suốt 20 ngày. Mỗi ngày có 3 phần: **Học** (lý thuyết), **Lab** (code harness), **Đề** (trắc nghiệm). Tick `[x]` khi xong.

---

## 0. Thông tin kỳ thi

| Mục | Chi tiết |
|---|---|
| Tên | Claude Certified Developer – Foundations (CCDV-F) |
| Hình thức | 53 câu trắc nghiệm, 120 phút, closed-book |
| Điểm đậu | 720/1000 |
| Ngày thi dự kiến | **30/11/2026** |
| Việc cần làm ngay | Kiểm tra điều kiện đăng ký, đặt lịch thi, xem exam guide chính thức |

### Trọng số domain (quyết định thời gian học)

| # | Domain | Trọng số | Số câu ước tính | Ưu tiên |
|---|---|---|---|---|
| D2 | Applications & Integration | 33,1% | ~18 | ⭐⭐⭐ |
| D5 | Model Selection & Optimization | 16,8% | ~9 | ⭐⭐⭐ |
| D1 | Agents & Workflows | 14,7% | ~8 | ⭐⭐⭐ |
| D6 | Prompt & Context Engineering | 11,0% | ~6 | ⭐⭐ |
| D8 | Tools & MCPs | 10,6% | ~6 | ⭐⭐ |
| D7 | Security & Safety | 8,1% | ~4 | ⭐⭐ |
| D3 | Claude Code | 3,1% | ~2 | ⭐ |
| D4 | Eval, Testing & Debugging | 2,6% | ~1 | ⭐ |

**D2 + D5 + D1 = 64,6% đề.** Nếu trễ lịch, hy sinh D3, D4 trước.

---

## 1. Nguyên tắc học

1. **Học → Làm → Kiểm tra** trong cùng một ngày. Lý thuyết không có lab thì quên nhanh, lab không có đề thì không biết bẫy.
2. **Ghi sổ lỗi mỗi ngày** (mẫu ở mục 8). Sổ lỗi là tài liệu ôn quan trọng nhất của tuần cuối.
3. **Docs là nguồn đúng cuối cùng.** Kiến thức trong tài liệu hoặc từ AI có thể cũ. Khi lệch, theo docs.
4. **Từ 26/11 ngừng code**, chỉ ôn và làm đề.
5. **Nhịp học:** ngày thường ~1,5–2 giờ, cuối tuần ~3 giờ.

---

## 2. Tài nguyên

### Trong project "Claude Leaning"
| Tài liệu | Dùng để |
|---|---|
| `CCDV-F_Cam_Nang_Kien_Thuc.html` | 91 concept theo 8 domain, có ô "Bẫy thi". Đọc trước mỗi domain |
| `CCDV-F_Note_8_Domain.md` | Bản tóm tắt nhanh để ôn cuối |
| `CCDV-F_De_Thi_Tieng_Viet.html` | Đề theo domain, Paper A/B/C/D, đề Mixed |
| `CLAUDE.md` (repo English Coach) | **Nguồn duy nhất cho phần lab**: 11 bước (Bước 0–10), chi tiết ở mục 5 |

### Anthropic Academy (anthropic.skilljar.com, miễn phí)
| Khóa | Domain chính | Khi nào học |
|---|---|---|
| **Building with the Claude API** | D2, D5, D6, D1, D8, D4 | Xuyên suốt, theo từng chương (xem lịch) |
| Claude Platform 101 | D2 | Ngày 1, nếu muốn có cái nhìn tổng quan |
| Introduction to Model Context Protocol | D8 | 21/11 |
| Model Context Protocol: Advanced Topics | D8 | Tuỳ chọn, chỉ xem lướt |
| Introduction to subagents | D1, D3 | 18/11 |
| Claude Code in Action | D3 | 24/11 |
| Introduction to agent skills | D3 | 24/11, xem lướt |

### Docs chính thức (platform.claude.com/docs, cũ là docs.claude.com)
Errors · Rate limits · Handling stop reasons · Streaming · Prompt caching · Tool use · Structured outputs · Batch processing · Files API · Citations · Vision · PDF support · Extended thinking · Prompt engineering · Models overview.

### Bài viết của Anthropic (đọc cho D1, D8)
- *Building effective agents* (6 pattern, workflow vs agent)
- *Writing tools for agents* (thiết kế tool, error message)
- *Effective context engineering for AI agents*

---

## 3. Lộ trình tổng quan

| Giai đoạn | Ngày | Trọng tâm | Lab (English Coach) |
|---|---|---|---|
| **A. Nền tảng API** | 11–15/11 | D2 | Bước 1, 2, 3, 4, 9 |
| **B. Tối ưu và Agent** | 16–19/11 | D5, D1 | Bước 5, 7 |
| **C. Tools, Prompt, Security** | 20–23/11 | D8, D6, D7 | Bước 6, 8 + Mock 1 |
| **D. Phần nhẹ và tổng hợp** | 24–25/11 | D3, D4 + Mock 2 | Bước 10, README |
| **E. Ôn và thi thử** | 26–29/11 | Sổ lỗi, domain yếu, Mock 3 | Ngừng code |
| **F. Thi** | 30/11 | — | — |

---

## 4. Lịch từng ngày

> Ký hiệu: 📘 Học · 💻 Lab · 📝 Đề. Nếu đã làm một số đề (ví dụ Paper A) thì đổi sang Paper khác cho mock.

### Giai đoạn A: Nền tảng API (D2)

**T4 11/11: Messages API cơ bản**
- [ ] 📘 Cẩm nang D2 phần Messages API, content blocks, header, `usage`, `stop_reason`
- [ ] 📘 Skilljar *Building with the Claude API*: Getting an API key → Making a request → Multi-turn → System prompts
- [ ] 💻 **Bước 1** `client.py` (Bước 0 đã xong)
- [ ] 📝 5 câu đầu của đề Domain 2

**T5 12/11: Streaming**
- [ ] 📘 Docs Streaming: thứ tự event, `ping`, event `error`, `usage` cuối nằm ở `message_delta`
- [ ] 📘 Skilljar: Response streaming, Temperature
- [ ] 💻 **Bước 2** chat streaming
- [ ] 📝 Phần còn lại của đề Domain 2

**T6 13/11: Structured outputs và tính năng khác**
- [ ] 📘 Docs Structured outputs, Vision, PDF, Citations, Files API
- [ ] 📘 Skilljar: Structured data; Features of Claude (Image, PDF, Citations); Code execution and the Files API
- [ ] 💻 **Bước 3** grammar JSON
- [ ] 📝 Ghi sổ lỗi

**T7 14/11 (3 giờ): Lỗi, retry, rate limits, Batches**
- [ ] 📘 Docs Errors + Rate limits + Batch processing (nắm bảng ở mục 6 / D2)
- [ ] 💻 **Bước 4** `break_things.py` (lỗi, retry bằng mock)
- [ ] 📝 Đề Domain 2 (bản 10 câu tình huống nếu có) + ghi sổ lỗi

**CN 15/11 (3 giờ): Batches + tổng kết D2**
- [ ] 💻 **Bước 9** `batch_grammar.py` (3 request, ghép bằng `custom_id`)
- [ ] 📝 Làm lại toàn bộ câu sai D2 trong sổ lỗi
- [ ] 📝 Mini-test: 15 câu D2 trộn, bấm giờ 30 phút. Mục tiêu ≥ 70%

### Giai đoạn B: Tối ưu và Agent (D5, D1)

**T2 16/11: Chọn model, cost, latency**
- [ ] 📘 Cẩm nang D5; docs Models overview, Extended thinking
- [ ] 📘 Skilljar: Extended thinking; Prompt caching
- [ ] 📝 Đề Domain 5 (lượt 1)

**T3 17/11: Prompt caching thực hành**
- [ ] 📘 Docs Prompt caching: thứ tự prefix tools → system → messages, độ dài tối thiểu, TTL, breakpoint
- [ ] 💻 **Bước 5** reading: caching + citations
- [ ] 📝 Làm lại câu sai D5

**T4 18/11: Agent và workflow patterns**
- [ ] 📘 Bài *Building effective agents*; Cẩm nang D1
- [ ] 📘 Skilljar: Agents and workflows (Parallelization, Chaining, Routing); *Introduction to subagents*
- [ ] 📝 Đề Domain 1 (lượt 1)

**T5 19/11: Workflow trong code**
- [ ] 💻 **Bước 7** essay: routing, evaluator-optimizer, extended thinking
- [ ] 📝 Đề Domain 1 bản 10 câu tình huống + ghi sổ lỗi

### Giai đoạn C: Tools, Prompt, Security (D8, D6, D7)

**T6 20/11: Tools nâng cao**
- [ ] 📘 Cẩm nang D8; bài *Writing tools for agents*; docs Tool use (parallel tool use, `tool_choice`, server tools, `pause_turn`)
- [ ] 💻 **Bước 6 phần 1**: 1 tool, vòng lặp, `is_error`
- [ ] 📝 Đề Domain 8 (lượt 1)

**T7 21/11 (3 giờ): MCP**
- [ ] 📘 Skilljar *Introduction to Model Context Protocol*
- [ ] 💻 **Bước 6 phần 2**: nhiều tool, `tool_choice`
- [ ] 💻 Tuỳ chọn: dựng MCP server nhỏ có 1 tool (stdio)
- [ ] 📝 Làm lại câu sai D8; mini-test 20 câu trộn D2/D5/D1/D8

**CN 22/11 (3 giờ): Prompt engineering + Security + Mock 1**
- [ ] 📘 Cẩm nang D6 + D7; Skilljar phần Prompt engineering (Being specific, XML tags, examples)
- [ ] 💻 **Bước 8** security: guard + 2 ca indirect injection
- [ ] 📝 **Mock 1**: một Paper đầy đủ, 53 câu, bấm 120 phút. Mục tiêu ≥ 65%

**T2 23/11: Phân tích Mock 1**
- [ ] 📝 Chấm Mock 1 theo domain (bảng mục 9)
- [ ] 📝 Đề Domain 6 + Domain 7
- [ ] 📘 Đọc lại ô "Bẫy thi" của domain yếu nhất

### Giai đoạn D: Phần nhẹ và tổng hợp (D3, D4)

**T3 24/11: Claude Code + Eval**
- [ ] 📘 Skilljar *Claude Code in Action* (xem nhanh); Cẩm nang D3 + D4
- [ ] 💻 **Bước 10** eval grammar + viết README
- [ ] 📝 Đề Domain 3 + Domain 4

**T4 25/11: Mock 2**
- [ ] 📝 **Mock 2**: Paper khác, bấm 120 phút. Mục tiêu ≥ 75%
- [ ] 📝 Ghi toàn bộ câu sai vào sổ lỗi

### Giai đoạn E: Ôn và thi thử (ngừng code)

**T5 26/11**
- [ ] 📝 Làm lại **toàn bộ** sổ lỗi, không xem đáp án trước
- [ ] 📘 Đọc lại `CCDV-F_Note_8_Domain.md` và mục 6 của file này

**T6 27/11**
- [ ] 📝 **Mock 3**: Paper còn lại hoặc đề Mixed. Mục tiêu ≥ 80%
- [ ] 📘 Ôn 2 domain yếu nhất

**T7 28/11**
- [ ] 📝 Làm đề Mixed theo domain yếu; làm lại câu sai của Mock 3
- [ ] 📘 Ôn tất cả ô "Bẫy thi" của D2, D5, D1

**CN 29/11: Nghỉ**
- [ ] 📘 Chỉ đọc cheat sheet (mục 7), không làm đề mới
- [ ] Chuẩn bị giấy tờ, kiểm tra lịch thi, ngủ sớm

**T2 30/11: Thi** → xem checklist mục 10.

---

## 5. Lab: app English Coach (theo `CLAUDE.md`)

Phần lab dùng **một nguồn duy nhất** là `CLAUDE.md` trong repo English Coach (Flask + một trang HTML). Agent trong VS Code đọc file đó và làm mentor theo từng bước. Bảng dưới chỉ để tra nhanh; chi tiết và tiêu chí "xong khi" nằm trong `CLAUDE.md`.

| Ngày | Bước | File | Domain | Luyện gì |
|---|---|---|---|---|
| 11/11 | 0 ✅ | `app.py`, `static/` | D7 | Khung Flask, `.env`, key chỉ ở backend |
| 11/11 | 1 | `client.py` | D2 | `usage`, đủ 7 `stop_reason`, `request_id`, header rate limit, Token Counting, SDK retry |
| 12/11 | 2 | `modes/chat.py` | D2, D6 | Streaming SSE, API stateless, lỗi giữa stream |
| 13/11 | 3 | `modes/grammar.py` | D2, D6 | Structured outputs, validate bằng code |
| 14/11 | 4 | `experiments/break_things.py` | D2 | 401/400, `max_tokens`, retry + backoff + `retry-after`, bảng lỗi đầy đủ |
| 15/11 | 9 | `experiments/batch_grammar.py` | D2, D5 | Batches, `custom_id`, kết quả không theo thứ tự |
| 17/11 | 5 | `modes/reading.py` | D5, D2 | Prompt caching, phá cache, cache read không tính ITPM, Citations |
| 19/11 | 7 | `modes/essay.py` | D1, D5, D6 | Routing, evaluator-optimizer, extended thinking, workflow vs agent |
| 20–21/11 | 6 | `modes/vocab_tool.py` | D8, D1 | Vòng tool use, `is_error`, parallel tool use, `tool_choice` |
| 22/11 | 8 | `security/guard.py` | D7 | Lọc input, indirect injection qua tài liệu và `tool_result` |
| 24/11 | 10 | `experiments/eval_grammar.py` | D4 | Eval chấm bằng code, regression, README |

Nguyên tắc chung: Python, SDK `anthropic`, model mặc định Haiku, `max_tokens` thấp; lỗi 429/5xx chỉ test bằng mock; sau mỗi bước agent ra 3 câu trắc nghiệm và ghi sổ lỗi.

---

## 6. Checklist kiến thức theo domain

> Tick khi giải thích lại được bằng lời của mình. Chi tiết đọc ở Cẩm nang.

### D2: Applications & Integration (33,1%)
- [ ] Messages API: `model`, `max_tokens` (bắt buộc), `messages` xen kẽ user/assistant, `system` là tham số riêng
- [ ] Header: `x-api-key`, `anthropic-version`, `content-type`
- [ ] Content blocks: text, image, document, tool_use, tool_result
- [ ] `usage`: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`
- [ ] **7 `stop_reason`**:

  | Giá trị | Ý nghĩa | Xử lý |
  |---|---|---|
  | `end_turn` | Trả lời xong | Dùng kết quả |
  | `max_tokens` | Chạm `max_tokens` | Tăng giới hạn hoặc gọi tiếp. **Không phải lỗi** |
  | `stop_sequence` | Gặp chuỗi dừng | Đọc field `stop_sequence` |
  | `tool_use` | Muốn gọi client tool | Chạy tool, gửi `tool_result` |
  | `pause_turn` | Vòng server tool chạm giới hạn lặp | Gửi lại nguyên nội dung assistant để chạy tiếp |
  | `refusal` | Model từ chối (HTTP 200, không phải lỗi) | Xem `stop_details` |
  | `model_context_window_exceeded` | Lấp đầy context window | Coi như output bị cắt |

- [ ] Streaming SSE: `message_start` → `content_block_start` → `content_block_delta` → `content_block_stop` → `message_delta` → `message_stop`; có `ping`; lỗi có thể đến **sau khi đã trả 200**
- [ ] **Bảng lỗi**:

  | Mã | Loại | Retry? |
  |---|---|---|
  | 400 | `invalid_request_error` (cả khi chạm spend limit tự đặt) | Không, sửa request |
  | 401 | `authentication_error` | Không |
  | 402 | `billing_error` | Không |
  | 403 | `permission_error` | Không |
  | 404 | `not_found_error` | Không |
  | 409 | `conflict_error` | Giải quyết xung đột rồi mới retry |
  | 413 | `request_too_large` | Không, giảm kích thước |
  | 429 | `rate_limit_error` | Có, theo `retry-after`. **Trừ** 429 do spend cap của tier: không có `retry-after`, retry vô ích |
  | 500 | `api_error` | Có, backoff |
  | 504 | `timeout_error` | Có |
  | 529 | `overloaded_error` | Có, backoff |

- [ ] SDK tự retry lỗi kết nối, 429, 5xx, **mặc định 2 lần**, có tôn trọng `retry-after`; chỉnh bằng `max_retries`, `timeout`
- [ ] Rate limits: RPM, ITPM, OTPM theo từng model class; thuật toán **token bucket** (nạp liên tục); **cache read không tính vào ITPM**; `max_tokens` không tính vào OTPM; header `anthropic-ratelimit-*`
- [ ] Message Batches: bất đồng bộ, rẻ hơn ~50%, xong trong tối đa 24 giờ; kết quả không theo thứ tự, ghép bằng `custom_id`; **không dùng cho realtime**
- [ ] Files API (`file_id`), Citations, Structured outputs, Token counting, Vision, PDF
- [ ] `request-id` trong mọi response, dùng khi liên hệ support

### D5: Model Selection & Optimization (16,8%)
- [ ] Haiku (nhanh, rẻ) · Sonnet (cân bằng) · Opus (mạnh nhất). Chọn bằng **eval trên tác vụ thật**
- [ ] Mixed models: model mạnh làm orchestrator, model rẻ làm worker/phân loại
- [ ] Đòn bẩy latency: model nhỏ, streaming, giảm output, caching, song song
- [ ] Đòn bẩy chi phí: model nhỏ, caching, Batch, cắt context
- [ ] Prompt caching: prefix **tools → system → messages**; `cache_control`; độ dài tối thiểu theo model; TTL mặc định 5 phút (có tuỳ chọn 1 giờ); ghi cache đắt hơn một chút, đọc cache rẻ hơn nhiều; multi-turn đặt breakpoint ở message cuối
- [ ] Phá cache: timestamp/ID động trong system prompt, đổi thứ tự tool
- [ ] Extended/adaptive thinking: cho bài suy luận nhiều bước, đổi lại tốn token và tăng latency

### D1: Agents & Workflows (14,7%)
- [ ] Workflow (code định luồng) vs agent (model tự quyết). **Bắt đầu đơn giản**
- [ ] 6 pattern: prompt chaining (có gate), routing, parallelization (sectioning/voting), orchestrator-workers, evaluator-optimizer, agent loop
- [ ] Stopping criteria: giới hạn vòng, ngân sách token/thời gian, checkpoint
- [ ] Subagents: cô lập context, chạy song song, trả tóm tắt
- [ ] Việc **bắt buộc xảy ra** → hook/code deterministic, không dựa vào prompt
- [ ] Memory có chọn lọc; durable state, idempotency cho agent chạy lâu
- [ ] ACI: tool dễ dùng cho model

### D6: Prompt & Context Engineering (11,0%)
- [ ] Rõ ràng, trực tiếp, có context và lý do; nói điều cần làm thay vì điều cấm
- [ ] XML tags tách instruction/dữ liệu/ví dụ; few-shot 3–5 ví dụ đa dạng trong `<example>`
- [ ] Role trong system prompt
- [ ] Chain of thought trong tag riêng, đáp án trong tag khác
- [ ] Long context: tài liệu lên đầu, câu hỏi ở cuối; trích dẫn trước khi trả lời
- [ ] Giảm hallucination: cho phép "không biết", bắt trích dẫn, có bước kiểm chứng
- [ ] Context engineering cho agent: chỉ nạp thứ cần, tóm tắt/compact khi dài
- [ ] Output nhất quán: đặc tả format, ví dụ, structured outputs

### D8: Tools & MCPs (10,6%)
- [ ] Tool: `name`, `description` (quan trọng nhất), `input_schema`
- [ ] `tool_result` nằm trong role **user**, `tool_use_id` khớp
- [ ] Parallel tool use: tất cả `tool_result` trong **cùng một** user message
- [ ] Lỗi tool: `is_error: true` + thông báo hành động được
- [ ] `tool_choice`: `auto` / `any` / `tool` / `none`
- [ ] Nhiều tool: namespace, mô tả rõ, tránh trùng; tool search + `defer_loading`
- [ ] Client tool (app chạy) vs server tool (Anthropic chạy, có thể trả `pause_turn`)
- [ ] MCP: host chứa client, mỗi client nối 1 server; primitives tools/resources/prompts; transports stdio / Streamable HTTP

### D7: Security & Safety (8,1%)
- [ ] Least privilege cho tool và credential; secrets ngoài prompt
- [ ] Prompt injection direct vs indirect (tài liệu, web, kết quả tool); defense in depth
- [ ] Output model là untrusted: validate, escape
- [ ] Authorization kiểm tra ở backend
- [ ] Human-in-the-loop cho hành động tác động lớn
- [ ] Privacy (tối thiểu dữ liệu, che PII), multi-tenant (cách ly dữ liệu)

### D3: Claude Code (3,1%)
- [ ] CLAUDE.md (memory project/user)
- [ ] Slash commands, Skills
- [ ] MCP scope local/project/user, `.mcp.json` chia sẻ team
- [ ] Permissions allow/ask/deny, plan mode
- [ ] `/compact` vs `/clear`
- [ ] Hooks (PreToolUse, PostToolUse…) chạy deterministic
- [ ] Headless `claude -p` cho CI; subagents trong `.claude/agents`

### D4: Eval, Testing & Debugging (2,6%)
- [ ] Success criteria đo được, đặt **trước** khi viết prompt
- [ ] Eval set có case thường, biên, khó
- [ ] Chấm: code → LLM-as-judge có rubric → người
- [ ] Regression sau mỗi lần đổi prompt/model; chạy nhiều lần vì output không deterministic
- [ ] Logging/observability ở production

---

## 7. Cheat sheet làm bài (đọc ngày 29/11)

1. Đáp án đúng thường là cơ chế **deterministic** (hook, gate, validation ở backend), không phải "thêm câu vào prompt".
2. Chọn giải pháp **đơn giản nhất** đủ giải quyết vấn đề: workflow trước agent.
3. Chỉ retry lỗi tạm thời (429 có `retry-after`, 500, 504, 529, lỗi kết nối). 4xx khác: sửa request.
4. `max_tokens` và `refusal` là `stop_reason`, **không phải lỗi HTTP**.
5. Realtime → không dùng Batch.
6. Muốn rẻ và nhanh hơn với prompt lặp lại → prompt caching, nội dung tĩnh lên đầu.
7. Tool lỗi → `tool_result` + `is_error: true`, không bao giờ trả kết quả giả.
8. Câu nhiều đáp án: xét từng lựa chọn độc lập.
9. Trung bình ~2 phút/câu. Đánh dấu câu khó, quay lại sau.

---

## 8. Mẫu sổ lỗi

Tạo file `NOTES_LOI_SAI.md`, mỗi câu sai một dòng:

| Ngày | Nguồn (đề, câu) | Domain | Mình chọn | Đáp án đúng | Vì sao sai | Quy tắc rút ra |
|---|---|---|---|---|---|---|
| 11/11 | Paper A, câu 3 | D8 | D | B | Tưởng trả kết quả giả cho mượt | Lỗi tool → `is_error: true`, không bao giờ trả kết quả giả |

---

## 9. Theo dõi tiến độ

### Điểm mock theo domain

| Domain | Mock 1 (22/11) | Mock 2 (25/11) | Mock 3 (27/11) |
|---|---|---|---|
| D2 | | | |
| D5 | | | |
| D1 | | | |
| D6 | | | |
| D8 | | | |
| D7 | | | |
| D3 | | | |
| D4 | | | |
| **Tổng** | **/ 65%** | **/ 75%** | **/ 80%** |

### Quy tắc điều chỉnh
- Domain nào dưới 60% ở mock → dành 1 buổi ôn riêng ngay hôm sau.
- Mock 3 dưới 75% → cân nhắc dời lịch thi thêm 1 tuần nếu được.
- Trễ lịch lab → bỏ Bước 10 và MCP server; **không** bỏ Bước 1, 2, 4, 5, 6, 7.

---

## 10. Checklist ngày thi (30/11)

- [ ] Giấy tờ tùy thân theo yêu cầu đơn vị tổ chức thi
- [ ] Nếu thi online: kiểm tra máy, webcam, mạng, phòng trống trước ít nhất 30 phút
- [ ] Ăn nhẹ, đến sớm
- [ ] Trong phòng thi: lượt 1 làm hết câu chắc chắn; lượt 2 quay lại câu đã đánh dấu; không để trống câu nào
- [ ] Gặp câu phân vân: loại đáp án kiểu "nhắc model trong prompt" và đáp án phức tạp không cần thiết

Chúc thi đậu! 🎯

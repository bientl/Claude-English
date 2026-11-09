# CCDV-F – Note nhanh 8 domain

Đề thi: 53 câu, 120 phút, cần 720/1000 để đậu. Thứ tự dưới đây xếp theo trọng số, từ cao xuống thấp.

| # | Domain | Trọng số |
|---|---|---|
| D2 | Applications & Integration | 33,1% |
| D5 | Model Selection & Optimization | 16,8% |
| D1 | Agents & Workflows | 14,7% |
| D6 | Prompt & Context Engineering | 11,0% |
| D8 | Tools & MCPs | 10,6% |
| D7 | Security & Safety | 8,1% |
| D3 | Claude Code | 3,1% |
| D4 | Eval, Testing & Debugging | 2,6% |

---

## D2 – Applications & Integration (33,1%) ⭐ ưu tiên số 1
**Cần nắm**
- **Messages API**: `model`, `max_tokens` (bắt buộc), `messages` có role user/assistant xen kẽ. System prompt là tham số `system` riêng, không nằm trong messages.
- **Content blocks**: text, image, document (PDF), tool_use, tool_result.
- **Header bắt buộc**: `x-api-key`, `anthropic-version`, `content-type: application/json`.
- **`usage`**: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`.
- **`stop_reason`**:
  - `end_turn`: model trả lời xong.
  - `max_tokens`: output bị cắt, cần tăng `max_tokens` hoặc gọi tiếp.
  - `stop_sequence`: gặp chuỗi dừng đã khai báo.
  - `tool_use`: model muốn gọi tool, phải chạy tool rồi gửi `tool_result` về.
  - `pause_turn`: server tool đang chạy dở, gửi lại để model chạy tiếp.
  - `refusal`: model từ chối trả lời.
- **Streaming (SSE)** để giảm thời gian tới token đầu tiên. Thứ tự event: message_start → content_block_start/delta/stop → message_delta → message_stop.
- **Lỗi và retry**:
  - Nên retry: 429 (rate limit), 500, 529 (overloaded). Dùng exponential backoff + jitter, và tôn trọng header `retry-after`.
  - Không retry: 400, 401, 403, 404, 413. Phải sửa request trước.
- **Rate limits**: RPM, ITPM, OTPM, tính theo từng model.
- **Message Batches API**: xử lý bất đồng bộ, rẻ hơn khoảng 50%, kết quả trả về trong tối đa 24 giờ. Chỉ dùng cho việc không cần trả lời ngay.
- **Các API và tính năng khác**:
  - Files API: upload một lần, tham chiếu nhiều lần qua `file_id`.
  - Citations: trích dẫn dẫn chứng từ tài liệu nguồn.
  - Structured outputs: bắt output theo JSON schema.
- **SDK**: SDK đã có sẵn `max_retries` và `timeout`, async client.

**Bẫy thi**: cần xử lý theo thời gian thực thì không chọn Batch. Gặp `max_tokens` đừng tưởng là lỗi. Lỗi 4xx (trừ 429) thì đừng retry.

## D5 – Model Selection & Optimization (16,8%)
**Cần nắm**
- **Model tiers**: Haiku nhanh và rẻ, Sonnet cân bằng, Opus mạnh nhất. Chọn model bằng eval trên chính tác vụ của mình, không chọn theo cảm tính.
- **Mixed models**: model mạnh làm orchestrator, model rẻ làm worker hoặc phân loại.
- **Đòn bẩy latency**: model nhỏ hơn, streaming, giảm output, prompt caching, chạy song song.
- **Đòn bẩy chi phí**: model nhỏ, caching, Batch, cắt bớt context.
- **Prompt caching**:
  - Thứ tự prefix: **tools → system → messages**. Thay đổi bất kỳ chỗ nào ở trước sẽ làm mất cache mọi phần phía sau.
  - Đặt nội dung tĩnh lên đầu, nội dung động xuống cuối.
  - Đánh dấu bằng `cache_control`. Có độ dài tối thiểu mới cache được (tùy model). TTL mặc định 5 phút, có tuỳ chọn 1 giờ.
  - Ghi cache đắt hơn input thường một chút; đọc cache rẻ hơn rất nhiều.
  - Chat nhiều lượt: đặt breakpoint ở message cuối để prefix tăng dần vẫn được cache.
- **Kiểm tra cache**: `cache_read_input_tokens > 0` nghĩa là cache hit. Nếu bằng 0 thì xem có gì thay đổi ở phần prefix không (timestamp, thứ tự tool…).
- **Extended / adaptive thinking**: dùng cho bài cần suy luận nhiều bước. Đổi lại sẽ tốn token và tăng latency.

**Bẫy thi**: chèn timestamp hoặc ID động vào system prompt sẽ phá cache. Đổi thứ tự tool cũng phá cache.

## D1 – Agents & Workflows (14,7%)
**Cần nắm**
- **Workflow vs agent**:
  - Workflow: luồng do code định sẵn.
  - Agent: model tự quyết bước tiếp theo.
  - Luôn bắt đầu đơn giản; chỉ thêm độ phức tạp khi đã chứng minh là cần.
- **6 pattern**:
  - Prompt chaining: kèm gate kiểm tra bằng code giữa các bước.
  - Routing: phân loại rồi chuyển đến đúng luồng xử lý.
  - Parallelization: sectioning (chia việc) hoặc voting (chạy nhiều lần lấy đồng thuận).
  - Orchestrator-workers: các subtask không biết trước.
  - Evaluator-optimizer: một model viết, một model chấm, lặp lại.
  - Agent loop: plan → act → observe.
- **Stopping criteria**: giới hạn số vòng lặp, ngân sách token hoặc thời gian, có checkpoint.
- **Subagents**: cô lập context, chạy song song, trả về bản tóm tắt gọn.
- **Hook (deterministic) vs model discretion**: việc **bắt buộc phải xảy ra** thì dùng hook hoặc code, không dựa vào việc nhắc trong prompt.
- **Memory**: chỉ lưu có chọn lọc. Agent chạy lâu cần durable state và idempotency.
- **ACI**: thiết kế tool dễ dùng cho model (tên rõ ràng, mô tả tốt, khó dùng sai).

**Bẫy thi**: tác vụ có các bước cố định thì chọn workflow, không chọn agent. Muốn "đảm bảo luôn luôn" thì cần cơ chế deterministic.

## D6 – Prompt & Context Engineering (11,0%)
**Cần nắm**
- **Viết prompt rõ ràng, trực tiếp**: kèm context và lý do. Nói điều cần làm thay vì điều cấm.
- **Cấu trúc prompt**:
  - Dùng XML tags để tách instruction, dữ liệu và ví dụ.
  - Few-shot: 3–5 ví dụ đa dạng.
  - Role đặt trong system prompt.
- **Chain of thought**: cho model suy nghĩ trong một tag riêng, câu trả lời đặt trong tag khác để dễ parse.
- **Long context**: đặt tài liệu dài lên đầu, câu hỏi ở cuối. Yêu cầu model trích dẫn trước rồi mới trả lời.
- **Giảm hallucination**: cho phép trả lời "không biết", bắt trích dẫn nguồn, có bước kiểm chứng.
- **Context window**: system prompt, tools, lịch sử hội thoại và output đều tính vào. Context engineering cho agent nghĩa là chỉ nạp thứ cần, tóm tắt hoặc compact khi dài.
- **Output nhất quán**: đặc tả format, đưa ví dụ, dùng structured outputs, prefill.

## D8 – Tools & MCPs (10,6%)
**Cần nắm**
- **Định nghĩa tool**: `name`, `description` (phần quan trọng nhất), `input_schema` (JSON Schema).
- **Vòng tool use**: model trả `tool_use` (có `id`) → app chạy tool → gửi `tool_result` có `tool_use_id` khớp trong message role **user**.
- **Parallel tool use**: nhiều `tool_use` trong một lượt thì trả tất cả `tool_result` trong **cùng một** user message.
- **Lỗi tool**: trả `tool_result` với `is_error: true` kèm thông báo rõ ràng để model tự sửa.
- **`tool_choice`**:
  - `auto`: model tự quyết.
  - `any`: bắt buộc gọi một tool nào đó.
  - `tool`: bắt buộc gọi tool chỉ định.
  - `none`: không gọi tool.
- **Thiết kế khi có nhiều tool**:
  - Đặt tên có namespace, mô tả rõ, tránh trùng chức năng.
  - Rất nhiều tool thì dùng tool search + `defer_loading`.
- **Client vs server tools**:
  - Client tool: app tự chạy.
  - Server tool (web search…): Anthropic chạy, có thể trả `pause_turn`.
- **MCP**:
  - Kiến trúc: host (ứng dụng) chứa client, mỗi client nối với một server.
  - Primitives: tools (model gọi), resources (dữ liệu cho ứng dụng), prompts (template cho user).
  - Transports: stdio (local) và Streamable HTTP (remote).

## D7 – Security & Safety (8,1%)
**Cần nắm**
- **Quyền và bí mật**:
  - Least privilege cho tool và credential (read-only nếu đủ dùng).
  - Secrets để trong vault hoặc biến môi trường, không đưa vào prompt.
- **Prompt injection**:
  - Direct: đến từ user. Indirect: nằm trong tài liệu, web hoặc kết quả tool.
  - Không có biện pháp đơn lẻ nào chặn hết, nên cần **defense in depth**.
- **Không tin output của model**:
  - Coi output là untrusted: validate và escape trước khi chạy hoặc render.
  - **Authorization kiểm tra ở backend**, không tin model tự kiểm tra quyền.
- **Hành động tác động lớn** (chuyển tiền, xoá dữ liệu, gửi ra ngoài) phải có human-in-the-loop.
- **Privacy và multi-tenant**:
  - Privacy: tối thiểu hoá dữ liệu, che PII, giới hạn thời gian lưu log.
  - Multi-tenant: cách ly dữ liệu giữa các khách hàng.

**Bẫy thi**: đáp án "thêm câu vào system prompt để model không làm X" hầu như luôn sai nếu có lựa chọn kiểm soát bằng code hoặc backend.

## D3 – Claude Code (3,1%) – chỉ đọc lướt
- **CLAUDE.md**: memory theo project/user, nạp tự động.
- **Slash commands & Skills**: custom slash commands, Skills.
- **MCP**: scope local/project/user; dùng `.mcp.json` để chia sẻ cho team.
- **Permissions**: allow/ask/deny, các permission mode, plan mode (khám phá → lập kế hoạch → code → commit).
- **Quản lý context**: `/compact` (tóm tắt, giữ lại) vs `/clear` (xoá sạch).
- **Hooks**: chạy deterministic quanh tool call (PreToolUse, PostToolUse…).
- **Headless**: `claude -p` cho CI.
- **Subagents**: khai báo trong `.claude/agents`.

## D4 – Eval, Testing & Debugging (2,6%) – chỉ đọc lướt
- Xác định success criteria đo được **trước** khi viết prompt.
- Eval set gồm cả case thường, case biên và case khó.
- **Cách chấm**: ưu tiên chấm bằng code → LLM-as-judge (có rubric) → người chấm.
- **Regression**: chạy lại eval sau mỗi lần đổi prompt hoặc model. Output không deterministic nên chạy nhiều lần.
- **Debug**: debug có hệ thống, kèm logging/observability ở production.

---

## 4 quy tắc làm bài
1. Đáp án đúng thường là cơ chế **deterministic** (hook, gate, validation ở backend), không phải "nhắc model trong prompt".
2. Chọn giải pháp **đơn giản nhất** đủ giải quyết vấn đề.
3. Câu nhiều đáp án: xét từng lựa chọn độc lập.
4. Trung bình khoảng 2 phút/câu. Đánh dấu câu khó, quay lại sau.

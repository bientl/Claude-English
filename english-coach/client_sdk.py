"""client.py: tạo client Anthropic và hàm call_claude() dùng chung cho mọi chế độ. [D2]

Các chế độ trong modes/*.py gọi call_claude() thay vì gọi client.messages.create trực tiếp,
để chỗ log usage và xử lý stop_reason chỉ nằm ở một nơi.
"""
import os
import sys

import anthropic
from dotenv import load_dotenv

# Terminal Windows mặc định dùng cp1252, print tiếng Việt sẽ lỗi UnicodeEncodeError.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# [D7] Key chỉ đọc từ .env / biến môi trường. Không hard-code, không in ra log.
load_dotenv()

# [D5] Model đọc từ biến môi trường, mặc định Haiku (nhanh, rẻ).
MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")

# [D2] Ghi tường minh max_retries và timeout (không dựa vào mặc định ngầm).
# SDK TỰ retry với exponential backoff, tôn trọng header retry-after, với các lỗi tạm thời:
#   - lỗi kết nối và timeout
#   - 408, 409, 429 (rate limit), và mọi lỗi 5xx (gồm 500, 529 overloaded)
# SDK KHÔNG retry lỗi do request: 400, 401, 403, 404, 413, 422. Retry cũng vô ích vì
# gửi lại y nguyên thì vẫn lỗi y nguyên.
# Mặc định của SDK: max_retries=2, timeout=10 phút. Ở đây đặt lại cho rõ.
client = anthropic.Anthropic(max_retries=2, timeout=60.0)

# [D1] Giới hạn số lần tự gửi lại khi gặp pause_turn, tránh vòng lặp vô hạn.
MAX_PAUSE_TURNS = 5


def call_claude(system, messages, max_tokens=500, **kwargs):
    """Gọi Messages API một lần (tự nối tiếp nếu pause_turn), log usage và stop_reason.

    - system: chuỗi system prompt. [D2] `system` là tham số RIÊNG của API,
      KHÔNG đưa vào `messages` (không có role "system" trong messages).
    - messages: list {"role": ..., "content": ...}. [D2] Role phải xen kẽ user/assistant
      và message đầu tiên phải là "user". API là STATELESS: mỗi lần gọi phải gửi lại
      toàn bộ lịch sử, model không tự nhớ lượt trước.
    - max_tokens: BẮT BUỘC với Messages API.
    - **kwargs: chuyển thẳng cho API (temperature, tools, stop_sequences, ...).

    Trả về đối tượng response gốc của SDK. Bên gọi tự xử lý stop_reason == "tool_use".
    Lỗi API (anthropic.APIStatusError, APIConnectionError) được để nổi lên cho bên gọi bắt.
    """
    messages = list(messages)  # không sửa list của bên gọi

    for _ in range(MAX_PAUSE_TURNS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            **kwargs,
        )
        log_response(response)

        if response.stop_reason != "pause_turn":
            return response

        # [D1, D8] pause_turn: server tool (vd web search) chạy dở vì chạm giới hạn vòng lặp.
        # Đây KHÔNG phải lỗi và KHÔNG phải output bị cắt. Gửi lại nguyên content của
        # assistant vào messages để model chạy tiếp.
        messages.append({"role": "assistant", "content": response.content})

    print(f"[client] CẢNH BÁO: vẫn pause_turn sau {MAX_PAUSE_TURNS} lần, dừng lại.")
    return response


def log_response(response):
    """In stop_reason và usage ra terminal (không bao giờ in key)."""
    u = response.usage
    print(
        f"[client] model={response.model} stop_reason={response.stop_reason} "
        f"input={u.input_tokens} output={u.output_tokens} "
        f"cache_creation={u.cache_creation_input_tokens or 0} "
        f"cache_read={u.cache_read_input_tokens or 0}"
    )
    notice = stop_reason_notice(response)
    if notice:
        print(f"[client] {notice}")


def stop_reason_notice(response):
    """[D2] Xử lý từng giá trị stop_reason. Trả về câu cảnh báo, hoặc None nếu bình thường."""
    reason = response.stop_reason
    if reason == "end_turn":
        return None  # model nói xong tự nhiên
    if reason == "max_tokens":
        return "CẢNH BÁO: output bị cắt vì chạm max_tokens. Tăng max_tokens hoặc yêu cầu trả lời ngắn hơn."
    if reason == "stop_sequence":
        # response.stop_sequence cho biết chuỗi dừng nào đã khớp
        return f"Model dừng vì gặp stop_sequence: {response.stop_sequence!r}"
    if reason == "tool_use":
        return "Model muốn gọi tool: bên gọi phải chạy tool rồi gửi tool_result."
    if reason == "pause_turn":
        return "pause_turn: server tool đang chạy dở, cần gửi lại để model chạy tiếp."
    if reason == "refusal":
        # Refusal đến dưới dạng HTTP 200, không phải exception.
        return "Model từ chối trả lời (refusal)."
    if reason == "model_context_window_exceeded":
        return "CẢNH BÁO: đầy context window, output bị cắt."
    return f"stop_reason lạ: {reason!r} (kiểm tra lại docs)."


def get_text(response):
    """[D2] response.content là LIST content block; chỉ ghép các block type == "text"."""
    return "".join(b.text for b in response.content if b.type == "text")


def usage_dict(response):
    """Gói usage thành dict để trả về trình duyệt hiển thị."""
    u = response.usage
    return {
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
        "cache_creation_input_tokens": u.cache_creation_input_tokens or 0,
        "cache_read_input_tokens": u.cache_read_input_tokens or 0,
    }


if __name__ == "__main__":
    # Thử nhanh: python client.py
    r = call_claude("You are a friendly English teacher.", [{"role": "user", "content": "Hello"}], max_tokens=100)
    print("Trả lời:", get_text(r))

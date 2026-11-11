"""client.py: gọi Messages API bằng HTTP thô (urllib), KHÔNG dùng anthropic SDK. [D2]

Bản dùng SDK được giữ ở client_sdk.py để đối chiếu.
Các chế độ trong modes/*.py gọi call_claude() thay vì tự gửi HTTP, để chỗ log usage
và xử lý stop_reason chỉ nằm ở một nơi.
"""
import json
import os
import sys
import urllib.error
import urllib.request

from dotenv import load_dotenv

# Terminal Windows mặc định dùng cp1252, print tiếng Việt sẽ lỗi UnicodeEncodeError.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# [D7] Key chỉ đọc từ .env / biến môi trường. Không hard-code, không in ra log.
load_dotenv()

# [D5] Model đọc từ biến môi trường, mặc định Haiku (nhanh, rẻ).
MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")

API_URL = "https://api.anthropic.com/v1/messages"
# [D2] anthropic-version là header BẮT BUỘC: chọn phiên bản của API (không phải phiên bản model).
API_VERSION = "2023-06-01"
# [D2] Timeout ghi tường minh (giây). Không có SDK nên cũng KHÔNG có retry tự động:
# retry sẽ tự viết ở Bước 4 (retry_with_backoff).
TIMEOUT = 60

# [D1] Giới hạn số lần tự gửi lại khi gặp pause_turn, tránh vòng lặp vô hạn.
MAX_PAUSE_TURNS = 5


class ApiError(Exception):
    """API trả về mã lỗi HTTP (4xx/5xx). Giữ lại mã, loại lỗi và request_id để xử lý/báo support."""

    def __init__(self, status_code, error_type, message, request_id=None):
        super().__init__(f"{status_code} {error_type}: {message}")
        self.status_code = status_code
        self.error_type = error_type  # ví dụ invalid_request_error, authentication_error
        self.message = message
        self.request_id = request_id


class ConnectionFailed(Exception):
    """Không kết nối được hoặc quá thời gian chờ (không có mã HTTP)."""


def _post(payload):
    """Gửi một request POST tới /v1/messages, trả về dict JSON đã parse."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # [D7] Chỉ báo là thiếu key, không in giá trị key.
        raise ConnectionFailed("Thiếu ANTHROPIC_API_KEY (kiểm tra file .env).")

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        # [D2] Lỗi HTTP không thành response thường: urllib ném HTTPError, body lỗi đọc qua e.read().
        # Dạng body: {"type": "error", "error": {"type": "...", "message": "..."}}
        request_id = e.headers.get("request-id")
        try:
            err = json.loads(e.read()).get("error", {})
        except ValueError:
            err = {}
        raise ApiError(e.code, err.get("type", "unknown"), err.get("message", e.reason), request_id) from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise ConnectionFailed(f"Không kết nối được tới API: {e}") from None


def call_claude(system, messages, max_tokens=500, **kwargs):
    """Gọi Messages API (tự nối tiếp nếu pause_turn), log usage và stop_reason.

    - system: chuỗi system prompt. [D2] `system` là tham số RIÊNG của API,
      KHÔNG đưa vào `messages` (không có role "system" trong messages).
    - messages: list {"role": ..., "content": ...}. [D2] Role phải xen kẽ user/assistant
      và message đầu tiên phải là "user". API là STATELESS: mỗi lần gọi phải gửi lại
      toàn bộ lịch sử, model không tự nhớ lượt trước.
    - max_tokens: BẮT BUỘC với Messages API (thiếu thì API trả 400).
    - **kwargs: thêm thẳng vào body (temperature, tools, stop_sequences, ...).

    Trả về response là DICT JSON gốc của API. Bên gọi tự xử lý stop_reason == "tool_use".
    Lỗi được để nổi lên cho bên gọi bắt: ApiError (mã HTTP lỗi) hoặc ConnectionFailed.
    """
    messages = list(messages)  # không sửa list của bên gọi

    for _ in range(MAX_PAUSE_TURNS + 1):
        response = _post(
            {
                "model": MODEL,
                "max_tokens": max_tokens,
                "system": system,
                "messages": messages,
                **kwargs,
            }
        )
        log_response(response)

        if response["stop_reason"] != "pause_turn":
            return response

        # [D1, D8] pause_turn: server tool (vd web search) chạy dở vì chạm giới hạn vòng lặp.
        # Đây KHÔNG phải lỗi và KHÔNG phải output bị cắt. Gửi lại nguyên content của
        # assistant vào messages để model chạy tiếp.
        messages.append({"role": "assistant", "content": response["content"]})

    print(f"[client] CẢNH BÁO: vẫn pause_turn sau {MAX_PAUSE_TURNS} lần, dừng lại.")
    return response


def log_response(response):
    """In stop_reason và usage ra terminal (không bao giờ in key)."""
    u = response["usage"]
    print(
        f"[client] model={response['model']} stop_reason={response['stop_reason']} "
        f"input={u['input_tokens']} output={u['output_tokens']} "
        f"cache_creation={u.get('cache_creation_input_tokens') or 0} "
        f"cache_read={u.get('cache_read_input_tokens') or 0}"
    )
    notice = stop_reason_notice(response)
    if notice:
        print(f"[client] {notice}")


def stop_reason_notice(response):
    """[D2] Xử lý từng giá trị stop_reason. Trả về câu cảnh báo, hoặc None nếu bình thường."""
    reason = response["stop_reason"]
    if reason == "end_turn":
        return None  # model nói xong tự nhiên
    if reason == "max_tokens":
        return "CẢNH BÁO: output bị cắt vì chạm max_tokens. Tăng max_tokens hoặc yêu cầu trả lời ngắn hơn."
    if reason == "stop_sequence":
        # response["stop_sequence"] cho biết chuỗi dừng nào đã khớp
        return f"Model dừng vì gặp stop_sequence: {response.get('stop_sequence')!r}"
    if reason == "tool_use":
        return "Model muốn gọi tool: bên gọi phải chạy tool rồi gửi tool_result."
    if reason == "pause_turn":
        return "pause_turn: server tool đang chạy dở, cần gửi lại để model chạy tiếp."
    if reason == "refusal":
        # Refusal đến dưới dạng HTTP 200, không phải lỗi.
        return "Model từ chối trả lời (refusal)."
    if reason == "model_context_window_exceeded":
        return "CẢNH BÁO: đầy context window, output bị cắt."
    return f"stop_reason lạ: {reason!r} (kiểm tra lại docs)."


def get_text(response):
    """[D2] response["content"] là LIST content block; chỉ ghép các block type == "text"."""
    return "".join(b["text"] for b in response["content"] if b["type"] == "text")


def usage_dict(response):
    """Gói usage thành dict để trả về trình duyệt hiển thị."""
    u = response["usage"]
    return {
        "input_tokens": u["input_tokens"],
        "output_tokens": u["output_tokens"],
        "cache_creation_input_tokens": u.get("cache_creation_input_tokens") or 0,
        "cache_read_input_tokens": u.get("cache_read_input_tokens") or 0,
    }


if __name__ == "__main__":
    # Thử nhanh: python client.py
    r = call_claude("You are a friendly English teacher.", [{"role": "user", "content": "Hello"}], max_tokens=100)
    print("Trả lời:", get_text(r))

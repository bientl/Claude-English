# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục đích dự án

Đây là project làm một app học tiếng Anh. Mục tiêu chính không phải app mà là thực hành các concept để thi chứng chỉ Claude developer (CCDV-F). Chúng ta vừa build vừa học các domain. Khi chọn cách implement, ưu tiên cách cho phép thực hành một domain của đề thi (Messages API, tool use, prompt caching, agents, MCP, eval...) hơn là cách đơn giản nhất.

## Trạng thái hiện tại

Repo chưa có source code, chưa có build/lint/test command, và chưa chọn tech stack. Khi bắt đầu code, hãy cập nhật file này với các lệnh và kiến trúc thật.

## Tài liệu tham khảo (thư mục `Document/`)

- `CCDV-F_Note_8_Domain.md`: note nhanh 8 domain của đề thi, xếp theo trọng số. Đề thi: 53 câu, 120 phút, cần 720/1000 để đậu. Đọc file này trước khi chọn domain nào để thực hành.
- `CCDV-F_Cam_Nang_Kien_Thuc.html`: cẩm nang kiến thức (file lớn, ~450 KB, nên grep thay vì đọc cả file).
- `CCDV-F_De_Thi_Tieng_Viet.html`: đề thi bản tiếng Việt (file lớn, ~640 KB, nên grep thay vì đọc cả file).

Trọng số domain (cao xuống thấp): D2 Applications & Integration 33,1% · D5 Model Selection & Optimization 16,8% · D1 Agents & Workflows 14,7% · D6 Prompt & Context Engineering 11,0% · D8 Tools & MCPs 10,6% · D7 Security & Safety 8,1% · D3 Claude Code 3,1% · D4 Eval, Testing & Debugging 2,6%. D2 là ưu tiên số 1.

## Lưu ý

- `CLAUDE.md.txt` là bản ghi chú ban đầu (tên file sai đuôi); nội dung của nó đã được gộp vào file này.
- Tài liệu và ghi chú học viết bằng tiếng Việt; giữ nguyên ngôn ngữ này khi thêm ghi chú mới.

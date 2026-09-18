# CP3 codebase

## Chạy AI thật cục bộ

1. Tạo biến môi trường `GEMINI_API_KEY` trong terminal (không ghi key vào file hoặc commit).
2. Chạy server từ thư mục gốc repo:

```powershell
$env:GEMINI_API_KEY = "<key-local>"
python codebase/server.py
```

3. Mở <http://127.0.0.1:8000/?ai=1>. Khi gửi câu hỏi, trình duyệt gọi `/api/ask`; server truy xuất top-k, gọi Gemini thật và chạy validator trước khi render.

Có thể kiểm tra lõi trực tiếp:

```powershell
python codebase/ai_tutor.py --question "Embedding là gì?" --json
```

Trace trả về gồm prompt, phản hồi thô, nguồn được phép, kết quả validator và latency. Không gửi dữ liệu khảo sát/raw chatlog vào endpoint; golden set chỉ giữ mã turn và câu hỏi đã rút gọn.

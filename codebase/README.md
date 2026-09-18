# CP3 codebase

## Chạy AI thật cục bộ

1. Tạo biến môi trường `OPENROUTER_API_KEY` trong terminal (không ghi key vào file hoặc commit).
2. Chạy server từ thư mục gốc repo:

```powershell
$secret = Read-Host "OpenRouter API key" -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new("", $secret).Password
Remove-Variable secret
.\.venv\Scripts\python.exe codebase\server.py
```

3. Mở <http://127.0.0.1:8000/?ai=1>. Khi gửi câu hỏi, trình duyệt gọi `/api/ask`; server truy xuất top-k, gọi model qua OpenRouter và chạy validator trước khi render.

Model mặc định là `google/gemini-3.6-flash`, cùng phiên bản Gemini đã dùng ở lượt đo trước. Có thể chọn model khác bằng biến môi trường `OPENROUTER_MODEL` hoặc tham số `--model` khi chạy `ai_tutor.py`. OpenRouter dùng [Chat Completions API](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request) và [model slug này](https://openrouter.ai/google/gemini-3.6-flash).

Có thể kiểm tra lõi trực tiếp:

```powershell
python codebase/ai_tutor.py --question "Embedding là gì?" --json
```

Trace trả về gồm prompt, phản hồi thô, nguồn được phép, kết quả validator và latency. Không gửi dữ liệu khảo sát/raw chatlog vào endpoint; golden set chỉ giữ mã turn và câu hỏi đã rút gọn.

## Video CP3 30 giây

Chạy server và mở `http://127.0.0.1:8000/?ai=1`. Chỉ quay cửa sổ trình duyệt: nhập “RAG là gì?”, bấm gửi, chờ câu trả lời AI thật và mở trích dẫn. Giữ terminal/API key ngoài khung hình. Lưu video để đội trưởng nộp cùng số đo từ `eval/run1_results.json`.

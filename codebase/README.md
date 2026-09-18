# CP3 codebase

## Chạy AI thật cục bộ

1. Tạo biến môi trường `GEMINI_API_KEY` trong terminal (không ghi key vào file hoặc commit).
2. Chạy server từ thư mục gốc repo:

```powershell
$secret = Read-Host "Gemini API key" -AsSecureString
$env:GEMINI_API_KEY = [System.Net.NetworkCredential]::new("", $secret).Password
Remove-Variable secret
.\.venv\Scripts\python.exe codebase\server.py
```

3. Mở <http://127.0.0.1:8000/?ai=1>. Khi gửi câu hỏi, trình duyệt gọi `/api/ask`; server truy xuất top-k, gọi Gemini thật và chạy validator trước khi render.

Model mặc định là `gemini-3.6-flash`. Có thể chọn model khác bằng biến môi trường `GEMINI_MODEL` hoặc tham số `--model` khi chạy `ai_tutor.py`.

Có thể kiểm tra lõi trực tiếp:

```powershell
python codebase/ai_tutor.py --question "Embedding là gì?" --json
```

Trace trả về gồm prompt, phản hồi thô, nguồn được phép, kết quả validator và latency. Không gửi dữ liệu khảo sát/raw chatlog vào endpoint; golden set chỉ giữ mã turn và câu hỏi đã rút gọn.

## Video CP3 30 giây

Chạy server và mở `http://127.0.0.1:8000/?ai=1`. Chỉ quay cửa sổ trình duyệt: nhập “RAG là gì?”, bấm gửi, chờ câu trả lời AI thật và mở trích dẫn. Giữ terminal/API key ngoài khung hình. Lưu video để đội trưởng nộp cùng số đo từ `eval/run1_results.json`.

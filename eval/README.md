# CP3 evaluation

`golden_set.json` có 20 case: 5 case cho mỗi lớp ①–④, 10 case thường gặp, 4 case hiếm và 10 case phát triển từ `source_turn_id` trong chatlog riêng. Phần `input` đã được rút gọn để không đưa raw chatlog, tên học viên hoặc dữ liệu khảo sát vào repository.

## Chạy lượt đo

Từ thư mục gốc repo, sau khi đặt `GEMINI_API_KEY` trong terminal:

```powershell
python eval/run_eval.py --live
```

Lệnh tạo:

- `run1_results.json`: bảng đạt/trượt, tỷ lệ và phân tích lỗi;
- `run1_trace.jsonl`: prompt, phản hồi thô của model và kết quả validator cho từng case. Trace chỉ dùng knowledge base tổng hợp của prototype và câu hỏi đã rút gọn.

`--limit N` dùng để chạy thử một phần bộ. Không commit API key, `.env`, raw data hoặc file Excel.

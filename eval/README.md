# CP3 evaluation

`golden_set.json` có 20 case: 5 case cho mỗi lớp ①–④, 10 case thường gặp, 4 case hiếm và 12 case phát triển từ `source_turn_id` đã đối chiếu với chatlog riêng. Phần `input` đã được rút gọn để không đưa raw chatlog, tên học viên hoặc dữ liệu khảo sát vào repository. Các case nguồn mâu thuẫn/khuyết/nghi sai dùng `source_fixture` độc lập với `expected_reason`; runner không đưa đáp án kỳ vọng vào tutor.

## Chạy lượt đo

Từ thư mục gốc repo, sau khi đặt `GEMINI_API_KEY` trong terminal:

```powershell
python eval/run_eval.py --live
```

Lệnh tạo:

- `run1_results.json`: bảng đạt/trượt, tỷ lệ và phân tích lỗi;
- `run1_trace.jsonl`: prompt, phản hồi thô của model và kết quả validator cho từng case. Trace chỉ dùng knowledge base tổng hợp của prototype và câu hỏi đã rút gọn.

`--limit N` dùng để chạy thử một phần bộ. Không commit API key, `.env`, raw data hoặc file Excel.

Nguyên nhân của lượt chạy trước khi audit và những sửa đổi cho bộ v2 nằm trong [`run1_analysis.md`](run1_analysis.md).

Trường `model` trong báo cáo là model được **yêu cầu**; `model_attempts` đếm số case đi tới lệnh gọi API, còn `model_responses` đếm số case thực sự nhận được phản hồi thô. Model mặc định là `gemini-3.6-flash`. Bộ `golden_set.json` đã được sửa ở phiên bản `cp3-v2-source-audited`; kết quả `run1` sinh trước phiên bản này không thể dùng làm tỷ lệ chất lượng của bộ mới. Chạy lại lệnh trên để cập nhật kết quả, giữ trace cũ riêng nếu cần đối chiếu.

Nếu `model_attempts > 0` nhưng `model_responses = 0`, lệnh trả exit code 2. Bảng đạt/trượt vẫn được lưu để kiểm tra lỗi hạ tầng, nhưng chưa đo được chất lượng trả lời của AI.

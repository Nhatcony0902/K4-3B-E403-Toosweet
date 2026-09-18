# Phân tích lượt đo CP3 ngày 18/9

## Lượt v1 trước audit

Lệnh `--live` chạy 20 case với `gemini-3.6-flash`: 9 đạt, 11 không đạt (45%). Có 13 case đi tới API, 7 case nhận phản hồi model. Sáu case bị HTTP 503 `UNAVAILABLE` do model đang có nhu cầu cao; đây là lỗi dịch vụ, không phải đánh giá đúng/sai của nội dung. [Báo cáo v1](history/run1_v1_unaudited_results.json) và [trace v1](history/run1_v1_unaudited_trace.jsonl) được lưu riêng để lệnh chạy v2 không ghi đè bằng chứng này.

Trong 11 case không đạt:

| Nhóm nguyên nhân | Case | Số lượng | Nhận xét |
|---|---|---:|---|
| HTTP 503 | G01, G04, G06, G08, G09, G20 | 6 | Không có phản hồi model; thử lại với backoff ngắn. |
| Định tuyến phạm vi | G14, G15 | 2 | Yêu cầu web và lịch học chưa được nhận diện đúng. |
| Nhãn kỳ vọng quá chặt/không đúng ý | G05, G10, G18 | 3 | G05/G18 từ chối an toàn với mã khác; G10 thiếu đoạn được chọn nên hỏi làm rõ phù hợp hơn. |

Case G07 có `CLARIFY` đúng nhưng model gán `reason_code=SOURCE_UNCLEAR`; backend v1 chưa chuẩn hóa mã này. Validator v2 đã xử lý. Lượt v1 còn hai lỗi của **bộ đo**: nhiều `source_turn_id` không tương ứng câu hỏi, và G16/G17/G19 được runner truyền `expected_reason` trực tiếp vào tutor. Vì vậy **9/20 không phải số đo chất lượng có thể nộp làm kết luận**. Giữ lượt v1 như dấu vết phát hiện lỗi.

## Sửa cho lượt v2

- `golden_set.json` có 20 case, 12 mã turn khác nhau được đối chiếu với chatlog K4 không preset. Mỗi case phát triển từ log có ghi cách rút gọn trong `provenance_note`.
- Runner chỉ cấp câu hỏi, trạng thái làm rõ và nguồn/metadata fixture; đáp án kỳ vọng chỉ được dùng khi chấm. Các fixture mâu thuẫn, khuyết và gắn cờ được khai báo riêng trong case.
- Định tuyến bổ sung cách hỏi về lịch/hạn nộp, yêu cầu điền hộ, system diagnostic và câu hỏi thiếu tham chiếu. Validator chuẩn hóa mã lý do của `CLARIFY`, giới hạn một lần làm rõ, kiểm tra bài của citation và ID trùng. HTTP 503 được thử lại tối đa hai lần với khoảng chờ tăng dần.

**Cần thực hiện tiếp:** chạy lại `python eval/run_eval.py --live` trên bộ v2, ghi số đạt/trượt mới theo từng lớp, đọc từng phản hồi để phân tích false `GROUNDED` và từ chối sai. Hai thành viên cần chấm độc lập cùng 5 output; nếu lệch từ 1/5 trở lên, sửa mô tả tiêu chí trước khi dùng tỷ lệ làm quality bar. Video 30 giây và việc nộp form CP3 do nhóm thực hiện.

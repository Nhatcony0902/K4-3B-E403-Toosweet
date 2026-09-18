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

## Lượt v2 sau audit nguồn gốc và chấm lại từ trace

Lượt chạy live trên `cp3-v2-source-audited` gửi 8 yêu cầu Gemini, nhận 5 phản hồi thật. Runner ban đầu in **19/20 (95%)**, nhưng G04 và G05 bị HTTP 429 `quota exceeded`, không có phản hồi model; trạng thái dự phòng `NO_SOURCE/PROCESSING_ERROR` tình cờ khớp nhãn `NO_SOURCE` nên bị tính đạt sai. G20 cũng bị HTTP 429 và đã được tính trượt. `python eval/run_eval.py --rescore` đọc lại trace gốc, không gọi API, cho kết quả đúng của lượt này: **17/20 (85%)**, 3 lỗi hạ tầng G04/G05/G20, không có case sai nhãn khác theo bộ chấm trạng thái hiện tại. Theo lớp: ① 3/5, ② 5/5, ③ 5/5, ④ 4/5. [Kết quả v2](run1_results.json) và [trace v2](run1_trace.jsonl) là bằng chứng gốc của lần chạy; `failure_analysis` giờ đếm đủ ba lỗi.

Trong 5 phản hồi model, G01/G02/G08 trả `GROUNDED` với citation có thật. G03 trả `NO_SOURCE` nhưng dùng mã lý do ngoài hợp đồng (`INSUFFICIENT_CONTEXT`), nên validator chuyển thành `NO_SOURCE/VALIDATION_FAILED`. G18 trả `GROUNDED` để bác bỏ việc mọi hệ thống bắt buộc dùng đúng 400 token; validator chặn vì số 400 nằm trong câu hỏi nhưng không nằm trong đoạn nguồn. Đây có thể là trường hợp chặn quá chặt; nhãn kỳ vọng `NO_SOURCE` cho G18 cũng cần hai người xem lại vì nguồn nêu khoảng 300–500 token, đủ để bác bỏ việc bài học bắt buộc đúng 400 token nhưng không đủ để kết luận về *mọi hệ thống*. Vì thế **85% là tỷ lệ khớp trạng thái đầu ra cuối cùng trên 20 case**, không phải độ chính xác ngữ nghĩa của model hay tỷ lệ đúng của 20 lần gọi AI.

**Cần thực hiện tiếp:** hai thành viên chấm độc lập 5 output có phản hồi model, đặc biệt G18; nếu lệch từ 1/5 trở lên, sửa mô tả tiêu chí trước khi dùng tỷ lệ làm quality bar. Khi quota cho phép, chạy lượt mới bằng `python eval/run_eval.py --live --run-name run2`; runner sẽ từ chối ghi đè trace v2. Video 30 giây và việc nộp form CP3 do nhóm thực hiện.

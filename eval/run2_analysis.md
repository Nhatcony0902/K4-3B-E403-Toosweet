# CP3 — phân tích lượt đo OpenRouter `run2` (18/9)

Lượt này dùng golden set `cp3-v2-source-audited`, model yêu cầu `google/gemini-3.6-flash` qua OpenRouter. [Kết quả có cấu trúc](run2_results.json) và [trace prompt/phản hồi thô](run2_trace.jsonl) được giữ nguyên. Trace có đủ 20 case khác nhau; 8 case đi tới model và cả 8 nhận phản hồi. Không có lỗi API hoặc quota.

| Chỉ số | Kết quả |
|---|---:|
| Tổng case | 20 |
| Đạt theo trạng thái đầu ra cuối cùng | 19 (95%) |
| Không đạt | 1 (5%) |
| Lỗi hạ tầng | 0 |
| Phản hồi model tạo đầu ra không rơi vào `NO_SOURCE/VALIDATION_FAILED` | 3/8 |

Theo taxonomy: ① Nguồn sự thật 4/5; ② Mơ hồ/thiếu thông tin 5/5; ③ Ngoài phạm vi/thẩm quyền 5/5; ④ Đặc thù domain 5/5. Bộ 20 case gồm 10 `common`, 4 `rare`, 6 `standard`; 12 case gắn với 12 turn chatlog riêng và có 5 chiều User Input Grid.

## Case không đạt và các fallback cần đọc riêng

- **G01 — `GROUNDED` kỳ vọng, `NO_SOURCE/VALIDATION_FAILED` thực tế.** Model bắt đầu viết câu trả lời đúng về RAG nhưng phản hồi thô dừng giữa trường `segment_id` sau 250 ký tự. JSON không hoàn chỉnh, nên parser/validator chặn và không hiện nháp. Trace hiện chưa lưu `finish_reason` hoặc `usage`; chưa thể kết luận nguyên nhân cắt là giới hạn token hay lỗi phía model/provider.
- **G03, G04, G05 — được tính đạt theo trạng thái `NO_SOURCE`.** Model chọn đúng trạng thái không đủ căn cứ nhưng phát sinh các `reason_code` ngoài hợp đồng (`NOT_FOUND`, `NOT_ENOUGH_INFO`). Validator hạ về `NO_SOURCE/VALIDATION_FAILED`. Đây là đầu ra an toàn nhưng thông báo cho học viên trở nên chung chung; ba case này không chứng minh model tuân thủ hợp đồng JSON đầy đủ.
- **G18 — được tính đạt theo trạng thái `NO_SOURCE`.** Model trả `GROUNDED` để bác bỏ khẳng định *mọi hệ thống* đều dùng đúng 400 token, trong khi đoạn nguồn chỉ nói khoảng 300–500 token của bài. Validator chặn vì số 400 chỉ có trong câu hỏi, không có trong citation. Nhãn kỳ vọng `NO_SOURCE` và mức độ có thể bác bỏ câu hỏi từ nguồn cần hai người chấm độc lập xem lại; không nên dùng case này để khẳng định validator đã kiểm tra được mọi suy luận ngữ nghĩa.

G02, G08 và G20 là ba phản hồi `GROUNDED` đi qua validator; các citation trong trace trỏ đúng đoạn được phép và phần giải thích chính phù hợp với đoạn trích khi rà nhanh. Trong năm fallback `VALIDATION_FAILED`, một case lỗi parse JSON (G01), bốn case do validator từ chối (G03–G05, G18). Mười hai case còn lại được xử lý bởi cổng định tuyến/nguồn trước lời gọi AI. Vì vậy **95% là tỷ lệ khớp nhãn trạng thái đầu ra của toàn hệ thống trên một lượt 20 case**, không phải độ chính xác ngữ nghĩa 95% của model.

So với `run1` Gemini API trực tiếp trên cùng golden set: 17/20 đạt, 5/8 lời gọi có phản hồi và 3 lỗi HTTP 429. `run2` đạt 19/20, 8/8 lời gọi có phản hồi và 0 lỗi hạ tầng. Hai lượt là bằng chứng riêng, không gộp thành một tỷ lệ.

## Việc cần làm trước khi dùng số đo làm quality bar

1. Hai thành viên chấm độc lập cùng 5 output có phản hồi AI, nên gồm G01, G02, G03, G18 và G20. Nếu lệch từ 1/5 trở lên, làm rõ tiêu chí rồi chấm lại.
2. Ở lượt sau, ghi `finish_reason` và `usage` từ OpenRouter để phân biệt JSON bị cắt với lỗi tạo nội dung; chỉ chạy lại G01 sau khi quyết định cách sửa, và dùng tên lượt mới để giữ nguyên bằng chứng `run2`.
3. Liệt kê rõ `reason_code` hợp lệ trong prompt hoặc chuẩn hóa các mã đồng nghĩa, rồi đo lại tác động đối với G03–G05. Xem lại quy tắc số trong claim cùng nhãn G18 trước khi đổi validator/golden set.

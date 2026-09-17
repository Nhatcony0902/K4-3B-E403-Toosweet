# CP2 — Bản bấm thử Tutor VLearn có căn cứ

Mở [index.html](index.html) bằng Chrome hoặc Edge. Đây là **bản CP2 chưa có AI**: dữ liệu bài học và câu trả lời viết sẵn, truy xuất theo từ khóa; giao diện và bốn nhánh bấm chạy trong trình duyệt. Chưa gửi TA hay lưu correction ra file. Mức đích từ CP3 là **Mock có AI thật ở lõi**, cần ít nhất một AI call thật vào quyết định đủ căn cứ và trace làm bằng chứng. Các cổng phạm vi/chất lượng nguồn, validator và giới hạn làm rõ trong spec mới chưa được triển khai ở bản này.

| Đường trải nghiệm | Cách thử | Kết quả cần thấy |
|---|---|---|
| Có căn cứ | Bấm **Happy: Embedding là gì?**, rồi bấm nút nguồn trong câu trả lời | Slide 3 · đoạn 1 được tô sáng |
| Chưa rõ câu hỏi | Bấm **Low-confidence ②: Similarity là gì?**, chọn một chip | Tutor hỏi rõ phần cần giải thích rồi hiện nguồn của phần đã chọn |
| Không có căn cứ | Bấm **No-grounding ①: LoRA cần bao nhiêu GPU?**, rồi **Hỏi TA** | Tutor không đoán; form điền sẵn ngữ cảnh, thao tác gửi chỉ được mô phỏng |
| Sửa câu trả lời | Bấm **Correction: hỏi rồi bấm "Nguồn không đúng"**, chọn Slide 2 · đoạn 2 | Câu cũ thu mờ; bản minh họa theo nguồn vừa chọn hiện cùng nút kiểm tra nguồn |

Sơ đồ và lý do thiết kế ở [spec.md §4 và §6](../codebase/spec.md). Điểm khớp và ngưỡng chỉ hiển thị trong trace để nhóm phát triển kiểm tra; phần giải thích cho học viên dẫn trực tiếp tới nội dung nguồn.

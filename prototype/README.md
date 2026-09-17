# CP2 — Mock Tutor VLearn có căn cứ

Mở [index.html](index.html) bằng Chrome hoặc Edge. Đây là bản **Mock**: dữ liệu bài học, điểm khớp và câu trả lời đều là ví dụ viết sẵn; giao diện và bốn nhánh bấm chạy trong trình duyệt. Chưa gọi model, chưa gửi TA, chưa lưu correction ra file. Lời gọi AI thật thuộc CP3.

| Đường trải nghiệm | Cách thử | Kết quả cần thấy |
|---|---|---|
| Có căn cứ | Bấm **Happy: Embedding là gì?**, rồi bấm nút nguồn trong câu trả lời | Slide 3 · đoạn 1 được tô sáng |
| Chưa rõ câu hỏi | Bấm **Low-confidence ②: Similarity là gì?**, chọn một chip | Tutor hỏi rõ phần cần giải thích rồi hiện nguồn của phần đã chọn |
| Không có căn cứ | Bấm **No-grounding ①: LoRA cần bao nhiêu GPU?**, rồi **Hỏi TA** | Tutor không đoán; form điền sẵn ngữ cảnh, thao tác gửi chỉ được mô phỏng |
| Sửa câu trả lời | Bấm **Correction: hỏi rồi bấm "Nguồn không đúng"**, chọn Slide 2 · đoạn 2 | Câu cũ thu mờ; bản minh họa theo nguồn vừa chọn hiện cùng nút kiểm tra nguồn |

Sơ đồ và lý do thiết kế ở [spec.md §4 và §6](../spec.md).

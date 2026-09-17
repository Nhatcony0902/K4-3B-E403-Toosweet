# Canvas CP1 — Track A1: Tutor VLearn trả lời có căn cứ

**Nhóm:** Toosweet · **Lớp:** 3B · **Phòng:** E403  
**Đội trưởng:** Lê Thanh Tình · **Mã học viên:** 2A202602449  
**Repo nhóm công khai:** https://github.com/Nhatcony0902/K4-3B-E403-Toosweet.git

| # | Mục | Nội dung bản nháp |
|---|---|---|
| 1 | **Track + đề** | **A1 · VLearn Tutor — cải thiện câu trả lời có căn cứ từ bài học đang mở.** |
| 2 | **Job executor** | Một học viên đang đọc bài trên VLearn, gặp khái niệm chưa hiểu và hỏi tutor ngay trong trang học. |
| 3 | **Pain** | Khi hỏi để hiểu bài, một số học viên không biết câu trả lời dựa trên nguồn nào; sau khi đọc, nhiều người vẫn mở lại slide/video hoặc hỏi công cụ khác. Nhóm muốn giúp học viên kiểm chứng ngay trong trang học; **cần hỏi thêm vì sao họ tìm nguồn khác**. |
| 4 | **1–2 bằng chứng đầu** | **Khảo sát:** 23 phiếu, 17 người đã dùng tutor trong 7 ngày qua; trong 17 người này, **4 không biết nguồn**, **5 mở lại slide/video** và **7 hỏi ChatGPT/Google** sau khi đọc (**12/17**, 70,6%, làm một trong hai việc). **Chatlog:** trong 2.555 lượt K4 không gắn cờ preset, **838 lượt (32,8%)** không có trích dẫn, thuộc 191 mã học viên (`T10366`, `T10436` là mã để kiểm tra). Cách đếm và giới hạn diễn giải: `survey-analysis.md`. |
| 5 | **Lát cắt một câu** | **Một học viên** hỏi về khái niệm trong bài đang mở; **AI quyết định** tài liệu có đủ đoạn liên quan để trả lời hay cần hỏi lại/báo thiếu căn cứ; **học viên nhận** giải thích ngắn kèm mã trang/đoạn để tự kiểm tra, hoặc một bước hỏi tiếp rõ ràng. |
| 6 | **AI tự làm đến đâu + willing users** | **Có điều kiện:** khi tìm thấy nguồn phù hợp, AI tạo câu trả lời kèm nguồn; khi câu hỏi mơ hồ hoặc không tìm thấy nguồn, AI hỏi lại hoặc nói rõ giới hạn, không đoán chắc. **Lý do:** giải thích sai có thể khiến học viên hiểu sai kiến thức. **Người ngoài nhóm đã đồng ý thử:** [Tên 1], [Tên 2], [Tên 3] — [CẦN XÁC NHẬN TRỰC TIẾP]. |
| 7 | **Phân công có tên** | **[Tên A]** — product lead, Canvas/spec, prompt và chuẩn đầu ra · **[Tên B]** — mining chatlog, bằng chứng, khảo sát · **[Tên C]** — golden set, tiêu chí đạt, eval · **[Tên D]** — gọi model, truy xuất nguồn, validator và trace · **[Tên E]** — UI, bốn đường trải nghiệm, video và user test. [Điều chỉnh theo thành viên thật.] |

## Tự soát trước khi nộp

- [x] Điền tên nhóm, phòng, đội trưởng, mã học viên và URL **repo nhóm mới, công khai**.
- [x] Điền tên thật và phần việc của từng thành viên; xác nhận số thành viên hợp lệ với TA nếu nhóm có 5 người (README đề bài ghi 3–4 người).
- [x] Xác nhận trực tiếp ít nhất 3 người ngoài nhóm đồng ý thử prototype; chỉ ghi tên khi họ đã đồng ý.
- [x] Mở lại `T10366` và `T10436` để chắc chúng phù hợp với pain đã chọn; thay bằng mã khác nếu không phù hợp.
- [x] Khảo sát có 23 phiếu nhưng chỉ 17 người báo đã dùng tutor trong 7 ngày qua; kiểm tra người trả lời có ngoài nhóm không trước khi dùng chuẩn khảo sát ≥20 người của rubric. Một phiếu không ghi tên. Không suy ra 12 người kiểm tra lại *vì* thiếu trích dẫn — bảng hỏi chưa hỏi nguyên nhân đó.
- [x] Đội trưởng nộp Canvas và link repo theo form CP1 được công bố tại khai mạc.

**Lưu ý dữ liệu:** Chỉ đưa số tổng hợp và ví dụ ngắn có mã lượt vào repo nhóm. Không sao chép hay commit nguyên `data/` của repo đề bài.

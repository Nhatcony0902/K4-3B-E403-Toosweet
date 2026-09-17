# Tóm tắt khảo sát cho Canvas CP1 — Track A1

Nguồn: file Excel `Mẫu không có tiêu đề (Câu trả lời).xlsx` do nhóm cung cấp, bản đọc ngày 17/09/2026. Bản này chỉ lưu số tổng hợp; không sao chép tên hoặc câu trả lời cá nhân vào repo công khai.

## Cách đếm

- Một hàng dữ liệu = một phiếu; bỏ hàng tiêu đề: **23 phiếu**.
- Nhóm đã dùng tutor gần đây = trả lời **“Có”** cho câu 1 “Trong 7 ngày qua bạn có hỏi AI tutor trên VLearn không?”: **17 phiếu**. Sáu phiếu “Chưa” không đưa vào các tỷ lệ trải nghiệm gần đây.
- Câu 4 về nguồn và câu 5 về hành động sau khi đọc được đếm trên đúng 17 phiếu này. Các lựa chọn ở câu 5 loại trừ nhau trong bảng trả lời.
- Số liệu chatlog được đếm riêng trên `tutor_turns.csv`: lọc `cohort_hint = K4` và `is_preset = False` được 2.555 lượt; trong đó lọc tiếp `has_citation = False` được 838 lượt và đếm 191 mã `student` khác nhau. `is_preset = False` là không được gắn cờ câu mẫu, không đảm bảo học viên tự gõ từ đầu.

| Chỉ số trong 17 người đã dùng gần đây | Số phiếu |
|---|---:|
| Không biết câu trả lời lấy từ đâu | 4/17 (23,5%) |
| Chọn “có trích trang/đoạn” | 9/17 (52,9%) |
| Chọn “biết rõ” | 4/17 (23,5%) |
| Mở lại slide/video để kiểm tra | 5/17 (29,4%) |
| Hỏi ChatGPT/Google sau khi đọc | 7/17 (41,2%) |
| Một trong hai hành động tiếp theo trên | 12/17 (70,6%) |
| Dùng luôn câu trả lời | 5/17 (29,4%) |

## Giới hạn khi diễn giải

- Hành động mở slide/video hoặc hỏi công cụ khác **không chứng minh nguyên nhân là thiếu trích dẫn**. Có người vẫn kiểm tra lại dù câu trả lời có trích trang/đoạn.
- Thời gian kiểm tra lại là câu trả lời tự do, có giá trị không phải thời gian (ví dụ “không có trong slide”, “tôi rất lười”) và có ngoại lệ lớn; chưa tính trung bình.
- Bảng có 22 tên không rỗng và một phiếu thiếu tên. Chưa xác minh tất cả người trả lời đều ngoài nhóm hoặc mỗi phiếu là một người khác nhau. Vì vậy chưa tuyên bố khảo sát đã đạt đầy đủ chuẩn A của rubric.
- Các câu hỏi về việc tutor từng trả lời sai/không có thông tin có nhiều câu đáp ngắn như “Có”, “Chưa”, không mô tả tình huống cụ thể; chưa dùng để khẳng định tỷ lệ lỗi.
- Bằng chứng chatlog là một nguồn riêng: `has_citation = False` chỉ cho biết không thấy trích dẫn, chưa chấm đúng/sai hay mức độ cần nguồn.

## Việc cần hỏi tiếp

Hỏi 3–5 người trong số đã mở lại slide/video hoặc tìm nguồn khác: “Lần đó bạn cần kiểm tra điều gì? Tutor có dẫn trang/đoạn không? Bạn mất bao lâu? Nếu có link đến đúng đoạn nguồn thì bước nào được rút ngắn?” Ghi câu trả lời nguyên văn và mã người trả lời, không công khai tên nếu chưa có sự đồng ý.

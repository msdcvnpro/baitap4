# 📊 Ứng Dụng Phân Tích & Thống Kê Dữ Liệu Excel

Ứng dụng Streamlit chuyên nghiệp để phân tích và thống kê dữ liệu từ file Excel với các biểu đồ trực quan màu sắc sinh động.

## ✨ Tính Năng

- 📁 **Đọc file Excel**: Hỗ trợ định dạng .xlsx và .xls
- 📊 **Thống kê tổng hợp**: 
  - Thống kê mô tả chi tiết (tổng, trung bình, trung vị, độ lệch chuẩn, min, max)
  - Phân tích từng cột riêng lẻ
  - Bảng tương quan giữa các cột
- 🎨 **Biểu đồ trực quan**:
  - Biểu đồ cột (Column Chart)
  - Biểu đồ đường (Line Chart)
  - Biểu đồ tròn (Pie Chart)
  - Biểu đồ phân tán (Scatter Plot)
  - Biểu đồ hộp (Box Plot)
  - Heatmap tương quan
  - Biểu đồ kết hợp (Combined)
- 🧮 **Tính toán tổng hợp**:
  - Tổng hợp theo nhóm
  - Phân tích xu hướng
  - So sánh dữ liệu
  - Các hàm tổng hợp (Sum, Mean, Max, Min, Count)

## 🚀 Cài Đặt

1. **Cài đặt các thư viện cần thiết**:
```bash
pip install -r requirements.txt
```

2. **Chạy ứng dụng**:
```bash
streamlit run app.py
```

3. **Mở trình duyệt**: Ứng dụng sẽ tự động mở tại `http://localhost:8501`

## 📖 Hướng Dẫn Sử Dụng

1. **Tải lên file Excel**: 
   - Chọn file Excel từ sidebar bên trái
   - Hỗ trợ nhiều sheet (có thể chọn sheet trong dropdown)

2. **Xem dữ liệu**:
   - Xem trước dữ liệu đã tải
   - Kiểm tra số dòng, số cột

3. **Phân tích thống kê**:
   - Xem thống kê tổng quan
   - Xem thống kê chi tiết từng cột
   - Phân tích phân phối dữ liệu

4. **Tạo biểu đồ**:
   - Chọn loại biểu đồ mong muốn
   - Chọn các cột để vẽ
   - Tùy chỉnh nhóm dữ liệu

5. **Tính toán tổng hợp**:
   - Tổng hợp theo nhóm với các hàm khác nhau
   - Phân tích xu hướng
   - So sánh các cột với nhau

## 📦 Các Thư Viện Sử Dụng

- `streamlit`: Framework để tạo ứng dụng web
- `pandas`: Xử lý và phân tích dữ liệu
- `plotly`: Tạo biểu đồ tương tác
- `openpyxl`: Đọc file Excel .xlsx
- `xlrd`: Đọc file Excel .xls
- `numpy`: Tính toán số học

## 🎨 Giao Diện

Ứng dụng có giao diện đẹp mắt với:
- Layout rộng (wide layout)
- Sidebar để upload file và tùy chọn
- Màu sắc sinh động trong biểu đồ
- Metrics và thống kê rõ ràng
- Responsive design

## 💡 Tạo Dữ Liệu Mẫu

Ứng dụng có chức năng tạo dữ liệu mẫu để bạn có thể thử nghiệm ngay mà không cần file Excel riêng. Chỉ cần click vào nút "Tạo file Excel mẫu" trong giao diện.

## 📝 Lưu Ý

- File Excel nên có header (tiêu đề cột) ở dòng đầu tiên
- Các cột số sẽ được tự động nhận diện để phân tích
- Các cột văn bản có thể dùng để nhóm dữ liệu

## 🔧 Tùy Chỉnh

Bạn có thể tùy chỉnh ứng dụng bằng cách:
- Thay đổi màu sắc trong biểu đồ
- Thêm các loại biểu đồ mới
- Thêm các hàm tính toán khác
- Tùy chỉnh layout và giao diện

## 📄 License

Free to use for any purpose.


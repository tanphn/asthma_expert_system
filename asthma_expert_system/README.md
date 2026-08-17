# 🫁 Hệ Thống Chuyên Gia Hỗ Trợ Ra Quyết Định Lâm Sàng Chẩn Đoán & Quản Lý Hen Phế Quản
### Asthma Clinical Decision Support System (Asthma CDSS)
*Chuẩn hóa theo Hướng dẫn Quốc tế **GINA (Global Initiative for Asthma)** & Phác đồ Điều trị của **Bộ Y Tế Việt Nam***

---

## 📌 Giới Thiệu Tổng Quan

**Hen phế quản (Asthma)** là một bệnh lý viêm mạn tính đường thở phổ biến, có tính chất biến đổi phức tạp theo thời gian và không gian. Việc chẩn đoán nhầm lẫn với các bệnh lý hô hấp/tim mạch khác (như COPD, suy tim trái, giãn phế quản, trào ngược GERD) hoặc kiểm soát kém do sai kỹ thuật sử dụng bình xịt/hít là nguyên nhân hàng đầu dẫn đến các đợt kịch phát nặng đe dọa tính mạng.

**Asthma CDSS** là hệ thống chuyên gia y tế (Clinical Decision Support System) hoàn chỉnh, được xây dựng dựa trên nền tảng **Động cơ suy diễn tiến (Forward Chaining)** kết hợp với **Hệ số tin cậy (Certainty Factors - CF)** và **Cơ chế giải thích (Explanation Facility)** nhằm hỗ trợ Bác sĩ, Nhân viên y tế và Sinh viên Y khoa trong:
1. Chẩn đoán xác định và tính toán xác suất phân biệt đa bệnh lý.
2. Phân loại mức độ nặng ban đầu theo tiêu chuẩn chức năng hô hấp.
3. Đề xuất bậc điều trị tối ưu theo 2 lộ trình: **Lộ trình 1 ưu tiên (GINA Track 1 SMART/MART)** và **Lộ trình 2 thay thế (GINA Track 2)**.
4. Đánh giá mức độ kiểm soát triệu chứng tại các lần tái khám, phát hiện nguy cơ đợt cấp tương lai và ra quyết định **Nâng bậc (Step-up)**, **Giảm bậc (Step-down)** hoặc **Duy trì & Huấn luyện lại**.
5. Tự động sinh **Kế hoạch hành động Hen cá nhân hóa 3 vùng màu (Xanh - Vàng - Đỏ)**.
6. Đánh giá thao tác và phát hiện lỗi sai then chốt khi sử dụng bình xịt/hít định liều (**pMDI, Turbuhaler, Diskus**).
7. Xuất phiếu khám bệnh / bệnh án điện tử định dạng **Print-ready HTML** có chữ ký chuyên gia.

---

## 🌟 Các Tính Năng Cốt Lõi

```
+-----------------------------------------------------------------------------------+
|                               ASTHMA CDSS PLATFORM                                |
+-----------------------+-------------------------+---------------------------------+
| 🩺 KHÁM LẦN ĐẦU        | 🔄 TÁI KHÁM & THEO DÕI  | 📋 KẾ HOẠCH HÀNH ĐỘNG 3 VÙNG    |
| • Triệu chứng biến đổi| • 4 Tiêu chí GINA       | • Vùng Xanh (An toàn - PEF ≥80%)|
| • Hô hấp ký & BDR test| • Đánh giá nguy cơ cấp  | • Vùng Vàng (Cảnh báo: 50-80%)  |
| • Certainty Scoring 7 | • Quyết định Nâng/Hạ bậc| • Vùng Đỏ (Cấp cứu - PEF <50%)  |
+-----------------------+-------------------------+---------------------------------+
| 💨 KỸ THUẬT BÌNH HÍT  | 🧭 GIẢI THÍCH LOGIC     | 🧪 6 CA BỆNH MẪU 1-CLICK        |
| • Kiểm tra pMDI/DPI   | • Truy vết cây suy diễn | • Nạp dữ liệu bệnh nhân thực tế |
| • Báo lỗi then chốt   | • Diễn giải HOW & WHY   | • Kiểm thử tự động tức thì      |
+-----------------------+-------------------------+---------------------------------+
```

### 1. Phân Hệ Khám Lần Đầu & Chẩn Đoán Phân Biệt (Initial Assessment)
- **Tiêu chuẩn vàng GINA**: Kết hợp tiêu chuẩn lâm sàng L1 (≥ 2 triệu chứng chính + tính biến đổi) và tiêu chuẩn cận lâm sàng L2 (FEV1/FVC giảm, test phục hồi phế quản ΔFEV1 ≥ 12% & ≥ 200mL, hoặc PEF biến thiên > 10%).
- **Ma trận Chẩn đoán Phân biệt (Certainty Factors)**: Tính điểm xác suất cho 7 bệnh lý:
  - 🟢 **Hen Phế Quản (Asthma)**
  - 🟠 **Bệnh Phổi Tắc Nghẽn Mạn Tính (COPD)**
  - 🔴 **Hội chứng Chồng lấp Hen - COPD (Asthma-COPD Overlap - ACO)**
  - 🔴 **Suy Tim Trái / Hen Tim (Cardiac Asthma)**
  - 🟣 **Giãn Phế Quản (Bronchiectasis)**
  - 🔵 **Ho mạn tính do Trào ngược Dạ dày Thực quản (GERD)**
  - 🟡 **Hẹp khí phế quản / Rối loạn chức năng dây thanh (VCD / Airway Obstruction)**
- **Phân loại mức độ nặng ban đầu**:
  - *Hen gián đoạn (Intermittent)*
  - *Hen dai dẳng nhẹ (Mild Persistent)*
  - *Hen dai dẳng trung bình (Moderate Persistent)*
  - *Hen dai dẳng nặng (Severe Persistent)*

### 2. Đề Xuất Phác Đồ Điều Trị Chuẩn GINA 2023/2024
- **Lộ trình 1 (Track 1 - Preferred Track)**:
  - Sử dụng **ICS-formoterol liều thấp** vừa làm thuốc kiểm soát vừa làm thuốc cắt cơn (Liệu pháp MART/SMART). Giảm 60-70% nguy cơ đợt kịch phát nặng so với dùng SABA đơn độc.
- **Lộ trình 2 (Track 2 - Alternative Track)**:
  - Thuốc kiểm soát duy trì hàng ngày (ICS hoặc ICS-LABA) kết hợp SABA cắt cơn khi cần.
- **Bảng quy đổi liều Corticoid hít (ICS)**: Chi tiết liều thấp, trung bình, cao cho *Budesonide, Fluticasone Propionate, Beclomethasone, Fluticasone Furoate* và các biệt dược thông dụng (*Symbicort, Seretide, Foster, Relvar, Ventolin, Spiriva, Singulair, Biologics*).

### 3. Phân Hệ Tái Khám & Theo Dõi (Follow-Up)
- **Công cụ đánh giá 4 câu hỏi kiểm soát triệu chứng GINA**:
  - `Score = 0`: Hen kiểm soát tốt (Well-controlled)
  - `Score = 1 - 2`: Hen kiểm soát một phần (Partly-controlled)
  - `Score = 3 - 4`: Hen không kiểm soát (Uncontrolled)
- **Đánh giá yếu tố nguy cơ tương lai**: Tiền sử đợt cấp, dùng ≥ 3 bình SABA/năm, FEV1 < 60%, hút thuốc, béo phì, tiền sử nhập ICU.
- **Quy tắc điều chỉnh bậc**:
  - **Tăng bậc duy trì (Step-up)**: Khi hen không kiểm soát dù đã tuân thủ tốt và dùng đúng kỹ thuật.
  - **Duy trì & Huấn luyện lại**: Khi mất kiểm soát do quên thuốc hoặc sai kỹ thuật xịt.
  - **Giảm bậc an toàn (Step-down)**: Khi hen kiểm soát tốt liên tục trong ≥ 3 tháng (giảm liều ICS 25-50%).

### 4. Kế Hoạch Hành Động Hen (Asthma Action Plan Generator)
Tự động tính toán các ngưỡng lưu lượng đỉnh PEF dựa trên giá trị tốt nhất của người bệnh (Personal Best PEF):
- 🟢 **Vùng Xanh (An toàn - PEF ≥ 80%)**: Hướng dẫn duy trì thuốc hàng ngày.
- 🟡 **Vùng Vàng (Cảnh báo - PEF 50 - 80%)**: Dấu hiệu hen xấu đi, cách tăng liều thuốc cắt cơn và điều chỉnh liều MART.
- 🔴 **Vùng Đỏ (Cấp cứu - PEF < 50%)**: Dấu hiệu nguy hiểm đe dọa tính mạng, liều cấp cứu khẩn và hướng dẫn gọi cấp cứu 115.

### 5. Đánh Giá & Huấn Luyện Kỹ Thuật Dùng Bình Xịt / Hít (Inhaler Technique Audit)
- Bảng kiểm chi tiết từng bước cho các thiết bị:
  - **pMDI (Bình xịt định liều)**: Ventolin, Seretide Evohaler, Flixotide, Foster pMDI.
  - **Turbuhaler (Bình hít bột khô DPI)**: Symbicort Turbuhaler, Pulmicort.
  - **Accuhaler / Diskus (Bình hít bột khô dạng vỉ)**: Seretide Accuhaler.
- Tự động phát hiện các **lỗi sai then chốt (Critical Errors)**: *Quên lắc bình, không thở ra hết trước khi hít, không phối hợp nhịp nhàng ấn-hít, không nín thở sau hít, không súc họng sau khi dùng Corticoid*.

### 6. Cơ Chế Giải Thích Minh Bạch (Explanation Facility & Audit Trail)
- **Giải thích HOW**: Chỉ ra từng quy tắc và dữ kiện dẫn tới chẩn đoán hoặc quyết định điều trị.
- **Giải thích WHY**: Diễn giải tầm quan trọng lâm sàng của từng câu hỏi/xét nghiệm đối với các giả thuyết bệnh học.
- **Audit Trail Log**: Xuất báo cáo cây suy luận dạng Markdown từng bước chi tiết.

---

## 🏛️ Cấu Trúc Thư Mục Dự Án

```
asthma_expert_system/
├── engine/                         # ĐỘNG CƠ HỆ THỐNG CHUYÊN GIA
│   ├── __init__.py
│   ├── wm.py                       # Working Memory: Quản lý Facts, Metadata, Provenance
│   ├── inference.py                # Forward Chaining Inference Engine
│   ├── certainty.py                # Động cơ Certainty Factors & Ma trận Chẩn đoán phân biệt
│   └── explanation.py              # Explanation Facility (HOW, WHY & Audit Trail)
├── kb/                             # CƠ SỞ TRI THỨC Y KHOA (KNOWLEDGE BASE)
│   ├── __init__.py
│   ├── facts_def.py                # Từ điển Facts chuẩn hóa (f0xx - f8xx)
│   ├── rules_diagnosis.py          # Tập luật Chẩn đoán xác định & Phân biệt bệnh
│   ├── rules_severity.py           # Tập luật Phân loại mức độ nặng ban đầu
│   ├── rules_control.py            # Tập luật Đánh giá kiểm soát triệu chứng GINA
│   ├── rules_treatment.py          # Tập luật Đề xuất bậc điều trị 1-5 (Track 1 & Track 2)
│   └── medications_db.py           # Dược thư: Bảng liều ICS, LABA, LAMA, Biệt dược & Thiết bị
├── modules/                        # PHÂN HỆ NGHIỆP VỤ LÂM SÀNG
│   ├── __init__.py
│   ├── initial_assessment.py       # Quy trình Khám lần đầu
│   ├── follow_up.py                # Quy trình Tái khám & Theo dõi
│   ├── action_plan.py              # Bộ sinh Kế hoạch hành động 3 vùng màu
│   ├── inhaler_technique.py        # Kiểm tra thao tác kỹ thuật bình hít
│   └── patient_cases.py            # 6 Ca lâm sàng mẫu nạp sẵn 1-click
├── utils/                          # TIỆN ÍCH & XUẤT BÁO CÁO
│   ├── __init__.py
│   ├── helpers.py                  # Hàm tiện ích định dạng, kiểm tra dữ liệu
│   └── report_generator.py         # Bộ tạo Phiếu khám bệnh HTML Print-Ready
├── app.py                          # ỨNG DỤNG WEB STREAMLIT CAO CẤP (GLASSMORPHISM UI)
├── main.py                         # ỨNG DỤNG TERMINAL CLI TƯƠNG TÁC
├── test_system.py                  # BỘ KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN (TEST SUITE)
└── README.md                       # TÀI LIỆU DỰ ÁN CHI TIẾT
```

---

## 🧪 6 Ca Lâm Sàng Mẫu Thực Tế (Preloaded Case Presets)

Hệ thống tích hợp sẵn 6 ca bệnh lâm sàng điển hình giúp người dùng kiểm thử toàn diện ngay trên giao diện:

| Ca | Tên Bệnh Nhân | Đặc Điểm Lâm Sàng & Cận Lâm Sàng | Kết Quả Chẩn Đoán | Mức Độ / Kiểm Soát | Đề Xuất Điều Trị |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Trần Thị Mai Lan** *(Nữ, 24t)* | Tiền sử viêm mũi dị ứng, ho khò khè đêm, FEV1/FVC 0.72, ΔFEV1 +16% (320mL), FeNO 48 ppb | **Hen Phế Quản Xác Định** *(CF: 100%)* | Dai dẳng trung bình | **Bậc 3** *(Track 1 SMART)* |
| **2** | **Nguyễn Văn Hùng** *(Nam, 62t)* | Hút thuốc lá 35 gói-năm, khó thở mạn tính, FEV1/FVC 0.62, ΔFEV1 +14%, FEV1 56% | **Hen Phế Quản Xác Định / Nghi ngờ ACO** | Dai dẳng nặng | **Bậc 5** *(+ LAMA Tiotropium)* |
| **3** | **Lê Hoàng Quân** *(Nam, 35t)* | Tái khám Bậc 3 nhưng vẫn mất kiểm soát (4/4 GINA), phát hiện không nín thở, không súc họng | **Hen Không Kiểm Soát** *(Do sai kỹ thuật)* | Mất kiểm soát do kỹ thuật | **Duy trì Bậc 3 & Huấn luyện lại** |
| **4** | **Phạm Thị Bích Ngọc** *(Nữ, 42t)* | Tái khám Bậc 3, không còn triệu chứng trong 4 tháng (0/4 GINA), FEV1 94% | **Hen Kiểm Soát Tốt** | Kiểm soát tốt ≥ 3 tháng | **Xem xét Giảm bậc (Bậc 2)** |
| **5** | **Đặng Quốc Cường** *(Nam, 48t)* | Ho khan kéo dài 5 tháng, tăng khi nằm ngửa sau ăn, ợ chua, hô hấp ký bình thường | **Chưa đủ bằng chứng Hen** | Xếp hạng 1: **GERD (75%)** | Tư vấn điều trị Trào ngược |
| **6** | **Vũ Minh Đức** *(Nam, 19t)* | Khó thở dữ dội sau đá bóng trời lạnh, nói từng từ, PEF 45%, tiền sử từng nằm ICU | **Hen Phế Quản Cấp Nặng** | Cảnh báo Đỏ khẩn cấp | **Cấp cứu khẩn cấp & Nhập viện** |

---

## 🚀 Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Yêu Cầu Môi Trường
- **Python**: Phiên bản 3.9 trở lên (đã kiểm thử tương thích hoàn hảo trên Python 3.10, 3.11, 3.12, 3.14).
- **Hệ điều hành**: Windows, macOS, hoặc Linux.

### 2. Cài Đặt Thư Viện Cần Thiết
Mở terminal / command prompt và cài đặt các package phụ thuộc:
```bash
python -m pip install streamlit pandas altair
```

### 3. Khởi Chạy Giao Diện Web Trực Quan (Streamlit Web App)
```bash
cd asthma_expert_system
streamlit run app.py
```
> Trình duyệt web sẽ tự động mở tại địa chỉ: **`http://localhost:8501`**

### 4. Khởi Chạy Giao Diện Dòng Lệnh (Terminal CLI)
```bash
cd asthma_expert_system
python main.py
```

### 5. Chạy Kiểm Thử Tự Động Toàn Diện (Test Suite)
```bash
cd asthma_expert_system
python test_system.py
```

---

## 📚 Tài Liệu Tham Khảo Y Khoa (References)

1. **Global Initiative for Asthma (GINA)**: *Global Strategy for Asthma Management and Prevention (Updated 2023 / 2024)*. URL: [ginasthma.org](https://ginasthma.org).
2. **Bộ Y Tế Việt Nam**: *Hướng dẫn Chẩn đoán và Điều trị Hen Phế Quản Người Lớn và Trẻ Em ≥ 12 Tuổi* (Quyết định số 1851/QĐ-BYT).
3. **Global Initiative for Chronic Obstructive Lung Disease (GOLD)**: *Global Strategy for Prevention, Diagnosis and Management of COPD (2024 Report)*.
4. **National Asthma Education and Prevention Program (NAEPP / EPR-3)**: *Expert Panel Report 3: Guidelines for the Diagnosis and Management of Asthma*.

---

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm Y Khoa (Medical Disclaimer)

Hệ thống **Asthma CDSS** được phát triển nhằm mục đích hỗ trợ ra quyết định lâm sàng, nghiên cứu học thuật và giáo dục y khoa. Các kết luận và đề xuất của hệ thống mang tính chất tham khảo dựa trên các hướng dẫn thực hành y khoa chuẩn. Bác sĩ điều trị chịu trách nhiệm cuối cùng trong việc thăm khám lâm sàng trực tiếp, chỉ định cận lâm sàng và đưa ra phác đồ điều trị phù hợp cho từng cá thể bệnh nhân.

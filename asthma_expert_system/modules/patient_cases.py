# asthma_expert_system/modules/patient_cases.py
"""
Bộ 6 Ca Lâm Sàng Thực Tế (Preloaded Clinical Test Cases)
Hỗ trợ kiểm thử, đánh giá và biểu diễn tính năng hệ thống chỉ với 1 cú click.
"""

from typing import Dict, Any, List

PATIENT_CASES: List[Dict[str, Any]] = [
    {
        "id": "CASE_1",
        "title": "Ca 1: Nữ 24 tuổi - Hen dị ứng điển hình (Khám lần đầu)",
        "patient_name": "Trần Thị Mai Lan",
        "age": 24,
        "gender": "Nữ",
        "mode": "Khám lần đầu",
        "summary": "Bệnh nhân nữ 24 tuổi, có tiền sử viêm mũi dị ứng, đến khám vì ho và khò khè tăng về đêm và khi tập thể dục.",
        "facts": {
            "f001": 24,
            "f002": "Nữ",
            "f003": True,  # Cơ địa dị ứng
            "f004": True,  # Mẹ bị hen
            "f005": 21.0,
            "f101": True,  # Ho từng cơn
            "f102": True,  # Khò khè
            "f103": True,  # Khó thở
            "f104": False,
            "f105": True,  # Biến đổi theo thời gian
            "f106": True,  # Nặng về đêm
            "f107": True,  # Nặng khi gắng sức
            "f108": False,
            "f109": False,
            "f110": False,
            "f111": False,
            "f112": False,
            "f113": False,
            "f120": 3,     # 3 ngày/tuần có triệu chứng
            "f121": 1,     # Đêm 1 lần/tuần
            "f122": 1,     # Giới hạn nhẹ
            "f123": 3,     # SABA 3 lần/tuần
            "f124": 0,     # Chưa có đợt cấp nặng
            "f201": 0.72,  # FEV1/FVC < 0.75
            "f202": 16.0,  # FEV1 tăng 16% (>12%)
            "f203": 320.0, # Tăng 320 mL (>200mL)
            "f204": 15.0,  # Biến thiên PEF 15%
            "f205": 82.0,  # FEV1 82% dự đoán
            "f207": True,  # BDR test (+)
            "f208": 48.0,  # FeNO cao
            "f209": 420.0, # Eosinophil máu cao
            "f401": False,
            "f402": True,  # Bụi nhà
            "f403": True,  # Thời tiết lạnh
            "f404": False,
            "f405": False,
            "f414": False,
            "f415": False
        },
        "expected_result": "Chẩn đoán Xác định Hen Phế Quản -> Mức độ: Hen dai dẳng nhẹ -> Đề xuất: GINA Step 2 (Track 1 MART hoặc ICS liều thấp)"
    },
    {
        "id": "CASE_2",
        "title": "Ca 2: Nam 62 tuổi - Tiền sử hút thuốc nghi ngờ Chồng lấp Hen - COPD (ACO)",
        "patient_name": "Nguyễn Văn Hùng",
        "age": 62,
        "gender": "Nam",
        "mode": "Khám lần đầu",
        "summary": "Nam 62 tuổi, tiền sử hút thuốc 35 gói-năm và có cơ địa hen từ trẻ. Khó thở gắng sức tăng dần kèm ho đờm mạn tính.",
        "facts": {
            "f001": 62,
            "f002": "Nam",
            "f003": True,
            "f004": False,
            "f005": 23.5,
            "f101": True,
            "f102": True,
            "f103": True,
            "f104": True,
            "f105": True,
            "f106": True,
            "f107": True,
            "f108": True,
            "f109": True,  # Ho đờm mạn tính
            "f110": False,
            "f111": False,
            "f112": False,
            "f113": True,  # Khó thở tiến triển
            "f120": 6,
            "f121": 3,
            "f122": 2,
            "f123": 10,
            "f124": 2,     # 2 đợt cấp/năm
            "f201": 0.62,  # Tắc nghẽn cố định FEV1/FVC < 0.70
            "f202": 14.0,  # FEV1 tăng 14% sau giãn
            "f203": 240.0,
            "f204": 18.0,
            "f205": 56.0,  # FEV1 56% dự đoán (nặng)
            "f207": True,
            "f401": True,  # Hút thuốc lá ≥ 10 gói-năm
            "f402": False,
            "f403": True,
            "f404": True,  # Đã có chẩn đoán COPD
            "f405": False
        },
        "expected_result": "Gợi ý Hội chứng Chồng lấp Hen - COPD (ACO) & Hen dai dẳng nặng -> Đề xuất: Bậc 4-5 + Thêm LAMA (Spiriva)"
    },
    {
        "id": "CaSE_3",
        "title": "Ca 3: Nam 35 tuổi - Hen mất kiểm soát do Sai Kỹ Thuật Hít (Tái khám)",
        "patient_name": "Lê Hoàng Quân",
        "age": 35,
        "gender": "Nam",
        "mode": "Tái khám",
        "summary": "Bệnh nhân tái khám phác đồ Bậc 3 nhưng triệu chứng vẫn liên tục. Bác sĩ phát hiện bệnh nhân không nín thở và không súc miệng.",
        "facts": {
            "f001": 35,
            "f002": "Nam",
            "f310": 3,     # Đang điều trị Bậc 3
            "f302": True,  # Dùng ICS-LABA
            "f701": True,  # Triệu chứng ngày > 2 lần/tuần
            "f702": True,  # Thức giấc đêm do hen
            "f703": True,  # Dùng thuốc cắt cơn > 2 lần/tuần
            "f704": True,  # Giới hạn hoạt động
            "f414": False, # Vẫn nhớ xịt thuốc
            "f415": True,  # SAI KỸ THUẬT HÍT (không nín thở, hít sai nhịp)
            "f416": True,  # Không súc miệng
            "f124": 0,
            "f205": 78.0
        },
        "expected_result": "Hen Không Kiểm Soát (4/4 GINA) do Sai Kỹ Thuật Hít -> Quyết định: DUY TRÌ BẬC 3 & Huấn luyện lại kỹ thuật (Chưa vội tăng liều)"
    },
    {
        "id": "CASE_4",
        "title": "Ca 4: Nữ 42 tuổi - Hen kiểm soát tốt liên tục ≥ 3 tháng (Tái khám giảm bậc)",
        "patient_name": "Phạm Thị Bích Ngọc",
        "age": 42,
        "gender": "Nữ",
        "mode": "Tái khám",
        "summary": "Bệnh nhân điều trị duy trì Symbicort Bậc 3 được 4 tháng. Hoàn toàn không còn triệu chứng, chức năng hô hấp ổn định.",
        "facts": {
            "f001": 42,
            "f002": "Nữ",
            "f310": 3,     # Đang ở Bậc 3
            "f302": True,
            "f701": False, # Không triệu chứng ngày
            "f702": False, # Không thức giấc đêm
            "f703": False, # Không dùng thuốc cắt cơn
            "f704": False, # Không hạn chế vận động
            "f414": False,
            "f415": False,
            "f124": 0,
            "f205": 94.0   # FEV1 94% bình thường
        },
        "expected_result": "Hen Kiểm Soát Tốt (0/4 GINA) -> Quyết định: Xem xét GIẢM BẬC an toàn xuống Bậc 2 (giảm 50% liều)"
    },
    {
        "id": "CASE_5",
        "title": "Ca 5: Nam 48 tuổi - Ho khan kéo dài do Trào ngược Dạ Dày (GERD)",
        "patient_name": "Đặng Quốc Cường",
        "age": 48,
        "gender": "Nam",
        "mode": "Khám lần đầu",
        "summary": "Bệnh nhân đến khám vì ho khan 5 tháng nay, tăng khi nằm ngửa sau ăn tối, kèm ợ chua, không khò khè, hô hấp ký hoàn toàn bình thường.",
        "facts": {
            "f001": 48,
            "f002": "Nam",
            "f003": False,
            "f004": False,
            "f101": True,  # Ho kéo dài
            "f102": False, # KHÔNG khò khè
            "f103": False, # KHÔNG khó thở
            "f104": False,
            "f105": False,
            "f106": False,
            "f107": False,
            "f108": False,
            "f112": True,  # Ho tăng khi nằm / sau ăn / ợ chua
            "f201": 0.82,  # FEV1/FVC bình thường
            "f202": 2.0,   # Test phục hồi âm tính
            "f205": 98.0,
            "f207": False,
            "f401": False
        },
        "expected_result": "Không đủ tiêu chuẩn Hen -> Chẩn đoán phân biệt xếp hạng 1: Trào ngược dạ dày thực quản (GERD)"
    },
    {
        "id": "CASE_6",
        "title": "Ca 6: Nam 19 tuổi - Cơn hen cấp nặng đe dọa tính mạng (Cảnh báo Đỏ)",
        "patient_name": "Vũ Minh Đức",
        "age": 19,
        "gender": "Nam",
        "mode": "Khám lần đầu",
        "summary": "Thanh niên 19 tuổi nhập viện cấp cứu vì cơn khó thở dữ dội sau khi đá bóng trời lạnh, không nói được cả câu, tiền sử từng nằm ICU.",
        "facts": {
            "f001": 19,
            "f002": "Nam",
            "f003": True,
            "f101": True,
            "f102": True,
            "f103": True,
            "f104": True,
            "f105": True,
            "f106": True,
            "f107": True,
            "f120": 7,
            "f121": 5,
            "f122": 2,     # Giới hạn nhiều
            "f123": 15,
            "f124": 3,
            "f204": 35.0,
            "f205": 45.0,  # FEV1 45% (rất nặng)
            "f403": True,
            "f418": True   # Tiền sử từng nằm ICU
        },
        "expected_result": "Hen dai dẳng nặng + BẬC 5 + KÍCH HOẠT CẢNH BÁO CẤP CỨU VÙNG ĐỎ"
    }
]

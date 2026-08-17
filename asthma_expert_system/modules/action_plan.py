# asthma_expert_system/modules/action_plan.py
"""
Bộ tạo Kế hoạch Hành động Hen Phế Quản Cá nhân hóa (Personalized Asthma Action Plan)
Theo tiêu chuẩn GINA phân màu 3 Vùng: Xanh (An toàn), Vàng (Cảnh báo), Đỏ (Cấp cứu).
"""

from typing import Dict, Any

def generate_action_plan(
    patient_name: str,
    patient_age: int,
    personal_best_pef: float,
    current_step: int,
    controller_med: str,
    reliever_med: str,
    doctor_name: str = "BS. Chuyên khoa Hô hấp",
    emergency_phone: str = "115"
) -> Dict[str, Any]:
    """
    Tạo dữ liệu kế hoạch hành động 3 vùng màu dựa trên thông số cá nhân của người bệnh.
    """
    pef = personal_best_pef if personal_best_pef and personal_best_pef > 0 else 450.0

    green_pef_min = round(pef * 0.80)
    yellow_pef_min = round(pef * 0.50)
    yellow_pef_max = round(pef * 0.80)
    red_pef_max = round(pef * 0.50)

    return {
        "patient_info": {
            "name": patient_name or "Nguyễn Văn A",
            "age": patient_age or 30,
            "personal_best_pef": pef,
            "current_step": current_step or 2,
            "doctor_name": doctor_name,
            "emergency_phone": emergency_phone
        },
        "green_zone": {
            "title": "🟢 VÙNG XANH - AN TOÀN (KIỂM SOÁT TỐT)",
            "criteria": [
                "Không có ho, không khò khè, không khó thở",
                "Ngủ ngon trọn giấc suốt đêm, không thức giấc vì hen",
                "Có thể làm việc, tập thể dục và sinh hoạt bình thường",
                f"Lưu lượng đỉnh PEF ≥ 80% giá trị tốt nhất (PEF ≥ {green_pef_min} L/phút)"
            ],
            "action": [
                f"TIẾP TỤC DÙNG THUỐC KIỂM SOÁT DUY TRÌ HẰNG NGÀY: {controller_med or 'Symbicort 160/4.5 mcg x 1 hít x 2 lần/ngày (sáng/tối)'}",
                "Súc miệng sạch bằng nước và nhổ bỏ sau mỗi lần xịt thuốc chứa Corticoid.",
                "Tránh tiếp xúc các dị nguyên kích phát đã biết (khói thuốc, bụi, lông thú, thời tiết lạnh)."
            ]
        },
        "yellow_zone": {
            "title": "🟡 VÙNG VÀNG - CẢNH BÁO (TRIỆU CHỨNG BẮT ĐẦU TỆ HƠN)",
            "criteria": [
                "Bắt đầu xuất hiện ho, khò khè, nghẹt thở hoặc nặng ngực",
                "Thức giấc ban đêm do khó thở hoặc ho",
                "Cảm thấy mệt khi làm các công việc thường ngày",
                "Bắt đầu cảm thấy như đang bị cảm lạnh/cảm cúm",
                f"Lưu lượng đỉnh PEF từ 50% đến dưới 80% (PEF: {yellow_pef_min} - {yellow_pef_max} L/phút)"
            ],
            "action": [
                f"XỊT THUỐC CẮT CƠN NGAY: {reliever_med or 'Symbicort 160/4.5 mcg: 1 nhát (hoặc Ventolin 100mcg: 2 nhát)'}.",
                "Nếu dùng liệu pháp MART: Tăng thêm 1 liều ICS-formoterol mỗi khi có triệu chứng (tối đa 8-12 nhát/ngày).",
                "Nếu dùng phác đồ thông thường: Có thể tăng gấp đôi liều ICS duy trì trong 1 - 2 tuần.",
                "Đo lại PEF sau 30-60 phút. Nếu triệu chứng không thuyên giảm sau 48 giờ, hãy liên hệ ngay với Bác sĩ."
            ]
        },
        "red_zone": {
            "title": "🔴 VÙNG ĐỎ - NGUY HIỂM (CƠN HEN CẤP NẶNG - CẦN CẤP CỨU)",
            "criteria": [
                "Rất khó thở, thở gấp, cánh mũi phập phồng, co kéo cơ cổ và lồng ngực",
                "Không thể nói trọn một câu mà không dừng lại để thở",
                "Môi hoặc đầu ngón tay tím tái",
                "Thuốc cắt cơn dạng xịt không mang lại tác dụng hoặc chỉ đỡ trong thời gian rất ngắn",
                f"Lưu lượng đỉnh PEF < 50% giá trị tốt nhất (PEF < {red_pef_max} L/phút)"
            ],
            "action": [
                "XỊT CẮT CƠN KHẨN CẤP: Dùng thuốc cắt cơn (Ventolin 2-4 nhát qua buồng đệm) LẶP LẠI MỖI 15-20 PHÚT.",
                f"GỌI NGAY CẤP CỨU {emergency_phone} HOẶC ĐƯỢC ĐƯA ĐẾN BỆNH VIỆN GẦN NHẤT NGAY LẬP TỨC.",
                "Ngồi thẳng người, hơi nghiêng về phía trước. TUYỆT ĐỐI KHÔNG NẰM NGỬA.",
                "Uống ngay 1 liều Corticoid toàn thân (Prednisolone 40-50mg) nếu đã được Bác sĩ hướng dẫn sẵn trước đó."
            ]
        }
    }

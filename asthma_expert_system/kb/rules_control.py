# asthma_expert_system/kb/rules_control.py
"""
Hệ thống luật Đánh giá Mức độ Kiểm soát Triệu chứng & Đánh giá Nguy cơ Tương lai (GINA Follow-up)
"""

RULES_CONTROL = [
    # ==========================================
    # ĐÁNH GIÁ MỨC ĐỘ KIỂM SOÁT TRIỆU CHỨNG (4 TUẦN QUA)
    # ==========================================
    {
        "id": "R_CTRL_WELL",
        "name": "Hen kiểm soát tốt (Well-Controlled)",
        "condition_desc": "Không có tiêu chí nào trong 4 câu hỏi kiểm soát GINA (Score = 0/4)",
        "condition_fn": lambda wm: (
            sum(1 for f in ["f701", "f702", "f703", "f704"] if wm.get(f)) == 0
        ),
        "consequent_facts": ["f705"],
        "cf": 0.95,
        "rationale": "Bệnh nhân không có triệu chứng ban ngày quá 2 lần/tuần, không thức giấc đêm, không cần dùng thuốc cắt cơn quá 2 lần/tuần và không bị giới hạn hoạt động."
    },
    {
        "id": "R_CTRL_PARTLY",
        "name": "Hen kiểm soát một phần (Partly-Controlled)",
        "condition_desc": "Có từ 1 đến 2 tiêu chí trong 4 câu hỏi kiểm soát GINA (Score = 1-2/4)",
        "condition_fn": lambda wm: (
            1 <= sum(1 for f in ["f701", "f702", "f703", "f704"] if wm.get(f)) <= 2
        ),
        "consequent_facts": ["f706"],
        "cf": 0.90,
        "rationale": "Bệnh nhân có 1 hoặc 2 dấu hiệu mất kiểm soát triệu chứng trong 4 tuần qua, cần rà soát kỹ thuật hít, tuân thủ và cân nhắc chỉnh thuốc."
    },
    {
        "id": "R_CTRL_UNCONTROLLED",
        "name": "Hen không kiểm soát (Uncontrolled)",
        "condition_desc": "Có từ 3 đến 4 tiêu chí trong 4 câu hỏi kiểm soát GINA (Score = 3-4/4)",
        "condition_fn": lambda wm: (
            sum(1 for f in ["f701", "f702", "f703", "f704"] if wm.get(f)) >= 3
        ),
        "consequent_facts": ["f707"],
        "cf": 0.95,
        "rationale": "Bệnh nhân có ≥ 3 dấu hiệu mất kiểm soát; nguy cơ cao xuất hiện đợt kịch phát nặng, cần can thiệp điều trị khẩn trương."
    },

    # ==========================================
    # QUY NẠP NGUYÊN NHÂN MẤT KIỂM SOÁT & YẾU TỐ NGUY CƠ TƯƠNG LAI
    # ==========================================
    {
        "id": "R_CAUSE_NON_ADHERENCE",
        "name": "Mất kiểm soát do kém tuân thủ điều trị",
        "condition_desc": "Hen không kiểm soát hoặc kiểm soát một phần + Có tiền sử quên/bỏ cữ thuốc kiểm soát duy trì (f414)",
        "condition_fn": lambda wm: (
            (wm.get("f706") or wm.get("f707")) and wm.get("f414")
        ),
        "consequent_facts": ["f414"],
        "cf": 0.85,
        "rationale": "Không dùng đều đặn thuốc kháng viêm kiểm soát là nguyên nhân phổ biến nhất khiến hen tái phát và không đạt kiểm soát."
    },
    {
        "id": "R_CAUSE_INCORRECT_TECHNIQUE",
        "name": "Mất kiểm soát do sai kỹ thuật sử dụng bình hít/xịt",
        "condition_desc": "Hen không kiểm soát hoặc kiểm soát một phần + Phát hiện lỗi sai trong các bước dùng thiết bị (f415)",
        "condition_fn": lambda wm: (
            (wm.get("f706") or wm.get("f707")) and wm.get("f415")
        ),
        "consequent_facts": ["f415"],
        "cf": 0.90,
        "rationale": "Sai kỹ thuật dùng bình xịt định liều hoặc bình hít bột khô khiến hạt thuốc không tới được phế quản, giảm hiệu quả điều trị nghiêm trọng."
    },
    {
        "id": "R_CAUSE_ENVIRONMENTAL_TRIGGER",
        "name": "Mất kiểm soát do yếu tố môi trường / dị nguyên kích phát",
        "condition_desc": "Hen mất kiểm soát + Tiếp xúc dị nguyên (f402) HOẶC Thay đổi thời tiết/ô nhiễm (f403) HOẶC Khói bụi nghề nghiệp (f406)",
        "condition_fn": lambda wm: (
            (wm.get("f706") or wm.get("f707")) and (wm.get("f402") or wm.get("f403") or wm.get("f406"))
        ),
        "consequent_facts": ["f402"],
        "cf": 0.80,
        "rationale": "Tiếp xúc liên tục với các tác nhân dị ứng (bụi nhà, lông thú) hoặc ô nhiễm môi trường gây viêm mạn tính dai dẳng đường thở."
    }
]

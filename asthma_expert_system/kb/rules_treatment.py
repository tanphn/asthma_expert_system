# asthma_expert_system/kb/rules_treatment.py
"""
Hệ thống luật Đề xuất Bậc điều trị & Điều chỉnh Phác đồ theo GINA 2023/2024
Bao gồm Lộ trình 1 (Track 1 MART - Ưu tiên) và Lộ trình 2 (Track 2 - Thay thế).
"""

RULES_TREATMENT = [
    # ==========================================
    # KHỞI ĐẦU ĐIỀU TRỊ (INITIAL TREATMENT SELECTION)
    # ==========================================
    {
        "id": "R_TX_STEP1",
        "name": "Khởi đầu Bậc 1 (GINA Step 1)",
        "condition_desc": "Hen gián đoạn (f601) + Triệu chứng < 2 lần/tháng + Không có đợt cấp trong năm qua (f124 == 0)",
        "condition_fn": lambda wm: (
            wm.get("f601") and (wm.get("f124") == 0 or wm.get("f124") is None)
        ),
        "consequent_facts": ["f801"],
        "cf": 0.90,
        "rationale": "Bệnh nhân có triệu chứng rất thưa thớt và không có yếu tố nguy cơ đợt cấp; chỉ cần điều trị kháng viêm khi có triệu chứng (Track 1: ICS-formoterol khi cần)."
    },
    {
        "id": "R_TX_STEP2",
        "name": "Khởi đầu Bậc 2 (GINA Step 2)",
        "condition_desc": "Hen dai dẳng nhẹ (f602) HOẶC Triệu chứng ≥ 2 lần/tháng nhưng không hàng ngày HOẶC Hen gián đoạn nhưng có yếu tố nguy cơ đợt cấp (f124 >= 1)",
        "condition_fn": lambda wm: (
            wm.get("f602") or (wm.get("f601") and wm.get("f124") and wm.get("f124") >= 1)
        ),
        "consequent_facts": ["f802"],
        "cf": 0.90,
        "rationale": "Triệu chứng xảy ra từ 2 lần/tháng trở lên cần liệu pháp kiểm soát thường xuyên hoặc ICS-formoterol khi cần để giảm nguy cơ bùng phát cơn hen nặng."
    },
    {
        "id": "R_TX_STEP3",
        "name": "Khởi đầu Bậc 3 (GINA Step 3 - SMART/MART)",
        "condition_desc": "Hen dai dẳng trung bình (f603) HOẶC Triệu chứng hầu hết các ngày trong tuần (f120 >= 4) HOẶC Thức giấc do hen ≥ 1 lần/tuần (f121 >= 1)",
        "condition_fn": lambda wm: (
            wm.get("f603") and not wm.get("f604")
        ),
        "consequent_facts": ["f803"],
        "cf": 0.92,
        "rationale": "Bệnh nhân có triệu chứng thường xuyên hoặc thức giấc đêm cần phối hợp duy trì liều thấp ICS-LABA (ưu tiên liệu pháp SMART với ICS-formoterol)."
    },
    {
        "id": "R_TX_STEP4",
        "name": "Khởi đầu Bậc 4 (GINA Step 4)",
        "condition_desc": "Hen dai dẳng nặng (f604) với triệu chứng hàng ngày, thức giấc đêm thường xuyên HOẶC FEV1 < 60% dự đoán (f205 < 60) nhưng đợt cấp < 2 lần/năm",
        "condition_fn": lambda wm: (
            wm.get("f604") and (wm.get("f124") is None or wm.get("f124") < 2)
        ),
        "consequent_facts": ["f804"],
        "cf": 0.92,
        "rationale": "Bệnh nhân có biểu hiện hen nặng ngay từ đầu hoặc tắc nghẽn thông khí đáng kể cần khởi đầu với liều trung bình ICS-formoterol duy trì và cắt cơn."
    },
    {
        "id": "R_TX_STEP5",
        "name": "Đề xuất Bậc 5 (GINA Step 5 - Hen nặng / Khó trị)",
        "condition_desc": "Hen dai dẳng nặng (f604) kèm tiền sử ≥ 2 đợt cấp cần Corticoid toàn thân/năm (f124 >= 2) HOẶC Không kiểm soát ở Bậc 4",
        "condition_fn": lambda wm: (
            (wm.get("f604") and wm.get("f124") is not None and wm.get("f124") >= 2) or
            (wm.get("f310") == 4 and wm.get("f707"))
        ),
        "consequent_facts": ["f805"],
        "cf": 0.95,
        "rationale": "Hen nặng khó kiểm soát hoặc tái phát nhiều đợt cấp nặng cần nâng lên Bậc 5, phối hợp thêm LAMA (Tiotropium) và hội chẩn chuyên khoa chỉ định thuốc sinh học (Biologics)."
    },

    # ==========================================
    # ĐIỀU CHỈNH TĂNG / GIẢM BẬC TÁI KHÁM (FOLLOW-UP ADJUSTMENTS)
    # ==========================================
    {
        "id": "R_TX_STEP_UP_SUSTAINED",
        "name": "Chỉ định Tăng bậc điều trị duy trì (Step-Up)",
        "condition_desc": "Hen không kiểm soát (f707) + Tuân thủ thuốc tốt (not f414) + Kỹ thuật hít đúng (not f415)",
        "condition_fn": lambda wm: (
            wm.get("f707") and not wm.get("f414") and not wm.get("f415")
        ),
        "consequent_facts": ["f810"],
        "cf": 0.92,
        "rationale": "Bệnh nhân không kiểm soát dù đã tuân thủ tốt và dùng đúng kỹ thuật -> Nguyên nhân do hoạt lực thuốc chưa đủ -> Cần nâng lên 1 bậc điều trị và đánh giá lại sau 2-3 tháng."
    },
    {
        "id": "R_TX_MAINTAIN_AND_TRAIN",
        "name": "Duy trì bậc hiện tại & Huấn luyện lại kỹ thuật/tuân thủ",
        "condition_desc": "Hen mất kiểm soát hoặc kiểm soát 1 phần (f706/f707) NHƯNG phát hiện Kém tuân thủ (f414) HOẶC Sai kỹ thuật hít (f415)",
        "condition_fn": lambda wm: (
            (wm.get("f706") or wm.get("f707")) and (wm.get("f414") or wm.get("f415"))
        ),
        "consequent_facts": ["f812"],
        "cf": 0.90,
        "rationale": "Chưa vội tăng bậc điều trị khi phát hiện lỗi kỹ thuật hoặc quên thuốc. Cần tập trung chỉnh kỹ thuật hít và nâng cao tuân thủ trước khi xem xét đổi liều."
    },
    {
        "id": "R_TX_STEP_DOWN",
        "name": "Chỉ định Giảm bậc điều trị an toàn (Step-Down)",
        "condition_desc": "Hen kiểm soát tốt hoàn toàn (f705) duy trì liên tục trong ≥ 3 tháng + Chức năng phổi ổn định",
        "condition_fn": lambda wm: (
            wm.get("f705") and wm.get("f310") and wm.get("f310") > 1
        ),
        "consequent_facts": ["f811"],
        "cf": 0.88,
        "rationale": "Khi hen đã kiểm soát tốt ổn định trong 3 tháng, nên tìm liều điều trị thấp nhất có hiệu quả bằng cách giảm liều ICS từ 25-50% hoặc giảm 1 bậc."
    },

    # ==========================================
    # CẢNH BÁO CẤP CỨU (EMERGENCY ALERTS)
    # ==========================================
    {
        "id": "R_EMERGENCY_ALERT",
        "name": "Cảnh báo Cơn Hen Phế Quản Cấp Nặng",
        "condition_desc": "Khó thở dữ dội, không nói được trọn câu, thở co kéo cơ hô hấp phụ, PEF < 50% dự đoán hoặc tiền sử từng vào ICU (f418)",
        "condition_fn": lambda wm: (
            wm.get("f418") and (wm.get("f103") or wm.get("f707"))
        ),
        "consequent_facts": ["f820"],
        "cf": 0.95,
        "rationale": "Bệnh nhân có tiền sử đợt cấp đe dọa tính mạng đang xuất hiện triệu chứng mất kiểm soát nặng -> Cần theo dõi sát tại cơ sở y tế có trang bị cấp cứu."
    }
]

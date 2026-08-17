# asthma_expert_system/kb/rules_severity.py
"""
Hệ thống luật Phân loại Mức độ Nặng Ban đầu của Hen Phế Quản (GINA & NIH/EPR-3).
Được đánh giá trước khi bắt đầu điều trị kiểm soát.
"""

RULES_SEVERITY = [
    {
        "id": "R_SEV_SEVERE",
        "name": "Hen dai dẳng nặng (Severe Persistent - L11)",
        "condition_desc": "Triệu chứng xuất hiện suốt cả ngày HOẶC Đêm > 4 lần/tuần HOẶC Giới hạn hoạt động nhiều (mức 2) HOẶC FEV1 < 60% dự đoán HOẶC PEF biến thiên > 30%",
        "condition_fn": lambda wm: (
            wm.get("f122") == 2 or
            (wm.get("f205") is not None and wm.get("f205") < 60) or
            (wm.get("f204") is not None and wm.get("f204") >= 30) or
            (wm.get("f120") >= 7 and wm.get("f121") >= 4)
        ),
        "consequent_facts": ["f604"],
        "cf": 0.95,
        "rationale": "Sự hiện diện của tổn thương chức năng hô hấp nặng (FEV1 < 60%), hạn chế hoạt động nhiều hoặc triệu chứng liên tục xếp vào nhóm Hen dai dẳng nặng."
    },
    {
        "id": "R_SEV_MODERATE",
        "name": "Hen dai dẳng trung bình (Moderate Persistent - L10)",
        "condition_desc": "Triệu chứng hàng ngày (f120 >= 5) HOẶC Đêm > 1 lần/tuần (f121 >= 2) HOẶC Giới hạn hoạt động nhẹ (mức 1) HOẶC FEV1 60-79% HOẶC dùng SABA hàng ngày (f123 >= 7)",
        "condition_fn": lambda wm: (
            not wm.get("f604") and (
                wm.get("f120") >= 5 or
                wm.get("f121") >= 2 or
                wm.get("f122") == 1 or
                wm.get("f123") >= 7 or
                (wm.get("f205") is not None and 60 <= wm.get("f205") < 80) or
                (wm.get("f204") is not None and 20 <= wm.get("f204") < 30)
            )
        ),
        "consequent_facts": ["f603"],
        "cf": 0.90,
        "rationale": "Triệu chứng xảy ra hàng ngày hoặc đêm thường xuyên (>1 lần/tuần) kèm FEV1 từ 60-79% phản ánh mức độ Hen dai dẳng trung bình."
    },
    {
        "id": "R_SEV_MILD_PERSISTENT",
        "name": "Hen dai dẳng nhẹ (Mild Persistent - L9)",
        "condition_desc": "Triệu chứng > 2 ngày/tuần nhưng không hàng ngày (3 <= f120 <= 4) HOẶC Đêm 3-4 lần/tháng (1 <= f121 <= 2/tuần) HOẶC Dùng SABA > 2 lần/tuần VÀ FEV1 >= 80%",
        "condition_fn": lambda wm: (
            not wm.get("f604") and not wm.get("f603") and (
                (2 < wm.get("f120") < 5) or
                (wm.get("f121") == 1) or
                (wm.get("f123") > 2) or
                (wm.get("f205") is not None and wm.get("f205") >= 80 and (wm.get("f120") > 2 or wm.get("f121") >= 1))
            )
        ),
        "consequent_facts": ["f602"],
        "cf": 0.88,
        "rationale": "Triệu chứng nhiều hơn 2 ngày/tuần nhưng không liên tục cả tuần và chức năng phổi còn tốt (FEV1 ≥ 80%) xếp vào Hen dai dẳng nhẹ."
    },
    {
        "id": "R_SEV_INTERMITTENT",
        "name": "Hen gián đoạn (Intermittent - L8)",
        "condition_desc": "Triệu chứng ban ngày ≤ 2 ngày/tuần VÀ Đêm ≤ 2 lần/tháng (f121 == 0) VÀ Không giới hạn hoạt động (f122 == 0) VÀ FEV1 >= 80%",
        "condition_fn": lambda wm: (
            not wm.get("f604") and not wm.get("f603") and not wm.get("f602") and (
                wm.get("f120") <= 2 and
                wm.get("f121") == 0 and
                wm.get("f122") == 0 and
                wm.get("f123") <= 2 and
                (wm.get("f205") is None or wm.get("f205") >= 80)
            )
        ),
        "consequent_facts": ["f601"],
        "cf": 0.85,
        "rationale": "Triệu chứng thưa thớt (≤ 2 lần/tuần), không có triệu chứng ban đêm, không giới hạn sinh hoạt và chức năng phổi bình thường xếp vào Hen gián đoạn."
    }
]

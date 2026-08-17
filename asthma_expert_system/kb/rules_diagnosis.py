# asthma_expert_system/kb/rules_diagnosis.py
"""
Hệ thống luật Chẩn đoán Xác định Hen & Chẩn đoán Phân biệt
Theo Hướng dẫn GINA 2023/2024 & Hội Phổi Việt Nam.
"""

RULES_DIAGNOSIS = [
    # ==========================================
    # KHỐI 1: CHẨN ĐOÁN LÂM SÀNG HEN PHẾ QUẢN
    # ==========================================
    {
        "id": "R_DIAG_L1",
        "name": "Nghi ngờ lâm sàng Hen (L1)",
        "condition_desc": "Có ≥ 2 triệu chứng chính (Ho, Khò khè, Khó thở, Nặng ngực) VÀ (Triệu chứng biến đổi theo thời gian HOẶC nặng về đêm HOẶC khởi phát khi gắng sức HOẶC sau nhiễm virus)",
        "condition_fn": lambda wm: (
            sum(1 for f in ["f101", "f102", "f103", "f104"] if wm.get(f)) >= 2
            and (wm.get("f105") or wm.get("f106") or wm.get("f107") or wm.get("f108"))
        ),
        "consequent_facts": ["f501", "f503"],
        "cf": 0.75,
        "rationale": "Sự hiện diện của nhiều hơn một triệu chứng hô hấp thay đổi theo thời gian và cường độ, kích phát bởi các yếu tố đặc trưng là nền tảng chẩn đoán lâm sàng hen."
    },
    {
        "id": "R_DIAG_L2",
        "name": "Bằng chứng rối loạn thông khí tắc nghẽn biến đổi (L2)",
        "condition_desc": "Test hồi phục phế quản (+) (FEV1 tăng ≥12% VÀ ≥200mL) HOẶC PEF biến thiên >10% HOẶC Test kích thích (+) HOẶC FEV1 tăng ≥12% sau điều trị thử",
        "condition_fn": lambda wm: (
            wm.get("f207") or
            wm.get("f206") or
            (wm.get("f202") is not None and wm.get("f202") >= 12 and (wm.get("f203") is None or wm.get("f203") >= 200)) or
            (wm.get("f204") is not None and wm.get("f204") > 10)
        ),
        "consequent_facts": ["f502"],
        "cf": 0.90,
        "rationale": "Dao động thông khí tắc nghẽn quá mức ghi nhận qua hô hấp ký hoặc đo biến thiên lưu lượng đỉnh xác nhận tính chất co thắt có hồi phục của hen."
    },
    {
        "id": "R_DIAG_L3",
        "name": "CHẨN ĐOÁN XÁC ĐỊNH HEN PHẾ QUẢN (L3 = L1 + L2)",
        "condition_desc": "Thỏa mãn cả Tiêu chuẩn lâm sàng nghi ngờ Hen (L1) VÀ Bằng chứng khách quan dao động luồng khí (L2)",
        "condition_fn": lambda wm: (
            wm.get("f501") and wm.get("f502")
        ),
        "consequent_facts": ["f504"],
        "cf": 0.98,
        "rationale": "Đạt Tiêu chuẩn Vàng GINA: Tiền sử triệu chứng hô hấp biến đổi điển hình kèm bằng chứng rối loạn thông khí tắc nghẽn có phục hồi."
    },
    {
        "id": "R_DIAG_L4",
        "name": "Chẩn đoán Hen ở bệnh nhân đang dùng thuốc kiểm soát (L4)",
        "condition_desc": "Đang dùng ICS/LABA + Còn triệu chứng lâm sàng hen + Có test hồi phục hoặc test kích thích dương tính",
        "condition_fn": lambda wm: (
            (wm.get("f301") or wm.get("f302"))
            and any(wm.get(f) for f in ["f101", "f102", "f103", "f104"])
            and (wm.get("f207") or wm.get("f206") or (wm.get("f202") is not None and wm.get("f202") >= 12))
        ),
        "consequent_facts": ["f504"],
        "cf": 0.95,
        "rationale": "Bệnh nhân đang dùng thuốc duy trì nhưng vẫn còn triệu chứng và test chức năng hô hấp dương tính xác định chẩn đoán hen phế quản."
    },

    # ==========================================
    # KHỐI 2: CHẨN ĐOÁN PHÂN BIỆT & BỆNH ĐỒNG MẮC
    # ==========================================
    {
        "id": "R_DIFF_COPD",
        "name": "Nghi ngờ Bệnh Phổi Tắc Nghẽn Mạn Tính (COPD)",
        "condition_desc": "Tiền sử hút thuốc lá ≥ 10 gói-năm + Tuổi > 40 + Khó thở liên tục tiến triển hoặc ho đờm mạn tính + FEV1/FVC < 0.70 sau giãn phế quản (không phục hồi hoàn toàn)",
        "condition_fn": lambda wm: (
            (wm.get("f401") or wm.get("f404"))
            and (wm.get("f001") is None or wm.get("f001") >= 40)
            and (wm.get("f109") or wm.get("f113") or wm.get("f103"))
            and (wm.get("f201") is not None and wm.get("f201") < 0.70)
            and (not wm.get("f207") and (wm.get("f202") is None or wm.get("f202") < 12))
        ),
        "consequent_facts": ["f509"],
        "cf": 0.88,
        "rationale": "Hút thuốc lá nhiều năm kết hợp với khó thở tiến triển mạn tính và tắc nghẽn đường thở cố định sau thử thuốc giãn phế quản là đặc trưng của COPD."
    },
    {
        "id": "R_DIFF_ACO",
        "name": "Nghi ngờ Hội chứng Chồng lấp Hen - COPD (ACO)",
        "condition_desc": "Bệnh nhân có tiền sử Hen hoặc cơ địa dị ứng + Tiền sử hút thuốc lá ≥ 10 gói-năm + Có cả tắc nghẽn cố định FEV1/FVC < 0.70 lẫn đáp ứng giãn phế quản FEV1 tăng ≥ 12% & ≥ 200mL",
        "condition_fn": lambda wm: (
            (wm.get("f401") or wm.get("f404"))
            and (wm.get("f003") or wm.get("f004") or wm.get("f105") or wm.get("f106"))
            and (wm.get("f201") is not None and wm.get("f201") < 0.70)
            and (wm.get("f207") or (wm.get("f202") is not None and wm.get("f202") >= 12))
        ),
        "consequent_facts": ["f514"],
        "cf": 0.85,
        "rationale": "Sự kết hợp giữa đặc tính viêm dị ứng dao động của Hen và tổn thương cấu trúc tắc nghẽn cố định do khói thuốc của COPD tạo nên hội chứng chồng lấp ACO."
    },
    {
        "id": "R_DIFF_HEART_FAILURE",
        "name": "Nghi ngờ Suy Tim Trái / Hen Tim (Cardiac Asthma)",
        "condition_desc": "Tiền sử Tăng huyết áp / Bệnh tim mạch + Khó thở kịch phát về đêm hoặc khi nằm + Nghe phổi có Ran ẩm 2 đáy phổi",
        "condition_fn": lambda wm: (
            wm.get("f405")
            and (wm.get("f103") or wm.get("f106"))
            and wm.get("f110")
        ),
        "consequent_facts": ["f510"],
        "cf": 0.85,
        "rationale": "Cơn khó thở kịch phát về đêm ở bệnh nhân tim mạch kèm ran ẩm đáy phổi phản ánh tình trạng ứ huyết mao mạch phổi do suy tim trái (hen tim)."
    },
    {
        "id": "R_DIFF_AIRWAY_OBSTRUCTION",
        "name": "Nghi ngờ Hẹp / Dị vật khí phế quản / Rối loạn chức năng dây thanh (VCD)",
        "condition_desc": "Tiếng rít thanh quản khu trú cố định (Stridor) + Khó thở thì hít vào hoặc không đáp ứng test giãn phế quản",
        "condition_fn": lambda wm: (
            wm.get("f111")
            and (wm.get("f103") or wm.get("f102"))
            and (wm.get("f202") is None or wm.get("f202") < 8)
        ),
        "consequent_facts": ["f511"],
        "cf": 0.80,
        "rationale": "Tiếng rít cố định không đáp ứng giãn phế quản gợi ý tổn thương hẹp cơ học trung tâm, u khí quản, dị vật hoặc co thắt dây thanh âm nghịch thường."
    },
    {
        "id": "R_DIFF_GERD",
        "name": "Nghi ngờ Ho kéo dài do Trào ngược dạ dày thực quản (GERD)",
        "condition_desc": "Ho khan kéo dài tăng khi nằm hoặc sau ăn no + Có triệu chứng ợ chua/nóng rát xương ức + Không có bằng chứng tắc nghẽn trên hô hấp ký",
        "condition_fn": lambda wm: (
            wm.get("f112")
            and wm.get("f101")
            and (wm.get("f201") is None or wm.get("f201") >= 0.75)
            and not wm.get("f502")
        ),
        "consequent_facts": ["f512"],
        "cf": 0.78,
        "rationale": "Acid dịch vị trào ngược gây kích thích phản xạ phế vị tại thực quản hoặc hít vi thể vào thanh khí quản gây ho mạn tính dễ nhầm với hen."
    },
    {
        "id": "R_DIFF_BRONCHIECTASIS",
        "name": "Nghi ngờ Giãn Phế Quản (Bronchiectasis)",
        "condition_desc": "Ho khạc đờm mủ lượng nhiều kéo dài nhiều năm + Các đợt nhiễm trùng tái diễn",
        "condition_fn": lambda wm: (
            wm.get("f109")
            and wm.get("f101")
        ),
        "consequent_facts": ["f513"],
        "cf": 0.82,
        "rationale": "Ho khạc đờm mủ đục số lượng lớn qua nhiều năm là dấu hiệu kinh điển của giãn phế quản, cần chụp CT ngực độ phân giải cao (HRCT) để chẩn đoán."
    }
]

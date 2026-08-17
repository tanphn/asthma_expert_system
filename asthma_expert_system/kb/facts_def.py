# asthma_expert_system/kb/facts_def.py
"""
Định nghĩa hệ thống Facts chuẩn cho Hệ thống Chuyên gia Chẩn đoán & Quản lý Hen Phế Quản
Tuân thủ Hướng dẫn GINA 2023/2024 & Hướng dẫn Chẩn đoán và Điều trị Hen Phế Quản - Bộ Y tế.
"""

FACTS_DEF = {
    # ==========================================
    # f0xx: THÔNG TIN HÀNH CHÍNH & CƠ ĐỊA (Demographics & History)
    # ==========================================
    "f001": {
        "name": "Tuổi",
        "desc": "Tuổi của bệnh nhân",
        "category": "Hành chính",
        "type": "numeric",
        "default": 30
    },
    "f002": {
        "name": "Giới tính",
        "desc": "Giới tính (Nam/Nữ)",
        "category": "Hành chính",
        "type": "string",
        "default": "Nam"
    },
    "f003": {
        "name": "Tiền sử dị ứng bản thân / Cơ địa Atopy",
        "desc": "Viêm mũi dị ứng, chàm/viêm da cơ địa, dị ứng thức ăn hoặc thuốc",
        "category": "Tiền sử",
        "type": "boolean",
        "default": False
    },
    "f004": {
        "name": "Tiền sử gia đình mắc Hen / Dị ứng",
        "desc": "Bố mẹ hoặc anh chị em ruột có tiền sử hen hoặc bệnh dị ứng",
        "category": "Tiền sử",
        "type": "boolean",
        "default": False
    },
    "f005": {
        "name": "Chỉ số BMI",
        "desc": "Chỉ số khối cơ thể (kg/m2) - BMI ≥ 30 tăng nguy cơ hen khó trị",
        "category": "Tiền sử",
        "type": "numeric",
        "default": 22.0
    },

    # ==========================================
    # f1xx: TRIỆU CHỨNG LÂM SÀNG (Clinical Symptoms)
    # ==========================================
    # Triệu chứng chính (Cardinals)
    "f101": {
        "name": "Ho kéo dài hoặc từng cơn",
        "desc": "Ho khan hoặc có đờm trong, thường dai dẳng, tái phát nhiều lần",
        "category": "Triệu chứng chính",
        "type": "boolean",
        "default": False
    },
    "f102": {
        "name": "Khò khè khi thở ra",
        "desc": "Tiếng rít/khò khè nghe được khi thở ra (đặc biệt khi gắng sức hoặc ban đêm)",
        "category": "Triệu chứng chính",
        "type": "boolean",
        "default": False
    },
    "f103": {
        "name": "Khó thở / Thở hụt hơi",
        "desc": "Cảm giác khó thở, thở gấp, ngột ngạt xuất hiện từng cơn",
        "category": "Triệu chứng chính",
        "type": "boolean",
        "default": False
    },
    "f104": {
        "name": "Cảm giác nặng ngực / Co thắt lồng ngực",
        "desc": "Cảm giác lồng ngực bị đè ép, thắt chặt lại khi thở",
        "category": "Triệu chứng chính",
        "type": "boolean",
        "default": False
    },

    # Đặc điểm biến đổi & Yếu tố khởi phát (Variability & Triggers)
    "f105": {
        "name": "Triệu chứng thay đổi theo thời gian / cường độ",
        "desc": "Triệu chứng xuất hiện không liên tục, lúc tăng lúc giảm rõ rệt",
        "category": "Đặc điểm triệu chứng",
        "type": "boolean",
        "default": False
    },
    "f106": {
        "name": "Triệu chứng nặng hơn về đêm hoặc sáng sớm",
        "desc": "Thường thức giấc lúc 2-4h sáng do ho, khò khè hoặc khó thở",
        "category": "Đặc điểm triệu chứng",
        "type": "boolean",
        "default": False
    },
    "f107": {
        "name": "Triệu chứng khởi phát khi gắng sức / cười to",
        "desc": "Xuất hiện hoặc tăng lên khi tập thể dục, chạy nhảy hoặc cười lớn",
        "category": "Đặc điểm triệu chứng",
        "type": "boolean",
        "default": False
    },
    "f108": {
        "name": "Triệu chứng khởi phát sau nhiễm virus hô hấp",
        "desc": "Cơn khó thở/ho kéo dài sau mỗi đợt cảm cúm, viêm đường hô hấp trên",
        "category": "Đặc điểm triệu chứng",
        "type": "boolean",
        "default": False
    },

    # Dấu hiệu phân biệt bệnh khác (Differential Signs)
    "f109": {
        "name": "Ho khạc đờm mủ đục kéo dài nhiều năm",
        "desc": "Khạc đờm đặc màu vàng/xanh lượng nhiều hàng ngày (gợi ý Giãn phế quản/COPD)",
        "category": "Dấu hiệu phân biệt",
        "type": "boolean",
        "default": False
    },
    "f110": {
        "name": "Ran ẩm / Ran nổ ở 2 đáy phổi",
        "desc": "Khám nghe phổi có ran ẩm 2 đáy phổi (gợi ý Suy tim trái hoặc ứ huyết phổi)",
        "category": "Dấu hiệu phân biệt",
        "type": "boolean",
        "default": False
    },
    "f111": {
        "name": "Tiếng rít thanh/khí quản cố định khu trú (Stridor)",
        "desc": "Tiếng rít thì hít vào hoặc rít cố định một vị trí (gợi ý Hẹp khí phế quản / Dị vật / VCD)",
        "category": "Dấu hiệu phân biệt",
        "type": "boolean",
        "default": False
    },
    "f112": {
        "name": "Ho / Khó thở tăng khi nằm ngửa hoặc sau ăn no",
        "desc": "Ợ chua, nóng rát sau xương ức, khàn giọng sáng sớm (gợi ý GERD)",
        "category": "Dấu hiệu phân biệt",
        "type": "boolean",
        "default": False
    },
    "f113": {
        "name": "Khó thở liên tục tiến triển tăng dần theo tuổi",
        "desc": "Khó thở không hồi phục hoàn toàn giữa các đợt, nặng dần theo năm tháng",
        "category": "Dấu hiệu phân biệt",
        "type": "boolean",
        "default": False
    },

    # Tần suất triệu chứng ban đầu (Severity Grading Inputs)
    "f120": {
        "name": "Tần suất triệu chứng ban ngày (ngày/tuần)",
        "desc": "Số ngày trong tuần xuất hiện triệu chứng ban ngày (0-7)",
        "category": "Mức độ ban đầu",
        "type": "numeric",
        "default": 0
    },
    "f121": {
        "name": "Tần suất thức giấc ban đêm do triệu chứng (lần/tuần)",
        "desc": "Số lần thức giấc ban đêm do ho/khó thở/khò khè trong tuần (0-7)",
        "category": "Mức độ ban đầu",
        "type": "numeric",
        "default": 0
    },
    "f122": {
        "name": "Mức độ giới hạn hoạt động",
        "desc": "0: Không hạn chế, 1: Hạn chế nhẹ, 2: Hạn chế nhiều/rất nhiều",
        "category": "Mức độ ban đầu",
        "type": "numeric",
        "default": 0
    },
    "f123": {
        "name": "Số lần sử dụng thuốc cắt cơn SABA/tuần",
        "desc": "Số lần xịt thuốc cắt cơn nhanh (Salbutamol/Ventolin) trong tuần",
        "category": "Mức độ ban đầu",
        "type": "numeric",
        "default": 0
    },
    "f124": {
        "name": "Số đợt cấp cần dùng Corticoid toàn thân trong 12 tháng qua",
        "desc": "Số lần phải nhập viện hoặc uống/tiêm Corticoid vì bùng phát cơn hen",
        "category": "Mức độ ban đầu",
        "type": "numeric",
        "default": 0
    },

    # ==========================================
    # f2xx: THĂM DÒ CHỨC NĂNG HÔ HẤP & CẬN LÂM SÀNG (Spirometry & Labs)
    # ==========================================
    "f201": {
        "name": "Chỉ số FEV1/FVC trước giãn phế quản",
        "desc": "Tỷ lệ FEV1/FVC (Bình thường > 0.75-0.80 ở người lớn, > 0.85 ở trẻ em)",
        "category": "Hô hấp ký",
        "type": "numeric",
        "default": None
    },
    "f202": {
        "name": "Mức tăng FEV1 sau test hồi phục phế quản (%)",
        "desc": "Phần trăm FEV1 tăng sau xịt 400 mcg Salbutamol (Dương tính nếu ≥ 12%)",
        "category": "Hô hấp ký",
        "type": "numeric",
        "default": None
    },
    "f203": {
        "name": "Thể tích FEV1 tuyệt đối tăng sau test hồi phục (mL)",
        "desc": "Thể tích FEV1 tăng tuyệt đối (mL) (Dương tính nếu ≥ 200 mL)",
        "category": "Hô hấp ký",
        "type": "numeric",
        "default": None
    },
    "f204": {
        "name": "Độ biến thiên lưu lượng đỉnh PEF trong ngày (%)",
        "desc": "Đo sáng - tối liên tục 1-2 tuần (Dương tính nếu > 10% ở người lớn, > 13% ở trẻ)",
        "category": "Hô hấp ký",
        "type": "numeric",
        "default": None
    },
    "f205": {
        "name": "FEV1 % so với giá trị dự đoán (% Predicted)",
        "desc": "Giá trị FEV1 % lý thuyết đo được (≥80%: Bình thường/Nhẹ, 60-79%: Trung bình, <60%: Nặng)",
        "category": "Hô hấp ký",
        "type": "numeric",
        "default": None
    },
    "f206": {
        "name": "Test kích thích phế quản (Methacholine / Histamine / Gắng sức)",
        "desc": "Dương tính khi PC20 ≤ 8 mg/mL hoặc FEV1 giảm ≥ 10-15% sau gắng sức",
        "category": "Hô hấp ký",
        "type": "boolean",
        "default": False
    },
    "f207": {
        "name": "Test hồi phục phế quản (BDR test) kết luận Dương tính",
        "desc": "Đã được kết luận dương tính bởi phòng thăm dò chức năng",
        "category": "Hô hấp ký",
        "type": "boolean",
        "default": False
    },
    "f208": {
        "name": "Nồng độ FeNO (Nitric Oxide khí thở ra - ppb)",
        "desc": "FeNO > 50 ppb (>35 ở trẻ): Viêm đường thở Type 2 ưa Eosinophil rõ rệt",
        "category": "Dấu ấn sinh học",
        "type": "numeric",
        "default": None
    },
    "f209": {
        "name": "Bạch cầu ái toan máu ngoại vi (Blood Eosinophils - tế bào/µL)",
        "desc": "Eosinophil ≥ 300 tế bào/µL: Kiểu hình viêm tăng bạch cầu ái toan (Type 2 High)",
        "category": "Dấu ấn sinh học",
        "type": "numeric",
        "default": None
    },
    "f210": {
        "name": "IgE toàn phần huyết thanh tăng cao (IU/mL)",
        "desc": "IgE huyết thanh toàn phần hoặc IgE đặc hiệu với dị nguyên dương tính",
        "category": "Dấu ấn sinh học",
        "type": "boolean",
        "default": False
    },

    # ==========================================
    # f3xx: TIỀN SỬ DÙNG THUỐC & BẬC ĐIỀU TRỊ HIỆN TẠI (Medications)
    # ==========================================
    "f301": {
        "name": "Đang sử dụng ICS đơn thuần (Inhaled Corticosteroid)",
        "desc": "Budesonide, Fluticasone propionate, Beclomethasone xịt hằng ngày",
        "category": "Thuốc",
        "type": "boolean",
        "default": False
    },
    "f302": {
        "name": "Đang sử dụng ICS-LABA kết hợp",
        "desc": "Symbicort (Budesonide/Formoterol), Seretide (Fluticasone/Salmeterol), Foster (Beclomethasone/Formoterol)",
        "category": "Thuốc",
        "type": "boolean",
        "default": False
    },
    "f303": {
        "name": "Đang sử dụng LTRA (Kháng thụ thể Leukotriene)",
        "desc": "Montelukast (Singulair 10mg/ngày)",
        "category": "Thuốc",
        "type": "boolean",
        "default": False
    },
    "f304": {
        "name": "Đang sử dụng LAMA (Kháng Cholinergic tác dụng kéo dài)",
        "desc": "Tiotropium (Spiriva Respimat)",
        "category": "Thuốc",
        "type": "boolean",
        "default": False
    },
    "f305": {
        "name": "Đang sử dụng Corticoid đường uống duy trì (OCS)",
        "desc": "Prednisolone / Methylprednisolone uống kéo dài",
        "category": "Thuốc",
        "type": "boolean",
        "default": False
    },
    "f306": {
        "name": "Đang dùng thuốc sinh học (Biologics)",
        "desc": "Anti-IgE (Omalizumab), Anti-IL5 (Mepolizumab/Benralizumab), Anti-IL4R (Dupilumab)",
        "category": "Thuốc",
        "type": "boolean",
        "default": False
    },
    "f310": {
        "name": "Bậc điều trị GINA hiện tại của bệnh nhân (Current Step)",
        "desc": "Bậc 1 đến Bậc 5 (0 nếu chưa điều trị thuốc kiểm soát)",
        "category": "Thuốc",
        "type": "numeric",
        "default": 0
    },

    # ==========================================
    # f4xx: YẾU TỐ NGUY CƠ, TUÂN THỦ & KỸ THUẬT (Risks, Triggers & Inhaler Skills)
    # ==========================================
    "f401": {
        "name": "Tiền sử hút thuốc lá / thuốc lào (≥ 10 gói-năm)",
        "desc": "Hút thuốc lá nhiều năm (tăng nguy cơ COPD hoặc hội chứng chồng lấp ACO)",
        "category": "Nguy cơ & Kích phát",
        "type": "boolean",
        "default": False
    },
    "f402": {
        "name": "Tiếp xúc dị nguyên hô hấp (Bụi nhà, phấn hoa, lông thú, nấm mốc)",
        "desc": "Triệu chứng bùng phát rõ khi dọn nhà, tiếp xúc chó mèo, môi trường nhiều phấn hoa",
        "category": "Nguy cơ & Kích phát",
        "type": "boolean",
        "default": False
    },
    "f403": {
        "name": "Ảnh hưởng bởi thay đổi thời tiết, không khí lạnh, khói bụi ô nhiễm",
        "desc": "Triệu chứng trở nặng khi trở trời, trời lạnh đột ngột hoặc sương mù ô nhiễm",
        "category": "Nguy cơ & Kích phát",
        "type": "boolean",
        "default": False
    },
    "f404": {
        "name": "Tiền sử đã được chẩn đoán COPD trước đây",
        "desc": "Bệnh phổi tắc nghẽn mạn tính đã được xác định",
        "category": "Nguy cơ & Kích phát",
        "type": "boolean",
        "default": False
    },
    "f405": {
        "name": "Tiền sử Tăng huyết áp / Bệnh tim mạch / Suy tim",
        "desc": "Bệnh tim thiếu máu cục bộ, tăng huyết áp, suy tim phân suất tống máu giảm",
        "category": "Nguy cơ & Kích phát",
        "type": "boolean",
        "default": False
    },
    "f406": {
        "name": "Tiếp xúc khói bụi, hóa chất nghề nghiệp",
        "desc": "Thợ mộc, thợ sơn, công nhân may mặc, hóa chất, thợ hàn",
        "category": "Nguy cơ & Kích phát",
        "type": "boolean",
        "default": False
    },
    "f414": {
        "name": "Kém tuân thủ điều trị thuốc kiểm soát hằng ngày",
        "desc": "Thường xuyên quên xịt thuốc, chỉ dùng khi thấy khó thở (kém tuân thủ < 75% liều)",
        "category": "Tuân thủ & Kỹ thuật",
        "type": "boolean",
        "default": False
    },
    "f415": {
        "name": "Thực hiện sai kỹ thuật sử dụng bình xịt / hít",
        "desc": "Không lắc bình, không thở ra hết trước hít, hít quá nhanh hoặc không nín thở sau hít",
        "category": "Tuân thủ & Kỹ thuật",
        "type": "boolean",
        "default": False
    },
    "f416": {
        "name": "Không súc họng sau khi xịt thuốc chứa Corticoid",
        "desc": "Nguy cơ tưa miệng, nấm candida hầu họng, khàn giọng",
        "category": "Tuân thủ & Kỹ thuật",
        "type": "boolean",
        "default": False
    },
    "f417": {
        "name": "Sử dụng quá nhiều bình thuốc cắt cơn SABA (≥ 3 bình/năm)",
        "desc": "Dùng ≥ 3 bình Salbutamol/năm làm tăng nguy cơ đợt cấp nặng & tử vong",
        "category": "Nguy cơ tương lai",
        "type": "boolean",
        "default": False
    },
    "f418": {
        "name": "Tiền sử từng phải đặt nội khí quản / nhập ICU vì cơn hen cấp",
        "desc": "Yếu tố nguy cơ cao đợt bùng phát tử vong",
        "category": "Nguy cơ tương lai",
        "type": "boolean",
        "default": False
    },

    # ==========================================
    # f5xx: CÁC GIẢ THUYẾT & KẾT LUẬN CHẨN ĐOÁN (Inferred Diagnostic Hypotheses)
    # ==========================================
    "f501": {
        "name": "Triệu chứng lâm sàng điển hình nghi ngờ Hen",
        "desc": "Có ≥ 2 triệu chứng chính và có đặc điểm biến đổi / yếu tố kích phát",
        "category": "Chẩn đoán Hen",
        "type": "boolean",
        "default": False
    },
    "f502": {
        "name": "Bằng chứng rối loạn thông khí tắc nghẽn biến đổi",
        "desc": "FEV1/FVC giảm kèm Test phục hồi phế quản (+) hoặc PEF biến thiên > 10%",
        "category": "Chẩn đoán Hen",
        "type": "boolean",
        "default": False
    },
    "f503": {
        "name": "Nghi ngờ Hen Phế Quản (Suspected Asthma)",
        "desc": "Lâm sàng phù hợp hen, cần làm thêm đo chức năng hô hấp để khẳng định",
        "category": "Chẩn đoán Hen",
        "type": "boolean",
        "default": False
    },
    "f504": {
        "name": "CHẨN ĐOÁN XÁC ĐỊNH HEN PHẾ QUẢN (Confirmed Asthma)",
        "desc": "Đủ cả 2 tiêu chuẩn vàng: Triệu chứng lâm sàng điển hình + Bằng chứng dao động luồng khí",
        "category": "Chẩn đoán Hen",
        "type": "boolean",
        "default": False
    },

    # Chẩn đoán phân biệt & Chồng lấp (Differentials & Overlap)
    "f509": {
        "name": "Bệnh Phổi Tắc Nghẽn Mạn Tính (COPD)",
        "desc": "Tiền sử hút thuốc, tuổi > 40, khó thở liên tục tiến triển, tắc nghẽn không hồi phục",
        "category": "Phân biệt chẩn đoán",
        "type": "boolean",
        "default": False
    },
    "f510": {
        "name": "Suy Tim Trái / Hen Tim (Cardiac Asthma)",
        "desc": "Tiền sử tim mạch/THA, khó thở kịch phát về đêm kèm ran ẩm 2 đáy phổi",
        "category": "Phân biệt chẩn đoán",
        "type": "boolean",
        "default": False
    },
    "f511": {
        "name": "Hẹp / Dị vật đường thở / Rối loạn chức năng dây thanh (VCD)",
        "desc": "Tiếng rít cố định hoặc thì hít vào, không đáp ứng thuốc giãn phế quản",
        "category": "Phân biệt chẩn đoán",
        "type": "boolean",
        "default": False
    },
    "f512": {
        "name": "Bệnh Trào Ngược Dạ Dày Thực Quản (GERD / Microaspiration)",
        "desc": "Ho khan kéo dài, tăng khi nằm hoặc sau ăn, ợ chua, vị toan miệng",
        "category": "Phân biệt chẩn đoán",
        "type": "boolean",
        "default": False
    },
    "f513": {
        "name": "Giãn Phế Quản (Bronchiectasis)",
        "desc": "Ho khạc đờm mủ lượng nhiều từng đợt tái diễn nhiều năm, ngón tay dùi trống",
        "category": "Phân biệt chẩn đoán",
        "type": "boolean",
        "default": False
    },
    "f514": {
        "name": "Hội chứng Chồng lấp Hen - COPD (Asthma-COPD Overlap - ACO)",
        "desc": "Vừa có đặc điểm viêm dị ứng/biến đổi dao động của Hen vừa có tắc nghẽn cố định do khói thuốc của COPD",
        "category": "Phân biệt chẩn đoán",
        "type": "boolean",
        "default": False
    },

    # ==========================================
    # f6xx: PHÂN LOẠI MỨC ĐỘ NẶNG BAN ĐẦU (Severity Classification)
    # ==========================================
    "f601": {
        "name": "Hen gián đoạn (Intermittent Asthma)",
        "desc": "Triệu chứng ban ngày ≤ 2 lần/tuần, triệu chứng ban đêm ≤ 2 lần/tháng, FEV1 ≥ 80%",
        "category": "Mức độ nặng ban đầu",
        "type": "boolean",
        "default": False
    },
    "f602": {
        "name": "Hen dai dẳng nhẹ (Mild Persistent Asthma)",
        "desc": "Triệu chứng > 2 lần/tuần nhưng không hàng ngày, đêm 3-4 lần/tháng, FEV1 ≥ 80%",
        "category": "Mức độ nặng ban đầu",
        "type": "boolean",
        "default": False
    },
    "f603": {
        "name": "Hen dai dẳng trung bình (Moderate Persistent Asthma)",
        "desc": "Triệu chứng hàng ngày, đêm > 1 lần/tuần, dùng SABA hàng ngày, FEV1 60-79%",
        "category": "Mức độ nặng ban đầu",
        "type": "boolean",
        "default": False
    },
    "f604": {
        "name": "Hen dai dẳng nặng (Severe Persistent Asthma)",
        "desc": "Triệu chứng liên tục suốt ngày, đêm thường xuyên, giới hạn hoạt động nhiều, FEV1 < 60%",
        "category": "Mức độ nặng ban đầu",
        "type": "boolean",
        "default": False
    },

    # ==========================================
    # f7xx: ĐÁNH GIÁ MỨC ĐỘ KIỂM SOÁT TÁI KHÁM GINA (GINA Control Assessment)
    # ==========================================
    # 4 Tiêu chí kiểm soát triệu chứng GINA trong 4 tuần qua
    "f701": {
        "name": "GINA-Q1: Triệu chứng ban ngày > 2 lần/tuần",
        "desc": "Có xuất hiện triệu chứng hen ban ngày nhiều hơn 2 lần mỗi tuần trong 4 tuần qua",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },
    "f702": {
        "name": "GINA-Q2: Thức giấc ban đêm do hen",
        "desc": "Có bất kỳ lần nào thức giấc ban đêm do ho, khó thở, khò khè trong 4 tuần qua",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },
    "f703": {
        "name": "GINA-Q3: Dùng thuốc cắt cơn > 2 lần/tuần",
        "desc": "Cần xịt thuốc cắt cơn nhiều hơn 2 lần/tuần (không tính liều dự phòng trước gắng sức)",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },
    "f704": {
        "name": "GINA-Q4: Giới hạn hoạt động thể lực do hen",
        "desc": "Có bất kỳ sự hạn chế hoạt động sinh hoạt, thể thao hay công việc do hen",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },
    # Kết luận kiểm soát
    "f705": {
        "name": "Hen kiểm soát tốt (Well-controlled Asthma)",
        "desc": "Thỏa 0/4 tiêu chí GINA - Bệnh nhân không có triệu chứng đáng kể",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },
    "f706": {
        "name": "Hen kiểm soát một phần (Partly-controlled Asthma)",
        "desc": "Thỏa 1 - 2/4 tiêu chí GINA - Bệnh nhân vẫn còn triệu chứng nhẹ",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },
    "f707": {
        "name": "Hen không kiểm soát (Uncontrolled Asthma)",
        "desc": "Thỏa 3 - 4/4 tiêu chí GINA - Cần can thiệp điều chỉnh phác đồ hoặc tuân thủ",
        "category": "Đánh giá kiểm soát",
        "type": "boolean",
        "default": False
    },

    # ==========================================
    # f8xx: ĐỀ XUẤT ĐIỀU TRỊ & HÀNH ĐỘNG LÂM SÀNG (Treatment & Action Recommendations)
    # ==========================================
    "f801": {
        "name": "Đề xuất Bậc 1 (GINA Step 1)",
        "desc": "Lựa chọn ưu tiên (Track 1): Liều thấp ICS-formoterol khi cần. Lựa chọn khác (Track 2): Liều thấp ICS mỗi khi dùng SABA.",
        "category": "Khuyến nghị điều trị",
        "type": "boolean",
        "default": False
    },
    "f802": {
        "name": "Đề xuất Bậc 2 (GINA Step 2)",
        "desc": "Track 1: Liều thấp ICS-formoterol khi cần. Track 2: Duy trì liều thấp ICS hàng ngày + SABA khi cần (hoặc LTRA hàng ngày).",
        "category": "Khuyến nghị điều trị",
        "type": "boolean",
        "default": False
    },
    "f803": {
        "name": "Đề xuất Bậc 3 (GINA Step 3)",
        "desc": "Track 1 (SMART): Duy trì liều thấp ICS-formoterol + cắt cơn khi cần. Track 2: Duy trì liều thấp ICS-LABA + SABA khi cần (hoặc ICS liều trung bình).",
        "category": "Khuyến nghị điều trị",
        "type": "boolean",
        "default": False
    },
    "f804": {
        "name": "Đề xuất Bậc 4 (GINA Step 4)",
        "desc": "Track 1 (SMART): Duy trì liều trung bình ICS-formoterol + cắt cơn khi cần. Track 2: Duy trì liều trung bình/cao ICS-LABA + SABA khi cần (± LAMA).",
        "category": "Khuyến nghị điều trị",
        "type": "boolean",
        "default": False
    },
    "f805": {
        "name": "Đề xuất Bậc 5 (GINA Step 5 - Hen nặng / Khó trị)",
        "desc": "Thêm LAMA (Tiotropium), đánh giá kiểu hình Type 2 (IgE, Eosinophil, FeNO) để chỉ định thuốc sinh học (Biologics) ± OCS liều thấp ngắn hạn.",
        "category": "Khuyến nghị điều trị",
        "type": "boolean",
        "default": False
    },
    "f810": {
        "name": "Chỉ định TĂNG BẬC điều trị (Step-Up)",
        "desc": "Tăng bậc duy trì dài hạn (đánh giá lại sau 2-3 tháng) hoặc tăng ngắn hạn 1-2 tuần khi có đợt cấp/nhiễm virus",
        "category": "Hành động lâm sàng",
        "type": "boolean",
        "default": False
    },
    "f811": {
        "name": "Chỉ định GIẢM BẬC điều trị (Step-Down)",
        "desc": "Khi hen kiểm soát tốt và chức năng phổi ổn định duy trì liên tục ≥ 3 tháng (giảm liều ICS 25-50%)",
        "category": "Hành động lâm sàng",
        "type": "boolean",
        "default": False
    },
    "f812": {
        "name": "DUY TRÌ BẬC điều trị hiện tại & Tối ưu tuân thủ/kỹ thuật",
        "desc": "Hen kiểm soát một phần do kỹ thuật hít hoặc yếu tố môi trường: Huấn luyện lại cách dùng bình xịt trước khi tăng liều",
        "category": "Hành động lâm sàng",
        "type": "boolean",
        "default": False
    },
    "f820": {
        "name": "Cảnh báo CƠN HEN CẤP NẶNG / NGUY CƠ CAO (Emergency Alert)",
        "desc": "Cần xử trí cấp cứu ngay: Khí dung Salbutamol liều cao + Ipratropium, Corticoid toàn thân sớm, thở oxy hỗ trợ",
        "category": "Cảnh báo khẩn cấp",
        "type": "boolean",
        "default": False
    }
}

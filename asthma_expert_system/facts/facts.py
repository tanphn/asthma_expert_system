class Fact:
    def __init__(self, id, name, description, type, value=False):
        self.id = id
        self.name = name
        self.description = description
        self.type = type  # Triệu chứng / Xét nghiệm / Logic / Điều trị
        self.value = value


# =========================================
# Knowledge Base: Facts
# =========================================

facts = {
    # ============================
    # Triệu chứng (f101–f124)
    # ============================
    "f101": {"name": "Ho", "desc": "Ho, kéo dài hoặc từng cơn", "type": "Triệu chứng", "value": False},
    "f102": {"name": "Khò_khè", "desc": "Khò khè khi thở ra", "type": "Triệu chứng", "value": False},
    "f103": {"name": "Khó_thở", "desc": "Khó thở / thở gấp", "type": "Triệu chứng", "value": False},
    "f104": {"name": "Nặng_ngực", "desc": "Cảm giác nặng ngực", "type": "Triệu chứng", "value": False},
    "f105": {"name": "Triệu_chứng_thay_đổi", "desc": "Triệu chứng thay đổi theo thời gian hoặc yếu tố kích thích", "type": "Triệu chứng", "value": False},
    "f106": {"name": "Triệu_chứng_ban_đêm", "desc": "Triệu chứng nặng hơn về đêm", "type": "Triệu chứng", "value": False},
    "f107": {"name": "Triệu_chứng_gắng_sức", "desc": "Triệu chứng nặng khi gắng sức", "type": "Triệu chứng", "value": False},
    "f108": {"name": "Cơn_hen_cấp", "desc": "Đợt bùng phát triệu chứng cần xử trí cấp cứu", "type": "Triệu chứng", "value": False},
    "f109": {"name": "Ho_đờm", "desc": "Ho có đờm / màu đờm", "type": "Triệu chứng", "value": False},
    "f110": {"name": "Khó_thở_tăng_khi_nằm", "desc": "Triệu chứng tăng khi nằm / ăn uống", "type": "Triệu chứng", "value": False},
    "f111": {"name": "ran_ẩm", "desc": "Khó thở kèm ran ẩm", "type": "Triệu chứng", "value": False},
    "f112": {"name": "tiếng_rít_cố_định", "desc": "Tiếng rít cố định, không đáp ứng giãn phế quản", "type": "Triệu chứng", "value": False},
    "f113": {"name": "không_đáp_ứng_giãn_phế_quản", "desc": "Không cải thiện sau test giãn phế quản", "type": "Triệu chứng", "value": False},
    "f114": {"name": "ho_tăng_khi_nằm_ăn_uống", "desc": "Ho/khó thở tăng khi nằm hoặc ăn uống", "type": "Triệu chứng", "value": False},
    "f115": {"name": "ho_đờm_mủ_nhiều_năm", "desc": "Ho khạc đờm mủ kéo dài nhiều năm", "type": "Triệu chứng", "value": False},

    # Triệu chứng không kiểm soát
    "f116": {"name": "uncontrolled_daytime", "desc": "Triệu chứng ban ngày thường xuyên", "type": "Triệu chứng không kiểm soát", "value": False},
    "f117": {"name": "uncontrolled_night", "desc": "Tỉnh giấc ban đêm", "type": "Triệu chứng không kiểm soát", "value": False},
    "f118": {"name": "uncontrolled_relief_use", "desc": "Tăng dùng thuốc cắt cơn", "type": "Triệu chứng không kiểm soát", "value": False},

    # Triệu chứng đánh giá mức độ
    "f119": {"name": "stable_3_months", "desc": "Kiểm soát ổn định ≥3 tháng", "type": "Triệu chứng kiểm soát", "value": False},
    "f120": {"name": "freq_day_symptoms", "desc": "Số ngày/tuần có triệu chứng", "type": "Triệu chứng", "value": 0},
    "f121": {"name": "freq_night_symptoms", "desc": "Số lần/tuần triệu chứng về đêm", "type": "Triệu chứng", "value": 0},
    "f122": {"name": "activity_limitation", "desc": "Giới hạn hoạt động (0=không, 1=nhẹ, 2=nhiều)", "type": "Triệu chứng", "value": 0},
    "f123": {"name": "SABA_use_per_week", "desc": "Sử dụng SABA/tuần", "type": "Triệu chứng", "value": 0},
    "f124": {"name": "exacerbation_last_year", "desc": "Số đợt cấp năm qua", "type": "Triệu chứng", "value": 0},

    # ============================
    # Xét nghiệm (f201–f209)
    # ============================
    "f201": {"name": "FEV1_FVC_thấp", "desc": "Tỷ lệ FEV1/FVC < bình thường", "type": "Xét nghiệm", "value": False},
    "f202": {"name": "FEV1_tăng_≥12%", "desc": "FEV1 tăng ≥12% & ≥200 mL sau giãn", "type": "Xét nghiệm", "value": False},
    "f203": {"name": "PEF_biến_thiên_>10%", "desc": "Lưu lượng đỉnh biến thiên >10%", "type": "Xét nghiệm", "value": False},
    "f204": {"name": "Test_hồi_phục_dương_tính", "desc": "Test hồi phục phế quản dương tính", "type": "Xét nghiệm", "value": False},
    "f205": {"name": "Test_kích_thích_dương", "desc": "Test kích thích phế quản dương tính", "type": "Xét nghiệm", "value": False},
    "f206": {"name": "FEV1_tỷ_lệ_bình_thường", "desc": "FEV1/FVC bình thường", "type": "Xét nghiệm", "value": False},
    "f207": {"name": "PEF_ổn_định", "desc": "Lưu lượng đỉnh ổn định", "type": "Xét nghiệm", "value": False},
    "f208": {"name": "FEV1_percent", "desc": "FEV1 % so với lý thuyết", "type": "Xét nghiệm", "value": 0},
    "f209": {"name": "PEF_variability_percent", "desc": "Biến thiên lưu lượng đỉnh (%)", "type": "Xét nghiệm", "value": 0},

    # ============================
    # Thuốc (f301–f317)
    # ============================
    "f301": {"name": "Dùng_ICS", "desc": "Dùng Corticoid dạng hít", "type": "Thuốc", "value": False},
    "f302": {"name": "Dùng_LABA", "desc": "Dùng Long-acting beta-2 agonist", "type": "Thuốc", "value": False},
    "f303": {"name": "Dùng_SABA", "desc": "Dùng Short-acting beta-2 agonist", "type": "Thuốc", "value": False},
    "f304": {"name": "Dùng_LTRA", "desc": "Dùng leukotriene receptor antagonist", "type": "Thuốc", "value": False},
    "f305": {"name": "Dùng_SLIT", "desc": "Dùng SLIT mạt bụi nhà", "type": "Thuốc", "value": False},
    "f306": {"name": "Dùng_OCS", "desc": "Dùng corticosteroid toàn thân", "type": "Thuốc", "value": False},
    "f307": {"name": "Tuân_thuần_đúng", "desc": "Tuân thủ thuốc hằng ngày", "type": "Thuốc", "value": False},
    "f310": {"name": "current_step", "desc": "Step điều trị hiện tại", "type": "Thuốc", "value": 0},
    "f317": {"name": "suggestion", "desc": "Gợi ý Step điều trị", "type": "Thuốc", "value": ""},

    # ============================
    # Nguy cơ (f401–f407, f414–f416)
    # ============================
    "f401": {"name": "Hút_thuốc", "desc": "Tiền sử hút thuốc", "type": "Nguy cơ", "value": False},
    "f402": {"name": "Dị_nguyên", "desc": "Tiếp xúc bụi, phấn hoa, lông thú", "type": "Nguy cơ", "value": False},
    "f403": {"name": "Thời_tiết", "desc": "Thay đổi thời tiết / lạnh / nóng", "type": "Nguy cơ", "value": False},
    "f404": {"name": "Tiền_sử_COPD", "desc": "Tiền sử COPD", "type": "Nguy cơ", "value": False},
    "f405": {"name": "Tiền_sử_Suy_tim", "desc": "Tiền sử suy tim trái / THA", "type": "Nguy cơ", "value": False},
    "f406": {"name": "Tuổi", "desc": "Tuổi bệnh nhân", "type": "Nguy cơ", "value": 0},
    "f407": {"name": "Giới_tính", "desc": "Nam / Nữ", "type": "Nguy cơ", "value": ""},

    "f414": {"name": "low_adherence", "desc": "Không tuân thủ thuốc", "type": "Nguy cơ", "value": False},
    "f415": {"name": "incorrect_technique", "desc": "Sai kỹ thuật xịt", "type": "Nguy cơ", "value": False},
    "f416": {"name": "eosinophil_high", "desc": "Tăng bạch cầu ái toan", "type": "Nguy cơ", "value": False},

    # ============================
    # Logic (f501–f512)
    # ============================
    "f501": {"name": "≥2_triệu_chứng", "desc": "Có ≥2 triệu chứng chính", "type": "Logic", "value": False},
    "f502": {"name": "variable_airflow_limitation", "desc": "Rối loạn thông khí tắc nghẽn biến đổi", "type": "Logic", "value": False},
    "f503": {"name": "suspected_asthma", "desc": "Nghi ngờ hen phế quản", "type": "Logic", "value": False},
    "f504": {"name": "confirmed_asthma", "desc": "Chẩn đoán HPQ chắc chắn", "type": "Logic", "value": False},
    "f505": {"name": "asthma_controlled", "desc": "Hen kiểm soát tốt", "type": "Logic", "value": False},
    "f506": {"name": "asthma_uncontrolled", "desc": "Hen không kiểm soát", "type": "Logic", "value": False},
    "f507": {"name": "step_up", "desc": "Tăng bậc điều trị", "type": "Hành động", "value": False},
    "f508": {"name": "step_down", "desc": "Giảm bậc điều trị", "type": "Hành động", "value": False},
    "f509": {"name": "COPD", "desc": "COPD", "type": "Phân biệt chẩn đoán", "value": False},
    "f510": {"name": "Heart_failure_left", "desc": "Suy tim trái", "type": "Phân biệt chẩn đoán", "value": False},
    "f511": {"name": "Airway_obstruction", "desc": "Hẹp/U/Dị vật khí – PQ", "type": "Phân biệt chẩn đoán", "value": False},
    "f512": {"name": "GERD_or_fistula", "desc": "GERD hoặc rò khí – thực quản", "type": "Phân biệt chẩn đoán", "value": False},
    "f513": {"name": "Bronchiectasis", "desc": "Giãn phế quản", "type": "Phân biệt chẩn đoán", "value": False},

    # ============================
    # Kết luận (f601–f607)
    # ============================
    "f601": {"name": "mild_intermittent", "desc": "Hen gián đoạn", "type": "Kết luận", "value": False},
    "f602": {"name": "mild_persistent", "desc": "Hen dai dẳng nhẹ", "type": "Kết luận", "value": False},
    "f603": {"name": "moderate_persistent", "desc": "Hen dai dẳng trung bình", "type": "Kết luận", "value": False},
    "f604": {"name": "severe_persistent", "desc": "Hen dai dẳng nặng", "type": "Kết luận", "value": False},
    "f605": {"name": "Poor_adherence", "desc": "Mất kiểm soát do không tuân thủ", "type": "Kết luận", "value": False},
    "f606": {"name": "Incorrect_inhaler_technique", "desc": "Mất kiểm soát do sai kỹ thuật hít", "type": "Kết luận", "value": False},
    "f607": {"name": "Environmental_trigger", "desc": "Mất kiểm soát do yếu tố kích phát", "type": "Kết luận", "value": False}
}


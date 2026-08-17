# asthma_expert_system/engine/certainty.py
"""
Hệ thống tính toán Hệ số Tin cậy (Certainty Factors - CF) và Ma trận Điểm số Chẩn đoán Phân biệt.
Hỗ trợ tổng hợp độ bất định theo mô hình MYCIN và xếp hạng khả năng mắc bệnh.
"""

from typing import Dict, Any, List
from engine.wm import WorkingMemory

def combine_cf(cf1: float, cf2: float) -> float:
    """
    Công thức kết hợp hai hệ số tin cậy độc lập khẳng định cùng một giả thuyết (MYCIN model):
    CF_comb = CF1 + CF2 * (1 - CF1)  [khi cả hai cùng dương]
    """
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1.0 - cf1)
    elif cf1 <= 0 and cf2 <= 0:
        return cf1 + cf2 * (1.0 + cf1)
    else:
        return (cf1 + cf2) / (1.0 - min(abs(cf1), abs(cf2)))

class CertaintyEngine:
    """
    Bộ tính toán độ tin cậy và xếp hạng chẩn đoán phân biệt đa tiêu chí.
    """
    def __init__(self, wm: WorkingMemory):
        self.wm = wm

    def evaluate_differentials(self) -> List[Dict[str, Any]]:
        """
        Tính toán điểm số xác suất phân biệt cho từng bệnh lý hô hấp & tim mạch thường gặp.
        Trả về danh sách đã sắp xếp từ cao đến thấp theo % xác suất.
        """
        wm = self.wm
        results = []

        # ----------------------------------------------------
        # 1. HEN PHẾ QUẢN (ASTHMA)
        # ----------------------------------------------------
        asthma_score = 0.0
        asthma_max = 100.0
        reasons_asthma = []

        # Triệu chứng chính (tối đa 30đ)
        symptom_count = sum(1 for f in ["f101", "f102", "f103", "f104"] if wm.get(f))
        if symptom_count >= 3:
            asthma_score += 30
            reasons_asthma.append("Đầy đủ các triệu chứng kinh điển (Ho, khò khè, khó thở, nặng ngực)")
        elif symptom_count >= 2:
            asthma_score += 20
            reasons_asthma.append("Có ≥ 2 triệu chứng hô hấp chính")
        elif symptom_count == 1:
            asthma_score += 8

        # Đặc điểm dao động & triggers (tối đa 25đ)
        if wm.get("f105"):
            asthma_score += 10
            reasons_asthma.append("Triệu chứng thay đổi theo thời gian/cường độ")
        if wm.get("f106"):
            asthma_score += 10
            reasons_asthma.append("Nặng hơn về đêm/sáng sớm")
        if wm.get("f107") or wm.get("f108"):
            asthma_score += 5
            reasons_asthma.append("Khởi phát khi gắng sức hoặc sau nhiễm virus")

        # Thăm dò chức năng thông khí (tối đa 35đ)
        if wm.get("f207") or (wm.get("f202") is not None and wm.get("f202") >= 12):
            asthma_score += 35
            reasons_asthma.append("Test hồi phục phế quản dương tính mạnh (ΔFEV1 ≥ 12%)")
        elif wm.get("f204") is not None and wm.get("f204") > 10:
            asthma_score += 25
            reasons_asthma.append("Dao động lưu lượng đỉnh PEF trong ngày > 10%")
        elif wm.get("f206"):
            asthma_score += 30
            reasons_asthma.append("Test kích thích phế quản dương tính")

        # Cơ địa dị ứng / Dấu ấn sinh học (tối đa 10đ)
        if wm.get("f003") or wm.get("f004"):
            asthma_score += 5
            reasons_asthma.append("Tiền sử cá nhân/gia đình có cơ địa dị ứng (Atopy)")
        if (wm.get("f208") is not None and wm.get("f208") >= 35) or (wm.get("f209") is not None and wm.get("f209") >= 300) or wm.get("f210"):
            asthma_score += 5
            reasons_asthma.append("Dấu ấn viêm Type 2 (FeNO/Eosinophil/IgE) tăng cao")

        asthma_pct = min(100.0, max(0.0, (asthma_score / asthma_max) * 100))
        results.append({
            "code": "ASTHMA",
            "name": "Hen Phế Quản (Asthma)",
            "fact_id": "f504",
            "probability": round(asthma_pct, 1),
            "level": "Rất cao" if asthma_pct >= 80 else ("Khá cao" if asthma_pct >= 60 else ("Nghi ngờ" if asthma_pct >= 40 else "Thấp")),
            "key_factors": reasons_asthma,
            "color": "#10B981" if asthma_pct >= 60 else "#3B82F6"
        })

        # ----------------------------------------------------
        # 2. BỆNH PHỔI TẮC NGHẼN MẠN TÍNH (COPD)
        # ----------------------------------------------------
        copd_score = 0.0
        reasons_copd = []
        if wm.get("f401"):
            copd_score += 35
            reasons_copd.append("Tiền sử hút thuốc lá/thuốc lào ≥ 10 gói-năm")
        if wm.get("f404"):
            copd_score += 30
            reasons_copd.append("Đã được chẩn đoán COPD trước đây")
        if wm.get("f001") is not None and wm.get("f001") >= 45:
            copd_score += 15
            reasons_copd.append("Độ tuổi khởi phát > 40-45 tuổi")
        if wm.get("f113") or wm.get("f109"):
            copd_score += 15
            reasons_copd.append("Khó thở gắng sức tiến triển liên tục / Ho đờm mạn tính")
        if wm.get("f201") is not None and wm.get("f201") < 0.70 and not wm.get("f207"):
            copd_score += 25
            reasons_copd.append("Tắc nghẽn thông khí cố định sau test giãn phế quản (FEV1/FVC < 0.70)")

        copd_pct = min(100.0, copd_score)
        results.append({
            "code": "COPD",
            "name": "Bệnh Phổi Tắc Nghẽn Mạn Tính (COPD)",
            "fact_id": "f509",
            "probability": round(copd_pct, 1),
            "level": "Rất cao" if copd_pct >= 80 else ("Khá cao" if copd_pct >= 60 else ("Nghi ngờ" if copd_pct >= 40 else "Thấp")),
            "key_factors": reasons_copd,
            "color": "#F59E0B"
        })

        # ----------------------------------------------------
        # 3. HỘI CHỨNG CHỒNG LẤP HEN - COPD (ACO)
        # ----------------------------------------------------
        aco_score = 0.0
        reasons_aco = []
        if (wm.get("f401") or wm.get("f404")) and (wm.get("f003") or wm.get("f105") or wm.get("f106")):
            aco_score += 40
            reasons_aco.append("Vừa có yếu tố nguy cơ khói thuốc vừa có cơ địa dị ứng/biến đổi dao động")
        if (wm.get("f201") is not None and wm.get("f201") < 0.70) and (wm.get("f207") or (wm.get("f202") is not None and wm.get("f202") >= 12)):
            aco_score += 45
            reasons_aco.append("Tắc nghẽn đường thở cố định (FEV1/FVC < 0.70) nhưng FEV1 vẫn đáp ứng giãn > 12%")
        if wm.get("f504") and wm.get("f509"):
            aco_score += 20

        aco_pct = min(100.0, aco_score)
        results.append({
            "code": "ACO",
            "name": "Hội chứng Chồng lấp Hen - COPD (ACO)",
            "fact_id": "f514",
            "probability": round(aco_pct, 1),
            "level": "Rất cao" if aco_pct >= 75 else ("Khá cao" if aco_pct >= 50 else ("Nghi ngờ" if aco_pct >= 30 else "Thấp")),
            "key_factors": reasons_aco,
            "color": "#EC4899"
        })

        # ----------------------------------------------------
        # 4. SUY TIM TRÁI / HEN TIM (CARDIAC ASTHMA)
        # ----------------------------------------------------
        cardiac_score = 0.0
        reasons_cardiac = []
        if wm.get("f405"):
            cardiac_score += 40
            reasons_cardiac.append("Tiền sử Tăng huyết áp / Bệnh tim mạch / Suy tim")
        if wm.get("f110"):
            cardiac_score += 35
            reasons_cardiac.append("Khám phổi phát hiện Ran ẩm / Ran nổ 2 đáy phổi")
        if wm.get("f106") or wm.get("f112"):
            cardiac_score += 15
            reasons_cardiac.append("Khó thở kịch phát khi nằm đầu thấp (Orthopnea) / Ban đêm")

        cardiac_pct = min(100.0, cardiac_score)
        results.append({
            "code": "CARDIAC_ASTHMA",
            "name": "Suy Tim Trái / Hen Tim (Cardiac Asthma)",
            "fact_id": "f510",
            "probability": round(cardiac_pct, 1),
            "level": "Rất cao" if cardiac_pct >= 75 else ("Khá cao" if cardiac_pct >= 50 else ("Nghi ngờ" if cardiac_pct >= 30 else "Thấp")),
            "key_factors": reasons_cardiac,
            "color": "#EF4444"
        })

        # ----------------------------------------------------
        # 5. GIÃN PHẾ QUẢN (BRONCHIECTASIS)
        # ----------------------------------------------------
        bronch_score = 0.0
        reasons_bronch = []
        if wm.get("f109"):
            bronch_score += 55
            reasons_bronch.append("Ho khạc đờm mủ đục số lượng nhiều kéo dài nhiều năm")
        if wm.get("f101") and wm.get("f108"):
            bronch_score += 25
            reasons_bronch.append("Nhiều đợt nhiễm trùng phế quản phổi tái diễn")

        bronch_pct = min(100.0, bronch_score)
        results.append({
            "code": "BRONCHIECTASIS",
            "name": "Giãn Phế Quản (Bronchiectasis)",
            "fact_id": "f513",
            "probability": round(bronch_pct, 1),
            "level": "Khá cao" if bronch_pct >= 50 else ("Nghi ngờ" if bronch_pct >= 30 else "Thấp"),
            "key_factors": reasons_bronch,
            "color": "#8B5CF6"
        })

        # ----------------------------------------------------
        # 6. TRÀO NGƯỢC DẠ DÀY THỰC QUẢN (GERD)
        # ----------------------------------------------------
        gerd_score = 0.0
        reasons_gerd = []
        if wm.get("f112"):
            gerd_score += 50
            reasons_gerd.append("Ho/khó thở tăng khi nằm ngửa, sau khi ăn no, ợ nóng")
        if wm.get("f101") and not wm.get("f502"):
            gerd_score += 25
            reasons_gerd.append("Ho khan kéo dài không kèm rối loạn thông khí trên hô hấp ký")

        gerd_pct = min(100.0, gerd_score)
        results.append({
            "code": "GERD",
            "name": "Ho mạn tính do Trào ngược (GERD)",
            "fact_id": "f512",
            "probability": round(gerd_pct, 1),
            "level": "Khá cao" if gerd_pct >= 50 else ("Nghi ngờ" if gerd_pct >= 30 else "Thấp"),
            "key_factors": reasons_gerd,
            "color": "#6366F1"
        })

        # ----------------------------------------------------
        # 7. HẸP KHÍ QUẢN / RỐI LOẠN DÂY THANH (VCD)
        # ----------------------------------------------------
        vcd_score = 0.0
        reasons_vcd = []
        if wm.get("f111"):
            vcd_score += 55
            reasons_vcd.append("Tiếng rít thanh/khí quản cố định (Stridor) thì hít vào")
        if wm.get("f103") and not wm.get("f207"):
            vcd_score += 25
            reasons_vcd.append("Khó thở không đáp ứng với thuốc giãn phế quản dạng xịt")

        vcd_pct = min(100.0, vcd_score)
        results.append({
            "code": "VCD_OBSTRUCTION",
            "name": "Hẹp đường thở / Rối loạn dây thanh (VCD)",
            "fact_id": "f511",
            "probability": round(vcd_pct, 1),
            "level": "Khá cao" if vcd_pct >= 50 else ("Nghi ngờ" if vcd_pct >= 30 else "Thấp"),
            "key_factors": reasons_vcd,
            "color": "#06B6D4"
        })

        # Sắp xếp kết quả theo xác suất giảm dần
        results.sort(key=lambda x: x["probability"], reverse=True)
        return results

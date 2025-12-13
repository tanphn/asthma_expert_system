# modules/initial_assessment.py
from facts.facts import facts
from engine.wm import WorkingMemory
from utils.helpers import input_boolean, input_float

def module_symptoms(wm: WorkingMemory):
    """CHỨC NĂNG 1 - Thu thập triệu chứng & nghi ngờ hen (L1)"""
    print("\n--- MODULE 1: Triệu chứng (Symptom collection) ---")

    # ====== Thu thập triệu chứng ======
    wm.set("f101", input_boolean("Ho, kéo dài hoặc từng cơn?"))
    wm.set("f102", input_boolean("Khò khè khi thở ra?"))
    wm.set("f103", input_boolean("Khó thở / thở gấp?"))
    wm.set("f104", input_boolean("Cảm giác nặng ngực?"))
    wm.set("f105", input_boolean("Triệu chứng thay đổi theo thời gian / có triggers?"))
    wm.set("f106", input_boolean("Triệu chứng nặng hơn về đêm?"))
    wm.set("f107", input_boolean("Triệu chứng nặng khi gắng sức?"))

    # ====== L1: Kiểm tra nghi ngờ hen ======
    main_count = sum(1 for f in ["f101", "f102", "f103", "f104"] if wm.get(f))

    if main_count >= 2 and (wm.get("f105") or wm.get("f106") or wm.get("f107")):
        wm.set("f501", True)
        wm.set("f503", True)
        print("✔ L1 thỏa: nghi ngờ hen (f501, f503 = True)")
        return True

    # ====== ELSE: Không đủ triệu chứng L1 → Gọi khối L5-x ======
    print("✖ L1 không thỏa: không đủ yếu tố lâm sàng nghi ngờ hen")
    print("✖ Không đủ thông tin để kết luận hen phế quản → Có thể là bệnh khác, kiểm tra L5-x")

    # ----------- L5-x: Phân biệt các bệnh khác -----------
    wm.set("f401", input_boolean("Tiền sử hút thuốc?"))
    wm.set("f404", input_boolean("Tiền sử COPD?"))
    wm.set("f405", input_boolean("Tiền sử suy tim trái / THA?"))
    wm.set("f115", input_boolean("Ho khạc đờm mủ nhiều năm?"))
    wm.set("f111", input_boolean("Có ran ẩm?"))
    wm.set("f103", input_boolean("Khó thở / thở gấp?"))
    wm.set("f112", input_boolean("Tiếng rít cố định?"))
    wm.set("f113", input_boolean("Không đáp ứng giãn phế quản?"))
    wm.set("f114", input_boolean("Ho/khó thở tăng khi nằm/ăn uống?"))

    # ----- Rule L5-x -----
    if wm.get("f401") and wm.get("f115") and wm.get("f201") and not wm.get("f204"):
        wm.set("f509", True)
        print("🚨 Nghi COPD")

    if wm.get("f103") and wm.get("f111") and wm.get("f405"):
        wm.set("f510", True)
        print("🚨 Nghi suy tim trái")

    if wm.get("f103") and wm.get("f112") and wm.get("f113"):
        wm.set("f511", True)
        print("🚨 Nghi hẹp/ứ đọng/dị vật phế quản")

    if wm.get("f114"):
        wm.set("f512", True)
        print("🚨 Nghi GERD hoặc rò khí–thực quản")

    if wm.get("f115"):
        wm.set("f513", True)
        print("🚨 Nghi giãn phế quản")

    # Sau khi chạy L5-x → trả về False để dừng L1
    return False


def module_tests(wm: WorkingMemory):
    """CHỨC NĂNG 2 - Thu thập xét nghiệm & xác định (L2, L3, L4)"""
    print("\n--- MODULE 2: Xét nghiệm (Spirometry / Tests) ---")
    # nhập các chỉ số
    fev1_fvc = input_float("Nhập FEV1/FVC (ví dụ 0.74) (để trống nếu không có)", allow_empty=True)
    if fev1_fvc is not None and fev1_fvc < 0.75:
        wm.set("f201", True)

    fev1_increase_pct = input_float("Nhập % tăng FEV1 sau giãn (ví dụ 12) (để trống nếu không có)", allow_empty=True)
    if fev1_increase_pct is not None and fev1_increase_pct >= 12:
        wm.set("f202", True)

    pef_var = input_float("Nhập biến thiên PEF (%) (ví dụ 10) (để trống nếu không có)", allow_empty=True)
    if pef_var is not None and pef_var > 10:
        wm.set("f203", True)

    wm.set("f204", input_boolean("Test hồi phục phế quản dương tính?"))
    wm.set("f205", input_boolean("Test kích thích phế quản dương tính?"))

    # Thiết lập L2
    if wm.get("f201") or wm.get("f202") or wm.get("f203"):
        wm.set("f502", True)
        print("✔ L2 thỏa: rối loạn thông khí tắc nghẽn biến đổi (f502=True)")
    else:
        print("⚠ L2 không thỏa: chưa có bằng chứng xét nghiệm rõ rệt")

    # L3: L1 và L2 -> chẩn đoán xác định
    if wm.get("f501") and wm.get("f502"):
        wm.set("f504", True)
        print("✔ L3 thỏa: chẩn đoán hen xác định (f504=True)")

    # L4: nếu đang dùng ICS/LABA + còn triệu chứng + test dương
    wm.set("f301", input_boolean("Đang dùng ICS?"))
    wm.set("f302", input_boolean("Đang dùng LABA?"))
    if (wm.get("f301") or wm.get("f302")) and any(wm.get(f) for f in ["f101","f102","f103","f104"]) and (wm.get("f204") or wm.get("f205")):
        wm.set("f504", True)
        print("✔ L4 thỏa: điều trị nhưng còn triệu chứng + test dương -> xác định hen (f504=True)")

def module_severity(wm: WorkingMemory):
    """CHỨC NĂNG 3 - Đánh giá mức độ nặng (L8-L11)"""
    print("\n--- MODULE 3: Đánh giá mức độ nặng (Severity) ---")
    # thu thập input cần cho severity
    wm.set("f120", input_float("Số ngày/tuần có triệu chứng (freq_day_symptoms) (0-7)"))
    wm.set("f121", input_float("Số lần/tuần triệu chứng ban đêm (freq_night_symptoms)"))
    wm.set("f122", input_float("Giới hạn hoạt động (0=không,1=nhẹ,2=nhiều)"))
    wm.set("f123", input_float("Số lần dùng SABA/tuần (SABA_use_per_week)"))
    wm.set("f208", input_float("FEV1_percent (%) nếu có (ví dụ 85) (để trống nhập 999) ", allow_empty=True) or 999)
    wm.set("f209", input_float("PEF_variability_percent (%) nếu có (ví dụ 15) (để trống nhập 999) ", allow_empty=True) or 999)

    f120 = wm.get("f120")
    f121 = wm.get("f121")
    f122 = wm.get("f122")
    f123 = wm.get("f123")
    f208 = wm.get("f208")
    f209 = wm.get("f209")

    # Clear previous severity facts
    for sid in ["f601","f602","f603","f604"]:
        if sid in facts:
            wm.set(sid, False)

    # L8: Mild intermittent
    cond_L8 = (f120 <= 2 and f121 <= 2 and f122 == 0 and f123 <= 2 and (f208 >= 80 or f209 < 20))
    # L9: Mild persistent
    cond_L9 = ((2 < f120 < 7) or (2 < f121 < 7) or (f123 > 2 and f208 >= 80))
    # L10: Moderate persistent
    cond_L10 = (f120 >= 7 or f121 >= 7 or f122 == 1 or (60 <= f208 < 80))
    # L11: Severe persistent
    cond_L11 = (f122 == 2 or f208 < 60 or f209 >= 30)

    if cond_L11:
        wm.set("f604", True)
        print("✔ L11: Hen dai dẳng nặng (f604=True)")
        return "severe"
    if cond_L10:
        wm.set("f603", True)
        print("✔ L10: Hen dai dẳng trung bình (f603=True)")
        return "moderate"
    if cond_L9:
        wm.set("f602", True)
        print("✔ L9: Hen dai dẳng nhẹ (f602=True)")
        return "mild_persistent"
    if cond_L8:
        wm.set("f601", True)
        print("✔ L8: Hen gián đoạn (mild intermittent) (f601=True)")
        return "intermittent"
    print("⚠ Không đủ dữ liệu để phân loại mức độ nặng (thiếu hoặc mâu thuẫn dữ liệu)")
    return None

def module_conclusion(wm: WorkingMemory):
    """Tổng kết kết quả chẩn đoán trước khi chuyển sang main()"""
    print("\n===== KẾT LUẬN CHẨN ĐOÁN =====")

    # 1. Kiểm tra nghi ngờ hen
    suspected = wm.get("f501")

    # 2. Kiểm tra chẩn đoán xác định
    confirmed = wm.get("f504")

    # 3. Kiểm tra mức độ nặng
    severity = None
    if wm.get("f604"):
        severity = "Hen dai dẳng nặng"
    elif wm.get("f603"):
        severity = "Hen dai dẳng trung bình"
    elif wm.get("f602"):
        severity = "Hen dai dẳng nhẹ"
    elif wm.get("f601"):
        severity = "Hen gián đoạn"

    # --- In kết luận ---
    if not suspected:
        print("❌ Không đủ tiêu chuẩn nghi ngờ hen (L1 không thỏa).")
        print("➡ Không thể chẩn đoán hen.")
        return

    print("✔ Nghi ngờ hen (L1 thỏa).")

    if confirmed:
        print("✔ Chẩn đoán: HEN PHẾ QUẢN XÁC ĐỊNH (L3 hoặc L4).")
    else:
        print("⚠ Chưa đủ bằng chứng xét nghiệm để kết luận xác định hen (L2 không thỏa).")
        print("➡ Chẩn đoán tạm thời: **Nghi ngờ hen, cần làm thêm xét nghiệm.**")
        return

    # Nếu đã xác định hen → đánh giá mức độ nặng
    if severity:
        print(f"🌡 Mức độ nặng: **{severity}**")
    else:
        print("⚠ Chưa đủ dữ liệu để phân loại mức độ nặng (L8-L11).")

    print("===== KẾT THÚC =====\n")
def run_initial_diagnosis(wm: WorkingMemory):
    print("\n===== KHÁM LẦN ĐẦU =====")

    # 1. Thu thập triệu chứng
    if not module_symptoms(wm):
        module_conclusion(wm)
        return

    # 2. Thu thập xét nghiệm
    module_tests(wm)

    # 3. Đánh giá mức độ nặng
    module_severity(wm)

    # 4. Kết luận
    module_conclusion(wm)
    print("\n🎉 HOÀN THÀNH KHÁM LẦN ĐẦU\n")
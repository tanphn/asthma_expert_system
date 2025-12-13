# asthma_expert_system/main.py
from facts.facts import facts
from engine.wm import WorkingMemory
from utils.helpers import input_boolean, input_float
from modules.initial_assessment import run_initial_diagnosis
from modules.follow_up import run_follow_up

# def module_symptoms(wm: WorkingMemory):
#     """CHỨC NĂNG 1 - Thu thập triệu chứng & nghi ngờ hen (L1)"""
#     print("\n--- MODULE 1: Triệu chứng (Symptom collection) ---")
#     wm.set("f101", input_boolean("Ho, kéo dài hoặc từng cơn?"))
#     wm.set("f102", input_boolean("Khò khè khi thở ra?"))
#     wm.set("f103", input_boolean("Khó thở / thở gấp?"))
#     wm.set("f104", input_boolean("Cảm giác nặng ngực?"))
#     wm.set("f105", input_boolean("Triệu chứng thay đổi theo thời gian / có triggers?"))
#     wm.set("f106", input_boolean("Triệu chứng nặng hơn về đêm?"))
#     wm.set("f107", input_boolean("Triệu chứng nặng khi gắng sức?"))

#     # L1: >=2 triệu chứng chính AND (f105 OR f106 OR f107)
#     main_count = sum(1 for f in ["f101","f102","f103","f104"] if wm.get(f))
#     if main_count >= 2 and (wm.get("f105") or wm.get("f106") or wm.get("f107")):
#         wm.set("f501", True)
#         wm.set("f503", True)
#         print("✔ L1 thỏa: nghi ngờ hen (f501, f503 = True)")
#         return True
#     else:
#         print("✖ L1 không thỏa: không đủ yếu tố lâm sàng nghi ngờ hen")
#         return False

# def module_tests(wm: WorkingMemory):
#     """CHỨC NĂNG 2 - Thu thập xét nghiệm & xác định (L2, L3, L4)"""
#     print("\n--- MODULE 2: Xét nghiệm (Spirometry / Tests) ---")
#     # nhập các chỉ số
#     fev1_fvc = input_float("Nhập FEV1/FVC (ví dụ 0.74) (để trống nếu không có)", allow_empty=True)
#     if fev1_fvc is not None and fev1_fvc < 0.75:
#         wm.set("f201", True)

#     fev1_increase_pct = input_float("Nhập % tăng FEV1 sau giãn (ví dụ 12) (để trống nếu không có)", allow_empty=True)
#     if fev1_increase_pct is not None and fev1_increase_pct >= 12:
#         wm.set("f202", True)

#     pef_var = input_float("Nhập biến thiên PEF (%) (ví dụ 10) (để trống nếu không có)", allow_empty=True)
#     if pef_var is not None and pef_var > 10:
#         wm.set("f203", True)

#     wm.set("f204", input_boolean("Test hồi phục phế quản dương tính?"))
#     wm.set("f205", input_boolean("Test kích thích phế quản dương tính?"))

#     # Thiết lập L2
#     if wm.get("f201") or wm.get("f202") or wm.get("f203"):
#         wm.set("f502", True)
#         print("✔ L2 thỏa: rối loạn thông khí tắc nghẽn biến đổi (f502=True)")
#     else:
#         print("⚠ L2 không thỏa: chưa có bằng chứng xét nghiệm rõ rệt")

#     # L3: L1 và L2 -> chẩn đoán xác định
#     if wm.get("f501") and wm.get("f502"):
#         wm.set("f504", True)
#         print("✔ L3 thỏa: chẩn đoán hen xác định (f504=True)")

#     # L4: nếu đang dùng ICS/LABA + còn triệu chứng + test dương
#     wm.set("f301", input_boolean("Đang dùng ICS?"))
#     wm.set("f302", input_boolean("Đang dùng LABA?"))
#     if (wm.get("f301") or wm.get("f302")) and any(wm.get(f) for f in ["f101","f102","f103","f104"]) and (wm.get("f204") or wm.get("f205")):
#         wm.set("f504", True)
#         print("✔ L4 thỏa: điều trị nhưng còn triệu chứng + test dương -> xác định hen (f504=True)")

# def module_severity(wm: WorkingMemory):
#     """CHỨC NĂNG 3 - Đánh giá mức độ nặng (L8-L11)"""
#     print("\n--- MODULE 3: Đánh giá mức độ nặng (Severity) ---")
#     # thu thập input cần cho severity
#     wm.set("f120", input_float("Số ngày/tuần có triệu chứng (freq_day_symptoms) (0-7)"))
#     wm.set("f121", input_float("Số lần/tuần triệu chứng ban đêm (freq_night_symptoms)"))
#     wm.set("f122", input_float("Giới hạn hoạt động (0=không,1=nhẹ,2=nhiều)"))
#     wm.set("f123", input_float("Số lần dùng SABA/tuần (SABA_use_per_week)"))
#     wm.set("f208", input_float("FEV1_percent (%) nếu có (ví dụ 85) (để trống nhập 999) ", allow_empty=True) or 999)
#     wm.set("f209", input_float("PEF_variability_percent (%) nếu có (ví dụ 15) (để trống nhập 999) ", allow_empty=True) or 999)

#     f120 = wm.get("f120")
#     f121 = wm.get("f121")
#     f122 = wm.get("f122")
#     f123 = wm.get("f123")
#     f208 = wm.get("f208")
#     f209 = wm.get("f209")

#     # Clear previous severity facts
#     for sid in ["f601","f602","f603","f604"]:
#         if sid in facts:
#             wm.set(sid, False)

#     # L8: Mild intermittent
#     cond_L8 = (f120 <= 2 and f121 <= 2 and f122 == 0 and f123 <= 2 and (f208 >= 80 or f209 < 20))
#     # L9: Mild persistent
#     cond_L9 = ((2 < f120 < 7) or (2 < f121 < 7) or (f123 > 2 and f208 >= 80))
#     # L10: Moderate persistent
#     cond_L10 = (f120 >= 7 or f121 >= 7 or f122 == 1 or (60 <= f208 < 80))
#     # L11: Severe persistent
#     cond_L11 = (f122 == 2 or f208 < 60 or f209 >= 30)

#     if cond_L11:
#         wm.set("f604", True)
#         print("✔ L11: Hen dai dẳng nặng (f604=True)")
#         return "severe"
#     if cond_L10:
#         wm.set("f603", True)
#         print("✔ L10: Hen dai dẳng trung bình (f603=True)")
#         return "moderate"
#     if cond_L9:
#         wm.set("f602", True)
#         print("✔ L9: Hen dai dẳng nhẹ (f602=True)")
#         return "mild_persistent"
#     if cond_L8:
#         wm.set("f601", True)
#         print("✔ L8: Hen gián đoạn (mild intermittent) (f601=True)")
#         return "intermittent"
#     print("⚠ Không đủ dữ liệu để phân loại mức độ nặng (thiếu hoặc mâu thuẫn dữ liệu)")
#     return None

# def module_control_and_treatment(wm: WorkingMemory):
#     """CHỨC NĂNG 4 - Đánh giá kiểm soát & Gợi ý tăng/giảm bậc (L6,L7,L12-L21)"""
#     print("\n--- MODULE 4: Kiểm soát & Gợi ý điều trị ---")
#     # kiểm soát: f116,f117,f118,f119
#     wm.set("f116", input_boolean("Triệu chứng ban ngày thường xuyên? (uncontrolled_daytime)"))
#     wm.set("f117", input_boolean("Tỉnh giấc ban đêm? (uncontrolled_night)"))
#     wm.set("f118", input_boolean("Tăng dùng thuốc cắt cơn? (uncontrolled_relief_use)"))
#     wm.set("f119", input_boolean("Ổn định >=3 tháng? (stable_3_months)"))

#     # nguyên nhân mất kiểm soát
#     wm.set("f414", input_boolean("Không tuân thủ thuốc? (low_adherence)"))
#     wm.set("f415", input_boolean("Sai kỹ thuật hít? (incorrect_technique)"))
#     wm.set("f402", input_boolean("Tiếp xúc dị nguyên gần đây? (allergen trigger)"))
#     wm.set("f403", input_boolean("Thời tiết ảnh hưởng/trigged?)"))

#     # clear control/action facts
#     for fid in ["f505","f506","f507","f508","f605","f606","f607"]:
#         if fid in facts:
#             wm.set(fid, False)

#     # L6: >=3 triệu chứng không kiểm soát -> f506,f507
#     if wm.get("f116") and wm.get("f117") and wm.get("f118"):
#         wm.set("f506", True)
#         wm.set("f507", True)
#         print("✔ L6 thỏa: Hen không kiểm soát -> tăng bậc (f506, f507)")
#     # L7: ≤2 triệu chứng không kiểm soát AND ổn định ≥3 tháng -> f505,f508
#     elif (not wm.get("f116") and not wm.get("f117") and not wm.get("f118")) and wm.get("f119"):
#         wm.set("f505", True)
#         wm.set("f508", True)
#         print("✔ L7 thỏa: Hen kiểm soát tốt -> có thể giảm bậc (f505, f508)")

#     # L17-L19: nguyên nhân mất kiểm soát -> set cause facts (f605-f607)
#     if (wm.get("f116") or wm.get("f117") or wm.get("f118")) and wm.get("f414"):
#         wm.set("f605", True)  # poor adherence
#         print("ℹ️ Nguyên nhân suy đoán: Poor adherence (f605)")
#     if (wm.get("f116") or wm.get("f117") or wm.get("f118")) and wm.get("f415"):
#         wm.set("f606", True)
#         print("ℹ️ Nguyên nhân suy đoán: Incorrect inhaler technique (f606)")
#     if (wm.get("f116") or wm.get("f117") or wm.get("f118")) and (wm.get("f402") or wm.get("f403")):
#         wm.set("f607", True)
#         print("ℹ️ Nguyên nhân suy đoán: Environmental trigger (f607)")

#     # L20: nếu uncontrolled AND NOT(f414/f415) => step_up (f507 already maybe set)
#     if (wm.get("f116") or wm.get("f117") or wm.get("f118")) and not wm.get("f414") and not wm.get("f415"):
#         wm.set("f507", True)
#         print("✔ L20: Không phải do tuân thủ/kỹ thuật -> đề xuất tăng bậc (f507)")

#     # L21 handled above (f505 & f119 -> f508)

#     # Gợi ý Step từ severity facts (L12-L16)
#     # We'll compute suggestion number f310 and human string f317
#     suggestion = None
#     if wm.get("f601") and wm.get("f124") == False:
#         # note: f124 might be number; ensure it's 0
#         if wm.get("f124") == 0:
#             suggestion = 1
#     if wm.get("f602"):
#         suggestion = 2
#     if wm.get("f603"):
#         suggestion = 3
#     if wm.get("f604") and (wm.get("f116") or wm.get("f117") or wm.get("f118")):
#         suggestion = 4
#     if wm.get("f604") and isinstance(wm.get("f124"), (int, float)) and wm.get("f124") >= 2:
#         suggestion = 5

#     if suggestion is not None:
#         wm.set("f310", suggestion)
#         wm.set("f317", f"Step {suggestion}")
#         print(f"🔔 Gợi ý điều trị: Step {suggestion}")
#     else:
#         print("🔔 Chưa có gợi ý Step phù hợp dựa trên dữ liệu hiện tại")

# def summarize(wm: WorkingMemory):
#     print("\n========================")
#     print("🏁 KẾT LUẬN CUỐI CÙNG")
#     print("========================")
#     facts_now = wm.all_facts()

#     # chẩn đoán
#     if facts_now["f504"]["value"]:
#         print(" - Chẩn đoán: Hen phế quản (Xác định).")
#     elif facts_now["f501"]["value"]:
#         print(" - Nghi ngờ hen (cần thêm xét nghiệm).")
#     else:
#         # check other differentials
#         diffs = ["f509","f510","f511","f512","f513"]
#         found = [d for d in diffs if facts_now.get(d, {}).get("value")]
#         if found:
#             print(" - Có dấu hiệu gợi ý bệnh khác:", ", ".join(found))
#         else:
#             print(" - Chưa đủ dữ liệu để kết luận.")

#     # severity
#     for sid, label in [("f601","Mild intermittent"),("f602","Mild persistent"),("f603","Moderate persistent"),("f604","Severe persistent")]:
#         if facts_now.get(sid, {}).get("value"):
#             print(f" - Mức độ nặng: {label}")

#     # control & actions
#     if facts_now["f506"]["value"]:
#         print(" - Hen không kiểm soát -> đề xuất tăng bậc (step-up).")
#     if facts_now["f505"]["value"]:
#         print(" - Hen kiểm soát tốt -> có thể xem xét giảm bậc (step-down).")
#     if facts_now["f507"]["value"]:
#         print(" - Hành động: Tăng bậc điều trị (f507).")
#     if facts_now["f508"]["value"]:
#         print(" - Hành động: Giảm bậc điều trị (f508).")

#     # suggestion step
#     if isinstance(facts_now["f310"]["value"], (int, float)):
#         print(f" - Gợi ý Step điều trị (f310): {facts_now['f310']['value']} ({facts_now.get('f317',{}).get('value','')})")
#     elif facts_now.get("f317", {}).get("value"):
#         print(f" - Gợi ý điều trị: {facts_now['f317']['value']}")

#     # causes
#     if facts_now.get("f605", {}).get("value"):
#         print(" - Nguyên nhân mất kiểm soát: Không tuân thủ thuốc.")
#     if facts_now.get("f606", {}).get("value"):
#         print(" - Nguyên nhân mất kiểm soát: Sai kỹ thuật hít.")
#     if facts_now.get("f607", {}).get("value"):
#         print(" - Nguyên nhân mất kiểm soát: Yếu tố môi trường (dị nguyên / thời tiết).")

# def main():
#     wm = WorkingMemory(facts)
#     wm.reset()

#     print("=== HỆ CHUYÊN GIA HỖ TRỢ CHẨN ĐOÁN VÀ ĐIỀU TRỊ HEN PHẾ QUẢN ===")

#     # Module 1
#     suspected = module_symptoms(wm)

#     if not suspected:
#         # Nếu không nghi ngờ hen, hỏi có muốn xét nghiệm / phân biệt hay không
#         do_diff = input_boolean("Không nghi ngờ hen rõ ràng. Bạn muốn tiếp tục xét nghiệm/phân biệt bệnh khác? (có/không)")
#         if do_diff:
#             # thu thập các facts để phân biệt (L5-x)
#             wm.set("f401", input_boolean("Tiền sử hút thuốc?"))
#             wm.set("f115", input_boolean("Ho khạc đờm mủ nhiều năm?"))
#             # có thể hỏi thêm test nếu muốn
#             fev1_fvc = input_float("Nhập FEV1/FVC nếu có (để trống nếu không có)", allow_empty=True)
#             if fev1_fvc is not None and fev1_fvc < 0.75:
#                 wm.set("f201", True)
#             wm.set("f204", input_boolean("Test hồi phục phế quản dương tính?"))
#             # kiểm tra L5-1..L5-5
#             if wm.get("f401") and wm.get("f115") and wm.get("f201") and not wm.get("f204"):
#                 wm.set("f509", True); print("🚨 Nghi COPD")
#             if wm.get("f103") and wm.get("f111") and wm.get("f405"):
#                 wm.set("f510", True); print("🚨 Nghi suy tim trái")
#             if wm.get("f103") and wm.get("f112") and wm.get("f113"):
#                 wm.set("f511", True); print("🚨 Nghi hẹp/ứ/dị vật PQ")
#             if wm.get("f114"):
#                 wm.set("f512", True); print("🚨 Nghi GERD / rò khí-thực quản")
#             if wm.get("f115"):
#                 wm.set("f513", True); print("🚨 Nghi giãn phế quản")
#         else:
#             print("Kết thúc: không tiến hành thêm.")
#             summarize(wm)
#             return

#     # Nếu nghi ngờ hen hoặc tiếp tục, sang module xét nghiệm
#     module_tests(wm)

#     # Chỉ đánh giá mức độ nếu hen được xác định hoặc nghi ngờ (bạn có thể thay đổi logic)
#     # Ở đây ta thực hiện luôn module_severity để có gợi ý Step.
#     module_severity(wm)

#     # Module control & treatment (tái khám/điều chỉnh)
#     module_control_and_treatment(wm)

#     # Tóm tắt kết quả
#     summarize(wm)

# if __name__ == "__main__":
#     main()

def main():
    print("===== HỆ THỐNG CHẨN ĐOÁN & QUẢN LÝ HEN PHẾ QUẢN =====")
    print("Chọn chế độ làm việc:")
    print("1. Khám lần đầu (Chẩn đoán hen + Đánh giá mức độ nặng)")
    print("2. Tái khám (Đánh giá mức độ kiểm soát)")

    choice = input("Nhập lựa chọn: ")

    # Tạo Working Memory từ facts dictionary (không dùng JSON)
    wm = WorkingMemory(facts)
    wm.reset()

    if choice == "1":
        run_initial_diagnosis(wm)

    elif choice == "2":
        run_follow_up(wm)

    else:
        print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()
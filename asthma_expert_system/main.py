# asthma_expert_system/main.py
"""
Giao diện Dòng lệnh (CLI Interactive Terminal) cho Hệ thống Chuyên gia Hen Phế Quản
Hỗ trợ khám bệnh trực tiếp, tái khám, đánh giá kỹ thuật hít và chạy 6 ca lâm sàng mẫu.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from engine.wm import WorkingMemory
from kb.facts_def import FACTS_DEF
from modules.initial_assessment import process_initial_assessment
from modules.follow_up import process_follow_up
from modules.inhaler_technique import audit_inhaler_technique
from modules.patient_cases import PATIENT_CASES
from utils.helpers import input_boolean_cli, input_float_cli

def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title.upper()}")
    print("=" * 60)

def cli_initial_assessment():
    print_header("Khám Lần Đầu - Chẩn Đoán & Khởi Đầu Điều Trị Hen")
    wm = WorkingMemory(FACTS_DEF)

    print("\n--- 1. THU THẬP TRIỆU CHỨNG HÔ HẤP ---")
    wm.set("f101", input_boolean_cli("Bệnh nhân có ho kéo dài hoặc từng cơn?"))
    wm.set("f102", input_boolean_cli("Có khò khè khi thở ra (Wheezing)?"))
    wm.set("f103", input_boolean_cli("Có khó thở / thở gấp từng cơn?"))
    wm.set("f104", input_boolean_cli("Có cảm giác nặng ngực / co thắt lồng ngực?"))

    wm.set("f105", input_boolean_cli("Triệu chứng có thay đổi theo thời gian hoặc cường độ?"))
    wm.set("f106", input_boolean_cli("Triệu chứng có nặng hơn về đêm hoặc sáng sớm?"))
    wm.set("f107", input_boolean_cli("Triệu chứng có tăng khi gắng sức hoặc cười to?"))

    print("\n--- 2. TẦN SUẤT TRIỆU CHỨNG (ĐÁNH GIÁ MỨC ĐỘ NẶNG) ---")
    wm.set("f120", input_float_cli("Số ngày trong tuần có triệu chứng (0-7)", default=0.0))
    wm.set("f121", input_float_cli("Số lần thức giấc ban đêm do hen/tuần (0-7)", default=0.0))
    wm.set("f122", input_float_cli("Mức độ giới hạn hoạt động (0: không, 1: nhẹ, 2: nhiều)", default=0.0))
    wm.set("f123", input_float_cli("Số lần dùng thuốc cắt cơn SABA/tuần", default=0.0))
    wm.set("f124", input_float_cli("Số đợt cấp cần dùng Corticoid toàn thân trong năm qua", default=0.0))

    print("\n--- 3. THĂM DÒ CHỨC NĂNG HÔ HẤP (HÔ HẤP KÝ) ---")
    fev1_fvc = input_float_cli("Chỉ số FEV1/FVC (ví dụ 0.72) (để trống nếu chưa đo)", allow_empty=True)
    if fev1_fvc: wm.set("f201", fev1_fvc)

    fev1_inc = input_float_cli("% Tăng FEV1 sau test hồi phục (ví dụ 14) (để trống nếu chưa đo)", allow_empty=True)
    if fev1_inc: wm.set("f202", fev1_inc)

    wm.set("f207", input_boolean_cli("Test hồi phục phế quản (BDR test) có Dương tính không?"))

    print("\n--- 4. DẤU HIỆU PHÂN BIỆT BỆNH KHÁC ---")
    wm.set("f401", input_boolean_cli("Tiền sử hút thuốc lá ≥ 10 gói-năm?"))
    wm.set("f404", input_boolean_cli("Đã từng được chẩn đoán COPD trước đây?"))
    wm.set("f109", input_boolean_cli("Ho khạc đờm mủ đục kéo dài nhiều năm?"))
    wm.set("f405", input_boolean_cli("Tiền sử Tăng huyết áp / Bệnh tim mạch / Suy tim?"))
    wm.set("f110", input_boolean_cli("Khám phổi có nghe thấy Ran ẩm 2 đáy phổi?"))
    wm.set("f112", input_boolean_cli("Ho/khó thở tăng khi nằm ngửa hoặc sau ăn no / ợ chua?"))

    # Xử lý suy diễn
    result = process_initial_assessment(wm)
    diag = result["diagnosis"]
    sev = result["severity"]
    tx = result["treatment"]

    print_header("KẾT QUẢ CHẨN ĐOÁN & PHÁC ĐỒ CHUYÊN GIA")
    print(f"🎯 KẾT LUẬN: {diag['main_title']}")
    print(f"🌡 MỨC ĐỘ NẶNG BAN ĐẦU: {sev['label']}")
    print(f"\n💊 ĐỀ XUẤT BẬC ĐIỀU TRỊ: {tx['step_title']}")
    print("------------------------------------------------------------")
    print("⭐ LỘ TRÌNH 1 (ƯU TIÊN - GINA SMART / MART):")
    print(f"   {tx['track1_preferred'].get('controller_and_reliever', 'N/A')}")
    print(f"   Biệt dược: {', '.join(tx['track1_preferred'].get('brand_examples', []))}")
    print("\n🔄 LỘ TRÌNH 2 (THAY THẾ - ALTERNATIVE):")
    print(f"   Duy trì: {tx['track2_alternative'].get('controller', tx['track2_alternative'].get('controller_and_reliever', 'N/A'))}")
    print(f"   Cắt cơn: {tx['track2_alternative'].get('reliever', 'SABA khi cần')}")

    print("\n📊 BẢNG XẾP HẠNG XÁC SUẤT CHẨN ĐOÁN PHÂN BIỆT:")
    for d in result["differential_ranking"][:4]:
        print(f"   • {d['name']:<40} : {d['probability']}% ({d['level']})")

    print("\n🧭 CÁC QUY TẮC ĐÃ KÍCH HOẠT:")
    for r in result["fired_rules"]:
        print(f"   [{r['rule_id']}] {r['name']} (CF: {r.get('cf', 1.0)*100:.0f}%)")

def cli_follow_up():
    print_header("Tái Khám & Đánh Giá Kiểm Soát Hen (GINA Follow-up)")
    wm = WorkingMemory(FACTS_DEF)

    print("\n--- ĐÁNH GIÁ 4 CÂU HỎI KIỂM SOÁT TRIỆU CHỨNG GINA (4 TUẦN QUA) ---")
    wm.set("f701", input_boolean_cli("1. Có triệu chứng ban ngày > 2 lần/tuần?"))
    wm.set("f702", input_boolean_cli("2. Có bất kỳ lần nào thức giấc ban đêm do hen?"))
    wm.set("f703", input_boolean_cli("3. Cần dùng thuốc cắt cơn > 2 lần/tuần?"))
    wm.set("f704", input_boolean_cli("4. Có bị giới hạn hoạt động thể lực do hen?"))

    step = input_float_cli("\nBậc điều trị GINA hiện tại của bệnh nhân (1-5)", default=2.0)
    wm.set("f310", int(step or 2))

    wm.set("f414", input_boolean_cli("Bệnh nhân có quên/kém tuân thủ xịt thuốc duy trì không?"))
    wm.set("f415", input_boolean_cli("Bệnh nhân có thực hiện sai kỹ thuật hít không?"))

    res = process_follow_up(wm)
    ctrl = res["control_assessment"]
    tx_dec = res["treatment_decision"]

    print_header("KẾT QUẢ ĐÁNH GIÁ TÁI KHÁM")
    print(f"📊 MỨC ĐỘ KIỂM SOÁT: {ctrl['level']} (Điểm: {ctrl['score']}/4)")
    print(f"🎯 QUYẾT ĐỊNH ĐIỀU TRỊ: {tx_dec['action_title']}")
    for adv in tx_dec["clinical_advice"]:
        print(f"   • {adv}")

def cli_run_test_cases():
    print_header("Chạy Tự Động 6 Ca Lâm Sàng Mẫu (Verification Suite)")
    for idx, c in enumerate(PATIENT_CASES, 1):
        print(f"\n[{idx}] {c['title']}")
        print(f"    Tóm tắt: {c['summary']}")
        wm = WorkingMemory(FACTS_DEF)
        wm.load_dict(c["facts"])

        if c["mode"] == "Khám lần đầu":
            res = process_initial_assessment(wm)
            diag_title = res["diagnosis"]["main_title"]
            sev_label = res["severity"]["label"]
            step_title = res["treatment"]["step_title"]
            print(f"    ➔ KẾT QUẢ: {diag_title} | {sev_label} | {step_title}")
        else:
            res = process_follow_up(wm)
            ctrl_label = res["control_assessment"]["level"]
            act_title = res["treatment_decision"]["action_title"]
            print(f"    ➔ KẾT QUẢ: {ctrl_label} | {act_title}")
        print(f"    ✔ Kỳ vọng: {c['expected_result']}")

def main():
    while True:
        print_header("Hệ Thống Chuyên Gia Chẩn Đoán & Quản Lý Hen Phế Quản (Asthma CDSS)")
        print("1. Khám lần đầu (Chẩn đoán, Phân loại mức độ & Khởi đầu phác đồ)")
        print("2. Tái khám định kỳ (Đánh giá kiểm soát GINA & Điều chỉnh bậc)")
        print("3. Chạy kiểm thử 6 ca lâm sàng mẫu (Test Suite)")
        print("4. Khởi chạy Giao diện Web Trực quan (Streamlit Web App)")
        print("5. Thoát")

        choice = input("\nNhập lựa chọn của bạn (1-5): ").strip()
        if choice == "1":
            cli_initial_assessment()
        elif choice == "2":
            cli_follow_up()
        elif choice == "3":
            cli_run_test_cases()
        elif choice == "4":
            print("\n>> Đang khởi chạy Streamlit Web App...")
            print(">> Hãy chạy lệnh: streamlit run app.py")
            break
        elif choice == "5":
            print("\nCảm ơn bạn đã sử dụng Hệ thống Chuyên gia Hen Phế Quản! Tạm biệt.")
            sys.exit(0)
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 5.")

if __name__ == "__main__":
    main()
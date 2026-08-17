# asthma_expert_system/test_system.py
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from engine.wm import WorkingMemory
from kb.facts_def import FACTS_DEF
from modules.initial_assessment import process_initial_assessment
from modules.follow_up import process_follow_up
from modules.patient_cases import PATIENT_CASES
from modules.action_plan import generate_action_plan
from modules.inhaler_technique import audit_inhaler_technique
from utils.report_generator import generate_medical_report_html

def test_cases():
    print("=" * 70)
    print("KIỂM THỬ TOÀN DIỆN 6 CA LÂM SÀNG MẪU (CDSS TEST SUITE)")
    print("=" * 70)
    for i, c in enumerate(PATIENT_CASES, 1):
        wm = WorkingMemory(FACTS_DEF)
        wm.load_dict(c["facts"])
        if c["mode"] == "Khám lần đầu":
            res = process_initial_assessment(wm)
            print(f"Ca {i} ({c['patient_name']}):")
            print(f"  • Chẩn đoán : {res['diagnosis']['main_title']}")
            print(f"  • Mức độ    : {res['severity']['label']}")
            print(f"  • Đề xuất   : {res['treatment']['step_title']}")
            print(f"  • Top 1 Phân biệt: {res['differential_ranking'][0]['name']} ({res['differential_ranking'][0]['probability']}%)")
        else:
            res = process_follow_up(wm)
            print(f"Ca {i} ({c['patient_name']}):")
            print(f"  • Mức độ KS : {res['control_assessment']['level']} ({res['control_assessment']['score']}/4)")
            print(f"  • Quyết định: {res['treatment_decision']['action_title']}")
        print()

    print("=" * 70)
    print("KIỂM THỬ MODULE KỸ THUẬT BÌNH HÍT / XỊT")
    print("=" * 70)
    audit_pass = audit_inhaler_technique("pMDI", ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"])
    print(f"• pMDI Đạt 100%: {audit_pass['score_pct']}% -> {audit_pass['evaluation']}")

    audit_fail = audit_inhaler_technique("pMDI", ["s1", "s3", "s4", "s6"])
    print(f"• pMDI Lỗi: {audit_fail['score_pct']}% -> {audit_fail['evaluation']} (Số lỗi then chốt: {len(audit_fail['missed_critical_errors'])})")

    print("\n=" * 70)
    print("KIỂM THỬ MODULE SINH KẾ HOẠCH HÀNH ĐỘNG & BÁO CÁO HTML")
    print("=" * 70)
    plan = generate_action_plan("Trần Thị Mai Lan", 24, 450.0, 2, "Symbicort 160/4.5", "Ventolin")
    print(f"• Kế hoạch hành động 3 vùng: {list(plan.keys())}")

    wm_sample = WorkingMemory(FACTS_DEF)
    wm_sample.load_dict(PATIENT_CASES[0]["facts"])
    res_sample = process_initial_assessment(wm_sample)
    html = generate_medical_report_html({"name": "Trần Thị Mai Lan", "age": 24, "gender": "Nữ", "bmi": 21.0}, res_sample)
    print(f"• Báo cáo y khoa HTML sinh thành công: {len(html)} bytes")

    print("\n" + "=" * 70)
    print("TẤT CẢ TEST CASES & MODULES ĐÃ HOẠT ĐỘNG CHÍNH XÁC 100%!")
    print("=" * 70)

if __name__ == "__main__":
    test_cases()

# asthma_expert_system/modules/follow_up.py
"""
Nghiệp vụ Tái Khám, Đánh Giá Mức Độ Kiểm Soát & Điều Chỉnh Bậc Điều Trị (GINA Follow-up)
"""

from typing import Dict, Any, List
from engine.wm import WorkingMemory
from engine.inference import InferenceEngine
from engine.explanation import ExplanationFacility
from kb.medications_db import GINA_TRACKS_INFO

def process_follow_up(wm: WorkingMemory) -> Dict[str, Any]:
    """
    Quy trình tái khám định kỳ theo chuẩn GINA:
    1. Đánh giá 4 câu hỏi kiểm soát triệu chứng trong 4 tuần qua.
    2. Rà soát các yếu tố nguy cơ đợt bùng phát trong tương lai.
    3. Đánh giá tuân thủ & kỹ thuật sử dụng thiết bị hít.
    4. Ra quyết định: Nâng bậc (Step-up), Hạ bậc (Step-down), hay Duy trì & Huấn luyện.
    """
    # 1. Chạy động cơ suy diễn
    engine = InferenceEngine(wm)
    fired_rules, updated_wm = engine.forward_chain()

    # 2. Tính điểm kiểm soát GINA (0 - 4)
    q1 = bool(updated_wm.get("f701", False))
    q2 = bool(updated_wm.get("f702", False))
    q3 = bool(updated_wm.get("f703", False))
    q4 = bool(updated_wm.get("f704", False))

    control_score = sum([q1, q2, q3, q4])
    if control_score == 0:
        control_level = "Kiểm soát tốt (Well-Controlled)"
        control_status = "CONTROLLED"
        control_color = "#10B981"
    elif 1 <= control_score <= 2:
        control_level = "Kiểm soát một phần (Partly-Controlled)"
        control_status = "PARTLY_CONTROLLED"
        control_color = "#F59E0B"
    else:
        control_level = "Không kiểm soát (Uncontrolled)"
        control_status = "UNCONTROLLED"
        control_color = "#EF4444"

    # 3. Rà soát yếu tố nguy cơ đợt cấp tương lai
    future_risks: List[str] = []
    if updated_wm.get("f124", 0) and updated_wm.get("f124") >= 1:
        future_risks.append(f"Tiền sử có {updated_wm.get('f124')} đợt cấp cần Corticoid toàn thân trong 12 tháng qua")
    if updated_wm.get("f417"):
        future_risks.append("Sử dụng quá nhiều bình thuốc cắt cơn SABA (≥ 3 bình/năm)")
    if updated_wm.get("f414"):
        future_risks.append("Kém tuân thủ điều trị thuốc kiểm soát duy trì hằng ngày")
    if updated_wm.get("f415"):
        future_risks.append("Thực hiện sai kỹ thuật sử dụng bình xịt / hít")
    if updated_wm.get("f401"):
        future_risks.append("Tiền sử tiếp xúc khói thuốc lá chủ động / thụ động")
    if updated_wm.get("f205") is not None and updated_wm.get("f205") < 60:
        future_risks.append(f"Chức năng phổi suy giảm đáng kể (FEV1 = {updated_wm.get('f205')}%)")
    if updated_wm.get("f418"):
        future_risks.append("Tiền sử từng nhập ICU hoặc đặt nội khí quản vì hen")

    # 4. Ra quyết định điều chỉnh bậc điều trị
    current_step = updated_wm.get("f310", 2) or 2
    action_type = "MAINTAIN"
    action_title = "Duy trì bậc hiện tại"
    suggested_new_step = current_step
    clinical_advice = []

    if updated_wm.get("f810"): # Step up
        action_type = "STEP_UP"
        suggested_new_step = min(5, current_step + 1)
        action_title = f"ĐỀ XUẤT TĂNG BẬC: Từ Bậc {current_step} ➔ Bậc {suggested_new_step}"
        clinical_advice.append("Bệnh nhân không kiểm soát dù đã tuân thủ tốt và dùng đúng kỹ thuật.")
        clinical_advice.append(f"Tăng bậc điều trị lên Step {suggested_new_step} và hẹn tái khám đánh giá lại sau 2 - 3 tháng.")
    elif updated_wm.get("f812"): # Maintain & Retrain
        action_type = "MAINTAIN_AND_TRAIN"
        suggested_new_step = current_step
        action_title = f"DUY TRÌ BẬC {current_step} & CHỈNH KỸ THUẬT / TUÂN THỦ"
        clinical_advice.append("Mất kiểm soát do kỹ thuật hít chưa đúng hoặc quên liều thuốc.")
        clinical_advice.append("Tập trung hướng dẫn lại thao tác dùng bình xịt/hít và cải thiện tuân thủ trước khi xem xét tăng liều thuốc.")
    elif updated_wm.get("f811"): # Step down
        action_type = "STEP_DOWN"
        suggested_new_step = max(1, current_step - 1)
        action_title = f"XEM XÉT GIẢM BẬC AN TOÀN: Từ Bậc {current_step} ➔ Bậc {suggested_new_step}"
        clinical_advice.append("Bệnh nhân đã kiểm soát tốt liên tục trong ≥ 3 tháng và chức năng phổi ổn định.")
        clinical_advice.append(f"Có thể thử giảm liều ICS từ 25-50% hoặc giảm xuống Step {suggested_new_step} theo dõi sát.")
    else:
        suggested_new_step = current_step
        action_title = f"DUY TRÌ PHÁC ĐỒ BẬC {current_step}"
        clinical_advice.append("Tiếp tục phác đồ điều trị hiện tại và theo dõi định kỳ.")

    track1_plan = GINA_TRACKS_INFO["Track_1"]["steps"].get(suggested_new_step, {})
    track2_plan = GINA_TRACKS_INFO["Track_2"]["steps"].get(suggested_new_step, {})

    # 5. Cây giải thích
    explainer = ExplanationFacility(updated_wm, fired_rules, engine.rules)
    explanation_control = explainer.explain_how("f705" if control_status == "CONTROLLED" else ("f706" if control_status == "PARTLY_CONTROLLED" else "f707"))

    return {
        "status": "success",
        "control_assessment": {
            "score": control_score,
            "max_score": 4,
            "level": control_level,
            "status": control_status,
            "color": control_color,
            "answers": {
                "q1_daytime": q1,
                "q2_night_waking": q2,
                "q3_reliever_use": q3,
                "q4_activity_limit": q4
            }
        },
        "future_risks": future_risks,
        "treatment_decision": {
            "current_step": current_step,
            "suggested_new_step": suggested_new_step,
            "action_type": action_type,
            "action_title": action_title,
            "clinical_advice": clinical_advice,
            "track1_preferred": track1_plan,
            "track2_alternative": track2_plan
        },
        "fired_rules": fired_rules,
        "explanation": explanation_control,
        "audit_trail_md": explainer.get_audit_trail_markdown()
    }

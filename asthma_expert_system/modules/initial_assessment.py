# asthma_expert_system/modules/initial_assessment.py
"""
Nghiệp vụ Khám Lần Đầu & Chẩn Đoán Xác Định Hen Phế Quản (Initial Clinical Assessment)
Tích hợp Động cơ suy diễn, Tính toán Certainty Factor và Đề xuất Bậc điều trị GINA.
"""

from typing import Dict, Any
from engine.wm import WorkingMemory
from engine.inference import InferenceEngine
from engine.certainty import CertaintyEngine
from engine.explanation import ExplanationFacility
from kb.medications_db import GINA_TRACKS_INFO

def process_initial_assessment(wm: WorkingMemory) -> Dict[str, Any]:
    """
    Thực hiện quy trình đánh giá khám lần đầu toàn diện:
    1. Chạy Forward Chaining suy diễn luật Chẩn đoán, Mức độ nặng, Đề xuất khởi đầu.
    2. Tính toán ma trận xác suất chẩn đoán phân biệt (Certainty Engine).
    3. Trích xuất phác đồ điều trị GINA Track 1 (Ưu tiên) và Track 2 (Thay thế).
    4. Tổng hợp cây giải thích (Explanation Facility).
    """
    # 1. Khởi chạy động cơ suy diễn
    engine = InferenceEngine(wm)
    fired_rules, updated_wm = engine.forward_chain()

    # 2. Đánh giá chẩn đoán phân biệt & Certainty Factor
    certainty_engine = CertaintyEngine(updated_wm)
    differential_ranking = certainty_engine.evaluate_differentials()

    # 3. Tổng hợp kết luận chẩn đoán
    is_confirmed = updated_wm.get("f504", False)
    is_suspected = updated_wm.get("f501", False) or updated_wm.get("f503", False)
    has_variable_limitation = updated_wm.get("f502", False)

    # 4. Xác định mức độ nặng ban đầu
    severity_label = "Chưa đủ dữ liệu phân loại"
    severity_code = "UNKNOWN"
    if updated_wm.get("f604"):
        severity_label = "Hen dai dẳng nặng (Severe Persistent)"
        severity_code = "SEVERE"
    elif updated_wm.get("f603"):
        severity_label = "Hen dai dẳng trung bình (Moderate Persistent)"
        severity_code = "MODERATE"
    elif updated_wm.get("f602"):
        severity_label = "Hen dai dẳng nhẹ (Mild Persistent)"
        severity_code = "MILD_PERSISTENT"
    elif updated_wm.get("f601"):
        severity_label = "Hen gián đoạn (Intermittent)"
        severity_code = "INTERMITTENT"

    # 5. Xác định đề xuất Bậc điều trị khởi đầu
    suggested_step = 2 # Mặc định Step 2 nếu hen nhẹ
    if updated_wm.get("f805"):
        suggested_step = 5
    elif updated_wm.get("f804"):
        suggested_step = 4
    elif updated_wm.get("f803"):
        suggested_step = 3
    elif updated_wm.get("f802"):
        suggested_step = 2
    elif updated_wm.get("f801"):
        suggested_step = 1

    track1_plan = GINA_TRACKS_INFO["Track_1"]["steps"].get(suggested_step, {})
    track2_plan = GINA_TRACKS_INFO["Track_2"]["steps"].get(suggested_step, {})

    # 6. Cơ chế giải thích
    explainer = ExplanationFacility(updated_wm, fired_rules, engine.rules)
    explanation_diagnosis = explainer.explain_how("f504" if is_confirmed else ("f501" if is_suspected else "f509"))

    return {
        "status": "success",
        "diagnosis": {
            "is_confirmed": is_confirmed,
            "is_suspected": is_suspected,
            "has_variable_limitation": has_variable_limitation,
            "main_title": "CHẨN ĐOÁN XÁC ĐỊNH HEN PHẾ QUẢN" if is_confirmed else ("NGHI NGỜ HEN PHẾ QUẢN (Cần thêm thăm dò chức năng)" if is_suspected else "CHƯA ĐỦ BẰNG CHỨNG CHẨN ĐOÁN HEN (Xem chẩn đoán phân biệt)"),
            "color": "#10B981" if is_confirmed else ("#F59E0B" if is_suspected else "#EF4444")
        },
        "severity": {
            "code": severity_code,
            "label": severity_label
        },
        "treatment": {
            "suggested_step": suggested_step,
            "step_title": f"BẬC {suggested_step} (GINA STEP {suggested_step})",
            "track1_preferred": track1_plan,
            "track2_alternative": track2_plan
        },
        "differential_ranking": differential_ranking,
        "fired_rules": fired_rules,
        "explanation": explanation_diagnosis,
        "audit_trail_md": explainer.get_audit_trail_markdown()
    }
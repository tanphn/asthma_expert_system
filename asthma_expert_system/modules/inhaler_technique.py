# asthma_expert_system/modules/inhaler_technique.py
"""
Module Đánh giá và Huấn luyện Kỹ thuật Sử dụng Thiết bị Hít/Xịt Hen Phế Quản (Inhaler Technique Audit)
Tự động phát hiện các lỗi sai nghiêm trọng làm giảm hiệu quả thuốc.
"""

from typing import Dict, Any, List
from kb.medications_db import INHALER_DEVICES

def audit_inhaler_technique(device_type: str, checked_step_ids: List[str]) -> Dict[str, Any]:
    """
    Đánh giá danh sách các bước bệnh nhân đã thực hiện đúng,
    tính điểm phần trăm thành thạo và chỉ ra các lỗi sai nguy hiểm.
    """
    device_info = INHALER_DEVICES.get(device_type)
    if not device_info:
        return {"status": "error", "message": "Thiết bị không tồn tại trong cơ sở dữ liệu."}

    all_steps = device_info["checklist_steps"]
    total_steps = len(all_steps)
    correct_count = len(checked_step_ids)

    missed_critical_errors = []
    missed_normal_steps = []

    for step in all_steps:
        sid = step["id"]
        if sid not in checked_step_ids:
            if step.get("critical", False):
                missed_critical_errors.append({
                    "step_text": step["text"],
                    "error_reason": step.get("error_reason", "Ảnh hưởng nghiêm trọng đến lượng thuốc vào phổi.")
                })
            else:
                missed_normal_steps.append(step["text"])

    score_pct = round((correct_count / total_steps) * 100, 1)

    if not missed_critical_errors and score_pct >= 90:
        evaluation = "Kỹ thuật Chuẩn xác (Xuất sắc)"
        status = "PASSED"
        color = "#10B981"
    elif not missed_critical_errors and score_pct >= 70:
        evaluation = "Kỹ thuật Khá (Cần lưu ý thêm một số bước nhỏ)"
        status = "WARNING"
        color = "#F59E0B"
    else:
        evaluation = "Kỹ thuật Chưa Đạt (Có lỗi sai nghiêm trọng)"
        status = "FAILED"
        color = "#EF4444"

    return {
        "device_type": device_type,
        "device_name": device_info["name"],
        "examples": device_info.get("examples", ""),
        "total_steps": total_steps,
        "correct_steps": correct_count,
        "score_pct": score_pct,
        "evaluation": evaluation,
        "status": status,
        "color": color,
        "missed_critical_errors": missed_critical_errors,
        "missed_normal_steps": missed_normal_steps,
        "all_steps": all_steps
    }

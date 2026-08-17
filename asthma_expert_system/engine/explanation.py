# asthma_expert_system/engine/explanation.py
"""
Cơ chế giải thích (Explanation Facility) của Hệ thống Chuyên gia.
Cung cấp khả năng giải thích HOW (Làm sao suy ra kết luận), WHY (Tại sao hỏi thông tin này),
và tạo chuỗi lập luận lâm sàng hoàn chỉnh (Audit Trail).
"""

from typing import Dict, Any, List
from engine.wm import WorkingMemory

class ExplanationFacility:
    """
    Module phụ trách diễn giải logic suy luận của Hệ thống Chuyên gia cho Bác sĩ & Người dùng.
    """
    def __init__(self, wm: WorkingMemory, fired_rules: List[Dict[str, Any]], all_rules: List[Dict[str, Any]]):
        self.wm = wm
        self.fired_rules = fired_rules
        self.all_rules = all_rules

    def explain_how(self, fact_id: str) -> Dict[str, Any]:
        """
        Giải thích LÀM SAO (HOW) hệ thống rút ra được kết luận cho một Fact cụ thể.
        """
        fact_meta = self.wm.get_meta(fact_id)
        if not fact_meta or fact_meta["value"] in (False, None, 0):
            return {
                "fact_id": fact_id,
                "concluded": False,
                "message": f"Giả thuyết '{fact_id}' chưa được xác nhận hoặc có giá trị âm tính.",
                "rules_involved": []
            }

        rules_involved = []
        for fired in self.fired_rules:
            if fact_id in fired["consequent_facts"]:
                rules_involved.append(fired)

        return {
            "fact_id": fact_id,
            "fact_name": fact_meta.get("name", fact_id),
            "fact_desc": fact_meta.get("desc", ""),
            "concluded": True,
            "cf": fact_meta.get("cf", 1.0),
            "rules_involved": rules_involved,
            "summary": f"Kết luận '{fact_meta.get('name')}' được xác lập dựa trên {len(rules_involved)} quy tắc đã kích hoạt."
        }

    def explain_why(self, fact_id: str) -> Dict[str, Any]:
        """
        Giải thích TẠI SAO (WHY) hệ thống cần thu thập hoặc hỏi thông tin về Fact này.
        """
        fact_meta = self.wm.get_meta(fact_id)
        dependent_rules = []

        for rule in self.all_rules:
            # Kiểm tra xem rule có tham chiếu tới fact_id không
            rdesc = rule.get("condition_desc", "")
            rid = rule.get("id", "")
            rname = rule.get("name", "")
            consequents = rule.get("consequent_facts", [])

            # Nếu mô tả điều kiện có đề cập hoặc rule dùng fact này
            if fact_id in rdesc or fact_id in str(rule.get("condition_fn")):
                dependent_rules.append({
                    "rule_id": rid,
                    "rule_name": rname,
                    "leads_to": consequents,
                    "rationale": rule.get("rationale", "")
                })

        return {
            "fact_id": fact_id,
            "fact_name": fact_meta.get("name", fact_id) if fact_meta else fact_id,
            "clinical_importance": fact_meta.get("desc", "") if fact_meta else "",
            "dependent_rules_count": len(dependent_rules),
            "dependent_rules": dependent_rules
        }

    def get_audit_trail_markdown(self) -> str:
        """
        Tạo báo cáo chi tiết toàn bộ chuỗi suy luận logic theo định dạng Markdown.
        """
        md = []
        md.append("## 🧭 Nhật Ký & Cây Suy Luận Chuyên Gia (Inference Audit Trail)\n")
        
        if not self.fired_rules:
            md.append("> *Chưa có quy tắc suy diễn nào được kích hoạt với dữ liệu hiện tại.*")
            return "\n".join(md)

        md.append(f"**Tổng số quy tắc đã kích hoạt thành công:** `{len(self.fired_rules)}`\n")

        for idx, r in enumerate(self.fired_rules, 1):
            md.append(f"### Bước {idx}: [{r['rule_id']}] {r['name']}")
            md.append(f"- **Vòng lặp suy diễn:** Vòng {r.get('iteration', 1)}")
            md.append(f"- **Điều kiện thỏa mãn:** {r['condition_desc']}")
            md.append(f"- **Kết luận xác lập:** `{', '.join(r['consequent_facts'])}`")
            md.append(f"- **Độ tin cậy (CF):** `{r.get('cf', 1.0) * 100:.0f}%`")
            md.append(f"- **Lý giải lâm sàng:** *{r['rationale']}*")
            md.append("")

        return "\n".join(md)

# asthma_expert_system/engine/inference.py
"""
Động cơ suy diễn Tiến (Forward Chaining Inference Engine) chuẩn cho Hệ thống Chuyên gia.
Hỗ trợ kiểm tra điều kiện linh hoạt (Callable hoặc Expression AST), ghi vết quy tắc kích hoạt,
tính toán Certainty Factors và liên kết với Explanation Facility.
"""

from typing import List, Dict, Any, Tuple
from engine.wm import WorkingMemory
from kb.rules_diagnosis import RULES_DIAGNOSIS
from kb.rules_severity import RULES_SEVERITY
from kb.rules_control import RULES_CONTROL
from kb.rules_treatment import RULES_TREATMENT

class InferenceEngine:
    """
    Động cơ suy diễn tiến (Forward Chaining) thực thi các tập luật theo chu kỳ suy diễn.
    """
    def __init__(self, wm: WorkingMemory, custom_rules: List[Dict[str, Any]] = None):
        self.wm = wm
        if custom_rules is not None:
            self.rules = custom_rules
        else:
            self.rules = (
                RULES_DIAGNOSIS +
                RULES_SEVERITY +
                RULES_CONTROL +
                RULES_TREATMENT
            )
        self.fired_rules: List[Dict[str, Any]] = []
        self.trace_logs: List[str] = []

    def load_rules(self, rules: List[Dict[str, Any]]):
        """Tải thêm hoặc thay thế tập luật suy diễn."""
        self.rules = rules

    def forward_chain(self, max_iterations: int = 20, verbose: bool = False) -> Tuple[List[Dict[str, Any]], WorkingMemory]:
        """
        Chạy thuật toán suy diễn tiến (Forward Chaining) cho đến khi đạt điểm dừng (không còn luật mới nào được kích hoạt).
        """
        self.fired_rules = []
        self.trace_logs = []
        already_fired_ids = set()

        iteration = 0
        changed = True

        if verbose:
            print(f"[InferenceEngine] Bắt đầu quá trình suy diễn tiến với {len(self.rules)} luật...")

        while changed and iteration < max_iterations:
            iteration += 1
            changed = False
            
            for rule in self.rules:
                rid = rule.get("id")
                if rid in already_fired_ids:
                    continue

                cond_fn = rule.get("condition_fn")
                is_satisfied = False

                try:
                    if callable(cond_fn):
                        is_satisfied = bool(cond_fn(self.wm))
                    elif isinstance(cond_fn, str):
                        # Đảm bảo tương thích nếu có rule dạng chuỗi
                        is_satisfied = self._eval_expression(cond_fn)
                except Exception as e:
                    if verbose:
                        print(f"[InferenceEngine Error in {rid}]: {e}")
                    is_satisfied = False

                if is_satisfied:
                    # Kích hoạt luật
                    already_fired_ids.add(rid)
                    consequents = rule.get("consequent_facts", [])
                    cf = rule.get("cf", 1.0)
                    rname = rule.get("name", rid)
                    rdesc = rule.get("condition_desc", "")
                    rationale = rule.get("rationale", "")

                    fired_record = {
                        "rule_id": rid,
                        "name": rname,
                        "condition_desc": rdesc,
                        "consequent_facts": consequents,
                        "cf": cf,
                        "rationale": rationale,
                        "iteration": iteration
                    }
                    self.fired_rules.append(fired_record)

                    log_msg = f"[KÍCH HOẠT VÒNG {iteration}] {rid}: {rname} -> Kết luận: {', '.join(consequents)}"
                    self.trace_logs.append(log_msg)
                    if verbose:
                        print(log_msg)

                    # Cập nhật facts vào Working Memory
                    for fid in consequents:
                        old_val = self.wm.get(fid)
                        if old_val is not True:
                            self.wm.set(fid, True, source_rule=rid, cf=cf)
                            changed = True

        if verbose:
            print(f"[InferenceEngine] Quá trình suy diễn hoàn tất sau {iteration} vòng lặp. Đã kích hoạt {len(self.fired_rules)} luật.")

        return self.fired_rules, self.wm

    def _eval_expression(self, expr_str: str) -> bool:
        """Đánh giá biểu thức boolean dạng chuỗi an toàn dựa trên WM."""
        context = {fid: self.wm.get(fid) for fid in self.wm._facts}
        try:
            return bool(eval(expr_str, {"__builtins__": None}, context))
        except Exception:
            return False

    def get_fired_rules(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các luật đã kích hoạt."""
        return self.fired_rules

    def get_trace_logs(self) -> List[str]:
        """Trả về nhật ký suy diễn chi tiết."""
        return self.trace_logs

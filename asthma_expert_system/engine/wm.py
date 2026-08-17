# asthma_expert_system/engine/wm.py
"""
Working Memory (Bộ nhớ làm việc) nâng cao cho Hệ thống Chuyên gia Hen Phế Quản.
Hỗ trợ quản lý trạng thái Facts, truy vết nguồn gốc suy diễn, lưu vết lịch sử và xuất dữ liệu.
"""

import copy
from typing import Dict, Any, Optional, List
from kb.facts_def import FACTS_DEF

class WorkingMemory:
    """
    Bộ nhớ làm việc lưu trữ trạng thái các Fact trong phiên khám bệnh hiện tại.
    """
    def __init__(self, base_facts_def: Optional[Dict[str, Dict[str, Any]]] = None):
        if base_facts_def is None:
            self._def = copy.deepcopy(FACTS_DEF)
        else:
            self._def = copy.deepcopy(base_facts_def)
        
        self._facts: Dict[str, Dict[str, Any]] = {}
        self._history: List[Dict[str, Any]] = []
        self.reset()

    def reset(self):
        """Khởi tạo lại toàn bộ facts về giá trị mặc định theo định nghĩa."""
        self._facts = {}
        for fid, fmeta in self._def.items():
            self._facts[fid] = {
                "id": fid,
                "name": fmeta.get("name", fid),
                "desc": fmeta.get("desc", ""),
                "category": fmeta.get("category", "Chung"),
                "type": fmeta.get("type", "boolean"),
                "value": copy.deepcopy(fmeta.get("default", False)),
                "is_derived": False,
                "source_rule": None,
                "cf": 1.0 if fmeta.get("default") not in (False, None, 0) else 0.0
            }
        self._history = []

    def set(self, fact_id: str, value: Any, source_rule: Optional[str] = None, cf: float = 1.0):
        """Gán giá trị cho một Fact với thông tin nguồn gốc suy diễn."""
        if fact_id not in self._facts:
            # Tự động khởi tạo nếu là fact mới
            self._facts[fact_id] = {
                "id": fact_id,
                "name": fact_id,
                "desc": "",
                "category": "Tự do",
                "type": "custom",
                "value": value,
                "is_derived": source_rule is not None,
                "source_rule": source_rule,
                "cf": cf
            }
        else:
            self._facts[fact_id]["value"] = value
            if source_rule is not None:
                self._facts[fact_id]["is_derived"] = True
                self._facts[fact_id]["source_rule"] = source_rule
                self._facts[fact_id]["cf"] = cf

        self._history.append({
            "fact_id": fact_id,
            "value": value,
            "source_rule": source_rule,
            "cf": cf
        })

    def get(self, fact_id: str, default: Any = None) -> Any:
        """Lấy giá trị của một Fact."""
        if fact_id in self._facts:
            val = self._facts[fact_id]["value"]
            return val if val is not None else default
        return default

    def get_meta(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Lấy metadata đầy đủ của Fact."""
        return self._facts.get(fact_id)

    def update(self, fact_dict: Dict[str, Any]):
        """Cập nhật hàng loạt facts từ một dictionary {fact_id: value}."""
        for fid, val in fact_dict.items():
            self.set(fid, val)

    def all_facts(self) -> Dict[str, Dict[str, Any]]:
        """Trả về bản sao toàn bộ trạng thái facts hiện tại."""
        return copy.deepcopy(self._facts)

    def get_active_facts(self) -> Dict[str, Any]:
        """Trả về danh sách các Fact đang có giá trị chân lý (True hoặc số khác 0)."""
        active = {}
        for fid, fdata in self._facts.items():
            val = fdata["value"]
            if val is True or (isinstance(val, (int, float)) and val > 0 and val != 999 and val != 22.0 and val != 30):
                active[fid] = fdata
        return active

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi trạng thái WM thành dạng dictionary đơn giản."""
        return {fid: fdata["value"] for fid, fdata in self._facts.items()}

    def load_dict(self, data: Dict[str, Any]):
        """Nạp dữ liệu vào WM từ một dictionary."""
        for fid, val in data.items():
            if fid in self._facts:
                self.set(fid, val)

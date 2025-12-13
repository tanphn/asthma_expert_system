# engine/wm.py
import copy
from typing import Dict, Any, Optional

class WorkingMemory:
    """
    Working Memory lưu trạng thái các Fact.
    Cho phép đọc/ghi giá trị, reset về trạng thái ban đầu.
    """
    def __init__(self, base_facts: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        base_facts: dict với key = fact_id, value = dict(name, desc, type, value)
        """
        if base_facts is not None:
            self._base: Dict[str, Dict[str, Any]] = copy.deepcopy(base_facts)
            self._facts: Dict[str, Dict[str, Any]] = copy.deepcopy(base_facts)
        else:
            self._base = {}
            self._facts = {}

    def reset(self):
        """Reset tất cả fact về giá trị mặc định"""
        self._facts = copy.deepcopy(self._base)

    def set(self, fact_id: str, value: Any):
        """Gán giá trị cho một fact"""
        if fact_id in self._facts:
            self._facts[fact_id]["value"] = value
        else:
            raise KeyError(f"Fact {fact_id} không tồn tại trong WM")

    def get(self, fact_id: str) -> Any:
        """Lấy giá trị của một fact"""
        if fact_id in self._facts:
            return self._facts[fact_id]["value"]
        else:
            raise KeyError(f"Fact {fact_id} không tồn tại trong WM")

    def update(self, fact_ids: list, value: Any = True):
        """Cập nhật nhiều fact cùng lúc"""
        for fid in fact_ids:
            self.set(fid, value)

    def all_facts(self) -> Dict[str, Dict[str, Any]]:
        """Trả về toàn bộ facts hiện tại"""
        return self._facts

    def display(self):
        """In toàn bộ WM ra màn hình"""
        print("=== Working Memory ===")
        for fid, fdata in self._facts.items():
            print(f"{fid}: {fdata['name']} = {fdata['value']}")
        print("=====================")

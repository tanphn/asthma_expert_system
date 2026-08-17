# asthma_expert_system/facts/facts.py
"""
Khả năng tương thích ngược (Backwards Compatibility) cho facts module.
Liên kết trực tiếp với tri thức chuẩn FACTS_DEF trong package kb.
"""

from kb.facts_def import FACTS_DEF

class Fact:
    def __init__(self, id, name, description, type, value=False):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.value = value

# Dictionary facts tương thích ngược
facts = {}
for fid, fmeta in FACTS_DEF.items():
    facts[fid] = {
        "name": fmeta.get("name", fid),
        "desc": fmeta.get("desc", ""),
        "type": fmeta.get("category", "Triệu chứng"),
        "value": fmeta.get("default", False)
    }

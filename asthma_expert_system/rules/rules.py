# asthma_expert_system/rules/rules.py
"""
Khả năng tương thích ngược (Backwards Compatibility) cho rules module.
Liên kết trực tiếp với các tập luật chuẩn trong package kb.
"""

from kb.rules_diagnosis import RULES_DIAGNOSIS
from kb.rules_severity import RULES_SEVERITY
from kb.rules_control import RULES_CONTROL
from kb.rules_treatment import RULES_TREATMENT

# Danh sách toàn bộ quy tắc chuẩn
rules = RULES_DIAGNOSIS + RULES_SEVERITY + RULES_CONTROL + RULES_TREATMENT

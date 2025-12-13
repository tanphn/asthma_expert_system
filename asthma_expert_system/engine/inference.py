# # engine/inference.py
# class InferenceEngine:
#     def __init__(self, facts, rules):
#         self.facts = facts
#         self.rules = rules
#         self.fired_rules = []

#     def forward_chain(self):
#         new_inference = True
#         while new_inference:
#             new_inference = False
#             for rule in self.rules:
#                 if rule["id"] in self.fired_rules:
#                     continue
#                 if rule["if"](self.facts):
#                     for fact_id in rule["then"]:
#                         if not self.facts[fact_id]["value"]:
#                             self.facts[fact_id]["value"] = True
#                             new_inference = True
#                     self.fired_rules.append(rule["id"])
def run_rules(facts, rules, verbose=False):
    """
    Simple forward chaining:
    - facts: dict of fact_id -> {value, ...}
    - rules: list of rule dicts with keys: id, if (callable), then (list), desc
    Returns:
      fired (list of rule ids fired in order), facts (updated)
    """
    fired = []
    changed = True

    # We loop until no change.
    while changed:
        changed = False
        for rule in rules:
            rid = rule.get("id")
            # do not re-fire the same rule multiple times (idempotent)
            if rid in fired:
                continue
            try:
                cond = rule["if"](facts)
            except Exception as e:
                # skip rule if error (but print if verbose)
                if verbose:
                    print(f"[rule error] {rid}: {e}")
                cond = False

            if cond:
                # apply rule
                for f_id in rule["then"]:
                    # if fact newly set, record reason and mark changed
                    if not facts[f_id]["value"]:
                        facts[f_id]["value"] = True
                        facts[f_id]["reason"] = rid
                        changed = True
                fired.append(rid)
                if verbose:
                    print(f"[FIRE] {rid}: {rule.get('desc')}")
    return fired, facts

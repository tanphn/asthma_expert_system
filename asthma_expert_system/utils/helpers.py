def input_boolean(prompt):
    while True:
        s = input(prompt + " (có/không): ").strip().lower()
        if s in ("có", "co", "yes", "y"):
            return True
        if s in ("không", "khong", "no", "n"):
            return False
        print("Vui lòng nhập 'có' hoặc 'không'.")

def input_float(prompt, allow_empty=False):
    while True:
        s = input(prompt + " (số, để trống nếu không có): ").strip()
        if s == "" and allow_empty:
            return None
        try:
            return float(s)
        except ValueError:
            print("Nhập số không đúng. Thử lại.")

def summarize_results(facts, fired_rules):
    print("\n========================")
    print("📌 CÁC LUẬT ĐÃ KÍCH HOẠT")
    print("========================")
    for r in fired_rules:
        print(f" - {r}")

    print("\n========================")
    print("🏁 KẾT LUẬN CUỐI CÙNG")
    print("========================")

    conclusions = []

    # 1) Chẩn đoán Hen phế quản
    if facts["f504"]["value"]:
        conclusions.append("🟢 **Chẩn đoán: Hen phế quản xác định**")

    elif facts["f501"]["value"]:
        conclusions.append("🟡 **Nghi ngờ hen phế quản (L1 thỏa)** – cần thêm xét nghiệm FEV1/FVC, test hồi phục hoặc kích thích.")

    # 2) Luật L4 (xác định hen khi có thuốc + test)
    if facts["f504"]["value"] and (facts["f301"]["value"] or facts["f302"]["value"]):
        conclusions.append("🟢 **Đã điều trị ICS/LABA nhưng triệu chứng còn → phù hợp Hen phế quản.**")

    # 3) Phân biệt bệnh khác (L5-x)
    diff = {
        "f509": "COPD",
        "f510": "Suy tim trái",
        "f511": "Hẹp/dị vật khí – phế quản",
        "f512": "GERD hoặc rò khí-thực quản",
        "f513": "Giãn phế quản"
    }

    for fid, label in diff.items():
        if facts[fid]["value"]:
            conclusions.append(f"🔴 **Có dấu hiệu gợi ý {label}** — cần kiểm tra thêm để loại trừ.")

    # 4) Kiểm soát điều trị (L6, L7)
    if facts["f506"]["value"]:
        conclusions.append("⬆ **Hen không kiểm soát → Cần tăng bậc điều trị.**")
    if facts["f505"]["value"]:
        conclusions.append("⬇ **Hen kiểm soát tốt → Có thể giảm bậc điều trị.**")

    # 5) Trường hợp không có kết luận
    if not conclusions:
        conclusions.append("⚠ **Chưa đủ dữ liệu để đưa ra kết luận rõ ràng.**")

    for c in conclusions:
        print(" - " + c)
def auto_compute_logic(facts):
    symptoms = ["f101", "f102", "f103", "f104"]
    count = sum(1 for s in symptoms if facts[s]["value"])
    if count >= 2:
        facts["f501"]["value"] = True

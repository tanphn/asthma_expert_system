# modules/follow_up.py

def collect_control_questions(wm):
    print("\n=== BƯỚC 1: ĐÁNH GIÁ KIỂM SOÁT TRIỆU CHỨNG ===")

    control_questions = {
        "f301": "Có bị triệu chứng ban ngày ≥ 2 lần/tuần? (y/n): ",
        "f302": "Có thức giấc do hen trong đêm? (y/n): ",
        "f303": "Có phải dùng thuốc cắt cơn ≥ 2 lần/tuần? (y/n): ",
        "f304": "Có hạn chế hoạt động vì hen? (y/n): "
    }

    for fid, q in control_questions.items():
        ans = input(q).strip().lower()
        wm.set(fid, ans == "y")

    return wm


def classify_control_level(wm):
    print("\n=== BƯỚC 2: PHÂN LOẠI MỨC ĐỘ KIỂM SOÁT ===")

    score = sum([
        wm.get("f301"),
        wm.get("f302"),
        wm.get("f303"),
        wm.get("f304")
    ])

    if score == 0:
        level = "Kiểm soát hoàn toàn"
    elif score <= 2:
        level = "Kiểm soát một phần"
    else:
        level = "Không kiểm soát"

    print(f"➡️ Mức độ kiểm soát: {level}")
    return level


def run_follow_up(wm):
    print("\n================ TÁI KHÁM ================")

    collect_control_questions(wm)
    classify_control_level(wm)

    print("\n🎉 HOÀN THÀNH TÁI KHÁM\n")

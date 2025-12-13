import streamlit as st
import pandas as pd

# =========================
# Giả sử WorkingMemory + facts đã có sẵn
# =========================
class WorkingMemory:
    def __init__(self, facts):
        self.facts = facts
        self.values = {}

    def reset(self):
        self.values = {}

    def set(self, fid, value):
        self.values[fid] = value

    def get(self, fid):
        return self.values.get(fid, False)

# Hàm nhập boolean
def st_boolean(label):
    return st.checkbox(label)

# Hàm nhập float
def st_float(label, allow_empty=False):
    val = st.text_input(label)
    if val.strip() == "" and allow_empty:
        return None
    try:
        return float(val)
    except:
        return None

# =========================
# Cấu hình facts
# =========================
facts = {}  # tạm thời rỗng, bạn có thể load facts chi tiết nếu cần
wm = WorkingMemory(facts)
wm.reset()

# =========================
# Chọn mode
# =========================
mode = st.selectbox("Chọn chế độ", ["Khám lần đầu", "Tái khám"])

# =========================
# KHÁM LẦN ĐẦU
# =========================
if mode == "Khám lần đầu":
    st.title("🫁 Hệ thống hỗ trợ chẩn đoán Hen phế quản - Khám lần đầu")

    # ---------- MODULE 1: TRIỆU CHỨNG ----------
    st.header("1️⃣ Thu thập triệu chứng")
    col1, col2 = st.columns(2)
    with col1:
        wm.set("f101", st_boolean("Ho, kéo dài hoặc từng cơn?"))
        wm.set("f102", st_boolean("Khò khè khi thở ra?"))
    with col2:
        wm.set("f103", st_boolean("Khó thở / thở gấp?"))
        wm.set("f104", st_boolean("Cảm giác nặng ngực?"))

    st.write("### Yếu tố tăng khả năng hen")
    wm.set("f105", st_boolean("Triệu chứng thay đổi theo thời gian hoặc có triggers?"))
    wm.set("f106", st_boolean("Triệu chứng nặng hơn về đêm?"))
    wm.set("f107", st_boolean("Triệu chứng nặng khi gắng sức?"))

    # Rule L1
    main_count = sum(1 for f in ["f101","f102","f103","f104"] if wm.get(f))
    l1_pass = False
    if main_count >= 2 and (wm.get("f105") or wm.get("f106") or wm.get("f107")):
        wm.set("f501", True)
        wm.set("f503", True)
        st.success("✔ L1 thỏa → Nghi ngờ hen")
        l1_pass = True
    else:
        st.error("✖ L1 KHÔNG thỏa → Không đủ triệu chứng nghi ngờ hen")

    # Nếu L1 fail → MODULE L5-x
    if not l1_pass:
        st.header("🔍 Phân biệt bệnh khác (L5-x)")
        colA, colB = st.columns(2)
        with colA:
            wm.set("f401", st_boolean("Tiền sử hút thuốc?"))
            wm.set("f404", st_boolean("Tiền sử COPD?"))
            wm.set("f405", st_boolean("Tiền sử suy tim trái / THA?"))
            wm.set("f115", st_boolean("Ho khạc đờm mủ nhiều năm?"))
        with colB:
            wm.set("f111", st_boolean("Có ran ẩm?"))
            wm.set("f112", st_boolean("Tiếng rít cố định?"))
            wm.set("f113", st_boolean("Không đáp ứng giãn phế quản?"))
            wm.set("f114", st_boolean("Ho/khó thở tăng khi nằm hoặc ăn uống?"))
        st.warning("Không thể chẩn đoán hen → cần xét bệnh khác")
        if wm.get("f401") and wm.get("f115"): st.error("🚨 Gợi ý COPD")
        if wm.get("f111") and wm.get("f405"): st.error("🚨 Gợi ý suy tim trái")
        if wm.get("f112") and wm.get("f113"): st.error("🚨 Gợi ý hẹp/dị vật phế quản")
        if wm.get("f114"): st.error("🚨 Gợi ý GERD / rò khí-thực quản")
        st.stop()

    # ---------- MODULE 2: XÉT NGHIỆM ----------
    st.header("2️⃣ Xét nghiệm")
    fev1_fvc = st_float("FEV1/FVC (VD: 0.72)", allow_empty=True)
    if fev1_fvc is not None and fev1_fvc < 0.75: wm.set("f201", True)
    fev1_pct = st_float("% tăng FEV1 sau giãn (VD: 12)", allow_empty=True)
    if fev1_pct is not None and fev1_pct >= 12: wm.set("f202", True)
    pef_var = st_float("Biến thiên PEF (%)", allow_empty=True)
    if pef_var is not None and pef_var > 10: wm.set("f203", True)
    wm.set("f204", st_boolean("Test hồi phục phế quản dương tính?"))
    wm.set("f205", st_boolean("Test kích thích phế quản dương tính?"))

    if wm.get("f201") or wm.get("f202") or wm.get("f203"):
        wm.set("f502", True)
        st.success("✔ L2 thỏa: Có bằng chứng rối loạn thông khí tắc nghẽn biến đổi")
    else:
        st.warning("⚠ L2 không thỏa — Chưa có bằng chứng xét nghiệm rõ ràng")

    if wm.get("f501") and wm.get("f502"):
        wm.set("f504", True)
        st.success("✔ L3 thỏa → Chẩn đoán hen xác định")

    if (wm.get("f301") or wm.get("f302")) and (wm.get("f204") or wm.get("f205")):
        wm.set("f504", True)
        st.success("✔ L4 thỏa → Hen xác định (test dương dù đang điều trị)")

    # ---------- MODULE 3: SEVERITY ----------
    st.header("3️⃣ Đánh giá mức độ nặng")
    wm.set("f120", st.number_input("Số ngày/tuần có triệu chứng (0–7)", min_value=0, max_value=7, value=0))
    wm.set("f121", st.number_input("Số lần/tuần triệu chứng ban đêm", min_value=0, max_value=7, value=0))
    wm.set("f122", st.selectbox("Giới hạn hoạt động (0=không,1=nhẹ,2=nhiều)", [0,1,2]))
    wm.set("f123", st.number_input("Số lần dùng SABA/tuần", min_value=0, max_value=60, value=0))
    wm.set("f124", st.number_input("Số đợt cấp năm qua",  min_value=0, max_value=7, value=0))
    wm.set("f208", st.number_input("FEV1 (%) — hoặc 999 nếu không có", min_value=0, max_value=1500, value=999))
    wm.set("f209", st.number_input("PEF variability (%) — hoặc 999 nếu không có", min_value=0, max_value=1500, value=999))

    # Suspected & Confirmed
    suspected = any([wm.get("f120")>0, wm.get("f121")>0, wm.get("f123")>0])
    wm.set("f501", suspected)
    confirmed = (wm.get("f208") != 999 or wm.get("f209") != 999)
    wm.set("f504", confirmed)

    # Severity
    f120, f121, f123, f124 = wm.get("f120"), wm.get("f121"), wm.get("f123"), wm.get("f124")
    for f in ["f601","f602","f603","f604"]: wm.set(f, False)
    if f120>=5 or f121>=3 or f123>=12: wm.set("f604", True)   # Hen dai dẳng nặng
    elif f120>=3 or f121>=2 or f123>=8: wm.set("f603", True)  # Hen dai dẳng trung bình
    elif f120>=1 or f121>=1 or f123>=4: wm.set("f602", True)  # Hen dai dẳng nhẹ
    else: wm.set("f601", True)                                 # Hen gián đoạn

    # ---------- MODULE 4: KẾT LUẬN ----------
    st.header("4️⃣ Kết luận")
    if not wm.get("f501"): st.error("❌ Không đủ tiêu chuẩn nghi ngờ hen.")
    else: st.success("✔ Nghi ngờ hen")

    if wm.get("f504"): st.success("✔ Chẩn đoán: Hen phế quản xác định")
    else: st.warning("⚠ Thiếu xét nghiệm → Chỉ nghi ngờ hen")

    if wm.get("f604"): st.info("🌡 Hen dai dẳng nặng")
    elif wm.get("f603"): st.info("🌡 Hen dai dẳng trung bình")
    elif wm.get("f602"): st.info("🌡 Hen dai dẳng nhẹ")
    elif wm.get("f601"): st.info("🌡 Hen gián đoạn")

    # ---------- MODULE 5: BẬC ĐIỀU TRỊ ----------
    st.header("5️⃣ Bậc điều trị")
    f601, f602, f603, f604 = wm.get("f601"), wm.get("f602"), wm.get("f603"), wm.get("f604")
    f116, f117, f118 = False, False, False  # tiền sử thuốc nếu có thể thêm input
    # f124 là số đợt cấp năm qua, đã lấy trên input

    # Logic Step dựa trên severity + số đợt cấp
    if f601: step=1
    elif f602: step=2
    elif f603: step=3
    elif f604:
        if f124 >= 2: step=5
        else: step=4
    else: step=1

    st.subheader(f"➡ Bậc điều trị đề xuất: Step {step}")

    # ---------- BẢNG 1: Thuốc kiểm soát theo 5 bậc ----------
    st.markdown("### BẢNG 1 — THUỐC KIỂM SOÁT HEN THEO 5 BẬC")
    df1 = pd.DataFrame({
        "Thuốc điều trị kiểm soát ưu tiên": [
            "Liều thấp ICS–formoterol khi cần",
            "Duy trì liều thấp ICS hoặc ICS–formoterol khi cần",
            "Duy trì liều thấp ICS–LABA",
            "Duy trì liều trung bình ICS–LABA",
            "Bổ sung LAMA; đánh giá kiểu hình hen ± kháng IgE/IL5/IL4R; xem xét ICS–LABA liều cao"
        ],
        "Thuốc điều trị kiểm soát khác": [
            "Liều thấp ICS mỗi khi dùng SABA",
            "Liều thấp ICS khi dùng SABA hoặc LTRA ngày hoặc SLIT mạt bụi nhà",
            "Liều trung bình ICS hoặc thêm LTRA hoặc SLIT",
            "Thêm LAMA hoặc LTRA, hoặc chuyển liều cao ICS",
            "Azithromycin (người lớn), LTRA; có thể OCS liều thấp"
        ]
    }, index=[1,2,3,4,5])

    st.table(df1)

    # ---------- BẢNG 2: Thuốc cắt cơn & ghi chú ----------
    st.markdown("### BẢNG 2 — THUỐC CẮT CƠN & GHI CHÚ")
    st.markdown("""
    **Thuốc cắt cơn:**  
    - ICS–formoterol liều thấp khi cần  
    - SABA khi cần ở bệnh nhân dùng ICS hoặc ICS/LABA  

    **Xem xét khi dùng SABA:** Kiểm tra tuân thủ thuốc kiểm soát hằng ngày  

    **SLIT (mạt bụi nhà):** Chỉ định khi hen + viêm mũi dị ứng, FEV1 > 70%, không kiểm soát với ICS thấp–trung bình
    """)
    st.markdown("### Nâng/hạ bậc điều trị")
    st.markdown("""
    **Nâng bậc dài hạn (≥2–3 tháng):** Triệu chứng do hen, tuân thủ tốt, kỹ thuật hít đúng → đánh giá lại sau 2–3 tháng  
    **Nâng bậc ngắn hạn (1–2 tuần):** Nhiễm virus, kích phát theo mùa, dị nguyên → theo kế hoạch hành động  
    **Điều chỉnh theo ngày (SMART):** Dùng ICS–formoterol duy trì + cắt cơn → điều chỉnh số liều mỗi ngày tùy triệu chứng  

    **Hạ bậc điều trị:**  
    - Bậc 5 → giảm liều OCS hoặc thay bằng ICS cao  
    - Bậc 4 → giảm 50% liều ICS hoặc chuyển ICS–formoterol về liều thấp  
    - Bậc 3 → giảm liều về 1 lần/ngày  
    - Bậc 2 → dùng ICS 1 lần/ngày hoặc chuyển ICS–formoterol khi cần
    """)

# =========================
# TÁI KHÁM
# =========================
else:
    st.title("🫁 Hệ thống hỗ trợ chẩn đoán Hen phế quản - Tái khám")
    st.header("1️⃣ Nhập dữ liệu kiểm soát triệu chứng")
    days_symptom = st.number_input("Số lần có triệu chứng ban ngày trong tuần", min_value=0, max_value=7, value=0)
    nights_symptom = st.number_input("Số lần tỉnh giấc ban đêm do hen", min_value=0, max_value=7, value=0)
    saba_use = st.number_input("Số lần dùng thuốc cắt cơn (SABA) trong tuần", min_value=0, max_value=20, value=0)
    activity_limit = st.selectbox("Hạn chế hoạt động do hen", [0,1,2])

    st.header("2️⃣ Bậc điều trị hiện tại")
    current_step = st.selectbox("Chọn bậc điều trị hiện tại", [1,2,3,4,5], index=0)

    # Lưu vào WM
    wm.set("f301", days_symptom>=2)
    wm.set("f302", nights_symptom>=1)
    wm.set("f303", saba_use>=2)
    wm.set("f304", activity_limit>=1)
    wm.set("f124", current_step)

    if st.button("📌 ĐÁNH GIÁ KIỂM SOÁT"):
        score = sum([wm.get(f) for f in ["f301","f302","f303","f304"]])
        if score==0:
            level="Kiểm soát hoàn toàn"
            suggested_step=max(1, current_step-1)
        elif score<=2:
            level="Kiểm soát một phần"
            suggested_step=current_step
        else:
            level="Không kiểm soát"
            suggested_step=min(5, current_step+1)

        st.success(f"➡️ Mức độ kiểm soát: {level}")
        st.info(f"➡️ Bậc điều trị gợi ý: Step {suggested_step}")
        st.info("🎉 Hoàn thành đánh giá tái khám!")

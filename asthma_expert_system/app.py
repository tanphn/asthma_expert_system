# asthma_expert_system/app.py
"""
HỆ THỐNG HỖ TRỢ RA QUYẾT ĐỊNH LÂM SÀNG CHẨN ĐOÁN & QUẢN LÝ HEN PHẾ QUẢN
(Clinical Decision Support System - Asthma CDSS • GINA 2023/2024 Guidelines)
Giao diện Chuyên nghiệp, Tích hợp Động cơ Suy diễn, Tính toán Độ tin cậy CF & Kế hoạch Hành động.
"""

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Import core modules
from engine.wm import WorkingMemory
from kb.facts_def import FACTS_DEF
from kb.medications_db import GINA_TRACKS_INFO, MEDICATIONS_DB, ICS_DOSE_EQUIVALENTS, INHALER_DEVICES
from modules.initial_assessment import process_initial_assessment
from modules.follow_up import process_follow_up
from modules.action_plan import generate_action_plan
from modules.inhaler_technique import audit_inhaler_technique
from modules.patient_cases import PATIENT_CASES
from utils.report_generator import generate_medical_report_html

# ==========================================
# CẤU HÌNH TRANG & GIAO DIỆN CAO CẤP
# ==========================================
st.set_page_config(
    page_title="Asthma CDSS - Hệ Thống Chuyên Gia Hen Phế Quản",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS phong cách y tế cao cấp (Clinical Glassmorphism)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0369A1 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    
    .diag-banner-success {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 6px solid #10B981;
        padding: 16px 20px;
        border-radius: 10px;
        color: #065F46;
        margin-bottom: 16px;
    }
    
    .diag-banner-warning {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 6px solid #F59E0B;
        padding: 16px 20px;
        border-radius: 10px;
        color: #92400E;
        margin-bottom: 16px;
    }
    
    .diag-banner-danger {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 6px solid #EF4444;
        padding: 16px 20px;
        border-radius: 10px;
        color: #991B1B;
        margin-bottom: 16px;
    }
    
    .drug-card {
        border: 1px solid #E0F2FE;
        background: #F8FAFC;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 10px 18px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo Working Memory trong Session State
if "wm" not in st.session_state:
    st.session_state.wm = WorkingMemory(FACTS_DEF)

if "patient_name" not in st.session_state:
    st.session_state.patient_name = "Nguyễn Văn A"
if "patient_age" not in st.session_state:
    st.session_state.patient_age = 30
if "patient_gender" not in st.session_state:
    st.session_state.patient_gender = "Nam"

# ==========================================
# SIDEBAR: ĐIỀU HƯỚNG & NẠP CA LÂM SÀNG
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("🫁 Asthma CDSS v2.5")
    st.caption("Clinical Decision Support System • GINA Guidelines")
    st.divider()

    # Chọn chế độ làm việc
    mode = st.radio(
        "📌 Chọn Phân Hệ Làm Việc:",
        [
            "🩺 Khám Lần Đầu (Initial Assessment)",
            "🔄 Tái Khám & Theo Dõi (Follow-Up GINA)",
            "📋 Kế Hoạch Hành Động (Action Plan)",
            "💨 Kiểm Tra Kỹ Thuật Hít (Inhaler Audit)",
            "🧭 Cây Suy Luận Logic (Inference Audit)",
            "💊 Tra Cứu Thuốc & Bảng Liều GINA"
        ]
    )

    st.divider()
    st.subheader("🧪 Thử Nghiệm 1-Click: 6 Ca Bệnh Mẫu")
    selected_case_id = st.selectbox(
        "Nạp dữ liệu bệnh nhân thực tế:",
        ["-- Tự nhập dữ liệu mới --"] + [c["title"] for c in PATIENT_CASES]
    )

    if selected_case_id != "-- Tự nhập dữ liệu mới --":
        target_case = next((c for c in PATIENT_CASES if c["title"] == selected_case_id), None)
        if target_case:
            if st.button("🚀 Nạp Dữ Liệu Ca Bệnh", use_container_width=True):
                st.session_state.wm.reset()
                st.session_state.wm.load_dict(target_case["facts"])
                st.session_state.patient_name = target_case["patient_name"]
                st.session_state.patient_age = target_case["age"]
                st.session_state.patient_gender = target_case["gender"]
                st.success(f"Đã nạp: **{target_case['patient_name']}**!")
                st.rerun()

    st.divider()
    if st.button("🔄 Đặt lại toàn bộ dữ liệu (Reset WM)", use_container_width=True):
        st.session_state.wm.reset()
        st.success("Đã làm mới Working Memory!")
        st.rerun()

# ==========================================
# BANNER TIÊU ĐỀ CHÍNH
# ==========================================
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: white;">Hệ Thống Chuyên Gia Chẩn Đoán & Quản Lý Hen Phế Quản</h1>
            <p style="margin: 4px 0 0 0; opacity: 0.85; font-size: 0.95rem;">
                Hỗ trợ ra quyết định lâm sàng (CDSS) • Chuẩn hóa theo GINA 2023/2024 & Phác đồ Bộ Y Tế
            </p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 10px;">
            <div style="font-size: 0.8rem; opacity: 0.8;">ĐỘNG CƠ SUY DIỄN</div>
            <div style="font-weight: 700; font-size: 1rem; color: #38BDF8;">Forward Chaining + CF</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Thông tin hành chính bệnh nhân nhanh
with st.expander("👤 Thông tin hành chính bệnh nhân", expanded=False):
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.session_state.patient_name = st.text_input("Họ và tên", value=st.session_state.patient_name)
    with col_p2:
        st.session_state.patient_age = st.number_input("Tuổi", min_value=1, max_value=120, value=st.session_state.patient_age)
        st.session_state.wm.set("f001", st.session_state.patient_age)
    with col_p3:
        st.session_state.patient_gender = st.selectbox("Giới tính", ["Nam", "Nữ"], index=0 if st.session_state.patient_gender == "Nam" else 1)
        st.session_state.wm.set("f002", st.session_state.patient_gender)
    with col_p4:
        bmi_val = st.number_input("Chỉ số BMI (kg/m²)", min_value=10.0, max_value=60.0, value=float(st.session_state.wm.get("f005", 22.0) or 22.0))
        st.session_state.wm.set("f005", bmi_val)


# ==============================================================================
# PHÂN HỆ 1: KHÁM LẦN ĐẦU (INITIAL ASSESSMENT)
# ==============================================================================
if mode == "🩺 Khám Lần Đầu (Initial Assessment)":
    st.subheader("🩺 Khám Lần Đầu: Chẩn Đoán Xác Định, Phân Loại Mức Độ & Khởi Đầu Điều Trị")

    tab_sym, tab_lab, tab_diff, tab_res = st.tabs([
        "1️⃣ Triệu Chứng & Tiền Sử",
        "2️⃣ Thăm Dò Chức Năng Phổi",
        "3️⃣ Yếu Tố Nguy Cơ & Bệnh Đồng Mắc",
        "📊 KẾT QUẢ ĐÁNH GIÁ & PHÁC ĐỒ GINA"
    ])

    with tab_sym:
        st.markdown("#### A. Bốn Triệu Chứng Hô Hấp Chính (Cardinal Symptoms)")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            f101 = st.checkbox("Ho kéo dài hoặc từng cơn (f101)", value=bool(st.session_state.wm.get("f101")))
            st.session_state.wm.set("f101", f101)
            f102 = st.checkbox("Khò khè khi thở ra (Wheezing) (f102)", value=bool(st.session_state.wm.get("f102")))
            st.session_state.wm.set("f102", f102)
        with col_s2:
            f103 = st.checkbox("Khó thở / Thở hụt hơi từng cơn (f103)", value=bool(st.session_state.wm.get("f103")))
            st.session_state.wm.set("f103", f103)
            f104 = st.checkbox("Cảm giác nặng ngực / Co thắt lồng ngực (f104)", value=bool(st.session_state.wm.get("f104")))
            st.session_state.wm.set("f104", f104)

        st.markdown("#### B. Đặc Điểm Biến Đổi & Yếu Tố Khởi Phát (Variability & Triggers)")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            f105 = st.checkbox("Triệu chứng thay đổi theo thời gian & cường độ (f105)", value=bool(st.session_state.wm.get("f105")))
            st.session_state.wm.set("f105", f105)
            f106 = st.checkbox("Triệu chứng nặng hơn về đêm hoặc sáng sớm (f106)", value=bool(st.session_state.wm.get("f106")))
            st.session_state.wm.set("f106", f106)
        with col_v2:
            f107 = st.checkbox("Khởi phát khi gắng sức / cười to (f107)", value=bool(st.session_state.wm.get("f107")))
            st.session_state.wm.set("f107", f107)
            f108 = st.checkbox("Khởi phát sau nhiễm virus hô hấp / cảm cúm (f108)", value=bool(st.session_state.wm.get("f108")))
            st.session_state.wm.set("f108", f108)

        st.markdown("#### C. Đánh Giá Mức Độ Nặng Ban Đầu (Tần suất triệu chứng)")
        col_sev1, col_sev2, col_sev3 = st.columns(3)
        with col_sev1:
            f120 = st.slider("Số ngày/tuần có triệu chứng (0-7)", 0, 7, int(st.session_state.wm.get("f120", 0) or 0))
            st.session_state.wm.set("f120", f120)
            f121 = st.slider("Số lần thức giấc ban đêm do hen/tuần (0-7)", 0, 7, int(st.session_state.wm.get("f121", 0) or 0))
            st.session_state.wm.set("f121", f121)
        with col_sev2:
            f122 = st.selectbox("Mức độ giới hạn hoạt động thể lực", [0, 1, 2], index=int(st.session_state.wm.get("f122", 0) or 0), format_func=lambda x: "0: Không giới hạn" if x==0 else ("1: Hạn chế nhẹ" if x==1 else "2: Hạn chế nhiều"))
            st.session_state.wm.set("f122", f122)
            f123 = st.number_input("Số lần dùng thuốc cắt cơn SABA/tuần", 0, 50, int(st.session_state.wm.get("f123", 0) or 0))
            st.session_state.wm.set("f123", f123)
        with col_sev3:
            f124 = st.number_input("Số đợt cấp cần Corticoid toàn thân trong năm qua", 0, 10, int(st.session_state.wm.get("f124", 0) or 0))
            st.session_state.wm.set("f124", f124)

    with tab_lab:
        st.markdown("#### A. Hô Hấp Ký & Lưu Lượng Đỉnh PEF (Spirometry & Peak Flow)")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            f201_val = st.number_input("Chỉ số FEV1/FVC (ví dụ: 0.72) [Để trống/0 nếu chưa đo]", 0.0, 1.0, float(st.session_state.wm.get("f201") or 0.0), step=0.01)
            st.session_state.wm.set("f201", f201_val if f201_val > 0 else None)

            f202_val = st.number_input("% Tăng FEV1 sau test giãn phế quản (ΔFEV1 %)", 0.0, 100.0, float(st.session_state.wm.get("f202") or 0.0), step=1.0)
            st.session_state.wm.set("f202", f202_val if f202_val > 0 else None)

            f203_val = st.number_input("Thể tích FEV1 tăng tuyệt đối (mL)", 0.0, 2000.0, float(st.session_state.wm.get("f203") or 0.0), step=50.0)
            st.session_state.wm.set("f203", f203_val if f203_val > 0 else None)

        with col_l2:
            f204_val = st.number_input("Độ biến thiên lưu lượng đỉnh PEF ngày (%)", 0.0, 100.0, float(st.session_state.wm.get("f204") or 0.0), step=1.0)
            st.session_state.wm.set("f204", f204_val if f204_val > 0 else None)

            f205_val = st.number_input("FEV1 % so với giá trị dự đoán (% Predicted)", 0.0, 150.0, float(st.session_state.wm.get("f205") or 0.0), step=1.0)
            st.session_state.wm.set("f205", f205_val if f205_val > 0 else None)

            f207 = st.checkbox("Kết luận Test hồi phục phế quản (BDR) Dương Tính", value=bool(st.session_state.wm.get("f207")))
            st.session_state.wm.set("f207", f207)

        st.markdown("#### B. Dấu Ấn Sinh Học & Phân Loại Kiểu Hình (Biomarkers & Phenotypes)")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            f208_val = st.number_input("Nồng độ FeNO khí thở ra (ppb)", 0.0, 200.0, float(st.session_state.wm.get("f208") or 0.0), step=1.0)
            st.session_state.wm.set("f208", f208_val if f208_val > 0 else None)
        with col_b2:
            f209_val = st.number_input("Bạch cầu ái toan máu ngoại vi (Eosinophils/µL)", 0.0, 2000.0, float(st.session_state.wm.get("f209") or 0.0), step=50.0)
            st.session_state.wm.set("f209", f209_val if f209_val > 0 else None)

    with tab_diff:
        st.markdown("#### Dấu Hiệu Phân Biệt Các Bệnh Lý Hô Hấp & Tim Mạch Khác")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            f401 = st.checkbox("Tiền sử hút thuốc lá/thuốc lào ≥ 10 gói-năm (f401)", value=bool(st.session_state.wm.get("f401")))
            st.session_state.wm.set("f401", f401)
            f404 = st.checkbox("Tiền sử đã được chẩn đoán COPD (f404)", value=bool(st.session_state.wm.get("f404")))
            st.session_state.wm.set("f404", f404)
            f109 = st.checkbox("Ho khạc đờm mủ nhiều năm (Nghi Giãn PQ/COPD) (f109)", value=bool(st.session_state.wm.get("f109")))
            st.session_state.wm.set("f109", f109)
            f113 = st.checkbox("Khó thở liên tục tiến triển tăng dần theo tuổi (f113)", value=bool(st.session_state.wm.get("f113")))
            st.session_state.wm.set("f113", f113)

        with col_d2:
            f405 = st.checkbox("Tiền sử Tăng huyết áp / Bệnh tim mạch / Suy tim (f405)", value=bool(st.session_state.wm.get("f405")))
            st.session_state.wm.set("f405", f405)
            f110 = st.checkbox("Khám nghe phổi có Ran ẩm 2 đáy (Nghi Hen tim) (f110)", value=bool(st.session_state.wm.get("f110")))
            st.session_state.wm.set("f110", f110)
            f111 = st.checkbox("Tiếng rít thanh quản cố định khu trú (Stridor / Nghi VCD) (f111)", value=bool(st.session_state.wm.get("f111")))
            st.session_state.wm.set("f111", f111)
            f112 = st.checkbox("Ho/khó thở tăng khi nằm ngửa hoặc sau ăn no (Nghi GERD) (f112)", value=bool(st.session_state.wm.get("f112")))
            st.session_state.wm.set("f112", f112)

    with tab_res:
        # Xử lý đánh giá
        result = process_initial_assessment(st.session_state.wm)
        diag = result["diagnosis"]
        sev = result["severity"]
        tx = result["treatment"]

        # Banner chẩn đoán
        banner_class = "diag-banner-success" if diag["is_confirmed"] else ("diag-banner-warning" if diag["is_suspected"] else "diag-banner-danger")
        st.markdown(f"""
        <div class="{banner_class}">
            <h2 style="margin: 0; font-size: 1.3rem;">{diag['main_title']}</h2>
            <div style="font-size: 1rem; margin-top: 6px;">
                <strong>Mức độ nặng ban đầu:</strong> {sev['label']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            st.markdown("### 📊 Xác Suất Chẩn Đoán Phân Biệt")
            diff_data = result["differential_ranking"]
            df_diff = pd.DataFrame(diff_data)
            
            # Biểu đồ cột ngang
            chart = alt.Chart(df_diff).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
                x=alt.X('probability:Q', title='Xác suất phù hợp (%)', scale=alt.Scale(domain=[0, 100])),
                y=alt.Y('name:N', sort='-x', title=None),
                color=alt.Color('color:N', scale=None),
                tooltip=['name', 'probability', 'level']
            ).properties(height=260)
            st.altair_chart(chart, use_container_width=True)

            for d in diff_data[:3]:
                with st.container():
                    st.markdown(f"**{d['name']}**: `{d['probability']}% ({d['level']})`")
                    if d.get('key_factors'):
                        st.caption("Dấu hiệu: " + "; ".join(d['key_factors']))

        with col_r2:
            st.markdown(f"### 💊 Phác Đồ Đề Xuất: {tx['step_title']}")
            
            # Track 1 card
            t1 = tx["track1_preferred"]
            st.markdown(f"""
            <div class="drug-card" style="border-left: 5px solid #0284C7; background: #F0F9FF;">
                <div style="font-weight: 700; color: #0369A1; font-size: 1rem;">⭐ LỘ TRÌNH 1 (ƯU TIÊN - GINA SMART / MART)</div>
                <div style="margin-top: 6px; font-weight: 600; font-size: 1.05rem; color: #0F172A;">{t1.get('controller_and_reliever', 'ICS-formoterol khi cần')}</div>
                <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">{t1.get('notes', '')}</div>
                <div style="font-size: 0.85rem; color: #0284C7; margin-top: 4px;"><strong>Biệt dược phổ biến:</strong> {', '.join(t1.get('brand_examples', []))}</div>
            </div>
            """, unsafe_allow_html=True)

            # Track 2 card
            t2 = tx["track2_alternative"]
            st.markdown(f"""
            <div class="drug-card" style="border-left: 5px solid #8B5CF6; background: #FAF5FF;">
                <div style="font-weight: 700; color: #7C3AED; font-size: 1rem;">🔄 LỘ TRÌNH 2 (THAY THẾ - ALTERNATIVE)</div>
                <div style="margin-top: 6px; font-size: 0.95rem; color: #0F172A;"><strong>Duy trì:</strong> {t2.get('controller', t2.get('controller_and_reliever', 'ICS liều thấp'))}</div>
                <div style="font-size: 0.95rem; color: #0F172A; margin-top: 2px;"><strong>Cắt cơn:</strong> {t2.get('reliever', 'SABA (Salbutamol 100mcg)')}</div>
                <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">{t2.get('notes', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.subheader("🖨️ Xuất Bệnh Án & Phiếu Khám")
        patient_dict = {
            "name": st.session_state.patient_name,
            "age": st.session_state.patient_age,
            "gender": st.session_state.patient_gender,
            "bmi": st.session_state.wm.get("f005", 22.0)
        }
        report_html = generate_medical_report_html(patient_dict, result, mode="Khám lần đầu")
        st.download_button(
            "📥 Tải Phiếu Khám Bệnh (HTML Print-Ready)",
            data=report_html,
            file_name=f"Phieu_Kham_Hen_{st.session_state.patient_name.replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True
        )


# ==============================================================================
# PHÂN HỆ 2: TÁI KHÁM & THEO DÕI (FOLLOW-UP GINA)
# ==============================================================================
elif mode == "🔄 Tái Khám & Theo Dõi (Follow-Up GINA)":
    st.subheader("🔄 Tái Khám: Đánh Giá Mức Độ Kiểm Soát Triệu Chứng & Điều Chỉnh Bậc")

    col_fu1, col_fu2 = st.columns([1, 1])

    with col_fu1:
        st.markdown("#### 1️⃣ Đánh Giá Kiểm Soát Triệu Chứng Trong 4 Tuần Qua (GINA Tool)")
        q1 = st.checkbox("Có triệu chứng ban ngày > 2 lần/tuần (GINA Q1)", value=bool(st.session_state.wm.get("f701")))
        st.session_state.wm.set("f701", q1)

        q2 = st.checkbox("Có thức giấc ban đêm do hen (GINA Q2)", value=bool(st.session_state.wm.get("f702")))
        st.session_state.wm.set("f702", q2)

        q3 = st.checkbox("Cần dùng thuốc cắt cơn > 2 lần/tuần (GINA Q3)", value=bool(st.session_state.wm.get("f703")))
        st.session_state.wm.set("f703", q3)

        q4 = st.checkbox("Có bị giới hạn hoạt động thể lực do hen (GINA Q4)", value=bool(st.session_state.wm.get("f704")))
        st.session_state.wm.set("f704", q4)

        st.markdown("#### 2️⃣ Bậc Điều Trị Hiện Tại & Đánh Giá Tuân Thủ")
        current_step = st.selectbox("Bậc điều trị GINA bệnh nhân đang dùng:", [1, 2, 3, 4, 5], index=int(st.session_state.wm.get("f310", 2) or 2) - 1)
        st.session_state.wm.set("f310", current_step)

        f414 = st.checkbox("Kém tuân thủ / Quên xịt thuốc kiểm soát duy trì (f414)", value=bool(st.session_state.wm.get("f414")))
        st.session_state.wm.set("f414", f414)

        f415 = st.checkbox("Phát hiện lỗi sai trong kỹ thuật hít bình xịt (f415)", value=bool(st.session_state.wm.get("f415")))
        st.session_state.wm.set("f415", f415)

    with col_fu2:
        st.markdown("#### 📊 Kết Quả Đánh Giá & Quyết Định Lâm Sàng")
        fu_res = process_follow_up(st.session_state.wm)
        ctrl = fu_res["control_assessment"]
        tx_dec = fu_res["treatment_decision"]

        # Card kết quả kiểm soát
        st.markdown(f"""
        <div style="background: {ctrl['color']}15; border-left: 6px solid {ctrl['color']}; padding: 16px; border-radius: 10px; margin-bottom: 16px;">
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: {ctrl['color']};">ĐÁNH GIÁ KIỂM SOÁT (ĐIỂM: {ctrl['score']}/4)</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-top: 4px;">{ctrl['level']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Card quyết định điều trị
        st.markdown(f"""
        <div class="drug-card" style="border: 2px solid #0EA5E9;">
            <div style="font-weight: 700; color: #0369A1; font-size: 1.1rem;">🎯 {tx_dec['action_title']}</div>
            <ul style="margin-top: 8px; padding-left: 20px; font-size: 0.95rem; color: #334155;">
                {''.join([f"<li>{adv}</li>" for adv in tx_dec['clinical_advice']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Yếu tố nguy cơ tương lai
        if fu_res["future_risks"]:
            st.markdown("##### ⚠️ Yếu Tố Nguy Cơ Đợt Cấp Tương Lai Được Phát Hiện:")
            for risk in fu_res["future_risks"]:
                st.warning(f"• {risk}")

    st.divider()
    patient_dict = {
        "name": st.session_state.patient_name,
        "age": st.session_state.patient_age,
        "gender": st.session_state.patient_gender,
        "bmi": st.session_state.wm.get("f005", 22.0)
    }
    report_html = generate_medical_report_html(patient_dict, fu_res, mode="Tái khám")
    st.download_button(
        "📥 Tải Phiếu Tái Khám Bệnh (HTML)",
        data=report_html,
        file_name=f"Phieu_Tai_Kham_Hen_{st.session_state.patient_name.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True
    )


# ==============================================================================
# PHÂN HỆ 3: KẾ HOẠCH HÀNH ĐỘNG (ACTION PLAN)
# ==============================================================================
elif mode == "📋 Kế Hoạch Hành Động (Action Plan)":
    st.subheader("📋 Kế Hoạch Hành Động Hen Phế Quản Cá Nhân Hóa (Asthma Action Plan)")
    st.caption("Kế hoạch phân vùng Xanh - Vàng - Đỏ giúp người bệnh tự quản lý cơn hen tại nhà.")

    col_ap1, col_ap2, col_ap3 = st.columns(3)
    with col_ap1:
        pb_pef = st.number_input("Lưu lượng đỉnh tốt nhất của bệnh nhân (Personal Best PEF - L/phút):", 100.0, 900.0, 450.0, step=10.0)
    with col_ap2:
        ctrl_med_custom = st.text_input("Thuốc kiểm soát duy trì hằng ngày:", value="Symbicort Turbuhaler 160/4.5 mcg: 1 hít x 2 lần/ngày (sáng/tối)")
    with col_ap3:
        rel_med_custom = st.text_input("Thuốc cắt cơn khẩn cấp:", value="Symbicort 160/4.5 mcg: 1 nhát (hoặc Ventolin 100mcg: 2 nhát)")

    plan = generate_action_plan(
        patient_name=st.session_state.patient_name,
        patient_age=st.session_state.patient_age,
        personal_best_pef=pb_pef,
        current_step=int(st.session_state.wm.get("f310", 2) or 2),
        controller_med=ctrl_med_custom,
        reliever_med=rel_med_custom
    )

    # 3 Cột Màu
    c_green, c_yellow, c_red = st.columns(3)
    with c_green:
        st.markdown(f"""
        <div style="background: #ECFDF5; border: 2px solid #10B981; border-radius: 12px; padding: 16px; min-height: 420px;">
            <div style="color: #065F46; font-weight: 700; font-size: 1.05rem;">{plan['green_zone']['title']}</div>
            <div style="margin-top: 10px; font-weight: 600; font-size: 0.85rem; color: #047857;">DẤU HIỆU:</div>
            <ul style="padding-left: 18px; font-size: 0.85rem; color: #064E3B;">
                {''.join([f"<li>{c}</li>" for c in plan['green_zone']['criteria']])}
            </ul>
            <div style="margin-top: 10px; font-weight: 600; font-size: 0.85rem; color: #047857;">HÀNH ĐỘNG:</div>
            <ul style="padding-left: 18px; font-size: 0.85rem; color: #064E3B;">
                {''.join([f"<li>{a}</li>" for a in plan['green_zone']['action']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_yellow:
        st.markdown(f"""
        <div style="background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 12px; padding: 16px; min-height: 420px;">
            <div style="color: #92400E; font-weight: 700; font-size: 1.05rem;">{plan['yellow_zone']['title']}</div>
            <div style="margin-top: 10px; font-weight: 600; font-size: 0.85rem; color: #B45309;">DẤU HIỆU:</div>
            <ul style="padding-left: 18px; font-size: 0.85rem; color: #78350F;">
                {''.join([f"<li>{c}</li>" for c in plan['yellow_zone']['criteria']])}
            </ul>
            <div style="margin-top: 10px; font-weight: 600; font-size: 0.85rem; color: #B45309;">HÀNH ĐỘNG:</div>
            <ul style="padding-left: 18px; font-size: 0.85rem; color: #78350F;">
                {''.join([f"<li>{a}</li>" for a in plan['yellow_zone']['action']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_red:
        st.markdown(f"""
        <div style="background: #FEF2F2; border: 2px solid #EF4444; border-radius: 12px; padding: 16px; min-height: 420px;">
            <div style="color: #991B1B; font-weight: 700; font-size: 1.05rem;">{plan['red_zone']['title']}</div>
            <div style="margin-top: 10px; font-weight: 600; font-size: 0.85rem; color: #B91C1C;">DẤU HIỆU CẤP CỨU:</div>
            <ul style="padding-left: 18px; font-size: 0.85rem; color: #7F1D1D;">
                {''.join([f"<li>{c}</li>" for c in plan['red_zone']['criteria']])}
            </ul>
            <div style="margin-top: 10px; font-weight: 600; font-size: 0.85rem; color: #B91C1C;">XỬ TRÍ KHẨN CẤP:</div>
            <ul style="padding-left: 18px; font-size: 0.85rem; color: #7F1D1D;">
                {''.join([f"<li>{a}</li>" for a in plan['red_zone']['action']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# PHÂN HỆ 4: KIỂM TRA KỸ THUẬT HÍT (INHALER AUDIT)
# ==============================================================================
elif mode == "💨 Kiểm Tra Kỹ Thuật Hít (Inhaler Audit)":
    st.subheader("💨 Kiểm Tra & Huấn Luyện Kỹ Thuật Dùng Bình Xịt / Hít")
    st.caption("Đánh giá thao tác thực hiện của người bệnh, tự động chỉ ra các bước sai sót nghiêm trọng.")

    device_choice = st.selectbox("Chọn loại thiết bị bệnh nhân đang sử dụng:", list(INHALER_DEVICES.keys()), format_func=lambda k: INHALER_DEVICES[k]["name"])
    dev_meta = INHALER_DEVICES[device_choice]

    st.markdown(f"**Các thuốc thông dụng:** `{dev_meta.get('examples', '')}`")

    st.markdown("#### Đánh dấu các bước bệnh nhân ĐÃ THỰC HIỆN ĐÚNG:")
    checked_steps = []
    for step in dev_meta["checklist_steps"]:
        is_crit = step.get("critical", False)
        label = f"{step['text']} {'🔴 [BƯỚC THEN CHỐT]' if is_crit else ''}"
        if st.checkbox(label, key=f"step_{device_choice}_{step['id']}"):
            checked_steps.append(step["id"])

    if st.button("📊 ĐÁNH GIÁ THAO TÁC", use_container_width=True):
        audit_res = audit_inhaler_technique(device_choice, checked_steps)
        
        st.markdown(f"""
        <div style="background: {audit_res['color']}15; border-left: 6px solid {audit_res['color']}; padding: 16px; border-radius: 10px; margin-top: 16px;">
            <div style="font-size: 1.2rem; font-weight: 700; color: #0F172A;">{audit_res['evaluation']} (Điểm: {audit_res['score_pct']}%)</div>
            <div style="font-size: 0.95rem; margin-top: 4px;">Đạt {audit_res['correct_steps']} / {audit_res['total_steps']} bước chuẩn.</div>
        </div>
        """, unsafe_allow_html=True)

        if audit_res["missed_critical_errors"]:
            st.error("🚨 PHÁT HIỆN LỖI SAI THEN CHỐT:")
            for err in audit_res["missed_critical_errors"]:
                st.markdown(f"- **Bước bỏ sót:** {err['step_text']}")
                st.markdown(f"  *Hậu quả:* {err['error_reason']}")


# ==============================================================================
# PHÂN HỆ 5: CÂY SUY LUẬN LOGIC (INFERENCE AUDIT)
# ==============================================================================
elif mode == "🧭 Cây Suy Luận Logic (Inference Audit)":
    st.subheader("🧭 Cơ Chế Giải Thích & Cây Suy Luận Chuyên Gia (Explanation Facility)")
    st.caption("Minh bạch hóa logic suy luận: xem chi tiết các quy tắc đã kích hoạt và vì sao đưa ra kết luận.")

    res_init = process_initial_assessment(st.session_state.wm)
    st.markdown(res_init["audit_trail_md"])


# ==============================================================================
# PHÂN HỆ 6: TRA CỨU THUỐC & BẢNG LIỀU GINA
# ==============================================================================
elif mode == "💊 Tra Cứu Thuốc & Bảng Liều GINA":
    st.subheader("💊 Tra Cứu Thuốc & Bảng Quy Đổi Liều Corticoid Dạng Hít (ICS) Chuẩn GINA")

    tab_med1, tab_med2 = st.tabs(["📋 Bảng Liều Corticoid Hít (ICS)", "💊 Danh Mục Biệt Dược Thông Dụng"])

    with tab_med1:
        st.markdown("#### Bảng Liều Hằng Ngày của các Corticoid Dạng Hít cho Người Lớn & Trẻ Vị Thành Niên (GINA 2023/2024)")
        ics_data = ICS_DOSE_EQUIVALENTS["adults_and_adolescents"]
        rows = []
        for ics_name, doses in ics_data.items():
            rows.append({
                "Hoạt chất & Thiết bị": ics_name,
                "Liều Thấp (Low)": doses["low"],
                "Liều Trung Bình (Medium)": doses["medium"],
                "Liều Cao (High)": doses["high"],
                "Biệt dược tham khảo": doses["common_brands"]
            })
        st.table(pd.DataFrame(rows))

    with tab_med2:
        st.markdown("#### Danh Mục Thuốc Phối Hợp ICS-LABA & Thuốc Cắt Cơn")
        for category, med_list in MEDICATIONS_DB.items():
            st.markdown(f"##### 🔹 {category}")
            for m in med_list:
                with st.expander(f"📦 {m.get('trade_name', 'Thuốc')} ({m.get('ingredients', '')})"):
                    st.write(f"- **Thiết bị:** {m.get('device', 'N/A')}")
                    if 'strengths' in m:
                        st.write(f"- **Hàm lượng:** {', '.join(m['strengths'])}")
                    if 'tracks' in m:
                        st.write(f"- **Lộ trình GINA:** {', '.join(m['tracks'])}")
                    if 'instruction' in m:
                        st.write(f"- **Hướng dẫn sử dụng:** {m['instruction']}")
                    if 'dose' in m:
                        st.write(f"- **Liều dùng:** {m['dose']}")

# asthma_expert_system/utils/report_generator.py
"""
Bộ tạo Báo cáo Y khoa & Xuất Phiếu Khám Bệnh (Clinical Medical Record Generator)
Tạo định dạng HTML Print-ready và Markdown chuẩn cho hồ sơ bệnh án điện tử (EMR).
"""

from datetime import datetime
from typing import Dict, Any

def generate_medical_report_html(patient_data: Dict[str, Any], assessment_result: Dict[str, Any], mode: str = "Khám lần đầu") -> str:
    """
    Sinh mã HTML chuẩn phong cách bệnh viện cho phiếu khám và tư vấn điều trị hen.
    """
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    pname = patient_data.get("name", "Bệnh nhân")
    page = patient_data.get("age", 30)
    pgender = patient_data.get("gender", "Nam")
    pbmi = patient_data.get("bmi", 22.0)

    # Chẩn đoán
    if mode == "Khám lần đầu":
        diag_title = assessment_result.get("diagnosis", {}).get("main_title", "Đang đánh giá")
        sev_label = assessment_result.get("severity", {}).get("label", "N/A")
        step_title = assessment_result.get("treatment", {}).get("step_title", "Bậc 2")
        track1 = assessment_result.get("treatment", {}).get("track1_preferred", {})
        track2 = assessment_result.get("treatment", {}).get("track2_alternative", {})
    else:
        ctrl = assessment_result.get("control_assessment", {})
        diag_title = f"TÁI KHÁM HEN: {ctrl.get('level', 'N/A')} ({ctrl.get('score', 0)}/4 tiêu chí GINA)"
        sev_label = f"Mức độ kiểm soát: {ctrl.get('level', 'N/A')}"
        tx_dec = assessment_result.get("treatment_decision", {})
        step_title = tx_dec.get("action_title", "Duy trì phác đồ")
        track1 = tx_dec.get("track1_preferred", {})
        track2 = tx_dec.get("track2_alternative", {})

    diffs = assessment_result.get("differential_ranking", [])
    diff_rows = ""
    for d in diffs[:4]:
        diff_rows += f"""
        <tr>
            <td style="padding: 6px 10px; border: 1px solid #E2E8F0;">{d['name']}</td>
            <td style="padding: 6px 10px; border: 1px solid #E2E8F0; font-weight: bold; color: {d.get('color', '#3B82F6')};">{d['probability']}% ({d['level']})</td>
            <td style="padding: 6px 10px; border: 1px solid #E2E8F0; font-size: 0.85rem;">{'; '.join(d.get('key_factors', [])) or 'Không có yếu tố nổi bật'}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1E293B; line-height: 1.5; padding: 20px; background: #FFFFFF; }}
            .report-card {{ max-width: 800px; margin: 0 auto; border: 2px solid #0EA5E9; border-radius: 8px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
            .header {{ border-bottom: 2px solid #0EA5E9; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
            .title {{ font-size: 1.4rem; font-weight: bold; color: #0369A1; text-transform: uppercase; margin: 0; }}
            .sub-title {{ font-size: 0.9rem; color: #64748B; }}
            .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; background: #F8FAFC; padding: 12px; border-radius: 6px; }}
            .meta-item {{ font-size: 0.9rem; }}
            .meta-label {{ color: #64748B; font-size: 0.8rem; text-transform: uppercase; }}
            .meta-val {{ font-weight: bold; color: #0F172A; }}
            .section {{ margin-top: 18px; }}
            .section-title {{ font-size: 1.05rem; font-weight: bold; color: #0284C7; border-left: 4px solid #0284C7; padding-left: 8px; margin-bottom: 8px; }}
            .diag-box {{ background: #ECFDF5; border: 1px solid #10B981; border-radius: 6px; padding: 12px; margin-bottom: 12px; }}
            .diag-main {{ font-size: 1.15rem; font-weight: bold; color: #065F46; }}
            .rx-card {{ background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 6px; padding: 12px; margin-top: 8px; }}
            .rx-title {{ font-weight: bold; color: #0369A1; margin-bottom: 4px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 0.9rem; }}
            th {{ background: #F1F5F9; padding: 8px 10px; border: 1px solid #CBD5E1; text-align: left; }}
            .footer {{ margin-top: 30px; display: flex; justify-content: space-between; font-size: 0.85rem; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 12px; }}
            .sign-box {{ text-align: right; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="report-card">
            <div class="header">
                <div>
                    <h1 class="title">Phiếu Khám & Tư Vấn Hen Phế Quản</h1>
                    <div class="sub-title">Hệ thống Hỗ trợ Ra Quyết định Lâm sàng (Asthma CDSS - GINA Standard)</div>
                </div>
                <div style="text-align: right; font-size: 0.85rem; color: #64748B;">
                    <div>Mã HS: <strong>ASTH-{datetime.now().strftime("%y%m%d%H%M")}</strong></div>
                    <div>Ngày khám: {now_str}</div>
                </div>
            </div>

            <div class="meta-grid">
                <div class="meta-item"><div class="meta-label">Họ và tên</div><div class="meta-val">{pname}</div></div>
                <div class="meta-item"><div class="meta-label">Tuổi / Giới</div><div class="meta-val">{page} tuổi ({pgender})</div></div>
                <div class="meta-item"><div class="meta-label">BMI</div><div class="meta-val">{pbmi} kg/m²</div></div>
                <div class="meta-item"><div class="meta-label">Chế độ khám</div><div class="meta-val">{mode}</div></div>
            </div>

            <div class="section">
                <div class="section-title">1. KẾT QUẢ ĐÁNH GIÁ & CHẨN ĐOÁN CHUYÊN GIA</div>
                <div class="diag-box">
                    <div class="diag-main">{diag_title}</div>
                    <div style="font-size: 0.95rem; color: #047857; margin-top: 4px;">
                        <strong>Phân loại mức độ:</strong> {sev_label}
                    </div>
                </div>
            </div>

            {f'''
            <div class="section">
                <div class="section-title">2. XÁC SUẤT CHẨN ĐOÁN PHÂN BIỆT (CERTAINTY SCORING)</div>
                <table>
                    <thead><tr><th>Bệnh lý</th><th>Độ tin cậy (CF)</th><th>Dấu hiệu nhận biết chính</th></tr></thead>
                    <tbody>{diff_rows}</tbody>
                </table>
            </div>
            ''' if diffs else ''}

            <div class="section">
                <div class="section-title">3. ĐỀ XUẤT PHÁC ĐỒ ĐIỀU TRỊ GINA ({step_title})</div>
                
                <div class="rx-card">
                    <div class="rx-title">⭐ LỘ TRÌNH 1 (ƯU TIÊN - GINA PREFERRED TRACK - SMART / MART):</div>
                    <div style="font-weight: 600; color: #0F172A;">{track1.get('controller_and_reliever', 'Chưa có dữ liệu')}</div>
                    <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">Ghi chú: {track1.get('notes', '')}</div>
                    <div style="font-size: 0.85rem; color: #0369A1; margin-top: 2px;">Ví dụ biệt dược: {', '.join(track1.get('brand_examples', []))}</div>
                </div>

                <div class="rx-card" style="background: #FAF5FF; border-color: #E9D5FF;">
                    <div class="rx-title" style="color: #7E22CE;">🔄 LỘ TRÌNH 2 (THAY THẾ - GINA ALTERNATIVE TRACK):</div>
                    <div style="font-weight: 600; color: #0F172A;">Thuốc duy trì: {track2.get('controller', track2.get('controller_and_reliever', 'ICS hàng ngày'))}</div>
                    <div style="font-weight: 600; color: #0F172A; margin-top: 2px;">Thuốc cắt cơn: {track2.get('reliever', 'SABA khi cần')}</div>
                    <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">Ghi chú: {track2.get('notes', '')}</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">4. LỜI DẶN BÁC SĨ & THEO DÕI</div>
                <ul style="font-size: 0.9rem; margin-top: 4px; padding-left: 20px;">
                    <li>Luôn mang theo thuốc cắt cơn bên mình mọi lúc mọi nơi.</li>
                    <li>Súc miệng sạch bằng nước và nhổ bỏ sau mỗi lần hít thuốc chứa Corticoid để tránh nấm họng.</li>
                    <li>Tránh tiếp xúc khói thuốc lá, lông chó mèo, bụi nhà, nấm mốc và giữ ấm khi trời lạnh.</li>
                    <li>Tái khám định kỳ sau <strong>1 - 3 tháng</strong> hoặc ngay khi có dấu hiệu bất thường vùng vàng/vùng đỏ.</li>
                </ul>
            </div>

            <div class="footer">
                <div>Hệ thống Chuyên gia Y tế CDSS • Hỗ trợ quyết định lâm sàng</div>
                <div class="sign-box">
                    <div>Bác sĩ điều trị / Chuyên khoa Hô hấp</div>
                    <div style="margin-top: 40px; font-weight: bold;">(Ký & ghi rõ họ tên)</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

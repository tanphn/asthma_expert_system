# asthma_expert_system/kb/medications_db.py
"""
Cơ sở dữ liệu Thuốc & Phác đồ điều trị Hen Phế Quản
Tham chiếu GINA 2023/2024 & Dược thư Quốc gia Việt Nam.
"""

GINA_TRACKS_INFO = {
    "Track_1": {
        "title": "LỘ TRÌNH 1 (ƯU TIÊN - PREFERRED TRACK)",
        "subtitle": "Liều thấp ICS-formoterol vừa làm thuốc kiểm soát vừa làm thuốc cắt cơn (Liệu pháp MART/SMART)",
        "why_preferred": "Giảm 60-70% nguy cơ đợt kịch phát nặng so với dùng SABA đơn độc cắt cơn; bệnh nhân luôn nhận được một lượng kháng viêm ICS mỗi khi có triệu chứng.",
        "steps": {
            1: {
                "name": "Bậc 1 (Step 1)",
                "controller_and_reliever": "ICS-formoterol liều thấp khi cần (PRN) (Ví dụ: Budesonide/formoterol 160/4.5 mcg 1 nhát khi khó thở)",
                "notes": "Không cần xịt duy trì hàng ngày. Tối đa 12 nhát/ngày đối với Budesonide/formoterol.",
                "brand_examples": ["Symbicort Turbuhaler 160/4.5 mcg", "Foster Nexthaler 100/6 mcg"]
            },
            2: {
                "name": "Bậc 2 (Step 2)",
                "controller_and_reliever": "ICS-formoterol liều thấp khi cần (PRN) (Hoặc ICS duy trì liều thấp hàng ngày nếu bệnh nhân quen dùng hàng ngày)",
                "notes": "Liều thấp ICS-formoterol khi cần chứng minh hiệu quả giảm đợt cấp tương đương ICS liều thấp hàng ngày.",
                "brand_examples": ["Symbicort Turbuhaler 160/4.5 mcg", "Foster 100/6 mcg"]
            },
            3: {
                "name": "Bậc 3 (Step 3 - Khởi đầu SMART)",
                "controller_and_reliever": "Duy trì liều thấp ICS-formoterol (1 hít x 2 lần/ngày) + Thêm 1 hít khi cần khi có triệu chứng (MART)",
                "notes": "Tổng liều tối đa thông thường không quá 8 nhát/ngày (tối đa tạm thời 12 nhát/ngày trong đợt cấp).",
                "brand_examples": ["Symbicort 160/4.5 mcg: 1 nhát x 2 lần/ngày (sáng/tối) + 1 nhát khi cần", "Foster 100/6 mcg: 1 nhát x 2 lần/ngày + 1 nhát khi cần"]
            },
            4: {
                "name": "Bậc 4 (Step 4 - Tăng liều SMART)",
                "controller_and_reliever": "Duy trì liều trung bình ICS-formoterol (2 hít x 2 lần/ngày) + Thêm 1 hít khi cần khi có triệu chứng (MART)",
                "notes": "Cân nhắc thêm LAMA (Tiotropium Respimat 2.5 mcg x 2 nhát/ngày) nếu vẫn chưa kiểm soát.",
                "brand_examples": ["Symbicort 160/4.5 mcg: 2 nhát x 2 lần/ngày + khi cần", "Foster 100/6 mcg: 2 nhát x 2 lần/ngày + khi cần"]
            },
            5: {
                "name": "Bậc 5 (Step 5 - Hen nặng / Khó trị)",
                "controller_and_reliever": "Duy trì liều cao ICS-LABA + Thêm LAMA (Spiriva Respimat 5 mcg/ngày) + Chuyển khám chuyên khoa Hen để đánh giá kiểu hình Type 2 (kháng IgE, kháng IL-5/IL-5R, kháng IL-4R)",
                "notes": "Xem xét Corticoid đường uống (OCS) liều thấp duy trì ngắn hạn kèm theo dõi tác dụng phụ nghiêm ngặt nếu các biện pháp khác thất bại.",
                "brand_examples": ["Symbicort 320/9 mcg hoặc 160/4.5 mcg liều cao + Spiriva Respimat 2.5 mcg (2 nhát/ngày) + Biologics (Xolair / Nucala / Fasenra / Dupixent)"]
            }
        }
    },
    "Track_2": {
        "title": "LỘ TRÌNH 2 (THAY THẾ - ALTERNATIVE TRACK)",
        "subtitle": "Duy trì ICS-LABA hoặc ICS hàng ngày + Dùng SABA làm thuốc cắt cơn khi cần",
        "why_preferred": "Áp dụng khi bệnh nhân không có điều kiện tiếp cận ICS-formoterol hoặc tuân thủ tốt thuốc kiểm soát duy trì hàng ngày và không muốn dùng liệu pháp SMART.",
        "steps": {
            1: {
                "name": "Bậc 1 (Step 1)",
                "controller": "Dùng liều thấp ICS mỗi khi dùng SABA (xịt cùng lúc hoặc thuốc kết hợp)",
                "reliever": "SABA khi cần (Salbutamol 100-200 mcg / Ventolin)",
                "notes": "Tuyệt đối không dùng SABA đơn độc mà không có ICS đi kèm.",
                "brand_examples": ["Ventolin Inhaler 100mcg + Flixotide Evohaler 50mcg"]
            },
            2: {
                "name": "Bậc 2 (Step 2)",
                "controller": "Duy trì liều thấp ICS hàng ngày (hoặc Kháng Leukotriene - LTRA Montelukast 10mg/ngày)",
                "reliever": "SABA khi cần (Ventolin 100mcg: 1-2 nhát)",
                "notes": "LTRA ít hiệu quả hơn ICS trong ngăn ngừa đợt kịch phát nhưng phù hợp bệnh nhân kèm viêm mũi dị ứng nặng.",
                "brand_examples": ["Flixotide 125mcg: 1 nhát x 2 lần/ngày (hoặc Pulmicort 200mcg) + Ventolin khi cần"]
            },
            3: {
                "name": "Bậc 3 (Step 3)",
                "controller": "Duy trì liều thấp ICS-LABA hàng ngày (hoặc ICS liều trung bình)",
                "reliever": "SABA khi cần (Ventolin 100mcg: 1-2 nhát)",
                "notes": "Kiểm tra kỹ thuật hít trước khi đổi thuốc.",
                "brand_examples": ["Seretide Evohaler 125/25mcg: 1 nhát x 2 lần/ngày + Ventolin khi cần", "Relvar Ellipta 92/22mcg: 1 hít/ngày + Ventolin khi cần"]
            },
            4: {
                "name": "Bậc 4 (Step 4)",
                "controller": "Duy trì liều trung bình hoặc cao ICS-LABA hàng ngày + xem xét thêm LAMA / LTRA",
                "reliever": "SABA khi cần (Ventolin 100mcg: 1-2 nhát)",
                "notes": "Nếu không kiểm soát với liều trung bình, có thể chuyển sang liều cao hoặc thêm Tiotropium.",
                "brand_examples": ["Seretide Accuhaler 500/50mcg: 1 hít x 2 lần/ngày + Ventolin khi cần", "Relvar Ellipta 184/22mcg: 1 hít/ngày + Spiriva Respimat"]
            },
            5: {
                "name": "Bậc 5 (Step 5)",
                "controller": "Duy trì liều cao ICS-LABA + Thêm LAMA + Đánh giá Phenotype chỉ định thuốc sinh học (Biologics)",
                "reliever": "SABA khi cần (Ventolin 100mcg)",
                "notes": "Gửi khám hội chẩn chuyên gia Hô hấp & Dị ứng lâm sàng.",
                "brand_examples": ["Seretide 500/50mcg + Spiriva Respimat 2.5mcg (2 nhát/ngày) + Biologics"]
            }
        }
    }
}

ICS_DOSE_EQUIVALENTS = {
    "adults_and_adolescents": {
        "Budesonide (DPI)": {
            "low": "200 - 400 mcg/ngày",
            "medium": "> 400 - 800 mcg/ngày",
            "high": "> 800 mcg/ngày",
            "common_brands": "Pulmicort Turbuhaler, Symbicort"
        },
        "Fluticasone Propionate (DPI/pMDI)": {
            "low": "100 - 250 mcg/ngày",
            "medium": "> 250 - 500 mcg/ngày",
            "high": "> 500 mcg/ngày",
            "common_brands": "Flixotide, Seretide"
        },
        "Beclomethasone Dipropionate (HFA - hạt siêu mịn)": {
            "low": "100 - 200 mcg/ngày",
            "medium": "> 200 - 400 mcg/ngày",
            "high": "> 400 mcg/ngày",
            "common_brands": "Foster Nexthaler/pMDI"
        },
        "Fluticasone Furoate (DPI)": {
            "low": "92 mcg/ngày (1 lần/ngày)",
            "medium": "Không áp dụng",
            "high": "184 mcg/ngày (1 lần/ngày)",
            "common_brands": "Relvar Ellipta"
        },
        "Ciclesonide (HFA)": {
            "low": "80 - 160 mcg/ngày",
            "medium": "> 160 - 320 mcg/ngày",
            "high": "> 320 mcg/ngày",
            "common_brands": "Alvesco"
        }
    }
}

MEDICATIONS_DB = {
    "ICS_LABA": [
        {
            "trade_name": "Symbicort Turbuhaler",
            "ingredients": "Budesonide / Formoterol fumarate",
            "strengths": ["160/4.5 mcg/liều", "80/4.5 mcg/liều", "320/9 mcg/liều"],
            "device": "Turbuhaler (DPI)",
            "tracks": ["Track 1 (SMART)", "Track 2"],
            "instruction": "Hít sâu và mạnh qua miệng. Súc miệng nhổ bỏ sau khi dùng."
        },
        {
            "trade_name": "Seretide Evohaler / Accuhaler",
            "ingredients": "Fluticasone propionate / Salmeterol xinafoate",
            "strengths": ["Evohaler: 50/25, 125/25, 250/25 mcg", "Accuhaler: 100/50, 250/50, 500/50 mcg"],
            "device": "pMDI (bình xịt định liều) / Accuhaler (DPI)",
            "tracks": ["Track 2 (Duy trì)"],
            "instruction": "Với Evohaler: Lắc kỹ, thở ra hết, ngậm kín, ấn xịt đồng thời hít vào chậm và sâu. Súc miệng sạch."
        },
        {
            "trade_name": "Foster Nexthaler / pMDI",
            "ingredients": "Beclomethasone dipropionate / Formoterol fumarate (hạt siêu mịn)",
            "strengths": ["100/6 mcg/liều", "200/6 mcg/liều"],
            "device": "Nexthaler (DPI) / pMDI",
            "tracks": ["Track 1 (SMART)", "Track 2"],
            "instruction": "Hạt siêu mịn phân bố sâu vào đường thở nhỏ. Súc miệng sau khi hít."
        },
        {
            "trade_name": "Relvar Ellipta",
            "ingredients": "Fluticasone furoate / Vilanterol trifenatate",
            "strengths": ["92/22 mcg/liều", "184/22 mcg/liều"],
            "device": "Ellipta (DPI)",
            "tracks": ["Track 2 (Duy trì 1 lần/ngày)"],
            "instruction": "Dùng 1 lần duy nhất mỗi ngày vào cùng một thời điểm. Súc miệng sạch."
        }
    ],
    "Relievers_SABA": [
        {
            "trade_name": "Ventolin Inhaler",
            "ingredients": "Salbutamol sulfate 100 mcg/nhát",
            "device": "pMDI",
            "indication": "Cắt cơn khó thở cấp tính trong Track 2 hoặc dự phòng co thắt phế quản do gắng sức (15 phút trước vận động).",
            "dose": "1-2 nhát xịt khi khó thở. Không dùng quá 8 nhát/ngày nếu không có chỉ định bác sĩ."
        },
        {
            "trade_name": "Berodual pMDI",
            "ingredients": "Fenoterol hydrobromide 50mcg + Ipratropium bromide 20mcg",
            "device": "pMDI",
            "indication": "Giãn phế quản tác dụng nhanh kết hợp SABA + SAMA.",
            "dose": "1-2 nhát khi khó thở."
        }
    ],
    "Add_on_Therapies": [
        {
            "trade_name": "Spiriva Respimat",
            "ingredients": "Tiotropium bromide 2.5 mcg/nhát",
            "class": "LAMA (Kháng Cholinergic tác dụng kéo dài)",
            "indication": "Bổ sung cho bệnh nhân Hen Bậc 4-5 hoặc kèm COPD (ACO) chưa kiểm soát.",
            "dose": "2 nhát (5 mcg) x 1 lần/ngày vào cùng một giờ."
        },
        {
            "trade_name": "Singulair / Montelukast",
            "ingredients": "Montelukast sodium 10mg (viên nén)",
            "class": "LTRA (Kháng thụ thể Leukotriene)",
            "indication": "Phù hợp bệnh nhân hen kèm viêm mũi dị ứng, hen gắng sức, hoặc không dung nạp ICS.",
            "dose": "10 mg uống 1 viên vào buổi tối trước khi đi ngủ."
        },
        {
            "trade_name": "Thuốc Sinh học (Biologics: Xolair, Nucala, Fasenra, Dupixent)",
            "ingredients": "Omalizumab (Anti-IgE), Mepolizumab (Anti-IL5), Dupilumab (Anti-IL4Rα)",
            "class": "Monoclonal Antibody (Sinh học điều trị trúng đích)",
            "indication": "Hen phế quản nặng dai dẳng Type 2 khó kiểm soát ở Bậc 5 sau khi tối ưu liều cao ICS-LABA và LAMA.",
            "dose": "Tiêm dưới da định kỳ mỗi 2-4 tuần tại cơ sở chuyên khoa."
        }
    ]
}

INHALER_DEVICES = {
    "pMDI": {
        "name": "Bình xịt định liều (pMDI - Pressurized Metered Dose Inhaler)",
        "examples": "Ventolin Inhaler, Seretide Evohaler, Foster pMDI, Flixotide Evohaler",
        "checklist_steps": [
            {"id": "s1", "text": "Mở nắp bảo vệ và kiểm tra đầu ngậm không có dị vật", "critical": False},
            {"id": "s2", "text": "Lắc đều bình xịt lên xuống 4 - 5 lần", "critical": True, "error_reason": "Không lắc khiến thuốc và chất đẩy không trộn đều -> liều lượng thuốc không đủ"},
            {"id": "s3", "text": "Cầm bình thẳng đứng (đáy bình hướng lên trên), thở ra hết thật nhẹ nhàng (không thở vào đầu ngậm)", "critical": True, "error_reason": "Không thở ra hết làm giảm thể tích khí hít vào đáy phổi"},
            {"id": "s4", "text": "Ngậm kín môi quanh đầu ngậm, không cắn răng, không để lưỡi che lỗ xịt", "critical": False},
            {"id": "s5", "text": "Bắt đầu hít vào CHẬM và SÂU qua miệng, đồng thời ẤN bình xịt 1 nhát dứt khoát", "critical": True, "error_reason": "Không phối hợp nhịp nhàng tay bấm - miệng hít khiến thuốc đọng ở họng thay vì vào phổi"},
            {"id": "s6", "text": "Tiếp tục hít vào thật sâu cho đến khi đầy phổi", "critical": False},
            {"id": "s7", "text": "Bỏ bình ra khỏi miệng, NÍN THỞ 5 - 10 giây (hoặc lâu nhất có thể trong mức thoải mái)", "critical": True, "error_reason": "Không nín thở làm các hạt thuốc bị thở ra ngoài trước khi lắng đọng vào phế quản"},
            {"id": "s8", "text": "Thở ra nhẹ nhàng qua mũi hoặc miệng", "critical": False},
            {"id": "s9", "text": "Nếu cần xịt nhát thứ hai, đợi khoảng 30-60 giây và lặp lại từ bước 2", "critical": False},
            {"id": "s10", "text": "Đậy nắp bình và SÚC MIỆNG sạch bằng nước (nhổ bỏ, không nuốt) nếu thuốc có chứa Corticoid", "critical": True, "error_reason": "Không súc miệng gây đọng thuốc dẫn đến nấm miệng (tưa lưỡi) và khàn giọng"}
        ]
    },
    "Turbuhaler": {
        "name": "Bình hít bột khô Turbuhaler (DPI)",
        "examples": "Symbicort Turbuhaler, Pulmicort Turbuhaler, Bricanyl Turbuhaler",
        "checklist_steps": [
            {"id": "t1", "text": "Vặn mở nắp bảo vệ thân bình", "critical": False},
            {"id": "t2", "text": "Cầm bình thẳng đứng, vặn đế xoay về một hướng hết cỡ, rồi vặn ngược lại cho đến khi nghe tiếng 'CLICK'", "critical": True, "error_reason": "Không nghe tiếng 'CLICK' nghĩa là liều thuốc chưa được nạp vào buồng hít"},
            {"id": "t3", "text": "Thở ra hết thật nhẹ nhàng ra ngoài (TUYỆT ĐỐI KHÔNG thổi vào đầu ngậm)", "critical": True, "error_reason": "Thổi vào bình làm ẩm bột thuốc, gây vón cục và tắc thiết bị"},
            {"id": "t4", "text": "Ngậm chặt môi quanh đầu ngậm (không cắn, giữ bình nghiêng hoặc ngang tự nhiên)", "critical": False},
            {"id": "t5", "text": "Hít vào MẠNH và SÂU bằng miệng (lực hít phải đủ mạnh để phân tán hạt bột mịn)", "critical": True, "error_reason": "Hít quá yếu không tạo đủ luồng khí để phân tách các vi hạt thuốc"},
            {"id": "t6", "text": "Bỏ bình ra khỏi miệng, NÍN THỞ khoảng 5 - 10 giây", "critical": True, "error_reason": "Không nín thở làm giảm độ lắng đọng thuốc trong phế quản"},
            {"id": "t7", "text": "Thở ra nhẹ nhàng, đậy nắp bình", "critical": False},
            {"id": "t8", "text": "SÚC MIỆNG sạch bằng nước và nhổ bỏ (đặc biệt quan trọng với Symbicort/Pulmicort)", "critical": True, "error_reason": "Ngăn ngừa nấm Candida hầu họng và khàn tiếng"}
        ]
    },
    "Accuhaler_Diskus": {
        "name": "Bình hít bột khô Accuhaler / Diskus",
        "examples": "Seretide Accuhaler, Flixotide Accuhaler, Serevent Accuhaler",
        "checklist_steps": [
            {"id": "a1", "text": "Mở bình bằng cách đặt ngón cái vào rãnh và đẩy hết cỡ về phía trước đến khi nghe 'TÁCH'", "critical": False},
            {"id": "a2", "text": "Gạt cần nạp thuốc xuống hết cỡ cho đến khi nghe tiếng 'CLICK' (cửa sổ liều giảm 1 số)", "critical": True, "error_reason": "Không gạt hết cần nạp thì liều thuốc dạng vỉ chưa được mở ra"},
            {"id": "a3", "text": "Thở ra hết ra ngoài (không thổi vào đầu ngậm)", "critical": True, "error_reason": "Hơi ẩm làm hỏng bột thuốc trong vỉ"},
            {"id": "a4", "text": "Ngậm kín môi quanh đầu ngậm, giữ bình nằm ngang", "critical": False},
            {"id": "a5", "text": "Hít vào ĐỀU, MẠNH và SÂU bằng miệng", "critical": True, "error_reason": "Cần lực hít đủ để hút toàn bộ liều bột thuốc"},
            {"id": "a6", "text": "Rút bình ra khỏi miệng, NÍN THỞ 10 giây", "critical": True, "error_reason": "Tăng hiệu quả hấp thu thuốc tại phế nang"},
            {"id": "a7", "text": "Thở ra từ từ, trượt rãnh đóng bình lại", "critical": False},
            {"id": "a8", "text": "SÚC MIỆNG sạch với nước và nhổ bỏ", "critical": True, "error_reason": "Tránh tác dụng phụ tại chỗ của Fluticasone"}
        ]
    }
}

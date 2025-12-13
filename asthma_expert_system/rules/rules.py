# asthma_expert_system/rules/rules.py
# List of rules as python list of dicts. The 'if' expressions use fact ids (fXXX).
rules = [
  {
    "id": "L1",
    "if": "( (f101 or f102 or f103 or f104) and ((f105) or (f106) or (f107)) )",
    "then": ["f501", "f503"],
    "description": ">=2 triệu chứng chính & triệu chứng thay đổi theo thời gian -> nghi ngờ hen"
  },
  {
    "id": "L2",
    "if": "(f201 or f202 or f203)",
    "then": ["f502"],
    "description": "Xét nghiệm: rối loạn thông khí tắc nghẽn biến đổi"
  },
  {
    "id": "L3",
    "if": "(f501 and f502)",
    "then": ["f504"],
    "description": "Thỏa Luật 1 và Luật 2 -> Chẩn đoán hen chắc chắn"
  },
  {
    "id": "L4",
    "if": "((f301 or f302) and (f101 or f102 or f103 or f104) and (f204 or f205))",
    "then": ["f504"],
    "description": "Đang dùng ICS/LABA + còn triệu chứng + test dương -> Khẳng định hen"
  },
  {
    "id": "L5-1",
    "if": "(f401 and f115 and f201 and (not f204))",
    "then": ["f509"],
    "description": "Triệu chứng và tiền sử phù hợp COPD"
  },
  {
    "id": "L5-2",
    "if": "(f103 and f111 and f405)",
    "then": ["f510"],
    "description": "Gợi ý suy tim trái"
  },
  {
    "id": "L5-3",
    "if": "(f103 and f112 and f113)",
    "then": ["f511"],
    "description": "Gợi ý hẹp/dị vật đường thở"
  },
  {
    "id": "L5-4",
    "if": "f114",
    "then": ["f512"],
    "description": "Gợi ý GERD/rò khí-thực quản"
  },
  {
    "id": "L5-5",
    "if": "f115",
    "then": ["f513"],
    "description": "Gợi ý giãn phế quản"
  },
  {
    "id": "L6",
    "if": "(f116 and f117 and f118)",
    "then": ["f506", "f507"],
    "description": ">=3 triệu chứng không kiểm soát -> hen không kiểm soát"
  },
  {
    "id": "L7",
    "if": "((not f116) and (not f117) and (not f118) and f119)",
    "then": ["f505", "f508"],
    "description": "Hen kiểm soát tốt, ổn định >=3 tháng -> giảm bậc"
  },
  {
    "id": "L8",
    "if": "(f120 <= 2 and f121 <= 2 and f122 == 0 and f123 <= 2 and (f208 >= 80 or f209 < 20))",
    "then": ["f601"],
    "description": "Hen gián đoạn (mild intermittent)"
  },
  {
    "id": "L9",
    "if": "((f120 > 2 and f120 < 7) or (f121 > 2 and f121 < 7) or (f123 > 2 and f208 >= 80))",
    "then": ["f602"],
    "description": "Hen dai dẳng nhẹ"
  },
  {
    "id": "L10",
    "if": "(f120 >= 7 or f121 >= 7 or f122 == 1 or (f208 >= 60 and f208 < 80))",
    "then": ["f603"],
    "description": "Hen dai dẳng trung bình"
  },
  {
    "id": "L11",
    "if": "(f122 == 2 or f208 < 60 or f209 >= 30)",
    "then": ["f604"],
    "description": "Hen dai dẳng nặng"
  },
  {
    "id": "L12",
    "if": "(f601 and f124 == 0)",
    "then": ["f310=1"],
    "description": "Gợi ý Step 1"
  },
  {
    "id": "L13",
    "if": "f602",
    "then": ["f310=2"],
    "description": "Gợi ý Step 2"
  },
  {
    "id": "L14",
    "if": "f603",
    "then": ["f310=3"],
    "description": "Gợi ý Step 3"
  },
  {
    "id": "L15",
    "if": "(f604 and (f116 or f117 or f118))",
    "then": ["f310=4"],
    "description": "Gợi ý Step 4"
  },
  {
    "id": "L16",
    "if": "(f604 and f124 >= 2)",
    "then": ["f310=5"],
    "description": "Gợi ý Step 5"
  },
  {
    "id": "L17",
    "if": "((f116 or f117 or f118) and f414)",
    "then": ["f605"],
    "description": "Mất kiểm soát do không tuân thủ"
  },
  {
    "id": "L18",
    "if": "((f116 or f117 or f118) and f415)",
    "then": ["f606"],
    "description": "Mất kiểm soát do sai kỹ thuật hít"
  },
  {
    "id": "L19",
    "if": "((f116 or f117 or f118) and (f402 or f403))",
    "then": ["f607"],
    "description": "Mất kiểm soát do yếu tố kích phát"
  },
  {
    "id": "L20",
    "if": "((f116 or f117 or f118) and (not f414) and (not f415))",
    "then": ["f507"],
    "description": "Tăng bậc điều trị (step-up)"
  },
  {
    "id": "L21",
    "if": "(f505 and f119)",
    "then": ["f508"],
    "description": "Giảm bậc điều trị (step-down)"
  }
]

# asthma_expert_system/utils/helpers.py
"""
Các hàm tiện ích bổ trợ cho Hệ thống Chuyên gia Hen Phế Quản.
"""

from typing import Any, Optional

def format_number(val: Any, unit: str = "", default: str = "N/A") -> str:
    """Định dạng số hiển thị kèm đơn vị."""
    if val is None or val == 999:
        return default
    try:
        fval = float(val)
        if fval.is_integer():
            return f"{int(fval)} {unit}".strip()
        return f"{fval:.2f} {unit}".strip()
    except (ValueError, TypeError):
        return default

def get_badge_html(text: str, bg_color: str = "#3B82F6", text_color: str = "#FFFFFF") -> str:
    """Tạo badge HTML đẹp mắt cho UI."""
    return f"""<span style="background-color: {bg_color}; color: {text_color}; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; display: inline-block; margin: 2px;">{text}</span>"""

def input_boolean_cli(prompt: str) -> bool:
    """Nhập giá trị boolean an toàn trên giao diện dòng lệnh CLI."""
    while True:
        s = input(f"{prompt} (c/k hoặc y/n): ").strip().lower()
        if s in ("c", "có", "co", "yes", "y", "1"):
            return True
        if s in ("k", "không", "khong", "no", "n", "0"):
            return False
        print(">> Vui lòng nhập 'c' (có) hoặc 'k' (không).")

def input_float_cli(prompt: str, allow_empty: bool = True, default: Optional[float] = None) -> Optional[float]:
    """Nhập giá trị float an toàn trên CLI."""
    while True:
        s = input(f"{prompt}: ").strip()
        if s == "" and allow_empty:
            return default
        try:
            return float(s)
        except ValueError:
            print(">> Giá trị nhập không hợp lệ, vui lòng nhập một số.")

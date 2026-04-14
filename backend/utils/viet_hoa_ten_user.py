from unidecode import unidecode

def xu_ly_ten_cho_logo(full_name: str) -> str:
    if not full_name or full_name == "Anonymous":
        return "MY"
    
    name_parts = full_name.strip().split()
    
    last_name = name_parts[-1]
    
    last_name_khong_dau = unidecode(last_name)
    
    return last_name_khong_dau.upper()
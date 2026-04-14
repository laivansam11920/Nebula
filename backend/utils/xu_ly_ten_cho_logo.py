from unidecode import unidecode

def xu_ly_ten_cho_logo(full_name):
    if not full_name or full_name == "User":
        return "MY"
    last_name = full_name.strip().split()[-1]
    return unidecode(last_name).upper()

def xu_ly_avatar(full_name):
    if not full_name or full_name == "User":
        return "A"
    return full_name.strip().split()[-1][0].upper()

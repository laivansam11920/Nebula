from pathlib import Path

def thu_muc_chinh(duong_dan=""):
    goc_du_an = Path(__file__).resolve().parent.parent.parent
    thu_muc = goc_du_an / duong_dan
    return str(thu_muc)
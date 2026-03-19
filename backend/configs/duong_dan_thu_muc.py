import os

def thu_muc_chinh(duong_dan=""):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    thu_muc = os.path.abspath(os.path.join(current_dir, '..', duong_dan))
    return thu_muc
from pathlib import Path


def thu_muc_chinh(duong_dan=""):
    goc_du_an = Path(__file__).resolve().parent.parent.parent
    thu_muc = goc_du_an / duong_dan
    return str(thu_muc)


import inspect


def duong_dan_hien_tai():
    config_file_path = Path(__file__).resolve()

    backend_dir = config_file_path.parent.parent

    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_path = Path(caller_filename).resolve()

    try:
        relative_path = caller_path.relative_to(backend_dir)
        return str(relative_path)
    except ValueError:
        return "Lỗi: File gọi hàm không nằm trong thư mục backend!"

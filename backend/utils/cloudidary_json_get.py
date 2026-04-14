from datetime import datetime
from utils.create_id import create_id


def make_json_cloud(upload_result, user_email: str, ten_goc: str, loai_file: str) -> dict:
    ext_raw = upload_result.get("format", "").lower()
    ext_display = ext_raw.upper() if ext_raw else "FILE"

    full_name = (
        ten_goc
        if ten_goc and ten_goc.strip()
        else f"{upload_result.get('public_id')}.{ext_raw}"
    )

    res_type = upload_result.get("resource_type", "raw")
    fe_type = "doc"
    if res_type == "image":
        fe_type = "img"
    elif res_type == "video":
        fe_type = "vid"
    elif ext_raw == "pdf":
        fe_type = "pdf"
    elif ext_raw in ["zip", "rar", "7z"]:
        fe_type = "zip"

    bytes_size = upload_result.get("bytes", 0)
    if bytes_size > 1024 * 1024:
        size_str = f"{round(bytes_size / (1024 * 1024), 1)} MB"
    else:
        size_str = f"{round(bytes_size / 1024, 1)} KB"

    raw_date = upload_result.get("created_at", "")
    try:
        date_obj = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = date_obj.strftime("%d/%m/%Y")
    except:
        formatted_date = datetime.now().strftime("%d/%m/%Y")
    secure_url = upload_result.get("secure_url", "")

    thumb_url = None
    if res_type == "image" and secure_url:
        thumb_url = secure_url.replace("/upload/", "/upload/w_200,c_fill/")
    ma_dinh_danh = create_id()
    file_info = {
        "id": upload_result.get("public_id"),
        "name": full_name,
        "url": secure_url,
        "size": size_str,
        "ext": ext_display,
        "type": fe_type,
        "date": formatted_date,
        "user_gmail": user_email,
        "thumb": thumb_url,
        "trang_thai": "chua_xoa",
        "ma_dinh_danh_file": ma_dinh_danh,
        "thoi_gian_ton_tai": 0,
        "loai_file": loai_file,
    }
    return file_info

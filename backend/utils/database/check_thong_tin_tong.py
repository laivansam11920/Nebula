from configs.db import db
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def lay_mot_truong_du_lieu(ten_collection, cot_can_tim, gia_tri_can_tim, cot_can_lay):
    try:
        bang_du_lieu = db[str(ten_collection)]

        ban_ghi_tim_thay = bang_du_lieu.find_one({str(cot_can_tim): gia_tri_can_tim})

        if not ban_ghi_tim_thay:
            return "Khong tim thay ban ghi nao", 404

        danh_sach_khoa = str(cot_can_lay).split(".")
        ket_qua = ban_ghi_tim_thay

        for khoa in danh_sach_khoa:
            if isinstance(ket_qua, dict):
                ket_qua = ket_qua.get(khoa)
            else:
                ket_qua = None
                break

        if ket_qua is None:
            return "Du lieu cua cot nay khong ton tai", 404

        return ket_qua, 200

    except Exception as e:
        logger.error(
            f"gap su co ở collection '{ten_collection}' khi tim '{gia_tri_can_tim}': {e}",
            duong_dan_hien_tai()
        )
        return "Loi he thong", 500

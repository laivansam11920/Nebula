from ddgs import DDGS
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

def get_realtime_info(query):
    try:
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(query, max_results=3)]
            if not results:
                logger.log("SEARCH TRỐNG KHÔNG: Không tìm thấy gì trên mạng!", duong_dan_hien_tai())
                return "Không có thông tin mới."
            logger.log(f"Đã tìm thấy {len(results)} đoạn tin tức.", duong_dan_hien_tai())
            return "\n".join(results)
    except Exception as e:
        logger.error(f"{e}", duong_dan_hien_tai())
        return ""

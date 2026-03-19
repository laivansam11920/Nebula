from ddgs import DDGS
from logs.logger import logger

def get_realtime_info(query):
    try:
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(query, max_results=3)]
            if not results:
                logger.warning("SEARCH TRỐNG KHÔNG: Không tìm thấy gì trên mạng!")
                return "Không có thông tin mới."
            logger.log(f"Đã tìm thấy {len(results)} đoạn tin tức.")
            return "\n".join(results)
    except Exception as e:
        logger.error(f"❌ Lỗi Search: {e}")
        return ""

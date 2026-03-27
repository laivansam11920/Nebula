from ddgs import DDGS


def get_realtime_info(query):
    try:
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(query, max_results=3)]
            if not results:
                print("SEARCH TRỐNG KHÔNG: Không tìm thấy gì trên mạng!")
                return "Không có thông tin mới."
            print(f"Đã tìm thấy {len(results)} đoạn tin tức.")
            return "\n".join(results)
    except Exception as e:
        print(f"❌ Lỗi Search: {e}")
        return ""

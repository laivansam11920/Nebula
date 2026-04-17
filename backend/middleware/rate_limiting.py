from flask import request, jsonify
from functools import wraps
import time
import redis
import uuid
import os
from configs.settings import ip_allow, MAX_REQUESTS, PERIOD
from utils.tim_kiem_db import tim_kiem
from utils.kiem_tra_het_han_toan_cuc import kiem_tra_het_han

url_tu_ket_sat = str(os.getenv("REDIS_URL_LIMITING", "redis://localhost:6379/2"))
redis_client = redis.from_url(url_tu_ket_sat)

def limit_requests(max_requests=MAX_REQUESTS, period=PERIOD):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            
            if ip in ip_allow:
                ket_qua = tim_kiem("godmode_admin", "trang_thai")
                if str(ket_qua) == "on":
                    ket_qua_thoi_gian = kiem_tra_het_han(
                        now, "godmode_admin", "godmode", "private", 
                        "thoi_gian_het_han", "trang_thai_thoi_gian", "da_het_han"
                    )
                    if str(ket_qua_thoi_gian["trang_thai"]) == "chua_het_han":
                        return f(*args, **kwargs)
            
            redis_key = f"rate_limit:{ip}"
            
            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(redis_key, 0, now - period)
            pipe.zcard(redis_key)
            
            results = pipe.execute()
            current_requests = results[1]
            
            if current_requests >= max_requests:
                return jsonify({
                    "status": "error",
                    "message": f"Quá nhiều yêu cầu! Thử lại sau {period} giây."
                }), 429
            
            unique_member = f"{now}-{uuid.uuid4()}"
            pipe = redis_client.pipeline()
            pipe.zadd(redis_key, {unique_member: now})
            pipe.expire(redis_key, period)
            pipe.execute()
            
            return f(*args, **kwargs)

        return decorated_function

    return decorator
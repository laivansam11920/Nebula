from flask import session, request, abort
from functools import wraps


def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(
                    413,
                    description=f"File quá lớn! Giới hạn là {max_length/1024/1024}MB",
                )
            return f(*args, **kwargs)

        return wrapper

    return decorator

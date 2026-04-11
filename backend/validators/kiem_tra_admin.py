from functools import wraps
from flask import session, request, jsonify, session


def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get("role")
            if user_role == "admin-root":
                return f(*args, **kwargs)
            if required_role == "admin" and user_role != "admin":
                return jsonify({"error": "Cần quyền Admin mới vào được nhé og!"}), 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator

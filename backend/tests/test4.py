from backend.utils.hash import hash
from backend.utils.make_token import tao_token_10_so

token_new = tao_token_10_so()
token_new_hash = hash(token_new)

logger(token_new_hash)

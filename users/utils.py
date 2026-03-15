from django.core.cache import cache
import random

PREFIX = "confitmation_code"
TTL = 300 #5 min

def _key(email):
    return  f"{PREFIX}:{email}"

def generate_confirmation_code():
    code = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return code

def save_code_to_cache(email, code):
    key = _key(email)
    cache.set(key, code, TTL)

def verify_confirmation_code(email, code):
    key = _key(email)
    stored = cache.get(key)
    if stored and stored == code:
        cache.delete(key)
        return True
    return False
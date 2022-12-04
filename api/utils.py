import string
import secrets


def generate_key(length: int = 1) -> str:
    chars = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(chars) for _ in range(length))
    return key

import os
import hashlib
import hmac
from datetime import datetime


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def generate_salt() -> str:
    return os.urandom(16).hex()


def hash_password(password: str, salt: str) -> str:
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        120_000,
    )
    return dk.hex()


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    actual_hash = hash_password(password, salt)
    return hmac.compare_digest(actual_hash, expected_hash)

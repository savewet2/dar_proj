from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    salt: str
    created_at: str

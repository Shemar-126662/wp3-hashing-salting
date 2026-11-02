"""Wachtwoordopslag met Argon2id en een willekeurige salt per hash."""
from argon2 import PasswordHasher, Type
from argon2.exceptions import InvalidHashError, VerificationError

password_hasher = PasswordHasher(
    time_cost=3, memory_cost=65536, parallelism=4,
    hash_len=32, salt_len=16, type=Type.ID,
)


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(password_hash, password):
    try:
        return password_hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError, TypeError):
        return False

import re
import bcrypt


def is_password_valid(password: str) -> bool:
    """
    Memvalidasi kata sandi berdasarkan 3 aturan dasar SQA:
    1. Minimal 8 karakter
    2. Mengandung minimal 1 huruf kapital
    3. Mengandung minimal 1 angka
    """
    if len(password.strip()) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True


def is_email_valid(email: str) -> bool:
    """
    Memvalidasi format alamat email berdasarkan aturan SQA:
    1. Memiliki format standar username@domain.tld
    2. Memiliki karakter '@'
    3. Memiliki domain dan TLD yang valid
    """
    if not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def hash_password(password: str) -> str:
    """
    Mengenkripsi/hashing kata sandi menggunakan algoritma bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Memverifikasi kata sandi teks polos dengan kata sandi yang telah di-hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )




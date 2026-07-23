import os
import re
import bcrypt
import pymysql
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

app = FastAPI(title="User Registration API")


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


def simpan_user_ke_db(email: str, hashed_password: str) -> bool:
    """
    Menyimpan data akun user (email dan hashed_password) ke dalam basis data MySQL.
    Menggunakan Environment Variables untuk konfigurasi koneksi DB.
    """
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "root")
    database = os.getenv("DB_NAME", "test_db")

    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=True,
        )
        with connection.cursor() as cursor:
            query = "INSERT INTO users (email, hashed_password) VALUES (%s, %s)"
            cursor.execute(query, (email, hashed_password))
        connection.close()
        return True
    except Exception as e:
        print(f"Error Database: {e}")
        return False


class UserRegisterRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not is_email_valid(v):
            raise ValueError("Format alamat email tidak valid.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_format(cls, v: str) -> str:
        if not is_password_valid(v):
            raise ValueError("Format kata sandi tidak memenuhi kriteria keamanan.")
        return v


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegisterRequest):
    hashed_pass = hash_password(user_data.password)
    success = simpan_user_ke_db(user_data.email, hashed_pass)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal menyimpan user ke database.",
        )
    return {
        "message": "User berhasil terdaftar",
        "email": user_data.email,
    }






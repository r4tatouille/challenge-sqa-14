import os
import pytest
import pymysql

from main import (
    hash_password,
    is_email_valid,
    is_password_valid,
    simpan_user_ke_db,
    verify_password,
)


@pytest.mark.parametrize(
    "password, expected, deskripsi_sqa",
    [
        # --- POSITIVE TESTING ---
        (
            "ValidPass123",
            True,
            "Lulus: Memenuhi semua syarat (>=8, ada kapital, ada angka)",
        ),
        # --- NEGATIVE TESTING ---
        ("Pendek1", False, "Gagal: Hanya 7 karakter (Batas bawah Aturan 1)"),
        ("tanpakapital123", False, "Gagal: Tidak ada huruf besar (Aturan 2)"),
        ("TanpaAngkaSamaSekali", False, "Gagal: Tidak ada angka (Aturan 3)"),
        ("      1A", False, "Gagal: Kombinasi spasi dengan panjang kurang dari 8"),
        ("", False, "Gagal: Input kosong (Edge case ekstrim)"),
    ],
)
def test_password_rules(password, expected, deskripsi_sqa):
    result = is_password_valid(password)

    assert result == expected, f"Gagal pada skenario: {deskripsi_sqa}"


@pytest.mark.parametrize(
    "email, expected, deskripsi_sqa",
    [
        # --- POSITIVE CASE ---
        (
            "mahasiswa@kampus.ac.id",
            True,
            "Lulus: Email valid dengan domain bertingkat (.ac.id)",
        ),
        (
            "user.name@domain.com",
            True,
            "Lulus: Email valid dengan titik pada username dan domain .com",
        ),
        # --- NEGATIVE CASE ---
        (
            "usertanpadomain",
            False,
            "Gagal: Alamat email tidak memiliki karakter '@' dan domain",
        ),
        (
            "user@.com",
            False,
            "Gagal: Alamat email tidak memiliki nama domain sebelum .com",
        ),
        (
            "@domain.com",
            False,
            "Gagal: Alamat email tidak memiliki username sebelum '@'",
        ),
        (
            "user@domain",
            False,
            "Gagal: Alamat email tidak memiliki Top-Level Domain (TLD)",
        ),
    ],
)
def test_email_rules(email, expected, deskripsi_sqa):
    result = is_email_valid(email)

    assert result == expected, f"Gagal pada skenario: {deskripsi_sqa}"


def test_password_hashing():
    raw_password = "PasswordRahasia123"
    hashed = hash_password(raw_password)

    assert (
        hashed != raw_password
    ), "Hasil hash_password tidak boleh sama dengan kata sandi asli"
    assert verify_password(
        raw_password, hashed
    ), "verify_password harus bernilai True untuk kata sandi yang benar"
    assert not verify_password(
        "PasswordSalah123", hashed
    ), "verify_password harus bernilai False untuk kata sandi yang salah"


@pytest.fixture
def db_connection():
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
    except Exception as e:
        pytest.skip(f"Koneksi MySQL tidak dapat dihubungi: {e}")

    # SETUP: Create table
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                hashed_password VARCHAR(255) NOT NULL
            )
        """
        )
        cursor.execute("TRUNCATE TABLE users")

    yield connection

    # TEARDOWN: Drop table
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users")
    connection.close()


def test_simpan_user_ke_db_integration(db_connection):
    test_email = "mahasiswa@kampus.ac.id"
    raw_pass = "ValidPass123"
    hashed_pass = hash_password(raw_pass)

    # 1. Simpan user ke database
    res = simpan_user_ke_db(test_email, hashed_pass)
    assert res is True, "Fungsi simpan_user_ke_db gagal mengembalikan True"

    # 2. Verifikasi dengan query SELECT
    with db_connection.cursor() as cursor:
        cursor.execute(
            "SELECT email, hashed_password FROM users WHERE email = %s",
            (test_email,),
        )
        row = cursor.fetchone()

    assert row is not None, "Data user tidak tersimpan di database"
    assert (
        row[0] == test_email
    ), f"Email tidak cocok. Expected: {test_email}, Got: {row[0]}"
    assert (
        row[1] == hashed_pass
    ), f"Hashed password tidak cocok. Expected: {hashed_pass}, Got: {row[1]}"




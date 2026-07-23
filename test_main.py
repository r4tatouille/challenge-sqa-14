import pytest

from main import is_email_valid, is_password_valid


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


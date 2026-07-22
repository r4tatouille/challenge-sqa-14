# [Security] Implementasi Hashing Kata Sandi

## Deskripsi

Menyimpan kata sandi dalam bentuk _plain text_ adalah celah keamanan fatal (OWASP Top 10). Kita perlu mengenkripsi kata sandi yang sudah divalidasi sebelum nantinya disimpan ke dalam _database_.

## Alur Kerja Git & GitHub Issue

Alur yang harus diikuti: **issue -> branch -> implementasi -> commit -> pull request -> ci -> merge**.

1. **Buat GitHub Issue** menggunakan [GitHub CLI](https://cli.github.com/) (`gh`) berdasarkan dokumen ini:

   ```bash
   gh issue create \
     --title "[Security] Implementasi Hashing Kata Sandi" \
     --body-file issues/2-issue_password_hash.md \
     --label "security"
   ```

   Catat nomor issue yang dihasilkan (misal `#2`), lalu gunakan nomor tersebut pada branch dan pesan commit.

2. **Buat branch baru** dari `main` dengan format `feature/issue-2-password-hash`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/issue-2-password-hash
   ```

## Tugas

1. Tambahkan pustaka kriptografi ringan ke dalam proyek menggunakan `uv` (misalnya `passlib` atau `bcrypt`).
2. Buat fungsi `hash_password(password: str) -> str` di dalam `main.py`.
3. Buat fungsi `verify_password(plain_password: str, hashed_password: str) -> bool`.

## Kriteria Penerimaan SQA (Acceptance Criteria)

Buat _Unit Test_ di `test_main.py` untuk memastikan:

- Hasil dari `hash_password` tidak sama dengan _password_ aslinya.
- Fungsi `verify_password` mengembalikan `True` jika disuntikkan _password_ asli dan _hash_-nya.
- Fungsi `verify_password` mengembalikan `False` jika disuntikkan _password_ yang salah.

## Instruksi CI/CD

Pastikan Anda menjalankan `uv run pytest` di lokal Anda sebelum membuat _Pull Request_. Pipeline GitHub Actions harus hijau (lulus tes).

Setelah implementasi selesai:

1. `git add . && git commit -m "feat: tambah password hashing"`
2. `git push origin feature/issue-2-password-hash`
3. Buka _Pull Request_ dari branch tersebut ke `main`.
4. Tunggu pipeline CI (GitHub Actions) berjalan dan pastikan statusnya **hijau/lulus**.
5. Setelah PR di-_review_ dan CI lulus, lakukan _merge_ ke `main`.

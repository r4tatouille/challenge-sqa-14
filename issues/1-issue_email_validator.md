# [Feature] Penambahan Validasi Email

## Deskripsi

Saat ini sistem kita baru memiliki validasi untuk kata sandi. Untuk melengkapi fitur registrasi pengguna, kita memerlukan fungsi baru untuk memvalidasi format alamat email.

## Alur Kerja Git & GitHub Issue

Alur yang harus diikuti: **issue -> branch -> implementasi -> commit -> pull request -> ci -> merge**.

1. **Buat GitHub Issue** menggunakan [GitHub CLI](https://cli.github.com/) (`gh`) berdasarkan dokumen ini:

   ```bash
   gh issue create \
     --title "[Feature] Penambahan Validasi Email" \
     --body-file issues/1-issue_email_validator.md \
     --label "feature"
   ```

   Catat nomor issue yang dihasilkan (misal `#1`), lalu gunakan nomor tersebut pada branch dan pesan commit.

2. **Buat branch baru** dari `main` dengan format `feature/issue-1-email-validator`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/issue-1-email-validator
   ```

## Tugas

1. Buat sebuah fungsi `is_email_valid(email: str) -> bool` di dalam `main.py`.
2. Fungsi harus memastikan email memiliki format standar (misal: memiliki karakter `@` dan domain yang valid). Anda bisa menggunakan _Regular Expression_ (Regex).

## Kriteria Penerimaan SQA (Acceptance Criteria)

Buat _Unit Test_ di `test_main.py` menggunakan `pytest.mark.parametrize` yang mencakup:

- **Positive Case:** `mahasiswa@kampus.ac.id`, `user.name@domain.com` (Harus `True`)
- **Negative Case:** `usertanpadomain`, `user@.com`, `@domain.com`, `user@domain` (Harus `False`)

## Instruksi CI/CD

Pastikan Anda menjalankan `uv run pytest` di lokal Anda sebelum membuat _Pull Request_. Pipeline GitHub Actions harus hijau (lulus tes).

Setelah implementasi selesai:

1. `git add . && git commit -m "feat: tambah validasi email"`
2. `git push origin feature/issue-1-email-validator`
3. Buka _Pull Request_ dari branch tersebut ke `main`.
4. Tunggu pipeline CI (GitHub Actions) berjalan dan pastikan statusnya **hijau/lulus**.
5. Setelah PR di-_review_ dan CI lulus, lakukan _merge_ ke `main`.

# [Database] Integrasi Penyimpanan Akun ke MySQL

## Deskripsi

Setelah email divalidasi dan kata sandi di-_hash_, data tersebut harus disimpan ke dalam sistem basis data yang persisten. Kita akan menggunakan MySQL untuk kebutuhan ini.

## Alur Kerja Git & GitHub Issue

Alur yang harus diikuti: **issue -> branch -> implementasi -> commit -> pull request -> ci -> merge**.

1. **Buat GitHub Issue** menggunakan [GitHub CLI](https://cli.github.com/) (`gh`) berdasarkan dokumen ini:

   ```bash
   gh issue create \
     --title "[Database] Integrasi Penyimpanan Akun ke MySQL" \
     --body-file issues/3-issue_insert_data_to_mysql.md \
     --label "database"
   ```

   Catat nomor issue yang dihasilkan (misal `#3`), lalu gunakan nomor tersebut pada branch dan pesan commit.

2. **Buat branch baru** dari `main` dengan format `feature/issue-3-mysql-integration`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/issue-3-mysql-integration
   ```

## Tugas

1. Tambahkan `pymysql` ke dalam dependensi menggunakan `uv`.
2. Buat fungsi `simpan_user_ke_db(email: str, hashed_password: str) -> bool` di `main.py`.
3. Gunakan _Environment Variables_ (`os.getenv`) untuk konfigurasi kredensial _database_ (Host, User, Password, DB Name) agar aman.
4. Buat file `docker-compose.yml` untuk memutar _container_ MySQL secara lokal.

## Kriteria Penerimaan SQA (Integration Testing)

- Buat _fixture_ di `pytest` untuk melakukan **Setup** (membuat tabel sementara) dan **Teardown** (menghapus tabel setelah tes selesai).
- Buat tes yang mensimulasikan penyimpanan data ke MySQL dan memverifikasi (menggunakan `SELECT`) bahwa data benar-benar tersimpan.
- Pastikan _pipeline_ CI di `.github/workflows/ci.yml` diperbarui untuk menggunakan _Service Container_ MySQL.

## Instruksi CI/CD

Pastikan Anda menjalankan `uv run pytest` di lokal Anda (dengan `docker-compose up -d` untuk database) sebelum membuat _Pull Request_. Pipeline GitHub Actions harus hijau (lulus tes).

Setelah implementasi selesai:

1. `git add . && git commit -m "feat: tambah integrasi MySQL"`
2. `git push origin feature/issue-3-mysql-integration`
3. Buka _Pull Request_ dari branch tersebut ke `main`.
4. Tunggu pipeline CI (GitHub Actions) berjalan dan pastikan statusnya **hijau/lulus**.
5. Setelah PR di-_review_ dan CI lulus, lakukan _merge_ ke `main`.

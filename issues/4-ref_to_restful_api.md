# [Refactor] Migrasi Modul menjadi RESTful API dengan FastAPI

## Deskripsi

_Script_ kita sudah memiliki logika validasi, keamanan (_hashing_), dan penyimpanan (_database_). Sekarang, kita harus mengekspos fitur-fitur ini agar bisa digunakan oleh aplikasi _frontend_ dengan menjadikannya sebuah RESTful API.

## Alur Kerja Git & GitHub Issue

Alur yang harus diikuti: **issue -> branch -> implementasi -> commit -> pull request -> ci -> merge**.

1. **Buat GitHub Issue** menggunakan [GitHub CLI](https://cli.github.com/) (`gh`) berdasarkan dokumen ini:

   ```bash
   gh issue create \
     --title "[Refactor] Migrasi Modul menjadi RESTful API dengan FastAPI" \
     --body-file issues/4-ref_to_restful_api.md \
     --label "refactor"
   ```

   Catat nomor issue yang dihasilkan (misal `#4`), lalu gunakan nomor tersebut pada branch dan pesan commit.

2. **Buat branch baru** dari `main` dengan format `feature/issue-4-restful-api`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/issue-4-restful-api
   ```

## Tugas

1. Instal `fastapi` dan `uvicorn` menggunakan `uv`.
2. Ubah struktur `main.py` untuk membuat _instance_ aplikasi FastAPI.
3. Buat sebuah _endpoint_ `POST /register`.
4. Pindahkan logika validasi email dan _password_ ke dalam skema Pydantic (`BaseModel` dengan `@field_validator`).
5. _Endpoint_ harus mengembalikan HTTP Status `201 Created` jika sukses, dan status error yang sesuai (misal `400` atau `422`) jika gagal.

## Menjalankan Server Secara Lokal

Setelah endpoint dibuat, jalankan server FastAPI secara lokal menggunakan mode _development_ agar otomatis _reload_ saat ada perubahan kode:

```bash
uv run fastapi dev main.py
```

Setelah server berjalan, buka dokumentasi API interaktif (Swagger UI) yang otomatis dibuat oleh FastAPI melalui browser:

```
http://localhost:8000/docs
```

Di halaman tersebut Anda dapat melihat dan mencoba langsung _endpoint_ `POST /register` yang baru dibuat, termasuk skema request/response-nya, tanpa perlu tools tambahan seperti Postman.

## Kriteria Penerimaan SQA (API Testing)

1. Instal `httpx` untuk pengujian API.
2. Buat skenario pengujian menggunakan `TestClient` bawaan FastAPI di `test_main.py`.
3. Buat asersi (_assertion_) untuk:
   - _Positive Case:_ Mengembalikan status `201` dan memastikan data masuk ke _database_.
   - _Negative Case:_ Mengirim JSON dengan format email salah, lalu asersi bahwa API mengembalikan status `422 Unprocessable Entity`.

## Instruksi CI/CD

Pastikan Anda menjalankan `uv run pytest` di lokal Anda sebelum membuat _Pull Request_. Pipeline GitHub Actions harus hijau (lulus tes).

Setelah implementasi selesai:

1. `git add . && git commit -m "feat: migrasi ke RESTful API dengan FastAPI"`
2. `git push origin feature/issue-4-restful-api`
3. Buka _Pull Request_ dari branch tersebut ke `main`.
4. Tunggu pipeline CI (GitHub Actions) berjalan dan pastikan statusnya **hijau/lulus**.
5. Setelah PR di-_review_ dan CI lulus, lakukan _merge_ ke `main`.

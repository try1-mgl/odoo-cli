# Panduan Kontribusi (Contributing Guidelines)

Terima kasih telah berkontribusi untuk `odoo-cli`! Untuk memastikan proses pengembangan berjalan lancar dan kolaboratif, silakan ikuti panduan berikut.

---

## 1. Persiapan Lingkungan Pengembangan

1.  **Instalasi Python & Manajer Paket `uv`:**
    Pastikan Anda menggunakan Python 3.11+ dan sudah memasang manajer paket `uv` (pustaka alternatif pip yang sangat cepat).
2.  **Koneksi Database Uji Coba:**
    Pastikan Odoo Docker lokal Anda berjalan di port `8069`.
3.  **Kloning Repositori & Sinkronisasi:**
    ```bash
    git clone <repo-url>
    cd odoo-cli
    uv sync
    ```

---

## 2. Alur Pengembangan Fitur (PR Workflow)

1.  Lakukan sinkronisasi branch `dev` lokal Anda dengan remote server:
    ```bash
    git checkout dev
    git pull origin dev
    ```
2.  Buat branch baru dari `dev` sesuai dengan konvensi [BRANCH_CONVENTION.md](BRANCH_CONVENTION.md):
    ```bash
    git checkout -b feat/connector-timeout
    ```
3.  Lakukan pengerjaan dan commit secara berkala.
4.  Lakukan pengujian lokal & verifikasi sintaks menggunakan `ruff` dan `markdownlint`:
    ```bash
    uv run ruff check .
    markdownlint docs/*.md
    ```
5.  Push branch ke remote GitHub dan buka **Pull Request (PR)** ke branch `dev`.
6.  Setelah minimal 1 anggota tim menyetujui, PR dapat di-merge ke `dev`.

---

## 3. Standard Kualitas Kode

*   **Type Hints:** Wajib menuliskan type hints pada parameter dan tipe data pengembalian fungsi baru.
*   **Keamanan API:** Hindari penggunaan fungsi `eval()` untuk mengevaluasi ekspresi parameter input eksternal. Gunakan safe parser kustom.
*   **Documentation:** Perbarui berkas `design_specs.md` jika Anda mengubah format kontrak API request/response.

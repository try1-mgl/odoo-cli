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
2.  Buat branch baru dari `dev` sesuai dengan **Konvensi Penamaan Branch** di bawah:
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

## 3. Konvensi Penamaan Branch & Commit

### Aturan Penamaan Branch
Semua pengerjaan wajib menggunakan branch yang dibuat dari `dev` dan dimerge kembali ke `dev` melalui Pull Request (PR).

| Tipe Branch | Format Nama | Contoh |
| :--- | :--- | :--- |
| **Fitur Baru** | `feat/<nama-fitur>` | `feat/mcp-server` |
| **Perbaikan Bug** | `fix/<nama-bug>` | `fix/connection-timeout` |
| **Alur Workflow** | `workflow/<nama-alur>` | `workflow/sales-invoice` |
| **Dokumentasi** | `docs/<topik>` | `docs/api-contract` |

### Format Commit Message (Conventional Commits)
Format commit: `<type>(<scope>): <subject>`

**Tipe Commit yang Diizinkan:**
*   `feat`: Penambahan fitur baru (misal: `feat(mcp): tambah tool introspeksi ERD`)
*   `fix`: Perbaikan bug (misal: `fix(connector): tangani timeout XML-RPC`)
*   `docs`: Perubahan dokumentasi saja
*   `style`: Perapian kode (formatting, missing semi-colons, ruff fix)
*   `refactor`: Perubahan struktur kode tanpa mengubah fungsi luar
*   `test`: Penambahan atau perbaikan unit test
*   `chore`: Pemeliharaan build tool, versi dependency, dll.

---

## 4. Standard Kualitas Kode

*   **Type Hints:** Wajib menuliskan type hints pada parameter dan tipe data pengembalian fungsi baru.
*   **Keamanan API:** Hindari penggunaan fungsi `eval()` untuk mengevaluasi ekspresi parameter input eksternal. Gunakan safe parser kustom.
*   **Documentation:** Perbarui berkas `design_specs.md` jika Anda mengubah format kontrak API request/response.

## 5. Versioning & Changelog

Proyek ini menggunakan **Semantic Versioning (SemVer)** dan dikelola menggunakan [Commitizen](https://commitizen-tools.github.io/commitizen/).

Setiap *commit* di *branch* utama yang menggunakan format *Conventional Commits* (seperti `feat:`, `fix:`, dll.) akan secara otomatis menentukan jenis kenaikan versi saat kita menjalankan perintah bump.

### Tata Cara Ganti Versi (Bump Version)
Ganti versi **hanya** dilakukan ketika kita siap merilis fitur baru (misal: saat menutup milestone).

1. Pastikan Anda berada di branch `main` (atau `dev` sesuai kebijakan rilis) dan kondisi working tree bersih:
   ```bash
   git status
   ```
2. Jalankan perintah `cz bump` menggunakan `uv`:
   ```bash
   uv run cz bump
   ```
   Perintah ini akan secara otomatis:
   - Menganalisis riwayat *commit* (feat -> MINOR, fix -> PATCH, BREAKING CHANGE -> MAJOR).
   - Mengubah `"version"` di `pyproject.toml`.
   - Membuat/mengupdate file `CHANGELOG.md`.
   - Membuat *Git Tag* untuk versi tersebut.
3. Push perubahan berserta *tags* ke GitHub:
   ```bash
   git push origin dev --tags
   ```

Aturan Dasar SemVer:
- **PATCH (x.x.1)**: Perbaikan *bug* (dihasilkan dari commit `fix:`).
- **MINOR (x.1.x)**: Fitur baru yang *backward-compatible* (dihasilkan dari commit `feat:`).
- **MAJOR (1.x.x)**: Perubahan signifikan yang merusak kompatibilitas sebelumnya (dihasilkan dari tag `BREAKING CHANGE:` di *body commit*).

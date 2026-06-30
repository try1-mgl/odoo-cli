# AGENTS.md — Panduan dan Aturan untuk AI Coding Agents

File ini berisi instruksi, batasan, dan pedoman gaya pengkodean untuk AI Agent yang berkontribusi dalam pengembangan repositori `odoo-cli`.

---

## 1. Aturan Pengkodean Umum

*   **Bahasa Pemrograman:** Python 3.11+ (Gunakan fitur type hinting di setiap fungsi dan method).
*   **Manajer Paket & Lingkungan:** Proyek menggunakan **`uv`**. Selalu jalankan dependency menggunakan `uv run` atau `uv sync`.
*   **Format Kode:** Gunakan tool `ruff` untuk linting dan formatting.
*   **Prinsip Tanpa Dependensi Berat:** Jaga agar dependensi eksternal tetap minimal (~1MB). Pustaka eksternal yang diizinkan hanya:
    *   `mcp` (untuk protokol MCP)
    *   `rich` (untuk output visual tabel dan teks)
    *   `questionary` (untuk input form dan menu TUI interaktif)
*   **XML-RPC:** Gunakan pustaka standar `xmlrpc.client` bawaan Python dengan menyertakan parameter `allow_none=True`.

---

## 2. Pedoman Konektivitas & Introspeksi

### A. Mekanisme Caching Introspeksi (Penting untuk Performa)

Mengambil skema field dari Odoo via `fields_get` memakan waktu **2-5 detik** — terlalu lambat untuk startup CLI/TUI. AI Agent **wajib** menggunakan caching dengan aturan berikut:

#### Lokasi & Penamaan Cache
- Direktori: `~/.cache/odoo_cli/`
- Format nama: `schema_<hash>.json`
- Hash di-generate dari `sha256(host + database + uid)[:12]`
- Contoh: `schema_learn_a1b2c3.json`
- File permission: **hanya user pemilik** (`0o600`)

#### Siklus Hidup Cache

```
[Mulai Aplikasi]
    │
    ▼
Cache file ~/.cache/odoo_cli/schema_<hash>.json ADA?
  ├── TIDAK → Full fetch + simpan cache → Gunakan skema
  │
  └── YA → Kirim query cepat (50ms):
           execute_kw(ir.module.module, search_read, ...)
              │
              ▼
           write_date Odoo > cached_at?
             ├── YA (ada update modul) → Full fetch + update cache
             └── TIDAK → Baca cache lokal (10ms) → Gunakan
```

#### Validasi Cache (Write-date Check)
Query cepat untuk deteksi perubahan modul terinstall:
```python
models.execute_kw(DB, uid, PASSWORD, 'ir.module.module', 'search_read',
    [[('state', '=', 'installed')]],
    {'fields': ['write_date'], 'order': 'write_date desc', 'limit': 1})
```

Mengapa `ir.module.module`? Setiap perubahan struktur tabel/ERD Odoo (install/update modul) **wajib** mengubah `write_date` pada modul terkait. Satu query ini cukup untuk mendeteksi perubahan tanpa perlu mendownload ulang seluruh skema.

#### Full Fetch Strategy (Saat Cache Invalid)
1. Ambil daftar semua model via `ir.model.search_read`
2. Ambil fields per model secara **paralel** (`ThreadPoolExecutor, max_workers=5`)
   - Parameter `fields_get`: `string`, `type`, `relation`, `required`, `readonly`
3. Parse derived data: kelompokkan relasi per tipe (many2one, one2many, many2many)
4. Simpan ke file dengan mode `0o600`
5. Tampilkan progress bar saat proses

#### Struktur Cache JSON
```json
{
  "metadata": {
    "version": "1.0",
    "host": "http://localhost:8069",
    "database": "learn",
    "user_id": 2,
    "odoo_version": "17.0",
    "cached_at": "2026-06-30T11:15:00Z",
    "last_module_write_date": "2026-06-29 18:30:15",
    "model_count": 452
  },
  "models_list": ["res.partner", "sale.order", ...],
  "models": {
    "res.partner": {
      "model_name": "Contact",
      "fields": {
        "name": { "type": "char", "string": "Name", "required": true },
        "parent_id": { "type": "many2one", "string": "Company", "relation": "res.partner" }
      },
      "relations": {
        "many2one": [{"field": "parent_id", "relation": "res.partner", "label": "Company"}],
        "one2many": [],
        "many2many": []
      }
    }
  }
}
```

Estimasi ukuran: ~100 KB (50 model) hingga ~1.2 MB (450+ model).

#### Edge Cases
| Skenario | Perilaku |
|---|---|
| **First run** (no cache) | Full fetch + progress bar |
| **Cache valid** | 0 query besar, startup <100ms |
| **Koneksi Odoo mati, cache ada** | Warning + pakai cache (lebih baik dari error total) |
| **Cache corrupt** | Hapus otomatis → fallback full fetch |
| **`--clear-cache`** | Hapus semua file di `~/.cache/odoo_cli/` |

#### Larangan
- **JANGAN** simpan credential (password, API key) di file cache
- **JANGAN** panggil `fields_get` untuk semua model tanpa cache — ini membuat startup lambat
- **JANGAN** panggil `fields_get` secara sekuensial — gunakan paralel (`ThreadPoolExecutor`)

Referensi lengkap: `docs/adr/0005-introspection-caching.md`

### B. Batasan OS & Jaringan
*   **Target OS:** Pengembangan dan pengujian difokuskan pada **Arch Linux**.
*   **Filesystem Independence:** Jangan menulis logika yang mengasumsikan tipe berkas database (seperti btrfs atau ext4). Semua komunikasi database murni melalui soket jaringan XML-RPC.
*   **Multi-Profile Support:** Koneksi database harus diload secara dinamis dari file `profiles.json` menggunakan profil tertentu (`--profile`).

---

## 3. Aturan Validasi Input & CRUD

*   **Paginasi Wajib:** Setiap operasi pencarian (`search`) ke Odoo wajib menyertakan parameter `limit` (default: 80) dan `offset`. Jangan pernah membiarkan query mengambil data tanpa batas.
*   **Smart Search Parser:** Sebelum mengirim domain pencarian ke Odoo, parsing string pencarian sederhana (seperti `name:eka OR city:Bandung`) menjadi domain Notasi Polish Odoo menggunakan parser internal.
*   **Validasi Lokal:** Sebelum memanggil XML-RPC Odoo untuk membuat/menulis data, bandingkan field input dengan metadata hasil introspeksi lokal. Lempar error secara lokal jika field tidak terdaftar atau tipe data tidak cocok guna menghemat request jaringan.

---

## 4. Mekanisme Workflow & Kompensasi Error (Rollback)

*   **Resolusi Variabel:** Langkah-langkah workflow berjalan sekuensial. Dukung ekspresi string penampung data (seperti `{{params.customer_id}}` dan `{{steps.buat_so.id}}`).
*   **Pembersihan Error (Rollback):** Karena transaksi XML-RPC bersifat auto-commit per request, jika terjadi kegagalan di tengah-tengah langkah workflow, Anda harus menjalankan instruksi kompensasi yang didefinisikan pada blok `"on_error"` di masing-masing step untuk menghapus atau membatalkan dokumen yang telanjur terbuat.

---

## 5. Strategi Rilis (Semantic Versioning)

*   Ganti versi di file `pyproject.toml` terlebih dahulu sebelum melakukan tag git rilis (misal: `v0.1.0`).
*   Ikuti prinsip **SemVer**:
    *   **MAJOR:** Jika ada perubahan struktur model atau kontrak API inti yang merusak sistem yang ada.
    *   **MINOR:** Jika ada penambahan menu TUI, tool MCP baru, atau alur workflow baru.
    *   **PATCH:** Untuk perbaikan bug ringan.

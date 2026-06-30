# ADR-0005: Strategi Caching Introspeksi (Kecepatan Startup)

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

`odoo-cli` bergantung pada introspeksi dinamis terhadap model Odoo via `fields_get` XML-RPC untuk mendapatkan daftar field, tipe data, dan relasi. Proses ini memakan waktu **2-5 detik** setiap kali tool dijalankan karena:

1. Odoo server harus membaca definisi class Python dari database.
2. Odoo melakukan evaluasi hak akses (ACL) terhadap user yang login untuk setiap field.
3. Mengembalikan dictionary berukuran besar (ratusan KB per model).

Untuk model seperti `res.partner` (~195 field) atau `sale.order` (~250 field), satu panggilan `fields_get` butuh 0.5-2 detik. Jika dilakukan untuk semua model (200-450+ model), startup menjadi sangat lambat dan tidak responsif, terutama bagi TUI dan CLI yang dieksekusi berulang kali.

### Estimasi Performa

| Skenario | Tanpa Cache | Dengan Cache (valid) | Dengan Cache (invalid) |
|---|---|---|---|
| Startup TUI | 4.5 detik | **0.08 detik** | 4.6 detik |
| Startup CLI | 4.5 detik | **0.05 detik** | — |
| Tab complete | N/A | **Instan** (<10ms) | — |

## Keputusan (Decision)

Kami memutuskan untuk menerapkan **mekanisme Metadata Caching lokal** dengan strategi sebagai berikut:

### 1. Lokasi & Penamaan File Cache

Cache disimpan di `~/.cache/odoo_cli/schema_<hash>.json` dengan hash berbasis `host + database + uid` untuk menghindari tabrakan antar server/database.

```
~/.cache/odoo_cli/
├── schema_learn_a1b2c3.json        # learn@localhost:8069
├── schema_prod_db1_x9y8z7.json     # prod_db1@staging.company.com
└── schema_test_z3w4v5.json          # test@192.168.1.50:8069
```

### 2. Struktur JSON Cache

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
        "email": { "type": "char", "string": "Email" },
        "parent_id": { "type": "many2one", "string": "Company", "relation": "res.partner" },
        "child_ids": { "type": "one2many", "string": "Contacts", "relation": "res.partner" },
        "category_id": { "type": "many2many", "string": "Tags", "relation": "res.category" }
      },
      "relations": {
        "many2one": [{"field": "parent_id", "relation": "res.partner", "label": "Company"}],
        "one2many": [{"field": "child_ids", "relation": "res.partner", "label": "Contacts"}],
        "many2many": [{"field": "category_id", "relation": "res.category", "label": "Tags"}]
      }
    }
  }
}
```

Estimasi ukuran: ~100 KB (50 model) hingga ~1.2 MB (450+ model). Dibaca dalam 10-20ms dari disk.

### 3. Alur Validasi Cache (Write-date Check)

Sebelum melakukan full fetch, system mengirim query cepat (~50ms) untuk deteksi perubahan:

```python
models.execute_kw(DB, uid, PASSWORD, 'ir.module.module', 'search_read',
    [[('state', '=', 'installed')]],
    {'fields': ['write_date'], 'order': 'write_date desc', 'limit': 1})
```

Logika:
- Jika `write_date` Odoo > `cached_at` di cache → ada perubahan modul → refetch
- Jika `write_date` Odoo <= `cached_at` → cache valid → baca lokal
- Jika koneksi gagal → fallback ke cache + beri warning

### 4. Full Fetch Strategy

Saat cache invalid/tidak ada:
1. **Ambil daftar semua model** via `ir.model.search_read`
2. **Ambil fields per model secara paralel** via `ThreadPoolExecutor(max_workers=5)`
   - `fields_get` per model dipanggil dengan atribut: `string`, `type`, `relation`, `required`, `readonly`
3. **Parse derived data** (relasi per tipe: many2one, one2many, many2many)
4. **Simpan ke file** dengan mode `0o600` (hanya user pemilik)
5. **Tampilkan progress bar** (Rich Progress) saat proses berlangsung

### 5. Keamanan Cache

| Aspek | Penanganan |
|---|---|
| Credential | **Tidak disimpan** — cache hanya berisi definisi field, bukan data |
| File permission | Mode `0o600` |
| Cache corrupt | Deteksi JSON invalid → hapus otomatis → fallback full fetch |
| Multi-user | Cache terpisah per `uid` |

## Konsekuensi (Consequences)

### Positif:
- Startup TUI/CLI dari 4.5 detik menjadi <100ms (95% lebih cepat)
- Autocomplete TUI menjadi instan
- AI Agent di MCP mode tidak perlu menunggu lama untuk setiap tool call
- Cache aman (tidak menyimpan credential atau data bisnis)

### Negatif:
- File cache memakan ruang disk (~1-2 MB per server/database)
- Perlu logika validasi write_date tambahan (~50ms tiap startup)
- Jika user berganti server, perlu `--clear-cache` manual

## Perintah Pendukung

```bash
# Paksa hapus semua cache dan refetch
odoo-cli --clear-cache
```

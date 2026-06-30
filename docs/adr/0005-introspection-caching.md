# ADR-0005: Mekanisme Caching Skema Introspeksi Odoo

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Mengambil data skema field (introspeksi) Odoo via XML-RPC `fields_get` memakan waktu 0.8 s.d 2.5 detik per model. Jika `odoo-cli` harus melakukan query langsung ke server setiap kali dijalankan (baik oleh manusia via TUI maupun AI via MCP), program akan terasa lambat (*laggy*). Kami memerlukan cara untuk menyimpan data skema di lokal namun tetap sinkron dengan perubahan modul kustom di server Odoo.

## Keputusan (Decision)

Kami memutuskan untuk mengimplementasikan **Local Schema Caching** dengan mekanisme validasi tanggal modifikasi terakhir dari modul terinstal (`ir.module.module`).

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **Startup Instan:** Loading TUI/MCP berkurang menjadi kurang dari 10ms saat membaca dari berkas cache JSON lokal.
* **Deteksi Perubahan Otomatis:** Kita hanya mengirim query XML-RPC minimal (waktu eksekusi ~30ms) untuk memeriksa `write_date` terbaru dari modul terinstal. Jika ada perubahan, cache diperbarui secara otomatis.
* **Validasi Lokal:** Memungkinkan program melakukan validasi tipe data input secara lokal sebelum mengirim request ke server Odoo, sehingga menghemat konsumsi jaringan.

### Kekurangan (Negatif):
* Menghasilkan berkas cache di direktori home (`~/.cache/odoo_cli/`). Pengguna perlu diberikan opsi perintah manual `--clear-cache` jika ingin menghapus cache tersebut secara paksa.

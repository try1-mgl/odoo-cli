# ADR-0003: Penggunaan Rich + LazyUI ketimbang Textual untuk TUI

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Untuk membangun mode interaktif TUI (Text User Interface) yang ramah pengguna, kami membutuhkan pustaka visual Python. Pilihan utamanya adalah:
1. **Textual:** Framework TUI reaktif berbasis komponen yang sangat canggih, namun memiliki ukuran pustaka yang besar, arsitektur kode yang kompleks, dan *learning curve* yang curam.
2. **Rich + LazyUI:** Kombinasi penampil visual terminal (`rich`) dan pengelola form/prompt deklaratif interaktif (`lazyui`).

## Keputusan (Decision)

Kami memutuskan menggunakan kombinasi **Rich + LazyUI** untuk menyusun antarmuka TUI pada `odoo-cli`.

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **Sangat Ringan:** Kombinasi ini hanya menambahkan overhead memori sekitar ~1MB, sangat cocok untuk tool CLI/TUI yang harus dijalankan cepat.
* **Format Output Indah:** `rich` mempermudah pembuatan tabel data Odoo dengan warna-warna status, alignment otomatis, dan penanganan pemotongan teks terminal (*text wrapping*).
* **Deklaratif Form yang Mudah:** `lazyui` mempermudah pembuatan prompt input data interaktif dengan kode minimal.
* **Kemudahan Integrasi:** Struktur data output `rich` sangat mudah disinkronkan dengan data JSON mentah hasil eksekusi CLI.

### Kekurangan (Negatif):
* Tidak memiliki fitur widget kompleks multipanel/multi-window seperti Textual. Namun, karena kebutuhan TUI `odoo-cli` didominasi oleh pemilihan menu, pengisian form, dan pembacaan tabel data, fungsionalitas Rich + LazyUI sudah sangat mencukupi.

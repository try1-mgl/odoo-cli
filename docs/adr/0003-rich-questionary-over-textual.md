# ADR-0003: Penggunaan Rich + Questionary ketimbang Textual untuk TUI

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Untuk membangun mode interaktif TUI (Text User Interface) yang ramah pengguna, kami membutuhkan pustaka visual Python. Pilihan utamanya adalah:
1. **Textual:** Framework TUI reaktif berbasis komponen yang sangat canggih, namun memiliki ukuran pustaka yang besar, arsitektur kode yang kompleks, dan *learning curve* yang curam.
2. **Rich + Questionary:** Kombinasi penampil visual terminal (`rich`) dan pengelola prompt/menu interaktif (`questionary`) yang ringan, matang, dan berbasis `prompt_toolkit`.

## Keputusan (Decision)

Kami memutuskan menggunakan kombinasi **Rich + Questionary** untuk menyusun antarmuka TUI pada `odoo-cli`.

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **Sangat Ringan:** Kombinasi ini sangat cepat dimuat dan tidak memerlukan overhead memori besar (di bawah ~1MB).
* **Format Output Indah:** `rich` mempermudah pembuatan tabel data Odoo dengan warna-warna status, alignment otomatis, dan penanganan pemotongan teks terminal (*text wrapping*).
* **Kompabilitas Arch Linux:** `questionary` terbukti berjalan dengan sangat stabil di terminal Arch Linux selama masa spike pengujian.
* **Kemudahan Integrasi:** Struktur data output `rich` sangat mudah disinkronkan dengan data JSON mentah hasil eksekusi CLI.

### Kekurangan (Negatif):
* Tidak memiliki fitur widget kompleks multipanel/multi-window seperti Textual. Namun, karena kebutuhan TUI `odoo-cli` didominasi oleh pemilihan menu, pengisian form, dan pembacaan tabel data, fungsionalitas Rich + Questionary sudah sangat mencukupi.

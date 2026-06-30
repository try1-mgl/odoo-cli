# ADR-0001: Penggunaan Python ketimbang Go

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Kami memerlukan bahasa pemrograman untuk membangun tool `odoo-cli` yang:
1. Berkomunikasi dengan server Odoo melalui protokol XML-RPC.
2. Mendukung Model Context Protocol (MCP) untuk interaksi dengan AI agents.
3. Memiliki ekosistem TUI (Text User Interface) yang modern dan interaktif.
4. Mudah dipasang dan dijalankan oleh developer maupun AI agents di lingkungan Linux Arch.

Go sempat dipertimbangkan karena menghasilkan single binary mandiri yang cepat dan portabel.

## Keputusan (Decision)

Kami memutuskan untuk menggunakan **Python 3.11+** sebagai bahasa pemrograman utama proyek ini.

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **XML-RPC Bawaan:** Python memiliki pustaka bawaan `xmlrpc.client` di pustaka standarnya (stdlib), sehingga tidak memerlukan dependensi eksternal untuk komunikasi Odoo.
* **Dukungan Resmi MCP:** Protokol MCP dikembangkan secara resmi oleh Anthropic dengan SDK Python (`mcp` library), meminimalkan risiko kompatibilitas.
* **TUI Stack yang Kaya:** Python memiliki pustaka visual TUI yang matang seperti `rich` dan `lazyui` untuk menghasilkan UI terminal yang indah.
* **Kecocokan Ekosistem Odoo:** Odoo sendiri dibangun di atas Python, sehingga struktur tipe data (dictionary, list) sangat selaras dan mudah dipetakan secara dinamis.

### Kekurangan (Negatif):
* Pengguna harus menginstal interpreter Python dan dependensi proyek. Risiko ini akan kami mitigasi dengan menggunakan manajer paket **`uv`** (`uv sync` / `uv run`) yang sangat cepat, terisolasi, dan menjamin replikasi dependensi secara deterministik.

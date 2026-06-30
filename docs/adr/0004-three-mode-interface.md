# ADR-0004: Implementasi Tiga Mode Antarmuka (TUI, CLI, dan MCP)

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Tool `odoo-cli` harus dapat digunakan secara fleksibel oleh berbagai konsumen:
1. **Developer / Admin (Manusia):** Membutuhkan antarmuka visual terminal interaktif (TUI) untuk eksplorasi cepat.
2. **Skrip otomatisasi / Integrasi pihak ketiga:** Membutuhkan mode input-output JSON standar (CLI) yang konsisten.
3. **AI Agent (seperti Claude/Gemini via IDE):** Membutuhkan protokol standar Model Context Protocol (MCP) untuk memanggil tool Odoo.

## Keputusan (Decision)

Kami memutuskan untuk mengimplementasikan **tiga mode antarmuka** sekaligus pada satu berkas entry point `odoo_cli.py` dengan deteksi otomatis tipe input/argumen.

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **Single Source of Truth:** Seluruh mode antarmuka memanggil logika eksekusi Odoo yang sama di folder `core/` (`connector.py`, `executor.py`). Tidak ada duplikasi logika bisnis.
* **Universal Bridge:** Menjembatani kebutuhan manusia dan AI dalam satu codebase tunggal.
* **Deteksi Otomatis:** Memudahkan pemanggilan tanpa konfigurasi rumit (cukup mendeteksi `--mcp`, parameter argumen CLI, atau input tty standar).

### Kekurangan (Negatif):
* Kompleksitas entrypoint `odoo_cli.py` meningkat karena harus memisahkan aliran data TUI (Rich), CLI (Standard IO), dan MCP (Stdio Server Protocol). Risiko ini akan kami mitigasi dengan memisahkan handler masing-masing mode ke modul terpisah jika file entrypoint terlalu besar.

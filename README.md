# odoo-cli — Terminal Client & MCP Server for Odoo ERP

`odoo-cli` adalah alat antarmuka baris perintah (CLI), terminal interaktif (TUI), dan Server Model Context Protocol (MCP) terpadu yang dirancang khusus untuk mempermudah eksplorasi, manipulasi data, dan otomatisasi alur kerja pada server Odoo (versi 17 ke atas).

Alat ini menjembatani interaksi antara pengembang manusia (melalui terminal interaktif) dan AI Coding Assistant (seperti Claude/Gemini via protokol MCP) secara aman dan responsif.

---

## ✨ Fitur Utama

1.  **Tiga Mode Akses Terpadu:**
    *   **TUI Mode (Human):** Antarmuka visual terminal interaktif berbasis `questionary` & `rich` untuk eksplorasi data yang ramah.
    *   **CLI Mode (Script):** Pemanggilan fungsi Odoo via JSON satu baris untuk skrip otomatisasi.
    *   **MCP Mode (AI):** Protokol standard stdio server untuk mengintegrasikan asisten koding AI langsung ke Odoo.
2.  **Smart Search Query Parser:** Mengonversi pencarian teks sederhana (seperti `name:eka OR city:Bandung`) ke format domain Notasi Polish Odoo secara otomatis.
3.  **Local Schema Caching:** Startup instan (< 10ms) dengan menyimpan metadata introspeksi model lokal secara cerdas dan mendeteksi kadaluwarsa cache secara dinamis.
4.  **Declarative JSON Workflows:** Otomatisasi rantai transaksi bisnis (SO ➡️ Delivery ➡️ Invoice) dengan penanganan rollback / pembatalan terotomatisasi jika terjadi kegagalan.
5.  **AI Safety Guardrails:** Konfirmasi persetujuan manusia (HITL) untuk database produksi dan pembuatan log undo transaksi pemulihan data.

---

## 🚀 Memulai (Getting Started)

### Prasyarat
*   Python 3.11 atau lebih tinggi.
*   Manajer paket **`uv`** (sangat direkomendasikan).

### Instalasi Proyek
1.  Kloning repositori ini.
2.  Pasang dependensi secara otomatis menggunakan `uv`:
    ```bash
    uv sync
    ```

### Konfigurasi Koneksi (Profiles)
Buat berkas konfigurasi `profiles.json` di direktori proyek Anda dengan mencontoh template [profiles.json.template](profiles.json.template):
```bash
cp profiles.json.template profiles.json
```
Edit berkas `profiles.json` dan masukkan kredensial koneksi server Odoo Anda.

---

## 📖 Cara Penggunaan (Usage)

### 1. Mode TUI (Interactive Terminal)
Jalankan menu interaktif dropdown dan form isian:
```bash
uv run python odoo_cli.py
```

### 2. Mode CLI (JSON-in JSON-out)
Kirim instruksi satu baris untuk integrasi skrip pihak ketiga:
```bash
uv run python odoo_cli.py '{"action": "search", "model": "res.partner", "domain": "name:eka", "limit": 2, "offset": 0}'
```

### 3. Mode MCP Server (AI Integration)
Sambungkan Odoo dengan asisten koding AI Anda menggunakan parameter `--mcp`:
```bash
uv run python odoo_cli.py --mcp
```

---

## 🛠️ Pengembangan (Development)

Silakan pelajari dokumen pedoman pengkodean kami berikut:
*   [PLAN.md](PLAN.md) — Rencana pengembangan dan peta jalan fitur.
*   [AGENTS.md](AGENTS.md) — Aturan gaya koding khusus asisten koding AI.
*   [CONTRIBUTING.md](CONTRIBUTING.md) — Panduan kolaborasi dan PR.
*   [BRANCH_CONVENTION.md](BRANCH_CONVENTION.md) — Konvensi nama branch & pesan git commit.
*   [docs/design_specs.md](docs/design_specs.md) — Arsitektur C4, User Stories, dan Kontrak API JSON.

---

## 📄 Lisensi
Proyek ini didistribusikan di bawah lisensi **MIT**.

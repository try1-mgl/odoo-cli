# odoo-cli — Universal Odoo CLI, TUI & MCP Tool

Satu tool untuk **human (CLI/TUI)** dan **AI agents (MCP)**.
Berkomunikasi dengan Odoo via XML-RPC, auto-adapt ke modul Odoo mana pun.

---

## Visi & Tujuan Akhir

Tool ini adalah **jembatan universal antara manusia/AI dan Odoo**.
Tidak perlu modifikasi di sisi Odoo — cukup koneksi XML-RPC, langsung bisa:
search, create, read, write, execute method, dan menjalankan alur bisnis.

---

## Target Pengguna

`odoo-cli` dirancang khusus untuk kelompok pengguna berikut:
1.  **Odoo Developers / Pengembang:** Membantu inspeksi struktur model database (ERD), debug method secara langsung tanpa menulis kode Python test script, serta melakukan *scaffolding* module kustom.
2.  **Power Users / Administrator Odoo:** Mempermudah manipulasi data skala besar, penyesuaian konfigurasi sistem cepat, dan analisis relasi data secara interaktif.
3.  **System Integrators / Backend Devs:** Pengembang sistem eksternal yang menggunakan Odoo sebagai backend database (ERD), membantu ekspor skema referensi API/Kontrak JSON untuk proyek lain.

---

## 3 Mode Operasi

| Mode | Perintah | Target | Interaksi |
|---|---|---|---|
| **TUI** | `python odoo_cli.py` | Human | Interactive (Rich + LazyUI) |
| **CLI** | `python odoo_cli.py '{json}'` | AI / script | JSON in → JSON out |
| **MCP** | `python odoo_cli.py --mcp` | AI Agents | MCP stdio protocol |

Deteksi otomatis di entry point:

```python
if '--mcp' in sys.argv:
    run_mcp()
elif not sys.stdin.isatty():
    run_cli()
elif len(sys.argv) > 1:
    run_cli()
else:
    run_tui()
```

---

## Fitur Utama

### 1. Universal CRUD (7 Actions) dengan Paginasi & Smart Parser

Bisa untuk **SEMUA model Odoo** — tanpa hardcode nama model.

*   **Paginasi bawaan:** Perintah `search` dan `read` wajib mendukung parameter opsional `limit` (default: 80) dan `offset` untuk mencegah kemacetan memori pada database besar.
*   **Smart Search Query Parser:** Pengguna/AI dapat menulis pencarian dengan format string sederhana (seperti query SQL/Google) yang otomatis diterjemahkan menjadi Domain Notasi Polish Odoo oleh parser internal:
    *   *Input:* `name:eka OR city:Bandung`
    *   *Hasil:* `['|', ('name', 'ilike', 'eka'), ('city', '=', 'Bandung')]`

| Action | Fungsi | Contoh |
|---|---|---|
| `search` | Cari record (support query parser & limit) | `res.partner, domain="name:budi", limit=10` |
| `create` | Buat record | `sale.order, values={...}` |
| `read` | Baca detail | `product.product, id=5` |
| `write` | Update | `stock.quant, id=3, values={inventory_quantity:10}` |
| `delete` | Hapus | `hr.leave, id=2` |
| `execute` | Panggil method Odoo | `sale.order, id=1, method="action_confirm"` |
| `schema` | Lihat struktur model | `res.partner` → balikin semua field + tipe |

### 2. Dynamic Introspection & ERD/Relation Mapper (Developer-Centric)

Query `ir.model` + `ir.model.fields` langsung dari Odoo.

- **Dukungan Modul Kustom:** Otomatis mendeteksi modul dan model kustom baru secara *real-time* tanpa perubahan kode di sisi CLI.
- **ERD & Relationship Mapper:** Mampu menganalisis hubungan relasional field (`many2one`, `one2many`, `many2many`) antar-model Odoo, kemudian menyajikannya dalam format tabel Markdown atau skema relasi terstruktur untuk mempermudah perancangan ERD proyek kustom.
- **Export Schema Reference:** Fitur ekspor skema data model menjadi file JSON atau dokumentasi Markdown untuk dijadikan referensi kontrak API/database bagi proyek eksternal lain yang terintegrasi dengan backend Odoo.

### 3. Workflow Runner dengan Validasi & Rollback

Flow bisnis didefinisikan sebagai file JSON.

```json
{
  "name": "Fulfill Sales Order",
  "params": ["customer", "products", "vendor"],
  "steps": [
    {
      "action": "create", 
      "model": "sale.order", 
      "values": "{{so_data}}", 
      "save_as": "so",
      "on_error": [
        {"action": "delete", "model": "sale.order", "id": "{{so}}"}
      ]
    },
    {"action": "execute", "model": "sale.order", "method": "action_confirm", "id": "{{so}}"}
  ]
}
```

*   **Rollback Handler (`on_error`):** Jika sebuah langkah eksekusi gagal, workflow runner akan menjalankan langkah kompensasi yang didefinisikan pada blok `on_error` untuk menjaga konsistensi data.
*   **JSON Schema Validation:** Menyediakan perintah `--validate-workflow <path>` untuk memverifikasi struktur file JSON sebelum dijalankan.

### 4. Template & Scaffold

Developer tinggal jalanin satu perintah untuk generate file baru:

```bash
python odoo_cli.py --scaffold method sale.order action_confirm
python odoo_cli.py --scaffold workflow approve_expense
```

### 5. TUI Mode & Interactive Cheatsheet (Human Friendly)

- Pilih menu dengan arrow key.
- Autocomplete nama model Odoo menggunakan data hasil introspeksi dinamis.
- Hasil ditampilkan sebagai tabel rapi (warna, alignment).
- **Cheatsheet Screen (`?` key):** Layar khusus berisi dokumentasi cepat sintaks domain Odoo (AND, OR, NOT), kamus operator umum (`ilike`, `child_of`, `in`), serta peta model Odoo terpopuler (`res.partner`, `hr.employee`, `sale.order`).

### 6. MCP Mode & Connection Resilience (AI Friendly)

Ekspos 8 tools via MCP protocol:
`search`, `create`, `read`, `write`, `delete`, `execute`, `schema`, `run_workflow`

*   **Auto-Reconnection:** Mendeteksi koneksi terputus atau sesi habis, lalu mengautentikasi ulang secara otomatis sebanyak 1 kali.
*   **API Key Support:** Mendukung autentikasi menggunakan Odoo API Key demi keamanan.

### 7. Database Discovery & Security/Session Manager

*   **Database Discovery:** Menggunakan service `/xmlrpc/2/db` Odoo (method `list`) untuk mendeteksi secara otomatis database Odoo apa saja yang aktif pada server.
*   **Password Hash & Encryption Inspector (Admin Only):** Mampu menarik daftar user dari model `res.users` beserta *encrypted password hash* mereka (jika memiliki hak akses admin). Tool secara otomatis mendeteksi dan menampilkan jenis algoritma enkripsi yang dipakai berdasarkan *prefix hash* (misal: `$pbkdf2-sha512$` untuk PBKDF2-SHA512 atau `$bcrypt$` / `$2b$` untuk Bcrypt).
*   **Multi-User Session Switcher:** Memungkinkan pengguna/AI memilih dan mengganti akun pengguna Odoo secara dinamis untuk melakukan operasi tertentu (misal: membuat SO menggunakan session Bu Nanda, lalu menyetujui expense menggunakan session Bu Ayu).

---

## Arsitektur Direktori

```
odoo-cli/
│
├── odoo_cli.py                 ← Entry point (TUI / CLI / MCP)
├── pyproject.toml              ← Metadata + dependencies
├── PLAN.md                     ← Dokumen ini
├── AGENTS.md                   ← Panduan gaya dan aturan untuk AI Agents
├── README.md                   ← Panduan pengguna
├── LICENSE                     ← MIT
│
├── docs/
│   ├── adr/
│   │   ├── 0001-use-python-over-go.md
│   │   ├── 0002-xmlrpc-over-rest.md
│   │   ├── 0003-rich-questionary-over-textual.md
│   │   ├── 0004-three-mode-interface.md
│   │   ├── 0005-introspection-caching.md
│   │   └── 0006-ai-safety-guardrails.md
│   └── design_specs.md         ← User stories, API contract, C4 diagram
│
├── core/
│   ├── __init__.py
│   ├── connector.py            ← XML-RPC connection & auth
│   ├── helpers.py              ← Utility functions (get_or_create, dll.)
│   ├── introspection.py        ← Dynamic model discovery & schema caching
│   ├── executor.py             ← 7 universal CRUD + execute
│   ├── workflows.py            ← Workflow JSON runner
│   ├── guardrails.py           ← AI safety, human-in-the-loop approval
│   └── history.py              ← Transaction history log & undo engine
│
├── odoo_methods/               ← Wrapper method bisnis per module
│   ├── __init__.py
│   ├── sale.py                 → action_confirm, _create_invoices
│   ├── purchase.py             → button_confirm, action_create_invoice
│   ├── stock.py                → button_validate
│   ├── account.py              → action_post
│   ├── hr_expense.py           → action_submit_sheet, action_approve_expense_sheets
│   └── hr_holidays.py          → action_approve, action_validate
│
├── workflows/                  ← Flow bisnis (JSON)
│   ├── fulfillment.json        → SO → PO → Receipt → DO → Invoice
│   ├── hr_meeting.json         → Client → Employee → Calendar → Expense → Approve
│   └── sales_invoice.json      → SO → Delivery → Invoice → Payment
│
├── templates/                  ← Template untuk extensi
│   ├── odoo_method.py          → Template wrapper module baru
│   └── workflow.json           → Template workflow kosong
│
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── ISSUE_TEMPLATE/
    │   ├── config.yml
    │   ├── 01_bug_report.yml
    │   ├── 02_feature_request.yml
    │   ├── 03_new_workflow.yml
    │   └── 04_compatibility.yml
    ├── workflows/
    │   └── ci.yml              ← Lint + validate otomatis
    ├── CONTRIBUTING.md
    └── BRANCH_CONVENTION.md
```

---

## Tech Stack

| Komponen | Pilihan | Alasan |
|---|---|---|
| Bahasa | Python 3.11+ | XML-RPC built-in, MCP SDK, code existing |
| XML-RPC | `xmlrpc.client` | Bawaan Python, nol dependensi |
| MCP | `mcp` | stdio transport, ringan |
| TUI output | `rich` | Tabel, warna, format rapi |
| TUI input | `questionary` | Prompt interaktif berbasis prompt_toolkit |
| Format data | JSON | Universal, mudah parse AI & human |
| Auth | ENV + default | `ODOO_URL`, `ODOO_DB`, `ODOO_USERNAME`, `ODOO_PASSWORD` |

### Dependencies

```toml
dependencies = [
    "mcp>=1.0.0",
    "rich>=13.0.0",
    "questionary>=2.0.0",
]
```

Total ~1.1MB tambahan dari Python stdlib.

---

## Workflow Kolaborasi (2 Orang)

### Branch Strategy

```
main          → stabil, siap release
dev           → integrasi harian
feat/*        → fitur baru (branch dari dev, merge ke dev)
fix/*         → perbaikan bug
workflow/*    → workflow JSON baru
docs/*        → dokumentasi
```

### Alur Kontribusi

1. Branch dari `dev` → `feat/executor`
2. Commit + Push
3. Buka PR ke `dev`
4. CI jalan (ruff check + syntax validate)
5. 1 orang review
6. Merge ke `dev`
7. Kalau `dev` stabil → merge ke `main`

### Pembagian Tugas (Saran)

| Orang | Tanggung Jawab |
|---|---|
| **Kamu** | `core/executor.py`, `core/introspection.py`, `odoo_cli.py` entry point, CLI + MCP mode |
| **Temen** | `core/workflows.py`, `odoo_methods/*.py`, `workflows/*.json`, TUI mode, Templates + scaffold |

### Versioning Strategy (SemVer)

Untuk mengelola siklus rilis secara profesional dan memastikan kestabilan bagi pengguna/AI, `odoo-cli` mengadopsi standar **Semantic Versioning (SemVer)** dengan format `vMAJOR.MINOR.PATCH` (misal: `v0.1.0`):

*   **MAJOR:** Perubahan besar yang merusak kompatibilitas API (*breaking changes*).
*   **MINOR:** Penambahan fitur baru yang bersifat *backward-compatible* (misal: penambahan menu TUI atau tool MCP baru).
*   **PATCH:** Perbaikan bug (*bug fixes*) tanpa penambahan fitur baru atau perubahan API.

#### Alur Rilis & Manajemen Versi di GitHub:
1.  **pyproject.toml Sync:** Sebelum melakukan rilis, versi pada file `pyproject.toml` wajib diperbarui (misal: `version = "0.1.0"`) agar CLI dapat membaca versi tersebut saat dijalankan dengan parameter `--version`.
2.  **Git Tag:** Tandai commit stabil pada branch `main` dengan perintah:
    ```bash
    git tag v0.1.0
    git push origin v0.1.0
    ```
3.  **GitHub Release:** Membuat rilis resmi baru di halaman GitHub dari tag tersebut, lengkap dengan lampiran berkas rilis dan ringkasan *Changelog* perubahan.

---

## Timeline Pengembangan

| Fase | Fitur | Perkiraan Hari |
|---|---|---|
| **v0.1-core** | connector, executor, introspection, CLI entry, pyproject.toml, .gitignore | Hari 1-2 |
| **v0.2-tui** | TUI mode (Rich + LazyUI), menu interaktif, output tabel | Hari 3 |
| **v0.3-mcp** | MCP mode, 8 tools, register guide | Hari 4 |
| **v0.4-workflows** | workflow runner, templates, scaffold command, contoh JSON | Hari 5-6 |
| **v0.5-polish** | README, .github/ templates, CI, final testing, push GitHub | Hari 7 |

---

## Cara Pakai

```bash
# Clone
git clone https://github.com/try1-mgl/odoo-cli.git
cd odoo-cli

# Setup
uv venv && uv sync

# ── TUI Mode (Human) ──
python odoo_cli.py

# ── CLI Mode (AI / Script) ──
python odoo_cli.py '{"action":"search","model":"res.partner","domain":[["name","ilike","budi"]]}'

# ── MCP Mode (AI Agents) ──
python odoo_cli.py --mcp

# ── Scaffold Mode (Developer) ──
python odoo_cli.py --scaffold method sale.order action_confirm
python odoo_cli.py --scaffold workflow approve_expense
```

---

## Mekanisme Integrasi & Spesifikasi OS

### 1. Cara Kerja Integrasi Jaringan & Multi-Container
`odoo-cli` bersifat **network-centric** dan berkomunikasi secara eksklusif menggunakan protokol **XML-RPC** melalui soket TCP/IP. Hal ini membuatnya sangat fleksibel untuk terintegrasi dengan berbagai jenis arsitektur Odoo:
*   **Odoo Docker (Containerized):** Menghubungkan ke port container yang dipetakan (*port mapping*) pada sistem host (default: `http://localhost:8069`). Tool ini mampu mengelola **satu atau lebih container Odoo secara bersamaan** dengan menyimpan profil koneksinya.
*   **Odoo Native (Bare-metal):** Menghubungkan ke service lokal Odoo yang berjalan langsung pada host OS (localhost/127.0.0.1).
*   **Proyek Eksternal / Remote Odoo:** Menghubungkan ke server Odoo lain (baik di AWS, VPS, maupun jaringan lokal) menggunakan alamat IP publik atau domain internet.
*   **Multi-Instance Profile Manager:** Pengguna dapat mendefinisikan beberapa profil koneksi (misal: `local_docker_1`, `local_docker_2`, `staging`) dalam sebuah file konfigurasi lokal (`profiles.json`) dan berpindah-pindah koneksi secara instan via argumen CLI atau menu TUI.

### 2. Kompatibilitas Versi Odoo
*   **Versi Target:** Kompatibel dengan berbagai versi Odoo mulai dari **Odoo 17 (sebagai batas versi paling lama)** hingga **versi Odoo terbaru (Odoo 18, 19, dst.)**. Pembatasan ini dilakukan untuk memastikan kecocokan dengan standard ORM Odoo modern yang diperkenalkan sejak versi 17.

### 3. Spesifikasi Lingkungan Kerja & Sistem Berkas (Filesystem)
*   **Batasan OS Target:** Selama fase pengembangan awal, proyek ini dikhususkan, dibatasi, dan diuji pada lingkungan **Arch Linux**.
*   **Kompatibilitas Filesystem (BTRFS / ext4):** Penggunaan sistem berkas di komputer Anda (seperti **BTRFS** atau **ext4**) **tidak berpengaruh sama sekali** terhadap cara kerja tool ini. Hal ini dikarenakan `odoo-cli` tidak membaca/menulis file database Odoo secara langsung pada level disk, melainkan murni melalui network requests HTTP/HTTPS API.

---

---

## Design Decisions (Keputusan Arsitektur)

Keputusan desain penting dicatat sebagai **ADR (Architecture Decision Records)** di `docs/adr/`. Berikut ringkasan topik yang telah disepakati:

| # | Topik | Status | File |
|---|---|---|---|
| **ADR-0001** | Python over Go | ✅ Disetujui | `docs/adr/0001-use-python-over-go.md` |
| **ADR-0002** | XML-RPC over REST | ✅ Disetujui | `docs/adr/0002-xmlrpc-over-rest.md` |
| **ADR-0003** | Rich + LazyUI over Textual | ✅ Disetujui | `docs/adr/0003-rich-lazyui-over-textual.md` |
| **ADR-0004** | Three-mode interface (CLI/TUI/MCP) | ✅ Disetujui | `docs/adr/0004-three-mode-interface.md` |
| **ADR-0005** | Introspection Caching Strategy | ✅ Disetujui | `docs/adr/0005-introspection-caching.md` |

### Topik Desain Mendatang (Menunggu Diskusi)

Topik-topik berikut masih perlu dibahas dan disepakati sebelum implementasi:

| # | Topik | Deskripsi Singkat |
|---|---|---|
| **Topic 2** | Variabel Scope & Ekspresi Workflow | Aturan resolusi `{{params.*}}` dan `{{steps.*}}` serta dukungan kondisional |
| **Topic 3** | Standarisasi & Pemetaan Error | `error_mapper.py` — terjemahan error Odoo ke format JSON ramah AI |
| **Topic 4** | Diagram Alur Navigasi TUI | State diagram perpindahan layar TUI |
| **Topic 5** | Strategi Pengujian | Unit test (mock) + integration test (Docker) |

---

## Catatan Penting

- Module Odoo komunitas/resmi mana pun bisa langsung dipakai tanpa perubahan kode.
- Cukup install di Odoo, `schema` detect otomatis, `execute` bisa panggil method-nya.
- Tool ini **tidak memodifikasi Odoo server** — hanya membaca dan menulis via API resmi.
- Sangat aman digunakan pada database production karena mengikuti hak akses user Odoo yang terautentikasi.

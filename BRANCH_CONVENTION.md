# Branching & Git Commit Convention

Dokumen ini menjelaskan standard penamaan branch dan commit pada proyek `odoo-cli`.

---

## 1. Aturan Penamaan Branch

Semua pengerjaan wajib menggunakan branch yang dibuat dari `dev` dan dimerge kembali ke `dev` melalui Pull Request (PR).

| Tipe Branch | Format Nama | Contoh |
| :--- | :--- | :--- |
| **Fitur Baru** | `feat/<nama-fitur>` | `feat/mcp-server` |
| **Perbaikan Bug** | `fix/<nama-bug>` | `fix/connection-timeout` |
| **Alur Workflow** | `workflow/<nama-alur>` | `workflow/sales-invoice` |
| **Dokumentasi** | `docs/<topik>` | `docs/api-contract` |

---

## 2. Format Commit Message (Standard Conventional Commits)

Format commit: `<type>(<scope>): <subject>`

### Tipe Commit yang Diizinkan:
*   `feat`: Penambahan fitur baru (misal: `feat(mcp): tambah tool introspeksi ERD`)
*   `fix`: Perbaikan bug (misal: `fix(connector): tangani timeout XML-RPC`)
*   `docs`: Perubahan dokumentasi saja (misal: `docs(adr): update ADR-0003`)
*   `style`: Perapian kode (formatting, missing semi-colons, ruff fix)
*   `refactor`: Perubahan struktur kode tanpa mengubah fungsi luar
*   `test`: Penambahan atau perbaikan unit test
*   `chore`: Pemeliharaan build tool, versi dependency, dll.

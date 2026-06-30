---
name: "⚙️ Pengujian Kompatibilitas Odoo (Odoo Version Compatibility)"
about: Laporkan kendala atau hasil pengujian kompabilitas odoo-cli pada versi Odoo tertentu (misal: Odoo 18)
title: "[COMPATIBILITY] "
labels: compatibility
assignees: ""
---

## Versi Odoo yang Diuji
Sebutkan versi Odoo yang digunakan saat terjadi masalah kompatibilitas (misal: Odoo 18.0 Enterprise).

## Gejala Masalah Kompatibilitas
Jelaskan perbedaan respons, perubahan skema ORM Odoo, atau hilangnya field bawaan Odoo pada versi tersebut yang memicu kegagalan sistem.

## Modul/Aksi yang Terdampak
Sebutkan aksi CLI (`search`, `execute`, `schema`, dsb.) yang mengalami kegagalan.

## Hasil Introspeksi (`fields_get` log)
Tempelkan data respons skema field dari Odoo jika ada perbedaan struktur:
```json
{
  "field_name": "..."
}
```

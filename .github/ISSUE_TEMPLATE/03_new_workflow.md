---
name: "🔄 Usulan Workflow Baru (New Business Workflow)"
about: Ajukan rantai transaksi bisnis baru untuk dibuat berkas JSON-nya
title: "[WORKFLOW] "
labels: workflow
assignees: ""
---

## Deskripsi Alur Bisnis
Jelaskan alur dokumen Odoo apa saja yang ingin digabungkan ke dalam satu file workflow sekuensial (misal: Procurement Flow).

## Rincian Langkah Sekuensial (Steps Breakdown)
Sebutkan model Odoo dan metode yang dipanggil pada setiap langkah:
1.  **Langkah 1:** Buat Purchase Order (`purchase.order` ➡️ `create`)
2.  **Langkah 2:** Konfirmasi Purchase Order (`purchase.order` ➡️ `button_confirm`)
3.  **Langkah 3:** ...

## Variabel Masukan (Params)
Sebutkan parameter apa saja yang harus diisi oleh pengguna (misal: `supplier_id`, `product_id`, `qty`).

## Rencana Penanganan Error (Rollback)
Jelaskan tindakan kompensasi apa yang harus dilakukan jika langkah di tengah-tengah alur gagal (misal: jika penerimaan barang gagal, hapus purchase order draft).

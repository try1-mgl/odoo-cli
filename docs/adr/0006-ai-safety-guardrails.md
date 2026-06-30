# ADR-0006: Fitur Keamanan AI & Log Pemulihan (Undo)

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Asisten koding AI (seperti Claude/Gemini via MCP) bekerja berdasarkan probabilitas dan dapat melakukan kesalahan ketik, halusinasi parameter, atau modifikasi data massal yang tidak diinginkan pada database Odoo. Ketika dihubungkan ke database operasional produksi (Production), kesalahan ini dapat berakibat fatal. Kami memerlukan sistem pengaman agar data tidak rusak dan dapat dipulihkan dengan cepat.

## Keputusan (Decision)

Kami memutuskan untuk membangun fitur **AI Safety Guardrails** berlapis yang mencakup:
1. **Undo Log (History):** Menyimpan kondisi data sebelum dimodifikasi ke file JSON lokal agar bisa dikembalikan via perintah `--undo`.
2. **Human-in-the-Loop (HITL):** Menahan aksi sensitif (`write`, `delete`, `execute`) di server produksi hingga mendapat konfirmasi ketik `y` dari pengguna manusia.
3. **Database Branching:** Menyediakan perintah kloning database cepat pada Odoo Docker lokal untuk ruang uji coba aman bagi AI.

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **Keamanan Maksimal:** Mengurangi risiko kerusakan database produksi akibat kesalahan eksekusi perintah AI.
* **Audit Trail:** Berkas history transaksi mencatat dengan jelas apa saja perubahan data yang telah dilakukan oleh AI.
* **Kemudahan Uji Coba:** Database branching mempermudah AI melakukan eksperimen data tanpa merusak data asli.

### Kekurangan (Negatif):
* Membutuhkan ruang penyimpanan tambahan untuk menyimpan berkas log transaksi lokal di direktori `~/.cache/odoo_cli/history/`. Log yang sudah tua perlu dibersihkan secara berkala.

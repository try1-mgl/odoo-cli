# ADR-0002: Penggunaan XML-RPC ketimbang REST API

* **Status:** Disetujui (Approved)
* **Tanggal:** 2026-06-30

## Konteks (Context)

Untuk menghubungkan `odoo-cli` dengan Odoo server (baik Odoo Docker, Native, maupun Remote), kami memerlukan protokol komunikasi API. Ada dua opsi utama:
1. **REST API (JSON-RPC / HTTP):** Lebih populer untuk web modern, tetapi Odoo tidak menyediakan REST API bawaan secara seragam pada Odoo Community Edition tanpa menginstal modul kustom pihak ketiga (seperti `controllers` kustom).
2. **XML-RPC:** Protokol API bawaan resmi Odoo yang tersedia secara *default* di semua versi Odoo dan semua edisi (Community & Enterprise) tanpa perlu konfigurasi tambahan.

## Keputusan (Decision)

Kami memutuskan menggunakan protokol **XML-RPC** (`xmlrpc.client` via Python) sebagai saluran komunikasi utama ke Odoo.

## Konsekuensi (Consequences)

### Kelebihan (Positif):
* **Zero Odoo Configuration:** Pengguna tidak perlu menginstal modul kustom apa pun di sisi Odoo Server. Selama port Odoo terbuka, `odoo-cli` langsung bisa terhubung.
* **Kompatibilitas Penuh:** Didukung penuh dari Odoo 17 hingga versi terbaru di semua jenis instalasi (Docker/Native).
* **Keamanan Bawaan:** Menggunakan mekanisme otentikasi standar Odoo (Database, User Login, Password/API Key) dan mematuhi aturan Access Rights (ACL) user tersebut.

### Kekurangan (Negatif):
* **Kecepatan & Overhead:** XML-RPC menggunakan format XML yang lebih berat dibanding JSON. Skenario ini kami mitigasi dengan membatasi jumlah data per request menggunakan parameter `limit` dan `offset` (paginasi) secara ketat pada setiap aksi query.

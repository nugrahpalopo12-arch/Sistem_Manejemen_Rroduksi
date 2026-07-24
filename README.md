# 🏭 SIMPRO - Sistem Informasi Produksi

Aplikasi desktop untuk mengelola data produksi harian pabrik, dibangun menggunakan **Python (Tkinter + ttkbootstrap)** dengan visualisasi data memakai **Matplotlib** dan penyimpanan data di **MySQL**.

## ✨ Fitur

- **Dashboard** — ringkasan total produksi, jumlah jenis produk, total barang cacat, dan produksi hari ini, lengkap dengan grafik tren 7 hari terakhir dan distribusi produk.
- **Data Produksi** — tabel data produksi harian dengan aksi Tambah, Edit, dan Hapus.
- **Tambah Data Produksi** — form input data produksi baru (jendela terpisah).
- **Edit Data Produksi** — form ubah data produksi yang sudah ada (jendela terpisah).
- **Statistik** — analisis produksi per produk dan persentase kualitas (barang bagus vs cacat).
- **Laporan, Pengaturan, Tentang** — halaman placeholder untuk pengembangan lebih lanjut.

---

## 🗂️ Struktur Proyek

```
SIMPRO/
├── main.py                # (opsional) entry point aplikasi, memanggil Dashboard
├── dashboard.py           # Halaman utama & sidebar navigasi
├── produksi.py            # Halaman tabel Data Produksi (CRUD)
├── tambah_produksi.py     # Jendela form Tambah Data Produksi
├── edit_produksi.py       # Jendela form Edit Data Produksi
├── statistik.py           # Halaman Statistik & analisis
├── koneksi.py             # Konfigurasi koneksi ke database MySQL
└── README.md
```

> **Catatan:** `koneksi.py` belum termasuk dalam file yang direview. Pastikan file ini ada di folder yang sama dan berisi fungsi `koneksi_db()` yang mengembalikan objek koneksi MySQL (atau `None` jika gagal).

---

## ⚙️ Kebutuhan Sistem

- Python 3.9 atau lebih baru
- MySQL Server (lokal atau remote)
- Sistem operasi: Windows (direkomendasikan, karena `dashboard.py` menggunakan `state('zoomed')` yang khusus Windows — sudah ada fallback untuk Linux/Mac)

### Dependensi Python

```bash
pip install ttkbootstrap matplotlib mysql-connector-python
```

| Library | Kegunaan |
|---|---|
| `tkinter` | GUI dasar (built-in Python) |
| `ttkbootstrap` | Tema modern untuk Tkinter (dipakai di form & tabel) |
| `matplotlib` | Grafik garis, donut, bar chart, dan pie chart |
| `mysql-connector-python` | Koneksi ke database MySQL |

---

## 🗄️ Struktur Database

Buat database dan tabel berikut sebelum menjalankan aplikasi:

```sql
CREATE DATABASE simpro;

USE simpro;

CREATE TABLE produksi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk VARCHAR(100) NOT NULL,
    jumlah_produksi INT NOT NULL,
    tanggal_produksi DATE NOT NULL,
    shift_kerja ENUM('Pagi', 'Siang', 'Malam') NOT NULL,
    jumlah_cacat INT NOT NULL DEFAULT 0
);
```

### Contoh `koneksi.py`

```python
import mysql.connector

def koneksi_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="simpro"
        )
    except mysql.connector.Error as e:
        print(f"[Koneksi] Gagal terhubung ke database: {e}")
        return None
```

---

## 🚀 Cara Menjalankan

1. Clone / salin seluruh file proyek ke satu folder.
2. Buat database dan tabel `produksi` seperti pada bagian [Struktur Database](#-struktur-database).
3. Sesuaikan kredensial database di `koneksi.py`.
4. Install dependensi:
   ```bash
   pip install ttkbootstrap matplotlib mysql-connector-python
   ```
5. Jalankan aplikasi dari `dashboard.py`:
   ```bash
   python dashboard.py
   ```

---

## 📝 Catatan Pengembangan

- Form **Tambah** dan **Edit Data Produksi** dijalankan sebagai proses Python terpisah (`subprocess`) dari halaman Data Produksi, sehingga tampil sebagai jendela pop-up mandiri.
- Format tanggal yang diterima aplikasi adalah **`YYYY-MM-DD`** (contoh: `2026-07-13`).
- Halaman **Laporan** dan **Pengaturan** saat ini masih berupa placeholder dan belum memiliki fungsi CRUD.
- Halaman **Statistik** saat ini menampilkan analisis "per Produk" dan "Kualitas Kinerja" — jika desain akhir mengikuti mockup referensi (bar per hari + distribusi produk + filter periode), bagian ini masih perlu disesuaikan lebih lanjut.

---

## 📌 Status

| Modul | Status |
|---|---|
| Dashboard | ✅ Selesai & diperbaiki |
| Data Produksi (CRUD) | ✅ Selesai & diperbaiki |
| Tambah Data Produksi | ✅ Selesai & diperbaiki |
| Edit Data Produksi | ✅ Selesai & diperbaiki |
| Statistik | ✅ Bug fix selesai — desain grafik masih bisa disesuaikan lagi |
| Laporan / Pengaturan / Tentang | 🚧 Placeholder |

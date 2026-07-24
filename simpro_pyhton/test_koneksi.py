from koneksi import koneksi_db

conn = koneksi_db()

if conn:

    print("=================================")
    print("BERHASIL TERHUBUNG KE DATABASE")
    print("=================================")

    conn.close()

else:

    print("Koneksi gagal")
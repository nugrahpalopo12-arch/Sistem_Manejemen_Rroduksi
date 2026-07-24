import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from koneksi import koneksi_db

class TambahProduksi:
    def __init__(self):
        # Tinggi window ditambah sedikit menjadi 650 agar lebih lega
        self.window = tb.Window(title="SIMPRO - Tambah Data Produksi", themename="flatly", size=(750, 650))
        self.window.place_window_center()
        self.window.resizable(True, True)
        
        self.buat_form()
        self.window.mainloop()

    def buat_form(self):
        # ==========================
        # 1. HEADER (Di-pack paling atas)
        # ==========================
        header_frame = tb.Frame(self.window, padding=20)
        header_frame.pack(side=TOP, fill=X)
        
        tb.Label(header_frame, text="Tambah Data Produksi", font=("Segoe UI", 18, "bold")).pack(anchor=W)
        tb.Label(header_frame, text="Isi form berikut untuk menambahkan data produksi baru", bootstyle="secondary").pack(anchor=W)

        # ==========================
        # 2. FOOTER (Di-pack lebih dulu dan dikunci di BOTTOM agar tidak tertendang)
        # ==========================
        footer_frame = tb.Frame(self.window, padding=(20, 10, 20, 20))
        footer_frame.pack(side=BOTTOM, fill=X)
        
        tb.Button(footer_frame, text="✖ Batal", bootstyle="secondary", command=self.window.destroy, width=15).pack(side=RIGHT, padx=(10, 0))
        tb.Button(footer_frame, text="💾 Simpan", bootstyle="primary", command=self.simpan_data, width=15).pack(side=RIGHT)

        # ==========================
        # 3. BODY (Di-pack terakhir di tengah untuk mengisi sisa ruang)
        # ==========================
        body_frame = tb.Frame(self.window, padding=(20, 0))
        body_frame.pack(side=TOP, fill=BOTH, expand=YES)
        body_frame.columnconfigure(0, weight=6)
        body_frame.columnconfigure(1, weight=4)

        # --- KOLOM KIRI: FORM ---
        form_frame = tb.Frame(body_frame)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        tb.Label(form_frame, text="Nama Produk", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
        self.ent_produk = tb.Entry(form_frame)
        self.ent_produk.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Jumlah Produksi", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
        self.ent_jumlah = tb.Entry(form_frame)
        self.ent_jumlah.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Tanggal Produksi (YYYY-MM-DD)", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
        self.ent_tanggal = tb.Entry(form_frame)
        self.ent_tanggal.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Shift Kerja", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
        self.cmb_shift = tb.Combobox(form_frame, values=["Pagi", "Siang", "Malam"], state="readonly")
        self.cmb_shift.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Jumlah Cacat", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
        self.ent_cacat = tb.Entry(form_frame)
        self.ent_cacat.pack(fill=X, pady=(0, 10))

        # --- KOLOM KANAN: KOTAK INFORMASI BIRU ---
        info_frame = tb.Frame(body_frame, bootstyle="info", padding=15)
        info_frame.grid(row=0, column=1, sticky="n")
        
        tb.Label(info_frame, text="ℹ️ Informasi", font=("Segoe UI", 12, "bold"), bootstyle="inverse-info").pack(anchor=W, pady=(0,10))
        tb.Label(info_frame, text="Pastikan data yang diinput\nsudah sesuai sebelum\ndisimpan.", bootstyle="inverse-info", justify=LEFT).pack(anchor=W)

    def simpan_data(self):
        produk = self.ent_produk.get()
        jumlah = self.ent_jumlah.get()
        tanggal = self.ent_tanggal.get()
        shift = self.cmb_shift.get()
        cacat = self.ent_cacat.get()

        if not produk or not jumlah or not tanggal or not shift or not cacat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        if not jumlah.isdigit() or not cacat.isdigit():
            messagebox.showerror("Error", "Jumlah Produksi dan Barang Cacat harus berupa angka!")
            return

        try:
            conn = koneksi_db()
            if conn:
                cursor = conn.cursor()
                sql = "INSERT INTO produksi (nama_produk, jumlah_produksi, tanggal_produksi, shift_kerja, jumlah_cacat) VALUES (%s, %s, %s, %s, %s)"
                val = (produk, jumlah, tanggal, shift, cacat)
                cursor.execute(sql, val)
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Sukses", "Data produksi berhasil ditambahkan!")
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

if __name__ == "__main__":
    TambahProduksi()
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime
import sys
from koneksi import koneksi_db

class EditProduksi:
    def __init__(self, id_produksi):
        self.id_produksi = id_produksi
        self.window = tb.Window(title="SIMPRO - Edit Data Produksi", themename="flatly", size=(750, 580))
        self.window.place_window_center()
        self.window.resizable(True, True)
        
        self.buat_form()
        self.muat_data_lama()
        self.window.mainloop()

    def buat_form(self):
        # ==========================
        # HEADER
        # ==========================
        header_frame = tb.Frame(self.window, padding=20)
        header_frame.pack(side=TOP, fill=X)
        
        tb.Label(header_frame, text="Edit Data Produksi", font=("Helvetica", 18, "bold")).pack(anchor=W)
        tb.Label(header_frame, text="Ubah data produksi yang dipilih", bootstyle="secondary").pack(anchor=W)

        # ==========================
        # FOOTER (Dikunci di Bawah)
        # ==========================
        footer_frame = tb.Frame(self.window, padding=(20, 10, 20, 20))
        footer_frame.pack(side=BOTTOM, fill=X)
        
        tb.Button(footer_frame, text="✖ Batal", bootstyle="secondary", command=self.window.destroy, width=15).pack(side=RIGHT, padx=(10, 0))
        tb.Button(footer_frame, text="💾 Simpan Perubahan", bootstyle="warning", command=self.update_data, width=20).pack(side=RIGHT)

        # ==========================
        # BODY (Form di Tengah)
        # ==========================
        body_frame = tb.Frame(self.window, padding=(20, 0))
        body_frame.pack(side=TOP, fill=BOTH, expand=YES)
        body_frame.columnconfigure(0, weight=6)
        body_frame.columnconfigure(1, weight=4)

        form_frame = tb.Frame(body_frame)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        tb.Label(form_frame, text="ID", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_id = tb.Entry(form_frame, state="readonly")
        self.ent_id.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Nama Produk", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_produk = tb.Entry(form_frame)
        self.ent_produk.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Jumlah Produksi", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_jumlah = tb.Entry(form_frame)
        self.ent_jumlah.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Tanggal Produksi", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_tanggal = tb.Entry(form_frame)
        self.ent_tanggal.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Shift Kerja", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.cmb_shift = tb.Combobox(form_frame, values=["Pagi", "Siang", "Malam"], state="readonly")
        self.cmb_shift.pack(fill=X, pady=(0, 10))

        tb.Label(form_frame, text="Jumlah Cacat", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(0, 2))
        self.ent_cacat = tb.Entry(form_frame)
        self.ent_cacat.pack(fill=X, pady=(0, 10))

        # Kotak Peringatan
        info_frame = tb.Frame(body_frame, bootstyle="warning", padding=15)
        info_frame.grid(row=0, column=1, sticky="n")
        
        tb.Label(info_frame, text="⚠️ Perhatian", font=("Helvetica", 12, "bold"), bootstyle="inverse-warning").pack(anchor=W, pady=(0,10))
        tb.Label(info_frame, text="Perubahan data akan\ntersimpan setelah klik\ntombol Simpan.", bootstyle="inverse-warning", justify=LEFT).pack(anchor=W)

    def muat_data_lama(self):
        self.ent_id.configure(state="normal")
        self.ent_id.insert(0, str(self.id_produksi))
        self.ent_id.configure(state="readonly")
        
        conn = None
        cursor = None
        try:
            conn = koneksi_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nama_produk, jumlah_produksi, tanggal_produksi, shift_kerja, jumlah_cacat FROM produksi WHERE id = %s", (self.id_produksi,))
                data = cursor.fetchone()

                if data:
                    # str() eksplisit: tanggal_produksi biasanya berupa objek
                    # datetime.date dari database, bukan string. Memasukkannya
                    # langsung ke Entry.insert() tanpa cast bisa memicu error.
                    self.ent_produk.insert(0, str(data[0]))
                    self.ent_jumlah.insert(0, str(data[1]))
                    self.ent_tanggal.insert(0, str(data[2]))
                    self.cmb_shift.set(str(data[3]))
                    self.ent_cacat.insert(0, str(data[4]))
                else:
                    messagebox.showerror("Error", "Data produksi dengan ID tersebut tidak ditemukan.")
            else:
                messagebox.showerror("Error", "Tidak dapat terhubung ke database.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_data(self):
        produk = self.ent_produk.get()
        jumlah = self.ent_jumlah.get()
        tanggal = self.ent_tanggal.get()
        shift = self.cmb_shift.get()
        cacat = self.ent_cacat.get()

        if not produk or not jumlah or not tanggal or not shift or not cacat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        if not jumlah.isdigit() or not cacat.isdigit():
            messagebox.showerror("Error", "Jumlah Produksi dan Cacat harus berupa angka!")
            return

        # Validasi format tanggal sebelum dikirim ke database.
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Format Tanggal Produksi harus YYYY-MM-DD, contoh: 2026-07-13")
            return

        conn = None
        cursor = None
        try:
            conn = koneksi_db()
            if conn:
                cursor = conn.cursor()
                sql = "UPDATE produksi SET nama_produk=%s, jumlah_produksi=%s, tanggal_produksi=%s, shift_kerja=%s, jumlah_cacat=%s WHERE id=%s"
                val = (produk, jumlah, tanggal, shift, cacat, self.id_produksi)
                cursor.execute(sql, val)
                conn.commit()

                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Tidak dapat terhubung ke database.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        EditProduksi(sys.argv[1])
    else:
        print("Error: edit_produksi.py membutuhkan argumen ID produksi.")
        sys.exit(1)
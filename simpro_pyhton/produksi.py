import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk
import subprocess
import sys
import os
from koneksi import koneksi_db

class Produksi:
    def __init__(self, parent):
        self.parent = parent
        
        # 1. Kustomisasi Gaya Tabel Modern
        gaya = tb.Style()
        gaya.configure("Treeview", 
                       rowheight=40, # Baris lebih renggang dan lega
                       font=("Segoe UI", 10), 
                       borderwidth=0)
        gaya.configure("Treeview.Heading", 
                       font=("Segoe UI", 11, "bold"), 
                       padding=10)
                       
        # Warna saat baris tabel dipilih/diklik (Biru sangat muda)
        gaya.map("Treeview", 
                 background=[('selected', '#eff6ff')], 
                 foreground=[('selected', '#0f172a')])
        
        self.buat_halaman()

    def buat_halaman(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Container Utama dengan Padding agar tidak mepet layar
        main_frame = tk.Frame(self.parent, bg="#f8fafc", padx=30, pady=30)
        main_frame.pack(fill=BOTH, expand=YES)

        # ==========================
        # 1. HEADER HALAMAN
        # ==========================
        header_frame = tk.Frame(main_frame, bg="#f8fafc")
        header_frame.pack(fill=X, pady=(0, 20))
        
        tk.Label(header_frame, text="Data Produksi", font=("Segoe UI", 24, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor=W)
        tk.Label(header_frame, text="Kelola data produksi harian pabrik", font=("Segoe UI", 11), bg="#f8fafc", fg="#64748b").pack(anchor=W)

        # ==========================
        # 2. BARIS TOMBOL AKSI
        # ==========================
        action_frame = tk.Frame(main_frame, bg="#f8fafc")
        action_frame.pack(fill=X, pady=(0, 15))

        tb.Button(action_frame, text="➕ Tambah", bootstyle="success", command=self.buka_tambah).pack(side=LEFT, padx=(0, 10))
        tb.Button(action_frame, text="✏️ Edit", bootstyle="warning", command=self.buka_edit).pack(side=LEFT, padx=(0, 10))
        tb.Button(action_frame, text="🗑️ Hapus", bootstyle="danger", command=self.hapus_data).pack(side=LEFT, padx=(0, 10))
        
        tb.Button(action_frame, text="🔄 Refresh", bootstyle="primary", command=self.tampilkan_data).pack(side=RIGHT)

        # ==========================
        # 3. BINGKAI TABEL (Card Web Style)
        # ==========================
        # Bingkai luar (Garis tepi abu-abu tipis)
        border_frame = tk.Frame(main_frame, bg="#e2e8f0", bd=1)
        border_frame.pack(fill=BOTH, expand=YES)

        # Bingkai dalam (Warna putih murni)
        inner_frame = tk.Frame(border_frame, bg="white")
        inner_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)

        kolom = ("ID", "Nama Produk", "Jumlah Produksi", "Tanggal Produksi", "Shift Kerja", "Jumlah Cacat")
        
        self.tabel = tb.Treeview(inner_frame, columns=kolom, show="headings", bootstyle="primary")
        self.tabel.pack(side=LEFT, fill=BOTH, expand=YES)

        # Tag untuk pewarnaan baris belang-belang (Zebra Striping)
        self.tabel.tag_configure("ganjil", background="#ffffff")
        self.tabel.tag_configure("genap", background="#f8fafc")

        # Scrollbar Modern
        scrollbar = tb.Scrollbar(inner_frame, orient=VERTICAL, command=self.tabel.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tabel.configure(yscrollcommand=scrollbar.set)

        # Format Kolom
        for col in kolom:
            self.tabel.heading(col, text=col)

        self.tabel.column("ID", width=60, anchor=CENTER)
        self.tabel.column("Nama Produk", width=250, anchor=W)
        self.tabel.column("Jumlah Produksi", width=120, anchor=CENTER)
        self.tabel.column("Tanggal Produksi", width=130, anchor=CENTER)
        self.tabel.column("Shift Kerja", width=100, anchor=CENTER)
        self.tabel.column("Jumlah Cacat", width=100, anchor=CENTER)

        # ==========================
        # 4. FOOTER (Total Data)
        # ==========================
        self.lbl_total = tk.Label(main_frame, text="Total Data: 0", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg="#64748b")
        self.lbl_total.pack(anchor=W, pady=(15, 0))

        self.tampilkan_data()

    # ==========================
    # LOGIKA DATABASE & DATA
    # ==========================
    def tampilkan_data(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        total_baris = 0
        try:
            conn = koneksi_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM produksi ORDER BY id DESC")
                rows = cursor.fetchall()
                
                # Memasukkan data dengan logika baris ganjil/genap
                for index, row in enumerate(rows):
                    tag_baris = "genap" if index % 2 == 0 else "ganjil"
                    self.tabel.insert("", "end", values=row, tags=(tag_baris,))
                    total_baris += 1
                    
                cursor.close()
                conn.close()
            else:
                messagebox.showerror("Error", "Tidak dapat terhubung ke database.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data produksi: {e}")
        
        self.lbl_total.configure(text=f"Total Data: {total_baris}")

    def hapus_data(self):
        item_terpilih = self.tabel.focus()
        if not item_terpilih:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus terlebih dahulu!")
            return

        data = self.tabel.item(item_terpilih, "values")
        id_produksi = data[0]

        konfirmasi = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus data {data[1]}?")
        if konfirmasi:
            conn = None
            cursor = None
            try:
                conn = koneksi_db()
                if not conn:
                    messagebox.showerror("Error", "Tidak dapat terhubung ke database.")
                    return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produksi WHERE id = %s", (id_produksi,))
                conn.commit()

                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.tampilkan_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    # ==========================
    # PEMANGGIL POP-UP FORM
    # ==========================
    def buka_tambah(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            path_script = os.path.join(script_dir, "tambah_produksi.py")
            subprocess.run([sys.executable, path_script])
            self.tampilkan_data() 
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka form: {e}")

    def buka_edit(self):
        item_terpilih = self.tabel.focus()
        if not item_terpilih:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin diedit terlebih dahulu!")
            return
            
        data = self.tabel.item(item_terpilih, "values")
        id_produksi = data[0]

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            path_script = os.path.join(script_dir, "edit_produksi.py")
            subprocess.run([sys.executable, path_script, str(id_produksi)])
            self.tampilkan_data() 
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka form: {e}")
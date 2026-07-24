import tkinter as tk
from tkinter import messagebox
from koneksi import koneksi_db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Statistik:
    def __init__(self, parent):
        self.parent = parent
        self.buat_halaman()

    def buat_halaman(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Container Utama
        main_frame = tk.Frame(self.parent, bg="#f8fafc", padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)

        # 1. HEADER (Atas)
        header_frame = tk.Frame(main_frame, bg="#f8fafc")
        header_frame.pack(side="top", fill="x", pady=(0, 10))
        tk.Label(header_frame, text="Statistik Produksi", font=("Segoe UI", 24, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w")
        # Ditambahkan warna biru cerah pada deskripsi sub-header
        tk.Label(header_frame, text="Lihat analisa dan ringkasan keseluruhan operasional pabrik", font=("Segoe UI", 11, "italic"), bg="#f8fafc", fg="#2563eb").pack(anchor="w")

        # 2. RINGKASAN DATA (Di bagian bawah dengan warna solid tebal)
        bottom_container = tk.Frame(main_frame, bg="#f8fafc")
        bottom_container.pack(side="bottom", fill="x", pady=(15, 0))
        
        tk.Label(bottom_container, text="Ringkasan Kinerja", font=("Segoe UI", 14, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w", pady=(0, 10))
        self.ringkasan_frame = tk.Frame(bottom_container, bg="#f8fafc")
        self.ringkasan_frame.pack(fill="x")
        self.ringkasan_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # 3. AREA GRAFIK (Tengah)
        grafik_frame = tk.Frame(main_frame, bg="#f8fafc")
        grafik_frame.pack(side="top", fill="both", expand=True)
        grafik_frame.columnconfigure((0, 1), weight=1)

        self.frame_kiri = tk.Frame(grafik_frame, bg="white", bd=1, relief="solid", highlightbackground="#e2e8f0", highlightthickness=1)
        self.frame_kiri.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.frame_kanan = tk.Frame(grafik_frame, bg="white", bd=1, relief="solid", highlightbackground="#e2e8f0", highlightthickness=1)
        self.frame_kanan.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.tampilkan_data()

    def tampilkan_data(self):
        try:
            conn = koneksi_db()
            if not conn: return
            cursor = conn.cursor()
            cursor.execute("SELECT nama_produk, SUM(jumlah_produksi) FROM produksi GROUP BY nama_produk")
            data_bar = cursor.fetchall()
            cursor.execute("SELECT SUM(jumlah_produksi), SUM(jumlah_cacat), COUNT(DISTINCT tanggal_produksi) FROM produksi")
            data_pie = cursor.fetchone()
            cursor.close()
            conn.close()

            # RENDER BAR CHART
            fig_bar, ax_bar = plt.subplots(figsize=(5, 3.5), dpi=95)
            fig_bar.patch.set_facecolor('#ffffff')
            ax_bar.set_facecolor('#ffffff')

            if data_bar:
                produk = [str(row[0]) for row in data_bar]
                jumlah = [int(row[1]) for row in data_bar]
                warna = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#0ea5e9']
                
                ax_bar.bar(produk, jumlah, color=[warna[i % len(warna)] for i in range(len(produk))])
                ax_bar.set_title('Total Produksi per Produk', fontsize=12, fontweight='bold', pad=15)
                
                plt.setp(ax_bar.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)
                ax_bar.spines['top'].set_visible(False)
                ax_bar.spines['right'].set_visible(False)
            
            fig_bar.tight_layout(pad=1.5) 
            canvas_bar = FigureCanvasTkAgg(fig_bar, master=self.frame_kiri)
            canvas_bar.draw()
            canvas_bar.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            # RENDER PIE CHART
            fig_pie, ax_pie = plt.subplots(figsize=(5, 3.5), dpi=95)
            fig_pie.patch.set_facecolor('#ffffff')

            total_prod = int(data_pie[0]) if data_pie and data_pie[0] else 0
            total_cacat = int(data_pie[1]) if data_pie and data_pie[1] else 0
            total_hari = int(data_pie[2]) if data_pie and data_pie[2] else 1
            bagus = total_prod - total_cacat

            if total_prod > 0:
                ax_pie.pie([bagus, total_cacat], labels=['Barang Bagus', 'Barang Cacat'], colors=['#10b981', '#ef4444'], autopct='%1.1f%%', startangle=140)
                ax_pie.set_title('Persentase Kualitas Kinerja', fontsize=12, fontweight='bold', pad=15)
            
            fig_pie.tight_layout()
            canvas_pie = FigureCanvasTkAgg(fig_pie, master=self.frame_kanan)
            canvas_pie.draw()
            canvas_pie.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            # 4 KOTAK RINGKASAN BAWAH (Menggunakan warna latar belakang solid yang tebal & teks putih murni)
            rata_rata = int(total_prod / total_hari) if total_hari > 0 else 0
            persen = (total_cacat / total_prod * 100) if total_prod > 0 else 0.0

            self.buat_card_ringkasan(0, "Total Produksi", f"{total_prod:,} Unit".replace(',', '.'), "#2563eb", "#bfdbfe") # Kotak Biru Tua
            self.buat_card_ringkasan(1, "Rata-rata Harian", f"{rata_rata:,} Unit".replace(',', '.'), "#10b981", "#a7f3d0") # Kotak Hijau
            self.buat_card_ringkasan(2, "Total Barang Cacat", f"{total_cacat:,} Unit".replace(',', '.'), "#ef4444", "#fecaca") # Kotak Merah
            self.buat_card_ringkasan(3, "Persentase Cacat", f"{persen:.2f} %", "#f59e0b", "#fde68a") # Kotak Jingga/Orange

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat statistik: {e}")

    def buat_card_ringkasan(self, col, judul, nilai, warna_bg, warna_teks_judul):
        # Mengubah bd=0 menjadi flat frame dengan warna latar belakang yang tebal
        card = tk.Frame(self.ringkasan_frame, bg=warna_bg, bd=0, relief="flat")
        card.grid(row=0, column=col, sticky="nsew", padx=8, ipady=12)
        
        # Teks judul menggunakan warna sekunder yang terang di atas latar belakang solid
        tk.Label(card, text=judul, font=("Segoe UI", 10, "bold"), bg=warna_bg, fg=warna_teks_judul).pack(anchor="w", padx=20, pady=(15, 2))
        # Angka nilai menggunakan warna putih murni agar kontras tingginya maksimal
        tk.Label(card, text=nilai, font=("Segoe UI", 24, "bold"), bg=warna_bg, fg="white").pack(anchor="w", padx=20, pady=(0, 15))
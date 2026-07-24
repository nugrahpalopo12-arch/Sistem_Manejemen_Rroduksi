import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sys
from koneksi import koneksi_db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("SIMPRO - Sistem Informasi Produksi")
        self.app.geometry("1200x750")
        self.app.configure(bg="#f8fafc") 
        try:
            self.app.state('zoomed')
        except tk.TclError:
            if sys.platform.startswith('linux'):
                try:
                    self.app.attributes('-zoomed', True)
                except tk.TclError:
                    pass

        self.buat_layout()
        self.tampilkan_dashboard()
        
        self.app.mainloop()

    def buat_layout(self):
        # ==========================
        # SIDEBAR KIRI
        # ==========================
        self.sidebar = tk.Frame(self.app, bg="#1e293b", width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        lbl_logo = tk.Label(self.sidebar, text="🏭 SIMPRO", font=("Segoe UI", 20, "bold"), bg="#1e293b", fg="white")
        lbl_logo.pack(pady=(35, 5), anchor="w", padx=20)
        tk.Label(self.sidebar, text="Sistem Informasi Produksi", font=("Segoe UI", 9), bg="#1e293b", fg="#94a3b8").pack(anchor="w", padx=20, pady=(0, 30))

        # 3 Menu Utama
        self.btn_dash = self.buat_tombol_menu("🏠  Dashboard", self.tampilkan_dashboard)
        self.btn_prod = self.buat_tombol_menu("📋  Data Produksi", self.buka_produksi)
        self.btn_stat = self.buat_tombol_menu("📊  Statistik", self.buka_statistik)

        # Profil Admin
        profil_frame = tk.Frame(self.sidebar, bg="#1e293b")
        profil_frame.pack(side="bottom", fill="x", pady=30, padx=20)
        
        tk.Label(profil_frame, text="👤", font=("Segoe UI", 24), bg="#1e293b", fg="white").pack(side="left", padx=(0, 10))
        teks_profil = tk.Frame(profil_frame, bg="#1e293b")
        teks_profil.pack(side="left")
        tk.Label(teks_profil, text="Admin", font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="white").pack(anchor="w")
        tk.Label(teks_profil, text="Administrator", font=("Segoe UI", 9), bg="#1e293b", fg="#94a3b8").pack(anchor="w")

        # ==========================
        # AREA KONTEN KANAN
        # ==========================
        self.main_content = tk.Frame(self.app, bg="#f8fafc")
        self.main_content.pack(side="left", fill="both", expand=True)

    def buat_tombol_menu(self, teks, command):
        btn = tk.Button(self.sidebar, text=teks, font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#cbd5e1", 
                        bd=0, anchor="w", padx=20, pady=12, cursor="hand2", command=command, 
                        activebackground="#2563eb", activeforeground="white")
        btn.pack(fill="x", pady=2, padx=10)
        return btn

    def reset_menu(self, btn_aktif):
        for btn in [self.btn_dash, self.btn_prod, self.btn_stat]:
            btn.configure(bg="#1e293b", fg="#cbd5e1")
        btn_aktif.configure(bg="#2563eb", fg="white")
        
        for widget in self.main_content.winfo_children():
            widget.destroy()

    # ==========================
    # HALAMAN: DASHBOARD
    # ==========================
    def tampilkan_dashboard(self):
        self.reset_menu(self.btn_dash)

        content_pad = tk.Frame(self.main_content, bg="#f8fafc", padx=35, pady=30)
        content_pad.pack(fill="both", expand=True)

        # 1. HEADER HALAMAN
        header_frame = tk.Frame(content_pad, bg="#f8fafc")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_frame = tk.Frame(header_frame, bg="#f8fafc")
        title_frame.pack(side="left")
        tk.Label(title_frame, text="Dashboard", font=("Segoe UI", 26, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w")
        tk.Label(title_frame, text="Selamat datang, Admin!", font=("Segoe UI", 12, "italic"), bg="#f8fafc", fg="#2563eb").pack(anchor="w")
        
        # Kotak Kalender Kanan Atas
        waktu_sekarang = datetime.now().strftime("%d %B %Y\n%H:%M:%S")
        cal_frame = tk.Frame(header_frame, bg="#ffffff", bd=1, relief="solid", highlightbackground="#cbd5e1", highlightthickness=1)
        cal_frame.pack(side="right", padx=5, pady=5, ipady=6, ipadx=15)
        tk.Label(cal_frame, text=f"📆 {waktu_sekarang}", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#334155", justify="right").pack()

        # AMBIL DATA DATABASE
        tot_prod = 0; tot_jenis = 0; tot_cacat = 0; prod_hari_ini = 0
        try:
            conn = koneksi_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(jumlah_produksi), COUNT(DISTINCT nama_produk), SUM(jumlah_cacat) FROM produksi")
                hasil = cursor.fetchone()
                if hasil:
                    tot_prod = int(hasil[0]) if hasil[0] else 0
                    tot_jenis = int(hasil[1]) if hasil[1] else 0
                    tot_cacat = int(hasil[2]) if hasil[2] else 0
                
                hari_ini = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("SELECT SUM(jumlah_produksi) FROM produksi WHERE tanggal_produksi = %s", (hari_ini,))
                hasil_hari_ini = cursor.fetchone()
                if hasil_hari_ini and hasil_hari_ini[0]:
                    prod_hari_ini = int(hasil_hari_ini[0])
                cursor.close()
                conn.close()
        except:
            pass

        # 2. KARTU DATA (Sekarang menggunakan warna solid yang kuat agar tidak terlihat putih)
        card_frame = tk.Frame(content_pad, bg="#f8fafc")
        card_frame.pack(fill="x", pady=5)
        card_frame.columnconfigure((0,1,2,3), weight=1)

        self.buat_card(card_frame, 0, "Total Produksi", f"{tot_prod:,}".replace(",", "."), "Unit", "#3b82f6", "#eff6ff", "#ffffff") # BIRU
        self.buat_card(card_frame, 1, "Total Produk", str(tot_jenis), "Jenis", "#10b981", "#ecfdf5", "#ffffff") # HIJAU
        self.buat_card(card_frame, 2, "Total Cacat", str(tot_cacat), "Unit", "#f59e0b", "#fffbeb", "#ffffff") # ORANGE/KUNING
        self.buat_card(card_frame, 3, "Produksi Hari Ini", f"{prod_hari_ini:,}".replace(",", "."), "Unit", "#8b5cf6", "#f5f3ff", "#ffffff") # UNGU

        # 3. AREA GRAFIK (Tanpa tabel log aktivitas di bawahnya, grafik menjadi lebih luas)
        grafik_frame = tk.Frame(content_pad, bg="#f8fafc")
        grafik_frame.pack(fill="both", expand=True, pady=(20, 0))
        grafik_frame.columnconfigure((0,1), weight=1)

        frame_kiri = tk.Frame(grafik_frame, bg="white", bd=1, relief="solid", highlightbackground="#cbd5e1", highlightthickness=1)
        frame_kiri.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(frame_kiri, text="Grafik Produksi 7 Hari Terakhir", font=("Segoe UI", 12, "bold"), bg="white", fg="#0f172a").pack(anchor="w", padx=20, pady=(15, 0))

        frame_kanan = tk.Frame(grafik_frame, bg="white", bd=1, relief="solid", highlightbackground="#cbd5e1", highlightthickness=1)
        frame_kanan.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        tk.Label(frame_kanan, text="Distribusi Produk", font=("Segoe UI", 12, "bold"), bg="white", fg="#0f172a").pack(anchor="w", padx=20, pady=(15, 0))

        self.render_grafik_dashboard(frame_kiri, frame_kanan)

    def buat_card(self, parent, col, judul, nilai, satuan, bg_color, title_color, val_color):
        # Frame kartu dibuat flat (tanpa outline) agar warna solidnya menonjol
        card = tk.Frame(parent, bg=bg_color, bd=0, relief="flat")
        card.grid(row=0, column=col, sticky="nsew", padx=10, ipady=15)
        
        tk.Label(card, text=judul, font=("Segoe UI", 11, "bold"), bg=bg_color, fg=title_color).pack(anchor="w", padx=20, pady=(15, 0))
        tk.Label(card, text=nilai, font=("Segoe UI", 32, "bold"), bg=bg_color, fg=val_color).pack(anchor="w", padx=20, pady=5)
        tk.Label(card, text=satuan, font=("Segoe UI", 10), bg=bg_color, fg=title_color).pack(anchor="w", padx=20, pady=(0, 15))

    def render_grafik_dashboard(self, frame_kiri, frame_kanan):
        conn = None
        try:
            conn = koneksi_db()
            if not conn: return
            cursor = conn.cursor()
            cursor.execute("SELECT tanggal_produksi, SUM(jumlah_produksi) FROM produksi GROUP BY tanggal_produksi ORDER BY tanggal_produksi DESC LIMIT 7")
            data_line = cursor.fetchall()

            cursor.execute("SELECT nama_produk, SUM(jumlah_produksi) AS total FROM produksi GROUP BY nama_produk ORDER BY total DESC LIMIT 5")
            data_pie = cursor.fetchall()
            cursor.close()

            # RENDER GRAFIK GARIS
            fig_line, ax_line = plt.subplots(figsize=(4, 2.5), dpi=90)
            fig_line.patch.set_facecolor('#ffffff')
            ax_line.set_facecolor('#ffffff')

            if data_line:
                data_line.reverse()
                tgl = [str(row[0])[-5:] for row in data_line]
                jml = [int(row[1]) for row in data_line]
                ax_line.plot(tgl, jml, marker='o', color='#2563eb', linestyle='-', linewidth=2.5, markersize=6)
                for x, y in zip(tgl, jml):
                    ax_line.annotate(f"{y:,}".replace(",", "."), (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='#334155', fontweight='bold')
                ax_line.spines['top'].set_visible(False)
                ax_line.spines['right'].set_visible(False)
                ax_line.spines['left'].set_color('#cbd5e1')
                ax_line.spines['bottom'].set_color('#cbd5e1')
                ax_line.tick_params(labelsize=9, colors='#475569')

            fig_line.tight_layout(pad=2.0)
            canvas_line = FigureCanvasTkAgg(fig_line, master=frame_kiri)
            canvas_line.draw()
            canvas_line.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
            plt.close(fig_line)  

            # RENDER GRAFIK DONUT
            fig_pie, ax_pie = plt.subplots(figsize=(4, 2.5), dpi=90)
            fig_pie.patch.set_facecolor('#ffffff')

            if data_pie:
                produk = [str(row[0]) for row in data_pie]
                jumlah = [int(row[1]) for row in data_pie]
                total = sum(jumlah) or 1
                warna = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444']

                wedges, _ = ax_pie.pie(jumlah, colors=warna[:len(jumlah)], startangle=90, wedgeprops={'width': 0.45, 'edgecolor': 'white', 'linewidth': 2})
                ax_pie.set_aspect('equal')

                legend_labels = [f"{nama} ({jml / total * 100:.0f}%)" for nama, jml in zip(produk, jumlah)]
                ax_pie.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.9, 0.5), fontsize=9, frameon=False)

            fig_pie.tight_layout(pad=2.0)
            canvas_pie = FigureCanvasTkAgg(fig_pie, master=frame_kanan)
            canvas_pie.draw()
            canvas_pie.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
            plt.close(fig_pie)  
        except Exception as e:
            print(f"[Dashboard] Gagal memuat grafik: {e}")
        finally:
            if conn: conn.close()

    def buka_produksi(self):
        self.reset_menu(self.btn_prod)
        try:
            from produksi import Produksi
            Produksi(self.main_content)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat halaman produksi: {e}")
            
    def buka_statistik(self):
        self.reset_menu(self.btn_stat)
        try:
            from statistik import Statistik
            Statistik(self.main_content)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat halaman statistik: {e}")

if __name__ == "__main__":
    Dashboard()
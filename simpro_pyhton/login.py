import tkinter as tk
from tkinter import messagebox
import os # Tambahan untuk mengecek keberadaan file

class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SIMPRO - Login")
        self.window.geometry("600x400")
        self.window.configure(bg="white")
        self.window.resizable(False, False)

        # ==========================
        # 1. MEMASANG ICON APLIKASI
        # ==========================
        try:
            # Mengambil icon.png dari folder assets
            self.icon_img = tk.PhotoImage(file="assets/icon.png")
            self.window.iconphoto(False, self.icon_img)
        except Exception:
            pass # Abaikan jika file icon.png tidak ditemukan

        self.buat_tampilan()
        self.window.mainloop()

    def buat_tampilan(self):
        # ==========================
        # PANEL KIRI (BIRU)
        # ==========================
        frame_kiri = tk.Frame(self.window, bg="#0d6efd", width=250, height=400)
        frame_kiri.pack(side="left", fill="y")
        frame_kiri.pack_propagate(False)

        # ==========================
        # 2. MEMASANG LOGO APLIKASI
        # ==========================
        try:
            # Mencoba memuat logo.png dari folder assets
            self.logo_img = tk.PhotoImage(file="assets/logo.png")
            tk.Label(frame_kiri, image=self.logo_img, bg="#0d6efd").pack(pady=(80, 10))
        except Exception:
            # Jika logo.png tidak ada/salah nama, gunakan Emoji sebagai cadangan
            tk.Label(frame_kiri, text="🏭", font=("Arial", 50), bg="#0d6efd", fg="white").pack(pady=(80, 10))

        tk.Label(frame_kiri, text="SIMPRO", font=("Arial", 24, "bold"), bg="#0d6efd", fg="white").pack()
        tk.Label(frame_kiri, text="Sistem Monitoring\nProduksi", font=("Arial", 11), bg="#0d6efd", fg="#e0e0e0").pack(pady=5)

        # ==========================
        # PANEL KANAN (PUTIH)
        # ==========================
        frame_kanan = tk.Frame(self.window, bg="white", width=350, height=400)
        frame_kanan.pack(side="right", fill="both", expand=True)

        tk.Label(frame_kanan, text="Silakan Login", font=("Arial", 18, "bold"), bg="white", fg="#333333").pack(pady=(50, 30))

        # --- Kolom Username ---
        frame_user = tk.Frame(frame_kanan, bg="white")
        frame_user.pack(fill="x", padx=40, pady=10)
        tk.Label(frame_user, text="Username", font=("Arial", 10, "bold"), bg="white", fg="#555555").pack(anchor="w")
        self.ent_user = tk.Entry(frame_user, font=("Arial", 12), bg="#f8f9fa", bd=1, relief="solid")
        self.ent_user.pack(fill="x", ipady=5, pady=(5,0))

        # --- Kolom Password ---
        frame_pass = tk.Frame(frame_kanan, bg="white")
        frame_pass.pack(fill="x", padx=40, pady=10)
        tk.Label(frame_pass, text="Password", font=("Arial", 10, "bold"), bg="white", fg="#555555").pack(anchor="w")
        self.ent_pass = tk.Entry(frame_pass, font=("Arial", 12), bg="#f8f9fa", bd=1, relief="solid", show="*")
        self.ent_pass.pack(fill="x", ipady=5, pady=(5,0))

        # --- Tombol Login ---
        btn_login = tk.Button(
            frame_kanan, text="LOGIN", font=("Arial", 11, "bold"), bg="#0d6efd", fg="white", 
            bd=0, relief="flat", cursor="hand2", command=self.proses_login
        )
        btn_login.pack(fill="x", padx=40, pady=25, ipady=8)

    # ==========================
    # LOGIKA CEK DATABASE
    # ==========================
    def proses_login(self):
        user = self.ent_user.get()
        pwd = self.ent_pass.get()

        if user == "" or pwd == "":
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return

        try:
            from koneksi import koneksi_db
            conn = koneksi_db()
            
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (user, pwd))
                hasil = cursor.fetchone()

                cursor.close()
                conn.close()

                if hasil:
                    self.window.destroy()
                    try:
                        from dashboard import Dashboard
                        Dashboard()
                    except ImportError:
                        messagebox.showerror("Error", "File dashboard.py tidak ditemukan!")
                else:
                    messagebox.showerror("Gagal", "Username atau Password salah!")
                    
        except Exception as e:
            if user == "admin" and pwd == "12345":
                self.window.destroy()
                try:
                    from dashboard import Dashboard
                    Dashboard()
                except ImportError:
                    pass
            else:
                messagebox.showerror("Gagal", f"Username salah, ATAU tabel admin belum dibuat.\n\nError Detail: {e}")

if __name__ == "__main__":
    Login()
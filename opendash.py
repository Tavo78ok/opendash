import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import psutil
import subprocess
import os
import shutil
import platform

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

class OpenDashApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- IDENTIDAD ---
        self.title("Opendash v1.0 | OpenArgOs Gold Edition")
        self.geometry("850x650")
        
        try:
            base_path = os.path.dirname(__file__)
            icon_path = os.path.join(base_path, "opendash.png")
            if not os.path.exists(icon_path):
                icon_path = "/usr/share/icons/hicolor/48x48/apps/opendash.png"
            if os.path.exists(icon_path):
                img = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, img)
        except:
            pass

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.sidebar, text="OpenArgOs", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.status_label = ctk.CTkLabel(self.sidebar, text="Sistema: Optimizado", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=10)

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Monitor")
        self.tabview.add("Limpiador")
        self.tabview.add("Gamer")
        self.tabview.add("Desinstalar")
        self.tabview.add("Red")

        self.setup_monitor()
        self.setup_limpiador()
        self.setup_gamer_tab()
        self.setup_desinstalar()
        self.setup_red_tab()

    # --- MONITOR ---
    def setup_monitor(self):
        tab = self.tabview.tab("Monitor")
        ctk.CTkLabel(tab, text="INFORMACIÓN DEL SISTEMA", font=("Arial", 16, "bold"), text_color="#3b8ed0").pack(pady=10)
        ctk.CTkLabel(tab, text=f"SO: {platform.system()} {platform.release()}", font=("Arial", 13)).pack()
        ctk.CTkLabel(tab, text=f"Arquitectura: {platform.machine()}", font=("Arial", 13)).pack()
        
        self.cpu_label = ctk.CTkLabel(tab, text="USO DE CPU: 0%", font=("Arial", 24, "bold"))
        self.cpu_label.pack(pady=20)
        self.ram_label = ctk.CTkLabel(tab, text="USO DE RAM: 0%", font=("Arial", 18))
        self.ram_label.pack(pady=5)
        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_label.configure(text=f"USO DE CPU: {cpu}%", text_color="#3b8ed0" if cpu < 75 else "#c0392b")
        self.ram_label.configure(text=f"USO DE RAM: {ram}%")
        self.after(1000, self.update_stats)

    # --- LIMPIADOR COMPLETO ---
    def setup_limpiador(self):
        tab = self.tabview.tab("Limpiador")
        ctk.CTkLabel(tab, text="Limpieza Profunda de Temporales", font=("Arial", 18, "bold")).pack(pady=20)
        ctk.CTkButton(tab, text="EJECUTAR LIMPIEZA TOTAL", command=self.limpiar).pack(pady=20)

    def limpiar(self):
        rutas = [os.path.expanduser("~/.cache/thumbnails"), os.path.expanduser("~/.local/share/Trash"), "/tmp"]
        liberado = 0
        for r in rutas:
            if os.path.exists(r):
                for dp, dn, filenames in os.walk(r):
                    for f in filenames:
                        try: liberado += os.path.getsize(os.path.join(dp, f))
                        except: pass
                shutil.rmtree(r, ignore_errors=True)
                os.makedirs(r, exist_ok=True)
        messagebox.showinfo("OpenArgOs", f"Limpieza terminada. Se liberaron {round(liberado/(1024*1024), 2)} MB.")

    # --- MODO GAMER (3 BOTONES) ---
    def setup_gamer_tab(self):
        tab = self.tabview.tab("Gamer")
        ctk.CTkLabel(tab, text="Gestión de Energía Gamer", font=("Arial", 18, "bold")).pack(pady=20)
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="AHORRO", fg_color="#27ae60", command=lambda: self.set_energy("power-saver")).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="EQUILIBRADO", fg_color="#f39c12", command=lambda: self.set_energy("balanced")).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="RENDIMIENTO", fg_color="#c0392b", command=lambda: self.set_energy("performance")).grid(row=0, column=2, padx=5)

    def set_energy(self, profile):
        try:
            subprocess.run(["powerprofilesctl", "set", profile], check=True)
            messagebox.showinfo("OpenArgOs", f"Modo {profile} activado con éxito.")
        except:
            messagebox.showerror("Error", "Asegúrate de tener power-profiles-daemon instalado.")

    # --- DESINSTALADOR CON REFRESCAR ---
    def setup_desinstalar(self):
        tab = self.tabview.tab("Desinstalar")
        ctk.CTkLabel(tab, text="Gestor de Aplicaciones Instaladas", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.app_listbox = tk.Listbox(tab, bg="#2b2b2b", fg="white", font=("Arial", 11), selectbackground="#3b8ed0")
        self.app_listbox.pack(pady=10, fill="both", expand=True, padx=40)
        
        btn_box = ctk.CTkFrame(tab, fg_color="transparent")
        btn_box.pack(pady=10)

        ctk.CTkButton(btn_box, text="REFRESCAR LISTA", command=self.listar_apps).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_box, text="DESINSTALAR", fg_color="#c0392b", command=self.desinstalar_seleccion).grid(row=0, column=1, padx=10)
        self.listar_apps()

    def listar_apps(self):
        self.app_listbox.delete(0, tk.END)
        try:
            output = subprocess.check_output("dpkg-query -W -f='${Package}\\n' | head -n 100", shell=True, text=True)
            for app in output.split('\n'):
                if app.strip(): self.app_listbox.insert(tk.END, app.strip())
        except: pass

    def desinstalar_seleccion(self):
        try:
            sel = self.app_listbox.get(self.app_listbox.curselection())
            if sel and messagebox.askyesno("Confirmar", f"¿Eliminar {sel}?"):
                cmd = f"pkexec apt purge -y {sel} && pkexec apt autoremove -y"
                subprocess.Popen(["x-terminal-emulator", "-e", f"bash -c '{cmd}; echo; read -p \"Proceso terminado. Enter para salir...\"'"])
        except:
            messagebox.showwarning("Atención", "Seleccioná una app de la lista.")

    # --- RED EN VIVO ---
    def setup_red_tab(self):
        tab = self.tabview.tab("Red")
        ctk.CTkLabel(tab, text="MONITOR DE TRÁFICO", font=("Arial", 18, "bold"), text_color="#3b8ed0").pack(pady=20)
        self.net_down = ctk.CTkLabel(tab, text="⬇ Descarga: 0 KB/s", font=("Arial", 16))
        self.net_down.pack(pady=5)
        self.net_up = ctk.CTkLabel(tab, text="⬆ Subida: 0 KB/s", font=("Arial", 16))
        self.net_up.pack(pady=5)
        
        self.last_recv = psutil.net_io_counters().bytes_recv
        self.last_sent = psutil.net_io_counters().bytes_sent
        self.update_net()

    def update_net(self):
        now = psutil.net_io_counters()
        down = (now.bytes_recv - self.last_recv) / 1024
        up = (now.bytes_sent - self.last_sent) / 1024
        self.net_down.configure(text=f"⬇ Descarga: {down:.1f} KB/s")
        self.net_up.configure(text=f"⬆ Subida: {up:.1f} KB/s")
        self.last_recv, self.last_sent = now.bytes_recv, now.bytes_sent
        self.after(1000, self.update_net)

if __name__ == "__main__":
    app = OpenDashApp()
    app.mainloop()
     

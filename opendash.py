# OpenDash v1.4 - Optimizador ArgOs Platinum
# Desarrollado por Tavo (Tavo78ok)
# Licencia: MIT
# GitHub: https://github.com/Tavo78ok/opendash

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import psutil
import subprocess
import platform
import os

class OpenDashApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OpenDash v1.4 - ArgOs Platinum")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")

        # Paleta de colores ArgOs
        self.color_neon = "#00ffa3"
        self.color_card = "#1a1c23"
        self.color_btn_reposo = "#2b2b2b"
        self.color_btn_activo = "#1f538d"

        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=self.color_neon)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Registro de pestañas
        self.tabview.add("Dashboard")
        self.tabview.add("Gamer")
        self.tabview.add("Inicio")
        self.tabview.add("Software")
        self.tabview.add("Red")

        # Inicialización de módulos
        self.setup_dashboard()
        self.setup_gamer()
        self.setup_inicio()
        self.setup_software()
        self.setup_red()

        self.update_dashboard()

    # --- 1. DASHBOARD ---
    def setup_dashboard(self):
        tab = self.tabview.tab("Dashboard")
        for widget in tab.winfo_children(): widget.destroy()

        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(20, 10))
        ctk.CTkLabel(header, text="Estado del Sistema", font=("Arial", 28, "bold")).pack(side="left")

        ctk.CTkButton(header, text="🧹 LIMPIEZA PROFUNDA", fg_color="#34495e", hover_color="#c0392b",
                      command=self.limpiar_sistema).pack(side="right")

        cards_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)
        self.cpu_f, self.cpu_l, self.cpu_b = self.create_card(cards_frame, "CPU", "0%", "📟", 0)
        self.ram_f, self.ram_l, self.ram_b = self.create_card(cards_frame, "RAM", "0 GB", "🖧", 1)
        self.disk_f, self.disk_l, self.disk_b = self.create_card(cards_frame, "DISCO", "0 GB", "💾", 2)

        info_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15, border_width=1, border_color="#333")
        info_frame.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(info_frame, text="📋 ESPECIFICACIONES DEL EQUIPO", font=("Arial", 16, "bold"), text_color=self.color_neon).pack(pady=15)
        self.info_text = ctk.CTkLabel(info_frame, text="Cargando...", font=("Courier New", 15), justify="left", anchor="w")
        self.info_text.pack(pady=10, padx=40, fill="both")
        self.refresh_sys_info()

    def create_card(self, master, title, value, icon, col):
        card = ctk.CTkFrame(master, fg_color=self.color_card, width=320, height=140, corner_radius=15)
        card.grid(row=0, column=col, padx=10, pady=10)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=f"{icon} {title}", font=("Arial", 13, "bold"), text_color="gray").pack(pady=(15,0))
        label = ctk.CTkLabel(card, text=value, font=("Arial", 30, "bold"))
        label.pack(pady=5)
        bar = ctk.CTkProgressBar(card, height=10, progress_color=self.color_neon)
        bar.pack(fill="x", padx=25, pady=10)
        bar.set(0)
        return card, label, bar

    # --- 2. MODO GAMER ---
    def setup_gamer(self):
        tab = self.tabview.tab("Gamer")
        for widget in tab.winfo_children(): widget.destroy()

        ctk.CTkLabel(tab, text="Optimización de Rendimiento", font=("Arial", 22, "bold"), text_color=self.color_neon).pack(pady=20)

        self.frame_perfiles = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15)
        self.frame_perfiles.pack(pady=10, padx=50, fill="x")

        self.btn_ahorro = ctk.CTkButton(self.frame_perfiles, text="MODO AHORRO", height=55, font=("Arial", 13, "bold"),
                                        fg_color=self.color_btn_reposo, command=lambda: self.aplicar_perfil("ahorro", self.btn_ahorro))
        self.btn_ahorro.pack(pady=12, padx=25, fill="x")

        self.btn_normal = ctk.CTkButton(self.frame_perfiles, text="MODO BALANCEADO", height=55, font=("Arial", 13, "bold"),
                                        fg_color=self.color_btn_reposo, command=lambda: self.aplicar_perfil("normal", self.btn_normal))
        self.btn_normal.pack(pady=12, padx=25, fill="x")

        self.btn_gamer = ctk.CTkButton(self.frame_perfiles, text="MODO GAMER 🔥", height=55, font=("Arial", 14, "bold"),
                                       fg_color=self.color_btn_reposo, command=lambda: self.aplicar_perfil("gamer", self.btn_gamer))
        self.btn_gamer.pack(pady=12, padx=25, fill="x")

        self.lista_botones_gamer = [self.btn_ahorro, self.btn_normal, self.btn_gamer]

        tip_card = ctk.CTkFrame(tab, fg_color="#1e2129", corner_radius=15, border_width=1, border_color=self.color_neon)
        tip_card.pack(pady=30, padx=50, fill="x")

        ctk.CTkLabel(tip_card, text="CONSEJOS DEL SISTEMA", font=("Arial", 14, "bold"), text_color=self.color_neon).pack(pady=(10,5))

        tips = [
            "• El Modo Gamer desactiva procesos secundarios para ganar FPS.",
            "• Usá el Modo Ahorro para maximizar la duración de la batería.",
            "• El Modo Balanceado mantiene las temperaturas bajo control."
        ]

        for tip in tips:
            ctk.CTkLabel(tip_card, text=tip, font=("Arial", 13), text_color="#cccccc", wraplength=500).pack(anchor="w", pady=3, padx=25)

        self.cargar_perfil_memoria()

    def aplicar_perfil(self, modo, boton_clicado, guardar=True):
        for btn in self.lista_botones_gamer:
            btn.configure(fg_color=self.color_btn_reposo, border_width=0)

        boton_clicado.configure(fg_color=self.color_btn_activo, border_width=2, border_color=self.color_neon)

        if guardar:
            with open(os.path.expanduser("~/.opendash_perfil"), "w") as f:
                f.write(modo)

        p_map = {"ahorro": "power-saver", "normal": "balanced", "gamer": "performance"}
        subprocess.run(["powerprofilesctl", "set", p_map[modo]])

    def cargar_perfil_memoria(self):
        ruta = os.path.expanduser("~/.opendash_perfil")
        perfil = "normal"
        if os.path.exists(ruta):
            with open(ruta, "r") as f: perfil = f.read().strip()

        if perfil == "ahorro": self.aplicar_perfil("ahorro", self.btn_ahorro, False)
        elif perfil == "gamer": self.aplicar_perfil("gamer", self.btn_gamer, False)
        else: self.aplicar_perfil("normal", self.btn_normal, False)

    # --- 3. GESTIÓN DE INICIO (AUTOSTART) ---
    def setup_inicio(self):
        tab = self.tabview.tab("Inicio")
        for widget in tab.winfo_children(): widget.destroy()

        header_f = ctk.CTkFrame(tab, fg_color="transparent")
        header_f.pack(fill="x", padx=40, pady=(20, 5))

        ctk.CTkLabel(header_f, text="Gestión de Autostart", font=("Arial", 22, "bold"), text_color=self.color_neon).pack(side="left")

        ctk.CTkButton(header_f, text="🔄 ACTUALIZAR", width=100, height=28, fg_color="#34495e",
                      font=("Arial", 11, "bold"), command=self.cargar_apps_inicio).pack(side="right")

        self.lbl_conteo = ctk.CTkLabel(tab, text="Analizando arranque...", font=("Arial", 12), text_color="gray")
        self.lbl_conteo.pack(pady=(0, 10))

        self.scroll_inicio = ctk.CTkScrollableFrame(tab, fg_color=self.color_card, corner_radius=15, border_width=1, border_color="#333")
        self.scroll_inicio.pack(padx=40, pady=10, fill="both", expand=True)

        self.cargar_apps_inicio()

    def cargar_apps_inicio(self):
        for widget in self.scroll_inicio.winfo_children(): widget.destroy()
        path = os.path.expanduser("~/.config/autostart")
        if not os.path.exists(path): os.makedirs(path)

        archivos = [f for f in os.listdir(path) if f.endswith((".desktop", ".disabled"))]
        activos = len([f for f in archivos if f.endswith(".desktop")])
        self.lbl_conteo.configure(text=f"Apps en inicio: {len(archivos)} | Activas: {activos} (Recomendado: menos de 5)")

        for archivo in archivos:
            estado = "ACTIVO" if archivo.endswith(".desktop") else "OFF"
            color_st = self.color_neon if estado == "ACTIVO" else "#e74c3c"

            f = ctk.CTkFrame(self.scroll_inicio, fg_color="transparent")
            f.pack(fill="x", pady=5, padx=10)

            nombre = archivo.replace(".desktop", "").replace(".disabled", "").replace("-", " ").capitalize()
            ctk.CTkLabel(f, text=f"🚀 {nombre}", font=("Arial", 13, "bold"), width=250, anchor="w").pack(side="left")

            btn_txt = "DESACTIVAR" if estado == "ACTIVO" else "ACTIVAR"
            ctk.CTkButton(f, text=btn_txt, width=110, height=30, fg_color="#2b2b2b", hover_color=color_st,
                          command=lambda a=archivo: self.toggle_autostart(a)).pack(side="right")
            ctk.CTkLabel(f, text=estado, text_color=color_st, width=80).pack(side="right", padx=10)

    def toggle_autostart(self, archivo):
        path = os.path.expanduser("~/.config/autostart")
        old = os.path.join(path, archivo)
        new = old.replace(".desktop", ".disabled") if archivo.endswith(".desktop") else old.replace(".disabled", ".desktop")
        os.rename(old, new)
        self.cargar_apps_inicio()

    # --- 4. SOFTWARE ---
    def setup_software(self):
        tab = self.tabview.tab("Software")
        for widget in tab.winfo_children(): widget.destroy()

        top_f = ctk.CTkFrame(tab, fg_color="transparent")
        top_f.pack(fill="x", padx=50, pady=20)

        self.entry_busqueda = ctk.CTkEntry(top_f, placeholder_text="🔍 Buscar aplicación para eliminar...", width=500)
        self.entry_busqueda.pack(side="left", padx=(0,10))
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_apps)

        ctk.CTkButton(top_f, text="🗑️ DESINSTALAR", fg_color="#c0392b", hover_color="#e74c3c", font=("Arial", 12, "bold"),
                      command=self.desinstalar_app).pack(side="right")

        self.app_listbox = tk.Listbox(tab, bg="#111", fg="white", font=("Arial", 12), borderwidth=0, highlightthickness=0)
        self.app_listbox.pack(pady=10, fill="both", expand=True, padx=50)
        self.listar_apps()

    # --- 5. RED ---
    def setup_red(self):
        tab = self.tabview.tab("Red")
        for widget in tab.winfo_children(): widget.destroy()
        self.net_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent", height=250)
        self.net_scroll.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(tab, text="🔍 ACTIVIDAD EN SEGUNDO PLANO", font=("Arial", 14, "bold"), text_color=self.color_neon).pack(pady=5)
        self.proc_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15)
        self.proc_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.proc_text = ctk.CTkLabel(self.proc_frame, text="Cargando procesos...", font=("Courier New", 12), justify="left", anchor="nw")
        self.proc_text.pack(fill="both", expand=True, padx=20, pady=15)
        self.refresh_net_cards()
        self.update_processes()

    # --- FUNCIONES DE SOPORTE ---
    def limpiar_sistema(self):
        if messagebox.askyesno("Limpieza", "¿Ejecutar limpieza de Caché, Paquetes Huérfanos y Papelera?"):
            user_path = os.path.expanduser("~/.local/share/Trash")
            cmd = (f"pkexec bash -c 'apt-get clean && apt-get autoremove -y; "
                   f"rm -rf {user_path}/files/*; rm -rf {user_path}/info/*; "
                   "echo -e \"\\n✨ SISTEMA LIMPIO. Presiona Enter...\"; read'")
            subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])

    def refresh_sys_info(self):
        try:
            uname = platform.uname()
            gpu = subprocess.check_output("lspci | grep -i vga | cut -d ':' -f3", shell=True, text=True).strip()
            cpu_model = subprocess.check_output("grep 'model name' /proc/cpuinfo | head -n1 | cut -d ':' -f2", shell=True, text=True).strip()
            info = (f" 🖥️  HOST:   {uname.node}\n 🐧 KERNEL: {uname.release}\n 📟 CPU:    {cpu_model}\n"
                    f" 🎮 GPU:    {gpu[:45]}\n ⏱️  UPTIME: {self.get_uptime()}")
            self.info_text.configure(text=info)
        except: pass

    def get_uptime(self):
        with open('/proc/uptime', 'r') as f:
            s = float(f.readline().split()[0])
            return f"{int(s//3600)}h {int((s%3600)//60)}m"

    def update_dashboard(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            self.cpu_l.configure(text=f"{cpu}%")
            self.cpu_b.set(cpu/100)
            self.ram_l.configure(text=f"{ram.used/(1024**3):.1f} GB")
            self.ram_b.set(ram.percent/100)
            self.disk_l.configure(text=f"{disk.free/(1024**3):.0f} GB Libres")
            self.disk_b.set(disk.percent/100)
        except: pass
        self.after(2000, self.update_dashboard)

    def listar_apps(self):
        self.app_listbox.delete(0, tk.END)
        output = subprocess.check_output("dpkg-query -W -f='${Package}\\n'", shell=True, text=True)
        self.todas_las_apps = sorted([app.strip() for app in output.split('\n') if app.strip()])
        for app in self.todas_las_apps: self.app_listbox.insert(tk.END, app)

    def filtrar_apps(self, e):
        b = self.entry_busqueda.get().lower()
        self.app_listbox.delete(0, tk.END)
        for app in self.todas_las_apps:
            if b in app.lower(): self.app_listbox.insert(tk.END, app)

    def desinstalar_app(self):
        try:
            sel = self.app_listbox.get(self.app_listbox.curselection())
            if messagebox.askyesno("Confirmar", f"¿Eliminar {sel}?"):
                cmd = f"pkexec bash -c 'apt purge -y {sel} && apt autoremove -y; read'"
                subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])
        except: pass

    def refresh_net_cards(self):
        for widget in self.net_scroll.winfo_children(): widget.destroy()
        for n, a in psutil.net_if_addrs().items():
            if n == "lo": continue
            card = ctk.CTkFrame(self.net_scroll, fg_color=self.color_card, corner_radius=12)
            card.pack(fill="x", pady=5, padx=10)
            ip = next((addr.address for addr in a if addr.family == 2), "N/A")
            ctk.CTkLabel(card, text=f"🌐 {n.upper()}", font=("Arial", 12, "bold")).pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(card, text=f"IP: {ip}", font=("Courier New", 12)).pack(side="left", padx=15)

    def update_processes(self):
        try:
            procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                           key=lambda x: x.info['cpu_percent'], reverse=True)[:10]
            header = f"{'PID':<8} {'NOMBRE':<20} {'CPU %':<10} {'RAM %':<10}\n" + "-"*50 + "\n"
            lines = "".join([f"{p.info['pid']:<8} {p.info['name'][:18]:<20} {p.info['cpu_percent']:<10} {p.info['memory_percent']:>5.1f}%\n" for p in procs])
            self.proc_text.configure(text=header + lines)
        except: pass
        self.after(3000, self.update_processes)

if __name__ == "__main__":
    app = OpenDashApp()
    app.mainloop()

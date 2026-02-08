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

        self.title("OpenDash v1.1 - ArgOs Master Gold")
        self.geometry("1050x800")
        ctk.set_appearance_mode("dark")
        
        self.color_neon = "#00ffa3"  
        self.color_card = "#1a1c23"  

        # --- Layout Principal ---
        self.tabview = ctk.CTkTabview(self, width=1000, height=750, segmented_button_selected_color=self.color_neon)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tabview.add("Dashboard")
        self.tabview.add("Gamer")
        self.tabview.add("Software")
        self.tabview.add("Red")

        # Inicializar todo
        self.setup_dashboard()
        self.setup_gamer()
        self.setup_software()
        self.setup_red()

        self.update_dashboard()

    # --- 1. DASHBOARD + FASTFETCH ---
    def setup_dashboard(self):
        tab = self.tabview.tab("Dashboard")
        for widget in tab.winfo_children(): widget.destroy()

        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(20, 10))
        ctk.CTkLabel(header, text="Panel de Control OpenArgOs", font=("Arial", 28, "bold")).pack(side="left")
        ctk.CTkButton(header, text="🧹 LIMPIAR SISTEMA", fg_color="#34495e", hover_color="#c0392b", 
                      command=self.limpiar_sistema).pack(side="right")

        cards = ctk.CTkFrame(tab, fg_color="transparent")
        cards.pack(fill="x", padx=30)
        self.cpu_f, self.cpu_l, self.cpu_b = self.create_card(cards, "CPU", "0%", "📟", 0)
        self.ram_f, self.ram_l, self.ram_b = self.create_card(cards, "RAM", "0 GB", "🖧", 1)
        self.disk_f, self.disk_l, self.disk_b = self.create_card(cards, "SISTEMA (SSD)", "0 GB", "💾", 2)

        info_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15)
        info_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        ctk.CTkLabel(info_frame, text="📊 INFORMACIÓN DEL SISTEMA", font=("Arial", 16, "bold"), text_color=self.color_neon).pack(pady=(10,5))
        
        self.info_text = ctk.CTkLabel(info_frame, text="", font=("Courier New", 16, "bold"), justify="left", anchor="w")
        self.info_text.pack(pady=15, padx=30, fill="both")
        self.refresh_sys_info()

    def create_card(self, master, title, value, icon, col):
        card = ctk.CTkFrame(master, fg_color=self.color_card, width=280, height=130, corner_radius=15)
        card.grid(row=0, column=col, padx=10, pady=10)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=f"{icon} {title}", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(10,0))
        label = ctk.CTkLabel(card, text=value, font=("Arial", 28, "bold"))
        label.pack(pady=5)
        bar = ctk.CTkProgressBar(card, height=8, progress_color=self.color_neon)
        bar.pack(fill="x", padx=20, pady=5)
        bar.set(0)
        return card, label, bar

    # --- 2. MODO GAMER CON TIPS ---
    def setup_gamer(self):
        tab = self.tabview.tab("Gamer")
        for widget in tab.winfo_children(): widget.destroy()
        ctk.CTkLabel(tab, text="Optimización y Energía", font=("Arial", 24, "bold"), text_color=self.color_neon).pack(pady=20)

        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20)

        left_p = ctk.CTkFrame(main_container, fg_color=self.color_card, corner_radius=15)
        left_p.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_p, text="Perfiles de Energía", font=("Arial", 16, "bold")).pack(pady=15)
        self.btn_ahorro = ctk.CTkButton(left_p, text="🍃 AHORRO", height=45, command=lambda: self.set_power_profile("power-saver"))
        self.btn_ahorro.pack(pady=10, padx=30, fill="x")
        self.btn_bal = ctk.CTkButton(left_p, text="⚖️ EQUILIBRADO", height=45, command=lambda: self.set_power_profile("balanced"))
        self.btn_bal.pack(pady=10, padx=30, fill="x")
        self.btn_perf = ctk.CTkButton(left_p, text="🚀 RENDIMIENTO", height=45, command=lambda: self.set_power_profile("performance"))
        self.btn_perf.pack(pady=10, padx=30, fill="x")

        right_p = ctk.CTkFrame(main_container, fg_color="#1e2129", corner_radius=15)
        right_p.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(right_p, text="💡 TIPS GAMER", font=("Arial", 16, "bold"), text_color=self.color_neon).pack(pady=15)
        tips = ("• RENDIMIENTO: Máxima potencia CPU.\n"
                "• EQUILIBRADO: Ideal para uso diario.\n"
                "• AHORRO: Alarga batería en laptops.\n"
                "• Tip: Cierra apps pesadas antes de jugar.")
        ctk.CTkLabel(right_p, text=tips, justify="left", font=("Arial", 13)).pack(pady=10, padx=20)

    # --- 3. SOFTWARE + BOTÓN DESINSTALAR ---
    def setup_software(self):
        tab = self.tabview.tab("Software")
        for widget in tab.winfo_children(): widget.destroy()
        
        top_f = ctk.CTkFrame(tab, fg_color="transparent")
        top_f.pack(fill="x", padx=50, pady=10)
        
        self.entry_busqueda = ctk.CTkEntry(top_f, placeholder_text="🔍 Buscar aplicación...", width=400)
        self.entry_busqueda.pack(side="left", padx=(0,10))
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_apps)

        ctk.CTkButton(top_f, text="🗑️ DESINSTALAR", fg_color="#c0392b", hover_color="#e74c3c", 
                      command=self.desinstalar_app).pack(side="right")

        self.app_listbox = tk.Listbox(tab, bg=self.color_card, fg="white", font=("Arial", 11), borderwidth=0)
        self.app_listbox.pack(pady=10, fill="both", expand=True, padx=50)
        self.listar_apps()

    # --- 4. RED (LLENA Y CON TARJETAS) ---
    def setup_red(self):
        tab = self.tabview.tab("Red")
        for widget in tab.winfo_children(): widget.destroy()
        
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent", width=900, height=500)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        for n, a in psutil.net_if_addrs().items():
            if n == "lo": continue
            card = ctk.CTkFrame(scroll, fg_color=self.color_card, corner_radius=12)
            card.pack(fill="x", pady=5, padx=10)
            
            stats = psutil.net_if_stats().get(n)
            est = "✅ ACTIVA" if stats and stats.isup else "❌ INACTIVA"
            
            ctk.CTkLabel(card, text=f"🌐 {n.upper()}", font=("Arial", 13, "bold")).pack(side="left", padx=20, pady=15)
            ip = next((addr.address for addr in a if addr.family == 2), "Sin IP")
            ctk.CTkLabel(card, text=f"IP: {ip}", font=("Courier New", 13), text_color=self.color_neon).pack(side="left", padx=20)
            ctk.CTkLabel(card, text=est, text_color=self.color_neon if "ACTIVA" in est else "#e74c3c").pack(side="right", padx=20)

    # --- LÓGICA DE ACTUALIZACIÓN ---
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

    def refresh_sys_info(self):
        try:
            u = psutil.disk_usage('/')
            gpu = subprocess.check_output("lspci | grep -i vga | cut -d ':' -f3", shell=True, text=True).strip()
            info = (f" OS:      OpenArgOs Gold\n KERNEL:  {platform.release()}\n"
                    f" UPTIME:  {self.get_uptime()}\n GPU:     {gpu[:35]}...\n"
                    f" RAM:     {psutil.virtual_memory().total // (1024**2)} MB\n"
                    f" DISCO:   {u.total // (1024**3)} GB")
            self.info_text.configure(text=info)
        except: pass

    def get_uptime(self):
        with open('/proc/uptime', 'r') as f:
            s = float(f.readline().split()[0])
            return f"{int(s//3600)}h {int((s%3600)//60)}m"

    def set_power_profile(self, p):
        subprocess.run(["powerprofilesctl", "set", p])
        for b in [self.btn_ahorro, self.btn_bal, self.btn_perf]: b.configure(border_width=0, fg_color="#3b3b3b")
        if "saver" in p: self.btn_ahorro.configure(border_width=2, border_color=self.color_neon, fg_color="#2ecc71")
        elif "bal" in p: self.btn_bal.configure(border_width=2, border_color=self.color_neon, fg_color="#3498db")
        else: self.btn_perf.configure(border_width=2, border_color=self.color_neon, fg_color="#e74c3c")

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
            if messagebox.askyesno("OpenArgOs", f"¿Eliminar {sel}?"):
                subprocess.Popen(["x-terminal-emulator", "-e", f"pkexec apt purge -y {sel} && pause"])
        except: messagebox.showwarning("Atención", "Selecciona una app primero.")

    def limpiar_sistema(self):
        if messagebox.askyesno("Limpieza", "¿Limpiar archivos temporales?"):
            subprocess.Popen(["x-terminal-emulator", "-e", "pkexec apt-get clean"])

if __name__ == "__main__":
    app = OpenDashApp()
    app.mainloop()
        

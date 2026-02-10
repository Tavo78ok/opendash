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

        self.title("OpenDash v1.3 - ArgOs Platinum")
        self.geometry("1100x850") 
        ctk.set_appearance_mode("dark")
        
        self.color_neon = "#00ffa3"  
        self.color_card = "#1a1c23"  

        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=self.color_neon)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tabview.add("Dashboard")
        self.tabview.add("Gamer")
        self.tabview.add("Software")
        self.tabview.add("Red")

        self.setup_dashboard()
        self.setup_gamer() # <--- Tips incluidos aquí
        self.setup_software()
        self.setup_red()

        self.update_dashboard()

    # --- 1. DASHBOARD ESTILO STACER ---
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

    # --- 2. MODO GAMER CON TIPS RECUPERADOS ---
    def setup_gamer(self):
        tab = self.tabview.tab("Gamer")
        for widget in tab.winfo_children(): widget.destroy()
        
        ctk.CTkLabel(tab, text="Optimización y Energía", font=("Arial", 24, "bold"), text_color=self.color_neon).pack(pady=20)

        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20)

        # Panel Izquierdo: Botones
        left_p = ctk.CTkFrame(main_container, fg_color=self.color_card, corner_radius=15)
        left_p.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_p, text="Perfiles de Energía", font=("Arial", 16, "bold")).pack(pady=15)
        self.btn_ahorro = ctk.CTkButton(left_p, text="🍃 AHORRO", height=45, command=lambda: self.set_power_profile("power-saver"))
        self.btn_ahorro.pack(pady=10, padx=30, fill="x")
        self.btn_bal = ctk.CTkButton(left_p, text="⚖️ BALANCE", height=45, command=lambda: self.set_power_profile("balanced"))
        self.btn_bal.pack(pady=10, padx=30, fill="x")
        self.btn_perf = ctk.CTkButton(left_p, text="🚀 PERFORMANCE", height=45, command=lambda: self.set_power_profile("performance"))
        self.btn_perf.pack(pady=10, padx=30, fill="x")

        # Panel Derecho: TIPS (RECUPERADOS)
        right_p = ctk.CTkFrame(main_container, fg_color="#1e2129", corner_radius=15, border_width=1, border_color="#333")
        right_p.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(right_p, text="💡 TIPS PARA GAMERS", font=("Arial", 16, "bold"), text_color=self.color_neon).pack(pady=15)
        
        tips_text = (
            "• PERFORMANCE: Activa todos los núcleos\n  al máximo. Ideal para jugar.\n\n"
            "• BALANCE: Equilibra calor y potencia.\n  Uso diario recomendado.\n\n"
            "• AHORRO: Baja frecuencias para cuidar\n  la batería o bajar temp.\n\n"
            "• TIP: Cerrar navegadores antes de abrir\n  un juego libera mucha RAM."
        )
        ctk.CTkLabel(right_p, text=tips_text, justify="left", font=("Arial", 13), padx=20).pack(pady=10, fill="both")

    # --- 3. SOFTWARE (TERMINAL FIX) ---
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

        self.app_listbox = tk.Listbox(tab, bg="#111", fg="white", font=("Arial", 12), borderwidth=0)
        self.app_listbox.pack(pady=10, fill="both", expand=True, padx=50)
        self.listar_apps()

    # --- 4. RED ---
    def setup_red(self):
        tab = self.tabview.tab("Red")
        for widget in tab.winfo_children(): widget.destroy()

        # Contenedor superior para tarjetas de red
        self.net_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent", height=250)
        self.net_scroll.pack(fill="x", padx=20, pady=10)

        # Divisor
        ctk.CTkLabel(tab, text="🔍 ACTIVIDAD EN SEGUNDO PLANO", font=("Arial", 14, "bold"), text_color=self.color_neon).pack(pady=5)

        # Tabla de Procesos
        self.proc_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15)
        self.proc_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.proc_text = ctk.CTkLabel(self.proc_frame, text="Cargando procesos...", font=("Courier New", 12), justify="left", anchor="nw")
        self.proc_text.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.refresh_net_cards()
        self.update_processes()

    def refresh_net_cards(self):
        for widget in self.net_scroll.winfo_children(): widget.destroy()
        for n, a in psutil.net_if_addrs().items():
            if n == "lo": continue
            card = ctk.CTkFrame(self.net_scroll, fg_color=self.color_card, corner_radius=12)
            card.pack(fill="x", pady=5, padx=10)
            stats = psutil.net_if_stats().get(n)
            est = "✅ CONECTADO" if stats and stats.isup else "❌ DESCONECTADO"
            ip = next((addr.address for addr in a if addr.family == 2), "N/A")
            ctk.CTkLabel(card, text=f"🌐 {n.upper()}", font=("Arial", 12, "bold")).pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(card, text=f"IP: {ip}", font=("Courier New", 12)).pack(side="left", padx=15)
            ctk.CTkLabel(card, text=est, text_color=self.color_neon if "✅" in est else "#e74c3c").pack(side="right", padx=15)

    def update_processes(self):
        try:
            # Obtenemos los 10 procesos que más CPU consumen (estilo monitor de recursos)
            procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), 
                           key=lambda x: x.info['cpu_percent'], reverse=True)[:10]
            
            header = f"{'PID':<8} {'NOMBRE':<20} {'CPU %':<10} {'RAM %':<10}\n"
            header += "-" * 50 + "\n"
            lines = ""
            for p in procs:
                lines += f"{p.info['pid']:<8} {p.info['name'][:18]:<20} {p.info['cpu_percent']:<10} {p.info['memory_percent']:>5.1f}%\n"
            
            self.proc_text.configure(text=header + lines)
        except: pass
        # Actualizamos cada 3 segundos la lista de procesos
        self.after(3000, self.update_processes)
    # --- LÓGICA ---
    def desinstalar_app(self):
        try:
            sel = self.app_listbox.get(self.app_listbox.curselection())
            if messagebox.askyesno("Confirmar", f"¿Eliminar {sel}?"):
                cmd = f"pkexec bash -c 'apt purge -y {sel} && apt autoremove -y; echo -e \"\\n✅ Finalizado. Presiona Enter...\"; read'"
                subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])
        except: messagebox.showwarning("Atención", "Selecciona una app primero.")

    # --- BUSCÁ ESTA PARTE EN TU CÓDIGO ---
    def limpiar_sistema(self):
        if messagebox.askyesno("Limpieza", "¿Ejecutar limpieza de Caché, Paquetes Huérfanos y Vaciar Papelera?"):
            # Reemplazamos el '~' por la ruta real de tu usuario
            # Si tu usuario no es cinnamontrixie, cambialo en la ruta de abajo
            user_path = "/home/cinnamontrixie/.local/share/Trash"
            
            cmd = (
                f"pkexec bash -c '"
                "apt-get clean && apt-get autoremove -y; "
                "echo \"Vaciando la papelera de reciclaje de usuario...\"; "
                f"rm -rf {user_path}/files/*; "
                f"rm -rf {user_path}/info/*; "
                "echo -e \"\\n✨ TODO LIMPIO: Sistema y Papelera. Presiona Enter...\"; read'"
            )
            subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])

    def refresh_sys_info(self):
        try:
            uname = platform.uname()
            gpu = subprocess.check_output("lspci | grep -i vga | cut -d ':' -f3", shell=True, text=True).strip()
            cpu_model = subprocess.check_output("grep 'model name' /proc/cpuinfo | head -n1 | cut -d ':' -f2", shell=True, text=True).strip()
            info = (
                f" 🖥️  HOST:        {uname.node}\n"
                f" 🐧 KERNEL:      {uname.release}\n"
                f" 🏗️  ARQ:         {uname.machine}\n"
                f" 📟 CPU:         {cpu_model}\n"
                f" 🎮 GPU:         {gpu[:50]}\n"
                f" ⏱️  UPTIME:      {self.get_uptime()}\n"
                f" 📦 PAQUETES:    {subprocess.check_output('dpkg -l | wc -l', shell=True, text=True).strip()} instalados"
            )
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

    def set_power_profile(self, p):
        subprocess.run(["powerprofilesctl", "set", p])
        messagebox.showinfo("Perfil", f"Modo {p} activado")

if __name__ == "__main__":
    app = OpenDashApp()
    app.mainloop()





     
    
        
     
         
       
     

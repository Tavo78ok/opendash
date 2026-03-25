#!/usr/bin/env python3
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import psutil
import subprocess
import platform
import os

class OpenDashApp(ctk.CTk):
    def __init__(self):
        # 1. ESTO ES CLAVE: Pasamos el className directamente al constructor de la base
        super().__init__(className='opendash')

        # 2. Configuramos la identidad
        self.title("OpenDash v1.5 - ArgOs Platinum")
        self.geometry("1100x650")

        # 3. Forzamos el nombre de la instancia para el Window Manager
        try:
            self.wm_instance_name("opendash")
            self.wm_class("opendash", "opendash")
        except:
            # Si falla el método directo, usamos el comando de TCL (el motor de Tkinter)
            try:
                self.tk.call('wm', 'iconname', self._w, 'opendash')
                self.tk.call('wm', 'class', self._w, 'opendash')
            except:
                pass

        ctk.set_appearance_mode("dark")
        # ... resto de tu código (iconos, colores, etc)

        self.color_neon = "#00ffa3"
        self.color_card = "#1a1c23"
        self.color_btn_reposo = "#2b2b2b"
        self.color_btn_activo = "#1f538d"
        self.datos_red = [0] * 50
        self.ultimo_io = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent

        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=self.color_neon)
        self.tabview.pack(padx=20, pady=(5, 10), fill="both", expand=True)

        self.tabview.add("Dashboard")
        self.tabview.add("Gamer")
        self.tabview.add("Inicio")
        self.tabview.add("Software")
        self.tabview.add("Red")

        self.setup_dashboard()
        self.setup_gamer()
        self.setup_inicio()
        self.setup_software()
        self.setup_red()

        # En lugar de una sola función, despertamos el dashboard directo
        self.after(500, self.update_dashboard) # El dashboard primero
        self.after(1000, self.carga_pesada_inicial) # Lo demás después
        self.after(1000, self.actualizar_grafico_red)

    def carga_pesada_inicial(self):
        # Aquí metés todo lo que consume tiempo al arrancar
        self.refresh_sys_info()
        self.listar_apps()
        self.cargar_apps_inicio()


    def setup_dashboard(self):
        tab = self.tabview.tab("Dashboard")
        for widget in tab.winfo_children(): widget.destroy()

        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(10, 5))
        ctk.CTkLabel(header, text="Estado del Sistema", font=("Arial", 24, "bold")).pack(side="left")
        
        btn_box = ctk.CTkFrame(header, fg_color="transparent")
        btn_box.pack(side="right")
        
        ctk.CTkButton(btn_box, text="🧹 LIMPIEZA PROFUNDA", fg_color="#3e4452", text_color="white", 
                      font=("Arial", 11, "bold"), height=32, command=self.limpiar_sistema).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_box, text="⚡ OPTIMIZAR RAM", fg_color=self.color_neon, text_color="black", 
                      font=("Arial", 11, "bold"), height=32, command=self.limpiar_ram).pack(side="left", padx=5)

        cards_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=10)
        self.cpu_f, self.cpu_l, self.cpu_b = self.create_card(cards_frame, "CPU", "0%", "📟", 0)
        self.ram_f, self.ram_l, self.ram_b = self.create_card(cards_frame, "RAM", "0 GB", "🖧", 1)
        self.disk_f, self.disk_l, self.disk_b = self.create_card(cards_frame, "DISCO", "0 GB", "💾", 2)

        info_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15, border_width=1, border_color="#333")
        info_frame.pack(fill="both", expand=True, padx=40, pady=(5, 20))
        
        ctk.CTkLabel(info_frame, text="🛡️ ESPECIFICACIONES DEL EQUIPO", font=("Arial", 14, "bold"), text_color=self.color_neon).pack(pady=(15, 5))

        # ARREGLO: Texto en Label con fuente 16 y Bold para que no quede pequeño
        self.info_text = ctk.CTkLabel(info_frame, text="Cargando...", font=("Courier New", 16, "bold"), 
                                     justify="left", anchor="nw")
        self.info_text.pack(fill="both", expand=True, padx=60, pady=20)
        self.refresh_sys_info()

    def create_card(self, master, title, value, icon, col):
        card = ctk.CTkFrame(master, fg_color=self.color_card, width=320, height=120, corner_radius=15)
        card.grid(row=0, column=col, padx=10)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=f"{icon} {title}", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(10,0))
        label = ctk.CTkLabel(card, text=value, font=("Arial", 26, "bold"))
        label.pack(pady=2)
        bar = ctk.CTkProgressBar(card, height=8, progress_color=self.color_neon)
        bar.pack(fill="x", padx=30, pady=10)
        bar.set(0)
        return card, label, bar

    def refresh_sys_info(self):
        try:
            uname = platform.uname()
            distro = "ArgOs Platinum Edition"
            pkgs = subprocess.check_output("dpkg -l | wc -l", shell=True, text=True).strip()

            try:
                gpu_cmd = r"lspci | grep -E 'VGA|3D' | cut -d ':' -f3 | sed 's/\[.*\]//g' | head -n 1"
                gpu = subprocess.check_output(gpu_cmd, shell=True, text=True).strip()
            except:
                gpu = "No detectada"

            info = (
                f" OS:        {distro}\n\n"
                f" HOST:      {uname.node}\n\n"
                f" KERNEL:    {uname.release}\n\n"
                f" PAQUETES:  {pkgs} (dpkg)\n\n"
                f" CPU:       {uname.processor[:35]}\n\n"
                f" GPU:       {gpu[:35]}\n\n"
                f" UPTIME:    {self.get_uptime()}"
            )
            self.info_text.configure(text=info)
        except: pass

    def limpiar_sistema(self):
        if messagebox.askyesno("Limpieza Profunda", "¿Desea ejecutar la limpieza total?\n(RAM, Paquetes y Papelera)"):
            usuario = os.getlogin()
            # ARREGLO: Ahora borra la papelera de forma efectiva por comandos
            cmd = (
                "echo '--- 🚀 OPTIMIZANDO RAM ---'; sync; echo 3 | sudo tee /proc/sys/vm/drop_caches; "
                "echo -e '\n--- 📦 LIMPIANDO PAQUETES ---'; sudo apt autoremove -y && sudo apt clean; "
                "echo -e '\n--- 🗑️ VACIANDO PAPELERA ---'; "
                f"rm -rf /home/{usuario}/.local/share/Trash/files/*; "
                f"rm -rf /home/{usuario}/.local/share/Trash/info/*; "
                "echo -e '\n✅ PROCESO TERMINADO. PRESIONE ENTER PARA SALIR.'; read"
            )
            subprocess.Popen(["x-terminal-emulator", "-e", "pkexec", "bash", "-c", cmd])

    def desinstalar_app(self):
        try:
            sel = self.app_listbox.get(self.app_listbox.curselection())
            if messagebox.askyesno("Confirmar", f"¿Eliminar {sel} y sus dependencias?"):
                # ARREGLO: Purge y Autoremove en cadena para limpieza total
                cmd = f"pkexec bash -c 'apt purge -y {sel} && apt autoremove -y; echo -e \"\\nListo. Presione Enter.\"; read'"
                subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])
                self.after(5000, self.listar_apps)
        except: pass

    # --- PESTAÑA RED (INTACTA COMO PEDISTE) ---
    def setup_red(self):
        tab = self.tabview.tab("Red")
        for widget in tab.winfo_children(): widget.destroy()
        
        card_grafico = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15, height=180)
        card_grafico.pack(padx=20, pady=10, fill="x")
        card_grafico.pack_propagate(False)
        
        ctk.CTkLabel(card_grafico, text="📊 FLUJO DE RED (KB/S)", font=("Arial", 11, "bold"), text_color=self.color_neon).pack(pady=5)
        self.canvas_red = tk.Canvas(card_grafico, height=100, bg="#1a1c23", highlightthickness=0)
        self.canvas_red.pack(padx=15, pady=5, fill="x")

        self.net_scroll = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=10, height=45)
        self.net_scroll.pack(fill="x", padx=20, pady=5)
        self.refresh_net_cards()
        
        ctk.CTkLabel(tab, text="🔍 PROCESOS ACTIVOS", font=("Arial", 12, "bold"), text_color=self.color_neon).pack(pady=5)
        
        self.proc_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15)
        self.proc_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.proc_text = ctk.CTkLabel(self.proc_frame, text="...", font=("Courier New", 11), justify="left", anchor="nw")
        self.proc_text.pack(fill="both", expand=True, padx=20, pady=10)
        self.update_processes()

    # (El resto de funciones: setup_gamer, setup_inicio, etc., se mantienen igual)
    def setup_gamer(self):
        tab = self.tabview.tab("Gamer")
        for widget in tab.winfo_children(): widget.destroy()

        # Título principal con más presencia
        ctk.CTkLabel(tab, text="🚀 Optimización de Rendimiento", 
                     font=("Arial", 26, "bold"), text_color=self.color_neon).pack(pady=(20, 10))

        ctk.CTkLabel(tab, text="Seleccioná un perfil para ajustar el consumo y la potencia del equipo.", 
                     font=("Arial", 13), text_color="gray").pack(pady=(0, 20))

        # Contenedor central para los botones y descripciones
        menu_frame = ctk.CTkFrame(tab, fg_color="transparent")
        menu_frame.pack(expand=True, fill="both", padx=50)

        # MODO AHORRO
        self.btn_ahorro = ctk.CTkButton(menu_frame, text="MODO AHORRO", height=55, width=400, font=("Arial", 14, "bold"),
                                        command=lambda: self.aplicar_perfil("ahorro", self.btn_ahorro))
        self.btn_ahorro.pack(pady=(10, 0))
        ctk.CTkLabel(menu_frame, text="🍃 Reduce la frecuencia del CPU y el brillo para maximizar la batería.", 
                     font=("Arial", 11, "italic"), text_color="#777").pack(pady=(2, 15))

        # MODO BALANCEADO
        self.btn_normal = ctk.CTkButton(menu_frame, text="MODO BALANCEADO", height=55, width=400, font=("Arial", 14, "bold"),
                                        command=lambda: self.aplicar_perfil("normal", self.btn_normal))
        self.btn_normal.pack(pady=(10, 0))
        ctk.CTkLabel(menu_frame, text="⚖️ Equilibrio inteligente entre temperatura, ruido y velocidad.", 
                     font=("Arial", 11, "italic"), text_color="#777").pack(pady=(2, 15))

        # MODO GAMER
        self.btn_gamer = ctk.CTkButton(menu_frame, text="MODO GAMER 🔥", height=55, width=400, font=("Arial", 14, "bold"),
                                       command=lambda: self.aplicar_perfil("gamer", self.btn_gamer))
        self.btn_gamer.pack(pady=(10, 0))
        ctk.CTkLabel(menu_frame, text="⚡ Desbloquea los límites de energía para máxima tasa de frames y respuesta.", 
                     font=("Arial", 11, "italic"), text_color="#777").pack(pady=(2, 15))

        # Zona de Tips al final para llenar el espacio inferior
        tip_frame = ctk.CTkFrame(tab, fg_color=self.color_card, corner_radius=15, border_width=1, border_color="#333")
        tip_frame.pack(side="bottom", pady=30, padx=60, fill="x")

        tip_content = ("💡 TIPS DE RENDIMIENTO\n"
                       "• El Modo Gamer es ideal si tenés la PC enchufada a la corriente.\n"
                       "• Si notás que los ventiladores hacen mucho ruido, probá el Modo Balanceado.\n"
                       "• Para ver películas o navegar, el Modo Ahorro mantiene el equipo frío.")
        
        ctk.CTkLabel(tip_frame, text=tip_content, font=("Arial", 12), justify="left", padx=20, pady=15).pack()

        self.lista_botones_gamer = [self.btn_ahorro, self.btn_normal, self.btn_gamer]
        self.cargar_perfil_memoria()

    def setup_software(self):
        tab = self.tabview.tab("Software")
        top = ctk.CTkFrame(tab, fg_color="transparent")
        top.pack(fill="x", padx=50, pady=20)
        self.entry_busqueda = ctk.CTkEntry(top, placeholder_text="🔍 Buscar aplicación...", width=450)
        self.entry_busqueda.pack(side="left", padx=10)
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_apps)
        ctk.CTkButton(top, text="🗑️ DESINSTALAR", fg_color="#e74c3c", font=("Arial", 11, "bold"), command=self.desinstalar_app).pack(side="right")
        self.app_listbox = tk.Listbox(tab, bg="#111", fg="white", font=("Arial", 11), borderwidth=0, highlightthickness=0)
        self.app_listbox.pack(pady=10, fill="both", expand=True, padx=50)
        self.listar_apps()

    def listar_apps(self):
        self.app_listbox.delete(0, tk.END)
        try:
            output = subprocess.check_output("dpkg-query -W -f='${Package}\\n'", shell=True, text=True)
            self.todas_las_apps = sorted([app.strip() for app in output.split('\n') if app.strip()])
            for app in self.todas_las_apps: self.app_listbox.insert(tk.END, app)
        except: pass

    def filtrar_apps(self, e):
        b = self.entry_busqueda.get().lower()
        self.app_listbox.delete(0, tk.END)
        for app in self.todas_las_apps:
            if b in app.lower(): self.app_listbox.insert(tk.END, app)

    def setup_inicio(self):
        tab = self.tabview.tab("Inicio")
        ctk.CTkLabel(tab, text="Gestión de Autostart", font=("Arial", 22, "bold")).pack(pady=15)
        self.scroll_inicio = ctk.CTkScrollableFrame(tab, fg_color=self.color_card, corner_radius=15)
        self.scroll_inicio.pack(padx=40, pady=10, fill="both", expand=True)
        self.cargar_apps_inicio()

    def cargar_apps_inicio(self):
        for w in self.scroll_inicio.winfo_children(): w.destroy()
        path = os.path.expanduser("~/.config/autostart")
        if not os.path.exists(path): return
        for archivo in os.listdir(path):
            if archivo.endswith((".desktop", ".disabled")):
                f = ctk.CTkFrame(self.scroll_inicio, fg_color="transparent")
                f.pack(fill="x", pady=5, padx=10)
                nombre = archivo.replace(".desktop", "").replace(".disabled", "").capitalize()
                ctk.CTkLabel(f, text=f"🚀 {nombre}", font=("Arial", 12)).pack(side="left")
                btn_txt = "DESACTIVAR" if archivo.endswith(".desktop") else "ACTIVAR"
                color = "#c0392b" if archivo.endswith(".desktop") else "#2980b9"
                ctk.CTkButton(f, text=btn_txt, width=100, fg_color=color, command=lambda a=archivo: self.toggle_autostart(a)).pack(side="right")

    def toggle_autostart(self, archivo):
        path = os.path.expanduser("~/.config/autostart")
        old = os.path.join(path, archivo)
        new = old.replace(".desktop", ".disabled") if archivo.endswith(".desktop") else old.replace(".disabled", ".desktop")
        os.rename(old, new); self.cargar_apps_inicio()

    def aplicar_perfil(self, modo, btn_clicado, guardar=True):
        for btn in self.lista_botones_gamer: btn.configure(fg_color=self.color_btn_reposo)
        btn_clicado.configure(fg_color=self.color_btn_activo)
        if guardar:
            with open(os.path.expanduser("~/.opendash_perfil"), "w") as f: f.write(modo)
        p_map = {"ahorro": "power-saver", "normal": "balanced", "gamer": "performance"}
        try: subprocess.run(["powerprofilesctl", "set", p_map[modo]])
        except: pass

    def cargar_perfil_memoria(self):
        ruta = os.path.expanduser("~/.opendash_perfil")
        if os.path.exists(ruta):
            with open(ruta, "r") as f: p = f.read().strip()
            if p == "ahorro": self.aplicar_perfil("ahorro", self.btn_ahorro, False)
            elif p == "gamer": self.aplicar_perfil("gamer", self.btn_gamer, False)
            else: self.aplicar_perfil("normal", self.btn_normal, False)
        else: self.aplicar_perfil("normal", self.btn_normal, False)

    def get_uptime(self):
        try:
            with open('/proc/uptime', 'r') as f:
                s = float(f.readline().split()[0])
                return f"{int(s//3600)}h {int((s%3600)//60)}m"
        except: return "N/A"

    def limpiar_ram(self):
        try:
            subprocess.run(["pkexec", "sh", "-c", "sync; echo 3 > /proc/sys/vm/drop_caches"])
            messagebox.showinfo("ArgOs Platinum", "¡Memoria optimizada!")
        except: pass

    def actualizar_grafico_red(self):
        try:
            io = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
            diff = (io - self.ultimo_io) / 1024
            self.ultimo_io = io
            self.datos_red.append(diff)
            self.datos_red.pop(0)
            self.canvas_red.delete("all")
            w, h = self.canvas_red.winfo_width(), self.canvas_red.winfo_height()
            if w > 1:
                pts = []
                for i, v in enumerate(self.datos_red):
                    pts.append(i * (w/49))
                    pts.append(h - min(v * 0.8, h))
                if len(pts) >= 4:
                    self.canvas_red.create_line(pts, fill=self.color_neon, width=2, smooth=True)
        except: pass
        self.after(1000, self.actualizar_grafico_red)

    def update_dashboard(self):
        try:
            # 1. Leemos los datos
            cpu_val = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disco = psutil.disk_usage('/')

            # 2. DEBUG: Esto imprimirá los números en la terminal de Kate
            print(f"DEBUG -> CPU: {cpu_val}% | RAM: {mem.percent}% | DISCO: {disco.percent}%")

            # 3. Actualizamos etiquetas (sin tanto cálculo raro por ahora)
            self.cpu_l.configure(text=f"{int(cpu_val)}%")
            self.ram_l.configure(text=f"{round(mem.used / (1024**3), 2)} GB")
            self.disk_l.configure(text=f"{round(disco.free / (1024**3), 1)} GB Libres")

            # 4. Actualizamos barras (Aseguramos que el valor sea entre 0 y 1)
            self.cpu_b.set(cpu_val / 100)
            self.ram_b.set(mem.percent / 100)
            self.disk_b.set(disco.percent / 100)

            self.update_idletasks()

        except Exception as e:
            print(f"Error crítico en dashboard: {e}")

        # 5. Reintento rápido
        self.after(1000, self.update_dashboard)

    def refresh_net_cards(self):
        for n, a in psutil.net_if_addrs().items():
            if n == "lo": continue
            ip = next((addr.address for addr in a if addr.family == 2), "N/A")
            ctk.CTkLabel(self.net_scroll, text=f"🌐 {n.upper()}    IP: {ip}", font=("Arial", 12, "bold")).pack(pady=10)
            break

    def update_processes(self):
        try:
            procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                           key=lambda x: x.info['cpu_percent'], reverse=True)[:10]
            header = f"{'PID':<10} {'NOMBRE':<22} {'CPU %':<12} {'RAM %':<10}\n" + "-"*55 + "\n"
            lines = "".join([f"{p.info['pid']:<10} {p.info['name'][:20]:<22} {p.info['cpu_percent']:<12} {p.info['memory_percent']:>5.1f}%\n" for p in procs])
            self.proc_text.configure(text=header + lines)
        except: pass
        self.after(3000, self.update_processes)

if __name__ == "__main__":
    # Truco para que el icono aparezca en el dock de Linux
    try:
        from ctypes import cdll
        myappid = 'argos.opendash.v1'
        # Esto le da un ID único al proceso
    except:
        pass
    app = OpenDashApp()
    app.mainloop()

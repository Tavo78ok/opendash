import customtkinter as ctk
import psutil
import os
import shutil
import threading
import time

class Opendash(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x650")
        self.title("Opendash v0.9.5 - Ultra Suite Familiar")
        ctk.set_appearance_mode("dark")
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tabview.add("Monitor")
        self.tabview.add("Red")
        self.tabview.add("Gamer")
        self.tabview.add("Limpieza")
        
        self.setup_monitor()
        self.setup_red()
        self.setup_gamer()
        self.setup_limpieza()
        
        # Iniciar actualización de datos
        self.actualizar_datos()

    def setup_monitor(self):
        tab = self.tabview.tab("Monitor")
        self.lbl_cpu = ctk.CTkLabel(tab, text="CPU: 0%", font=("Arial", 16))
        self.lbl_cpu.pack(pady=10)
        self.bar_cpu = ctk.CTkProgressBar(tab)
        self.bar_cpu.pack(pady=5, fill="x", padx=50)

    def setup_red(self):
        tab = self.tabview.tab("Red")
        ctk.CTkLabel(tab, text="Velocidad Actual", font=("Arial", 14)).pack(pady=10)
        self.lbl_net = ctk.CTkLabel(tab, text="0.0 KB/s", font=("Consolas", 35), text_color="#3a7ebf")
        self.lbl_net.pack(pady=20)

    def setup_gamer(self):
        tab = self.tabview.tab("Gamer")
        self.btn_gamer = ctk.CTkButton(tab, text="ACTIVAR MODO ALTO RENDIMIENTO 🎮", 
                                       command=self.modo_gamer, fg_color="#6200ee", height=50)
        self.btn_gamer.pack(pady=50)

    def setup_limpieza(self):
        tab = self.tabview.tab("Limpieza")
        ctk.CTkLabel(tab, text="Limpiador de Temporales", font=("Arial", 16)).pack(pady=20)
        self.btn_limpiar = ctk.CTkButton(tab, text="LIMPIAR BASURA ✨", 
                                         command=self.ejecutar_limpieza, fg_color="#2d8a4e")
        self.btn_limpiar.pack(pady=10)
        self.lbl_status = ctk.CTkLabel(tab, text="Sistema listo")
        self.lbl_status.pack(pady=10)

    def modo_gamer(self):
        os.system("powerprofilesctl set performance")
        self.btn_gamer.configure(text="¡MODO GAMER ACTIVO! 🔥", state="disabled")

    def ejecutar_limpieza(self):
        rutas = [os.path.expanduser("~/.cache/thumbnails"), "/tmp"]
        for r in rutas:
            if os.path.exists(r):
                shutil.rmtree(r, ignore_errors=True)
                os.makedirs(r, exist_ok=True)
        self.lbl_status.configure(text="¡Limpieza completada! Liberaste espacio.", text_color="green")

    def actualizar_datos(self):
        # CPU
        cpu = psutil.cpu_percent()
        self.lbl_cpu.configure(text=f"CPU: {cpu}%")
        self.bar_cpu.set(cpu / 100)
        # Red en hilo aparte
        threading.Thread(target=self.calc_red, daemon=True).start()
        self.after(2000, self.actualizar_datos)

    def calc_red(self):
        t0 = psutil.net_io_counters().bytes_recv
        time.sleep(1)
        t1 = psutil.net_io_counters().bytes_recv
        vel = (t1 - t0) / 1024
        self.lbl_net.configure(text=f"{vel:.1f} KB/s")

if __name__ == "__main__":
    app = Opendash()
    app.mainloop()
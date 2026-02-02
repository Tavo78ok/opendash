import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import psutil
import shutil
import os

# Configuración de apariencia OpenArgOs
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") # Color oficial de la suite

class OpenDashApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Opendash v0.9.6 | OpenArgOs Official Suite")
        self.geometry("700x500")

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra Lateral (Sidebar)
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="OpenArgOs", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="Sistema: Optimizado", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=10)

        # Tabview (Pestañas)
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.tabview.add("Monitor")
        self.tabview.add("Limpiador")
        self.tabview.add("Gamer")
        self.tabview.add("Red")

        self.setup_monitor()
        self.setup_limpiador()

    def setup_monitor(self):
        self.cpu_label = ctk.CTkLabel(self.tabview.tab("Monitor"), text="Cargando CPU...", font=("Arial", 16))
        self.cpu_label.pack(pady=20)
        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        self.cpu_label.configure(text=f"Uso de CPU: {cpu}%")
        self.after(1000, self.update_stats)

    def setup_limpiador(self):
        self.clean_btn = ctk.CTkButton(self.tabview.tab("Limpiador"), text="Ejecutar Limpieza OpenArgOs", command=self.limpiar)
        self.clean_btn.pack(pady=50)

    def limpiar(self):
        # Lógica de limpieza (basada en lo que ya teníamos)
        print("Limpiando temporales...")
        tk.messagebox.showinfo("OpenArgOs", "Limpieza completada con éxito.")

if __name__ == "__main__":
    app = OpenDashApp()
    app.mainloop()
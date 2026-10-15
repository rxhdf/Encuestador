# app.py
import customtkinter as ctk
from tkinter import messagebox
import threading

from main import ejecutar_bot_encuestas

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppFormulario(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Botsito FreeFire")
        # Ventana significativamente más grande y cómoda
        self.geometry("850x720")
        self.resizable(False, False)

        # Definimos fuentes grandes, limpias y antialiased (suaves)
        # Usamos "DejaVu Sans" o "Ubuntu" que se renderizan de forma excelente en Linux sin pixeles
        self.fuente_titulo = ctk.CTkFont(family="DejaVu Sans", size=26, weight="bold")
        self.fuente_etiqueta = ctk.CTkFont(family="DejaVu Sans", size=16, weight="bold")
        self.fuente_general = ctk.CTkFont(family="DejaVu Sans", size=15)
        self.fuente_log = ctk.CTkFont(family="DejaVu Sans", size=14)

        # --- Título ---
        self.label_titulo = ctk.CTkLabel(self, text="Automatizador de Encuestas de Google", font=self.fuente_titulo)
        self.label_titulo.pack(pady=25)

        # --- Campo de URL ---
        self.label_url = ctk.CTkLabel(self, text="URL del Google Form (modo viewform):", font=self.fuente_etiqueta)
        self.label_url.pack(anchor="w", padx=60)

        self.entry_url = ctk.CTkEntry(
            self, 
            placeholder_text="https://docs.google.com/forms/d/e/.../viewform", 
            width=730, 
            height=48, 
            font=self.fuente_general
        )
        self.entry_url.pack(pady=10)

        # --- Botón de Ejecución Ampliado ---
        self.btn_iniciar = ctk.CTkButton(
            self, 
            text="Iniciar Simulación (N encuestas)", 
            command=self.ejecutar_en_hilo, 
            fg_color="#2b8a3e", 
            hover_color="#2b7034",
            font=self.fuente_etiqueta,
            height=52,
            corner_radius=8
        )
        self.btn_iniciar.pack(pady=25)

        # --- Consola Visual (Más grande y legible) ---
        self.label_log = ctk.CTkLabel(self, text="Progreso y registro en tiempo real:", font=self.fuente_etiqueta)
        self.label_log.pack(anchor="w", padx=60)

        # Cuadro de texto amplio con fuente suave y no pixelada
        self.textbox_log = ctk.CTkTextbox(
            self, 
            width=730, 
            height=320, 
            corner_radius=8, 
            font=self.fuente_log
        )
        self.textbox_log.pack(pady=10)
        self.textbox_log.configure(state="disabled")

    def log(self, mensaje):
        """Función segura para imprimir en la consola de la interfaz"""
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", mensaje + "\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")

    def ejecutar_en_hilo(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL válida de Google Forms.")
            return
        
        self.btn_iniciar.configure(state="disabled", fg_color="gray")
        
        hilo = threading.Thread(target=self.proceso_hilo, args=(url,))
        hilo.start()

    def proceso_hilo(self, url):
        ejecutar_bot_encuestas(url, self.log, total_encuestas=227)
        self.btn_iniciar.configure(state="normal", fg_color="#2b8a3e")

if __name__ == "__main__":
    app = AppFormulario()
    app.mainloop()
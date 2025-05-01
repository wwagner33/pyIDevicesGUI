import tkinter as tk
from tkinter import ttk

class AboutDialog(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre")
        self.geometry("400x250")
        self.resizable(False, False)

        ttk.Label(self, text="pyIDevices GUI", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(self, text="Versão 0.1").pack()

        texto = (
            "Autor: Wellington Sarmento 🐼\n"
            "Baseado no projeto original de Helltar\n"
            "https://github.com/Helltar/idevicegui\n\n"
            "Licença GNU GPL v3.0\n"
            "🄯2025"
        )
        ttk.Label(self, text=texto, justify="center", wraplength=360).pack(pady=10)
        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=5)
        # Torna a janela modal
        self.transient(master)   # associa visualmente ao pai
        self.grab_set()          # bloqueia interação com outras janelas
        self.wait_window(self)   # espera o fechamento da janela


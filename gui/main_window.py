import tkinter as tk
from tkinter import ttk, messagebox
from app import idevice
import os
import sys
import subprocess
from app.utils import bytes_para_gb
from gui.about_dialog import AboutDialog
from tkinter import filedialog
from app import diagnostics, imagemounter, screenshot, config, logger, backup, usbtools


class MainWindow(tk.Tk):
    def __init__(self):
        from app import config, logger
        
        super().__init__()
        self.title("pyIDevices GUI")
        self.geometry("600x350")
        self.resizable(False, False)

        # Define ícone da janela
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../resources/apple.png")
        )
        print(f"🔍 Tentando carregar ícone: {icon_path}")

        try:
            icon_image = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, icon_image)
            print("✅ Ícone carregado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao carregar ícone: {e}")

        self.create_menu()
        self.create_widgets()
        logger.info(f"Último diretório de backup usado: {config.get_backup_path()}")

    def create_menu(self):
        menubar = tk.Menu(self)

        # Menu Dispositivo
        dispositivo_menu = tk.Menu(menubar, tearoff=0)
        dispositivo_menu.add_command(label="Montar Imagens", command=self.montar_imagem)
        dispositivo_menu.add_command(label="Fazer Backup", command=self.fazer_backup)
        dispositivo_menu.add_command(label="Capturar Tela", command=self.capturar_tela)
        dispositivo_menu.add_command(label="Ver Diagnóstico", command=self.ver_diagnostico)
        dispositivo_menu.add_separator()
        dispositivo_menu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Dispositivo", menu=dispositivo_menu)

        # Menu Ajuda
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        ajuda_menu.add_command(label="Sobre", command=self.exibir_sobre)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)

        # Menu Ferramentas
        ferramentas_menu = tk.Menu(menubar, tearoff=0)
        ferramentas_menu.add_command(label="Abrir Arquivo de Log", command=self.ver_log)
        ferramentas_menu.add_command(label="Abrir pasta de Backup", command=self.abrir_backup_dir)
        ferramentas_menu.add_command(label="Verificar Confiança USB", command=self.validar_dispositivo)
        ferramentas_menu.add_separator()
        ferramentas_menu.add_command(label="Ver Dispositivos USB", command=self.ver_usb)
        menubar.add_cascade(label="Ferramentas", menu=ferramentas_menu)

        self.config(menu=menubar)


    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Aba: Informações do dispositivo
        self.device_frame = ttk.Frame(self.notebook)
        self.info_text = tk.Text(self.device_frame, height=12, width=70)
        self.info_text.pack(expand=True, fill="both")
        ttk.Button(self.device_frame, text="Atualizar Informações", command=self.atualizar_info).pack(pady=5)
        self.notebook.add(self.device_frame, text="📱 Dispositivo")

        # Aba: Log do sistema
        self.log_frame = ttk.Frame(self.notebook)
        self.log_text = tk.Text(self.log_frame, height=12, width=70, state="disabled", bg="#f4f4f4")
        self.log_text.pack(expand=True, fill="both")
        self.notebook.add(self.log_frame, text="📝 Log")

        # Atualiza o log ao trocar para a aba "Log"
        self.notebook.bind("<<NotebookTabChanged>>", self.atualizar_log_aba)

    def atualizar_info(self):
        self.info_text.delete(1.0, tk.END)

        if not idevice.is_device_plugged():
            self.info_text.insert(tk.END, "❌ Nenhum dispositivo conectado.\n")
            return

        nome = idevice.get_device_name()
        ios = idevice.get_device_info_by_key("ProductVersion")
        ciclo = idevice.get_device_cycle_count()
        total = idevice.get_disk_usage(idevice.TOTAL_DISK_CAPACITY)
        usado = idevice.get_disk_usage(idevice.TOTAL_DATA_CAPACITY)
        livre = idevice.get_disk_usage(idevice.TOTAL_DATA_AVAILABLE)

        self.info_text.insert(tk.END, f"📱 Nome: {nome}\n")
        self.info_text.insert(tk.END, f"📦 iOS: {ios}\n")
        self.info_text.insert(tk.END, f"🔋 Ciclos de bateria: {ciclo}\n")
        self.info_text.insert(tk.END, f"💾 Total: {bytes_para_gb(total)} GB\n")
        self.info_text.insert(tk.END, f"💾 Usado: {bytes_para_gb(usado)} GB\n")
        self.info_text.insert(tk.END, f"💾 Livre: {bytes_para_gb(livre)} GB\n")


    def montar_imagem(self):
        if not idevice.is_device_plugged():
            messagebox.showerror("Erro", "Nenhum dispositivo conectado.")
            return

        dmg_path = filedialog.askopenfilename(
            title="Escolha a imagem DMG",
            filetypes=[("Imagens Apple Disk", "*.dmg")]
        )
        if not dmg_path:
            return

        sucesso, saida = imagemounter.montar_imagem(dmg_path)
        if sucesso:
            messagebox.showinfo("Imagem", f"Imagem montada com sucesso!\n\n{saida}")
        else:
            messagebox.showerror("Erro", f"Erro ao montar imagem:\n\n{saida}")

    def ver_diagnostico(self):
        if not idevice.is_device_plugged():
            messagebox.showerror("Erro", "Nenhum dispositivo conectado.")
            return

        sucesso, dados = diagnostics.obter_diagnostico()
        if sucesso:
            self.info_text.insert(tk.END, "\n🔧 Diagnóstico:\n")
            self.info_text.insert(tk.END, dados + "\n")
        else:
            messagebox.showerror("Erro", f"Erro ao obter diagnóstico:\n\n{dados}")

    def fazer_backup(self):
        from tkinter import filedialog
        from app import backup, config, logger

        if not idevice.is_device_plugged():
            messagebox.showerror("Erro", "Nenhum dispositivo iOS conectado.")
            return

        pasta_backup = filedialog.askdirectory(
            title="Escolha o diretório de destino do backup",
            initialdir=config.get_backup_path() or os.path.expanduser("~")
        )

        if not pasta_backup:
            return  # usuário cancelou

        self.info_text.insert(tk.END, f"\n📦 Iniciando backup para: {pasta_backup}\n")
        sucesso, mensagem = backup.realizar_backup(pasta_backup)

        if sucesso:
            messagebox.showinfo("Backup", "Backup realizado com sucesso!")
            self.info_text.insert(tk.END, "✅ Backup concluído com sucesso.\n")
            config.set_backup_path(pasta_backup)
        else:
            messagebox.showerror("Erro", f"Erro ao fazer backup:\n\n{mensagem}")
            self.info_text.insert(tk.END, f"❌ Erro no backup:\n{mensagem}\n")

    def capturar_tela(self):
        if not idevice.is_device_plugged():
            messagebox.showerror("Erro", "Nenhum dispositivo conectado.")
            return

        pasta = filedialog.askdirectory(title="Escolha a pasta para salvar a captura")
        if not pasta:
            return

        sucesso, resultado = screenshot.capturar_screenshot(pasta)
        if sucesso:
            messagebox.showinfo("Captura de Tela", f"Imagem salva em:\n{resultado}")
        else:
            messagebox.showerror("Erro", f"Erro ao capturar tela:\n\n{resultado}")

    def exibir_sobre(self):
        AboutDialog(self)

    def ver_log(self):
        log_path = os.path.expanduser("~/.local/share/pyIDevicesGUI/app.log")
        try:
            subprocess.run(["xdg-open", log_path])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o log:\n{e}")
    
    def abrir_backup_dir(self):
        backup_dir = config.get_backup_path()
        if not backup_dir or not os.path.isdir(backup_dir):
            messagebox.showwarning("Backup", "Nenhum diretório de backup foi salvo ainda.")
            return
        try:
            subprocess.run(["xdg-open", backup_dir])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta:\n{e}")

    def validar_dispositivo(self):
        if not idevice.is_device_plugged():
            messagebox.showerror("Erro", "Nenhum dispositivo conectado.")
            return
        try:
            resultado = subprocess.run(["idevicepair", "validate"], capture_output=True, text=True)
            if "SUCCESS" in resultado.stdout.upper():
                messagebox.showinfo("Confiança", "✅ O dispositivo confia neste computador.")
            else:
                messagebox.showwarning("Confiança", "⚠️ O dispositivo pode não estar confiando.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao validar confiança:\n{e}")

    def atualizar_log_aba(self, event=None):
        if self.notebook.index("current") == 1:  # aba Log
            log_path = os.path.expanduser("~/.local/share/pyIDevicesGUI/app.log")
            try:
                with open(log_path, "r") as f:
                    conteudo = f.read()
                self.log_text.configure(state="normal")
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, conteudo)
                self.log_text.see(tk.END)
                self.log_text.configure(state="disabled")
            except Exception as e:
                self.log_text.configure(state="normal")
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, f"Erro ao carregar log:\n{e}")
                self.log_text.configure(state="disabled")
    def ver_usb(self):
        sucesso, saida = usbtools.listar_usb()
        if sucesso:
            janela = tk.Toplevel(self)
            janela.title("Dispositivos USB")
            janela.geometry("600x400")
            texto = tk.Text(janela, wrap="word")
            texto.insert(tk.END, saida)
            texto.pack(expand=True, fill="both")
            ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=5)
            texto.configure(state="disabled")
        else:
            messagebox.showerror("Erro", f"Erro ao listar USB:\n\n{saida}")

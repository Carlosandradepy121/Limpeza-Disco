import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import subprocess
from pathlib import Path
from navegadores_cleaner import NavegadoresCleaner  # Importar o módulo de limpeza de navegadores

class LimpezaWindows:
    def __init__(self, root):
        self.root = root
        self.root.title("Limpeza de Arquivos Temporários Windows")
        self.root.geometry("600x650")  # Aumentei a altura para acomodar mais opções
        self.root.minsize(600, 650)    # Tamanho mínimo para garantir visibilidade
        
        # Configuração de estilo
        self.configurar_estilo()
        
        # Frame principal com scroll para acomodar mais opções
        main_container = tk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Adicionar canvas com scrollbar
        canvas = tk.Canvas(main_container)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame principal (agora dentro do scrollable_frame)
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(main_frame, text="Limpeza de Arquivos Temporários", font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=10)
        
        # Descrição
        descricao = ttk.Label(
            main_frame, 
            text="Este programa irá limpar arquivos temporários do Windows para liberar espaço em disco.", 
            wraplength=500,
            font=("Segoe UI", 10)
        )
        descricao.pack(pady=10)
        
        # Opções de limpeza do Windows
        self.opcoes_frame = tk.LabelFrame(main_frame, text="Opções de Limpeza do Windows", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        self.opcoes_frame.pack(fill=tk.X, pady=5)
        
        # Variáveis para as opções do Windows
        self.var_temp = tk.BooleanVar(value=True)
        self.var_prefetch = tk.BooleanVar(value=True)
        self.var_recent = tk.BooleanVar(value=False)
        self.var_downloads = tk.BooleanVar(value=False)
        self.var_windows_update = tk.BooleanVar(value=True)
        
        # Checkboxes para Windows
        tk.Checkbutton(self.opcoes_frame, text="Pasta Temp do Windows", variable=self.var_temp, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.opcoes_frame, text="Pasta Prefetch", variable=self.var_prefetch, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.opcoes_frame, text="Arquivos de Atualização do Windows", variable=self.var_windows_update, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.opcoes_frame, text="Arquivos Recentes", variable=self.var_recent, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.opcoes_frame, text="Pasta Downloads (cuidado!)", variable=self.var_downloads, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        
        # NOVA SEÇÃO: Navegadores
        self.navegadores_frame = tk.LabelFrame(main_frame, text="Limpeza de Navegadores", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        self.navegadores_frame.pack(fill=tk.X, pady=10)
        
        # Variáveis para as opções de navegadores
        self.var_chrome = tk.BooleanVar(value=False)
        self.var_edge = tk.BooleanVar(value=False)
        self.var_firefox = tk.BooleanVar(value=False)
        self.var_opera = tk.BooleanVar(value=False)
        self.var_brave = tk.BooleanVar(value=False)
        
        # Checkboxes para navegadores
        tk.Checkbutton(self.navegadores_frame, text="Google Chrome", variable=self.var_chrome, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.navegadores_frame, text="Microsoft Edge", variable=self.var_edge, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.navegadores_frame, text="Mozilla Firefox", variable=self.var_firefox, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.navegadores_frame, text="Opera", variable=self.var_opera, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.navegadores_frame, text="Brave", variable=self.var_brave, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        
        # Botão para selecionar todos os navegadores
        selecionar_nav_btn = tk.Button(
            self.navegadores_frame,
            text="Selecionar Todos",
            command=self.selecionar_todos_navegadores,
            font=("Segoe UI", 9),
            padx=5,
            pady=2
        )
        selecionar_nav_btn.pack(anchor=tk.W, pady=5)
        
        # Opções de limpeza de aplicativos de desenvolvimento
        self.dev_frame = tk.LabelFrame(main_frame, text="Limpeza de Aplicativos de Desenvolvimento", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        self.dev_frame.pack(fill=tk.X, pady=10)
        
        # Variáveis para as opções de desenvolvimento
        self.var_android_studio = tk.BooleanVar(value=False)
        self.var_python = tk.BooleanVar(value=False)
        self.var_nodejs = tk.BooleanVar(value=False)
        
        # Checkboxes para aplicativos de desenvolvimento
        tk.Checkbutton(self.dev_frame, text="Android Studio (cache, build e temporários)", variable=self.var_android_studio, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.dev_frame, text="Python (__pycache__, .pyc, build, dist)", variable=self.var_python, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        tk.Checkbutton(self.dev_frame, text="Node.js (node_modules, npm-cache)", variable=self.var_nodejs, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=3)
        
        # Barra de progresso - Frame normal
        self.progresso_frame = tk.Frame(main_frame)
        self.progresso_frame.pack(fill=tk.X, pady=10)
        
        self.barra_progresso = ttk.Progressbar(self.progresso_frame, mode="indeterminate")
        self.barra_progresso.pack(fill=tk.X, pady=5)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para iniciar a limpeza")
        self.status_label = tk.Label(self.progresso_frame, textvariable=self.status_var, font=("Segoe UI", 9, "italic"))
        self.status_label.pack(pady=5)
        
        # Botões - Usando Frame e Button padrão do Tk
        self.botoes_frame = tk.Frame(main_frame)
        self.botoes_frame.pack(fill=tk.X, pady=10)
        
        # Rótulo explicativo
        lbl_botoes = tk.Label(self.botoes_frame, text="Escolha uma opção:", font=("Segoe UI", 10, "bold"))
        lbl_botoes.pack(side=tk.LEFT, padx=5)
        
        # Botões - Usando Tk.Button em vez de ttk.Button
        self.sair_btn = tk.Button(
            self.botoes_frame, 
            text="Sair", 
            command=root.destroy,
            font=("Segoe UI", 10),
            padx=10,
            pady=5
        )
        self.sair_btn.pack(side=tk.RIGHT, padx=5)
        
        self.limpar_btn = tk.Button(
            self.botoes_frame, 
            text="Limpeza Avançada", 
            command=self.iniciar_limpeza,
            font=("Segoe UI", 10, "bold"),
            bg="#e1e1e1",
            padx=10,
            pady=5
        )
        self.limpar_btn.pack(side=tk.RIGHT, padx=5)
        
        self.limpeza_rapida_btn = tk.Button(
            self.botoes_frame, 
            text="Limpeza Rápida", 
            command=self.limpeza_rapida,
            font=("Segoe UI", 10),
            padx=10,
            pady=5
        )
        self.limpeza_rapida_btn.pack(side=tk.RIGHT, padx=5)
        
        # Inicializar na tela
        print("Iniciando interface gráfica...")
        self.centralize_window()
        print("Interface carregada.")
    
    def selecionar_todos_navegadores(self):
        """Seleciona ou deseleciona todos os navegadores"""
        # Verifica se todos já estão selecionados
        todos_selecionados = (
            self.var_chrome.get() and 
            self.var_edge.get() and 
            self.var_firefox.get() and 
            self.var_opera.get() and
            self.var_brave.get()
        )
        
        # Inverte a seleção
        valor = not todos_selecionados
        
        # Marca ou desmarca todos
        self.var_chrome.set(valor)
        self.var_edge.set(valor)
        self.var_firefox.set(valor)
        self.var_opera.set(valor)
        self.var_brave.set(valor)
        
    def configurar_estilo(self):
        """Configura o estilo visual da aplicação"""
        # Simplificado para evitar problemas com ttk
        pass
    
    def centralize_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def limpeza_rapida(self):
        """Executa uma limpeza rápida com configurações predefinidas"""
        print("Botão Limpeza Rápida pressionado")
        # Salva as configurações atuais
        temp_original = self.var_temp.get()
        prefetch_original = self.var_prefetch.get()
        recent_original = self.var_recent.get()
        downloads_original = self.var_downloads.get()
        android_studio_original = self.var_android_studio.get()
        python_original = self.var_python.get()
        nodejs_original = self.var_nodejs.get()
        windows_update_original = self.var_windows_update.get()
        chrome_original = self.var_chrome.get()
        edge_original = self.var_edge.get()
        firefox_original = self.var_firefox.get()
        opera_original = self.var_opera.get()
        brave_original = self.var_brave.get()
        
        # Define as configurações para limpeza rápida
        self.var_temp.set(True)
        self.var_prefetch.set(True)
        self.var_recent.set(False)
        self.var_downloads.set(False)
        self.var_android_studio.set(False)
        self.var_python.set(False)
        self.var_nodejs.set(False)
        self.var_windows_update.set(True)
        # Navegadores na limpeza rápida
        self.var_chrome.set(True)     # Chrome é comum
        self.var_edge.set(True)       # Edge é padrão no Windows
        self.var_firefox.set(False)
        self.var_opera.set(False)
        self.var_brave.set(False)
        
        # Executa a limpeza
        self.iniciar_limpeza()
        
        # Restaura as configurações originais após iniciar a limpeza
        self.var_temp.set(temp_original)
        self.var_prefetch.set(prefetch_original)
        self.var_recent.set(recent_original)
        self.var_downloads.set(downloads_original)
        self.var_android_studio.set(android_studio_original)
        self.var_python.set(python_original)
        self.var_nodejs.set(nodejs_original)
        self.var_windows_update.set(windows_update_original)
        self.var_chrome.set(chrome_original)
        self.var_edge.set(edge_original)
        self.var_firefox.set(firefox_original)
        self.var_opera.set(opera_original)
        self.var_brave.set(brave_original)
        
    def iniciar_limpeza(self):
        """Inicia o processo de limpeza em uma thread separada"""
        print("Iniciando processo de limpeza")
        self.limpar_btn.configure(state="disabled")
        self.limpeza_rapida_btn.configure(state="disabled")
        self.barra_progresso.start(10)
        
        # Iniciar thread de limpeza
        threading.Thread(target=self.executar_limpeza, daemon=True).start()
    
    def executar_limpeza(self):
        """Executa a limpeza dos diretórios selecionados"""
        try:
            total_limpo = 0
            
            # Windows Temp
            if self.var_temp.get():
                self.status_var.set("Limpando pasta Temp do Windows...")
                self.root.update_idletasks()
                espaco = self.limpar_diretorio(os.path.join(os.environ['SYSTEMROOT'], 'Temp'))
                espaco += self.limpar_diretorio(os.path.join(os.environ['LOCALAPPDATA'], 'Temp'))
                total_limpo += espaco
            
            # Prefetch
            if self.var_prefetch.get():
                self.status_var.set("Limpando pasta Prefetch...")
                self.root.update_idletasks()
                espaco = self.limpar_diretorio(os.path.join(os.environ['SYSTEMROOT'], 'Prefetch'))
                total_limpo += espaco

            # Windows Update
            if self.var_windows_update.get():
                self.status_var.set("Limpando arquivos de atualização do Windows...")
                self.root.update_idletasks()
                
                # SoftwareDistribution - onde o Windows armazena arquivos de atualização
                windows_update_path = os.path.join(os.environ['SYSTEMROOT'], 'SoftwareDistribution', 'Download')
                espaco = self.limpar_diretorio(windows_update_path)
                
                # Pasta de logs do Windows Update
                windows_update_logs = os.path.join(os.environ['SYSTEMROOT'], 'SoftwareDistribution', 'DataStore', 'Logs')
                espaco += self.limpar_diretorio(windows_update_logs)
                
                # Pasta Delivery Optimization (usado pelo Windows para cache de atualizações)
                delivery_optimization = os.path.join(os.environ['ALLUSERSPROFILE'], 'Microsoft', 'Windows', 'DeliveryOptimization')
                espaco += self.limpar_diretorio(delivery_optimization)
                
                # Componentes antigos do Windows (precisam ser removidos como administrador)
                try:
                    winsxs_temp = os.path.join(os.environ['SYSTEMROOT'], 'WinSxS', 'Temp')
                    espaco += self.limpar_diretorio(winsxs_temp)
                except:
                    print("Não foi possível limpar a pasta WinSxS, requer privilégios de administrador")
                
                total_limpo += espaco
            
            # Limpeza de Navegadores
            # Google Chrome
            if self.var_chrome.get():
                self.status_var.set("Limpando cache do Google Chrome...")
                self.root.update_idletasks()
                espaco = NavegadoresCleaner.limpar_chrome(lambda msg: self.atualizar_status(msg))
                total_limpo += espaco
            
            # Microsoft Edge
            if self.var_edge.get():
                self.status_var.set("Limpando cache do Microsoft Edge...")
                self.root.update_idletasks()
                espaco = NavegadoresCleaner.limpar_edge(lambda msg: self.atualizar_status(msg))
                total_limpo += espaco
            
            # Mozilla Firefox
            if self.var_firefox.get():
                self.status_var.set("Limpando cache do Mozilla Firefox...")
                self.root.update_idletasks()
                espaco = NavegadoresCleaner.limpar_firefox(lambda msg: self.atualizar_status(msg))
                total_limpo += espaco
            
            # Opera
            if self.var_opera.get():
                self.status_var.set("Limpando cache do Opera...")
                self.root.update_idletasks()
                espaco = NavegadoresCleaner.limpar_opera(lambda msg: self.atualizar_status(msg))
                total_limpo += espaco
            
            # Brave
            if self.var_brave.get():
                self.status_var.set("Limpando cache do Brave Browser...")
                self.root.update_idletasks()
                espaco = NavegadoresCleaner.limpar_brave(lambda msg: self.atualizar_status(msg))
                total_limpo += espaco
            
            # Arquivos Recentes
            if self.var_recent.get():
                self.status_var.set("Limpando arquivos recentes...")
                self.root.update_idletasks()
                espaco = self.limpar_diretorio(os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent'))
                total_limpo += espaco
            
            # Downloads
            if self.var_downloads.get():
                self.status_var.set("Limpando pasta Downloads...")
                self.root.update_idletasks()
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                espaco = self.limpar_diretorio(downloads_path)
                total_limpo += espaco
            
            # Android Studio
            if self.var_android_studio.get():
                self.status_var.set("Limpando arquivos temporários do Android Studio...")
                self.root.update_idletasks()
                
                # Pastas do Android Studio a serem limpas
                android_paths = [
                    os.path.join(os.environ['LOCALAPPDATA'], 'Android', 'Sdk', 'temp'),
                    os.path.join(os.environ['USERPROFILE'], '.gradle', 'caches'),
                    os.path.join(os.environ['USERPROFILE'], '.android', 'cache'),
                ]
                
                # Limpar pastas de projeto (build, .gradle)
                espaco = 0
                for caminho in android_paths:
                    if os.path.exists(caminho):
                        espaco += self.limpar_diretorio(caminho)
                
                # Procurar e limpar pastas build e .gradle em projetos Android
                projetos_path = os.path.join(os.environ['USERPROFILE'], 'AndroidStudioProjects')
                if os.path.exists(projetos_path):
                    for root, dirs, files in os.walk(projetos_path):
                        if os.path.basename(root) == 'build' or os.path.basename(root) == '.gradle':
                            espaco += self.limpar_diretorio(root)
                
                total_limpo += espaco
            
            # Python
            if self.var_python.get():
                self.status_var.set("Limpando arquivos temporários do Python...")
                self.root.update_idletasks()
                
                # Limpar cache pip
                pip_cache = os.path.join(os.environ['LOCALAPPDATA'], 'pip', 'cache')
                espaco = 0
                if os.path.exists(pip_cache):
                    espaco += self.limpar_diretorio(pip_cache)
                
                # Procurar e limpar __pycache__, build, dist em projetos Python
                # Começando pela pasta de documentos do usuário
                documentos_path = os.path.join(os.environ['USERPROFILE'], 'Documents')
                espaco += self.limpar_python_files(documentos_path)
                
                # Pasta de projetos comum
                projetos_path = os.path.join(os.environ['USERPROFILE'], 'Projects')
                if os.path.exists(projetos_path):
                    espaco += self.limpar_python_files(projetos_path)
                
                total_limpo += espaco
            
            # Node.js
            if self.var_nodejs.get():
                self.status_var.set("Limpando arquivos temporários do Node.js...")
                self.root.update_idletasks()
                
                # Limpar cache npm
                npm_cache = os.path.join(os.environ['USERPROFILE'], '.npm', '_cacache')
                espaco = 0
                if os.path.exists(npm_cache):
                    espaco += self.limpar_diretorio(npm_cache)
                
                # Limpar node_modules em projetos
                documentos_path = os.path.join(os.environ['USERPROFILE'], 'Documents')
                espaco += self.limpar_node_modules(documentos_path)
                
                # Pasta de projetos comum
                projetos_path = os.path.join(os.environ['USERPROFILE'], 'Projects')
                if os.path.exists(projetos_path):
                    espaco += self.limpar_node_modules(projetos_path)
                
                total_limpo += espaco
            
            # Finalizar
            self.barra_progresso.stop()
            
            # Converter para MB ou GB para exibição
            if total_limpo > 1024 * 1024 * 1024:  # Se for mais de 1GB
                espaco_str = f"{total_limpo / (1024 * 1024 * 1024):.2f} GB"
            else:
                espaco_str = f"{total_limpo / (1024 * 1024):.2f} MB"
                
            messagebox.showinfo(
                "Limpeza Concluída", 
                f"Limpeza concluída com sucesso!\nEspaço liberado: {espaco_str}"
            )
            
            self.status_var.set(f"Limpeza concluída. Espaço liberado: {espaco_str}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a limpeza:\n{str(e)}")
            self.status_var.set("Erro durante a limpeza")
            self.barra_progresso.stop()
            print(f"Erro na limpeza: {e}")
        
        finally:
            self.limpar_btn.configure(state="normal")
            self.limpeza_rapida_btn.configure(state="normal")
    
    def atualizar_status(self, mensagem):
        """Atualiza a mensagem de status e força a interface a atualizar"""
        self.status_var.set(mensagem)
        self.root.update_idletasks()
    
    def limpar_python_files(self, start_path):
        """Limpa arquivos temporários de projetos Python"""
        espaco_total = 0
        try:
            for root, dirs, files in os.walk(start_path):
                # Limpar __pycache__
                if os.path.basename(root) == "__pycache__":
                    espaco_total += self.limpar_diretorio(root)
                
                # Limpar pastas build e dist
                if os.path.basename(root) in ["build", "dist"]:
                    if os.path.exists(os.path.join(os.path.dirname(root), "setup.py")):
                        # Verifica se é um projeto Python
                        espaco_total += self.limpar_diretorio(root)
                
                # Remover arquivos .pyc
                for file in files:
                    if file.endswith(".pyc"):
                        try:
                            filepath = os.path.join(root, file)
                            tamanho = os.path.getsize(filepath)
                            os.unlink(filepath)
                            espaco_total += tamanho
                        except (PermissionError, OSError):
                            pass
        except Exception as e:
            print(f"Erro ao limpar arquivos Python em {start_path}: {e}")
        
        return espaco_total
    
    def limpar_node_modules(self, start_path):
        """Limpa pastas node_modules em projetos Node.js"""
        espaco_total = 0
        try:
            for root, dirs, files in os.walk(start_path):
                # Se encontrar um package.json, verificar se há node_modules
                if "package.json" in files and "node_modules" in dirs:
                    node_modules_path = os.path.join(root, "node_modules")
                    espaco_total += self.limpar_diretorio(node_modules_path)
        except Exception as e:
            print(f"Erro ao limpar node_modules em {start_path}: {e}")
        
        return espaco_total
    
    def limpar_diretorio(self, diretorio):
        """Limpa um diretório e retorna o espaço liberado em bytes"""
        espaco_liberado = 0
        
        try:
            # Verificar se o diretório existe
            if not os.path.exists(diretorio):
                return 0
                
            # Calcular espaço ocupado antes da limpeza
            espaco_antes = self.calcular_tamanho_diretorio(diretorio)
            
            # Excluir arquivos e pastas
            for item in os.listdir(diretorio):
                item_path = os.path.join(diretorio, item)
                try:
                    if os.path.isfile(item_path):
                        # Calcular tamanho do arquivo
                        tamanho = os.path.getsize(item_path)
                        os.unlink(item_path)
                        espaco_liberado += tamanho
                    elif os.path.isdir(item_path):
                        tamanho = self.calcular_tamanho_diretorio(item_path)
                        shutil.rmtree(item_path, ignore_errors=True)
                        espaco_liberado += tamanho
                except (PermissionError, OSError):
                    # Ignorar arquivos que não podem ser excluídos
                    pass
                    
            return espaco_liberado
            
        except Exception as e:
            print(f"Erro ao limpar {diretorio}: {e}")
            return espaco_liberado
    
    def calcular_tamanho_diretorio(self, diretorio):
        """Calcula o tamanho total de um diretório em bytes"""
        tamanho_total = 0
        try:
            for path, dirs, files in os.walk(diretorio):
                for f in files:
                    try:
                        fp = os.path.join(path, f)
                        tamanho_total += os.path.getsize(fp)
                    except (OSError, PermissionError):
                        pass
        except (OSError, PermissionError):
            pass
            
        return tamanho_total

def main():
    print("Iniciando programa de limpeza de arquivos temporários...")
    root = tk.Tk()
    app = LimpezaWindows(root)
    print("Iniciando loop principal...")
    root.mainloop()
    print("Programa encerrado.")

if __name__ == "__main__":
    main() 
import os
import subprocess
import sys

def main():
    # Nome do arquivo a ser compilado
    arquivo_py = "limpeza_windows.py"
    
    # Verifica se o arquivo Python existe
    if not os.path.exists(arquivo_py):
        print(f"ERRO: O arquivo {arquivo_py} não foi encontrado!")
        return
    
    print("Iniciando compilação do programa em arquivo executável...")
    
    # Comando para compilar o programa (criando um único arquivo executável)
    comando = [
        "pyinstaller",
        "--onefile",              # Criar um único arquivo executável
        "--noconsole",            # Não mostrar console ao executar
        "--name", "Limpeza_Windows",  # Nome do executável
        "--icon", "NONE",          # Sem ícone específico
        arquivo_py
    ]
    
    try:
        # Executa o comando PyInstaller
        subprocess.run(comando, check=True)
        
        # Verifica se o executável foi criado
        caminho_exe = os.path.join("dist", "Limpeza_Windows.exe")
        if os.path.exists(caminho_exe):
            print("\nCompilação concluída com sucesso!")
            print(f"O executável foi criado em: {os.path.abspath(caminho_exe)}")
            
            # Copia o executável para o diretório atual para facilitar o acesso
            import shutil
            shutil.copy(caminho_exe, ".")
            print(f"O executável também foi copiado para: {os.path.abspath('Limpeza_Windows.exe')}")
        else:
            print("\nERRO: O executável não foi encontrado após a compilação.")
    
    except Exception as e:
        print(f"\nERRO durante a compilação: {e}")

if __name__ == "__main__":
    main() 
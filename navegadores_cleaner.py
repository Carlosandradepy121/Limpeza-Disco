import os
import shutil
from pathlib import Path

class NavegadoresCleaner:
    """Classe auxiliar para limpar cache de navegadores"""
    
    @staticmethod
    def limpar_chrome(root_update_func=None):
        """Limpa os arquivos de cache do Google Chrome"""
        espaco_liberado = 0
        
        # Pastas de cache do Chrome
        chrome_paths = [
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'GPUCache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Media Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Application Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Service Worker', 'CacheStorage'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Service Worker', 'ScriptCache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Storage', 'ext'),
        ]
        
        # Verificar perfis adicionais (Profile 1, Profile 2, etc.)
        chrome_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
        if os.path.exists(chrome_dir):
            for item in os.listdir(chrome_dir):
                if item.startswith('Profile '):
                    chrome_paths.extend([
                        os.path.join(chrome_dir, item, 'Cache'),
                        os.path.join(chrome_dir, item, 'Code Cache'),
                        os.path.join(chrome_dir, item, 'GPUCache'),
                        os.path.join(chrome_dir, item, 'Media Cache'),
                        os.path.join(chrome_dir, item, 'Application Cache'),
                        os.path.join(chrome_dir, item, 'Service Worker', 'CacheStorage'),
                        os.path.join(chrome_dir, item, 'Service Worker', 'ScriptCache'),
                    ])
        
        # Limpar cada pasta
        for path in chrome_paths:
            if os.path.exists(path):
                if root_update_func:
                    root_update_func(f"Limpando cache do Chrome: {os.path.basename(path)}")
                
                espaco_liberado += NavegadoresCleaner._limpar_diretorio(path)
                
        return espaco_liberado
    
    @staticmethod
    def limpar_edge(root_update_func=None):
        """Limpa os arquivos de cache do Microsoft Edge"""
        espaco_liberado = 0
        
        # Pastas de cache do Edge
        edge_paths = [
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'GPUCache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Media Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Service Worker', 'CacheStorage'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Service Worker', 'ScriptCache'),
        ]
        
        # Verificar perfis adicionais
        edge_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data')
        if os.path.exists(edge_dir):
            for item in os.listdir(edge_dir):
                if item.startswith('Profile '):
                    edge_paths.extend([
                        os.path.join(edge_dir, item, 'Cache'),
                        os.path.join(edge_dir, item, 'Code Cache'),
                        os.path.join(edge_dir, item, 'GPUCache'),
                        os.path.join(edge_dir, item, 'Service Worker', 'CacheStorage'),
                    ])
        
        # Limpar cada pasta
        for path in edge_paths:
            if os.path.exists(path):
                if root_update_func:
                    root_update_func(f"Limpando cache do Edge: {os.path.basename(path)}")
                    
                espaco_liberado += NavegadoresCleaner._limpar_diretorio(path)
                
        return espaco_liberado
    
    @staticmethod
    def limpar_firefox(root_update_func=None):
        """Limpa os arquivos de cache do Mozilla Firefox"""
        espaco_liberado = 0
        
        # Localizar pastas de perfil do Firefox
        firefox_dir = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
        
        if os.path.exists(firefox_dir):
            # Cada perfil tem seu próprio diretório
            for profile_dir in os.listdir(firefox_dir):
                profile_path = os.path.join(firefox_dir, profile_dir)
                
                if os.path.isdir(profile_path):
                    # Pasta de cache dentro do perfil
                    cache_paths = [
                        os.path.join(profile_path, 'cache2'),
                        os.path.join(profile_path, 'thumbnails'),
                        os.path.join(profile_path, 'startupCache'),
                        os.path.join(profile_path, 'shader-cache'),
                    ]
                    
                    for path in cache_paths:
                        if os.path.exists(path):
                            if root_update_func:
                                root_update_func(f"Limpando cache do Firefox: {os.path.basename(path)}")
                                
                            espaco_liberado += NavegadoresCleaner._limpar_diretorio(path)
        
        return espaco_liberado
    
    @staticmethod
    def limpar_opera(root_update_func=None):
        """Limpa os arquivos de cache do Opera"""
        espaco_liberado = 0
        
        # Pastas de cache do Opera
        opera_paths = [
            os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera Stable', 'Cache'),
            os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera Stable', 'GPUCache'),
            os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera Stable', 'System Cache'),
            os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera Stable', 'Code Cache'),
        ]
        
        # Limpar cada pasta
        for path in opera_paths:
            if os.path.exists(path):
                if root_update_func:
                    root_update_func(f"Limpando cache do Opera: {os.path.basename(path)}")
                    
                espaco_liberado += NavegadoresCleaner._limpar_diretorio(path)
                
        return espaco_liberado
    
    @staticmethod
    def limpar_brave(root_update_func=None):
        """Limpa os arquivos de cache do Brave Browser"""
        espaco_liberado = 0
        
        # Pastas de cache do Brave
        brave_paths = [
            os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Code Cache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'GPUCache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Service Worker', 'CacheStorage'),
        ]
        
        # Verificar perfis adicionais
        brave_dir = os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data')
        if os.path.exists(brave_dir):
            for item in os.listdir(brave_dir):
                if item.startswith('Profile '):
                    brave_paths.extend([
                        os.path.join(brave_dir, item, 'Cache'),
                        os.path.join(brave_dir, item, 'Code Cache'),
                        os.path.join(brave_dir, item, 'GPUCache'),
                        os.path.join(brave_dir, item, 'Service Worker', 'CacheStorage'),
                    ])
        
        # Limpar cada pasta
        for path in brave_paths:
            if os.path.exists(path):
                if root_update_func:
                    root_update_func(f"Limpando cache do Brave: {os.path.basename(path)}")
                    
                espaco_liberado += NavegadoresCleaner._limpar_diretorio(path)
                
        return espaco_liberado
    
    @staticmethod
    def limpar_todos_navegadores(root_update_func=None):
        """Limpa o cache de todos os navegadores suportados"""
        espaco_total = 0
        
        # Chrome
        espaco_total += NavegadoresCleaner.limpar_chrome(root_update_func)
        
        # Edge
        espaco_total += NavegadoresCleaner.limpar_edge(root_update_func)
        
        # Firefox
        espaco_total += NavegadoresCleaner.limpar_firefox(root_update_func)
        
        # Opera
        espaco_total += NavegadoresCleaner.limpar_opera(root_update_func)
        
        # Brave
        espaco_total += NavegadoresCleaner.limpar_brave(root_update_func)
        
        return espaco_total
    
    @staticmethod
    def _limpar_diretorio(diretorio):
        """Limpa um diretório e retorna o espaço liberado em bytes"""
        espaco_liberado = 0
        
        try:
            # Verificar se o diretório existe
            if not os.path.exists(diretorio):
                return 0
                
            # Calcular espaço ocupado
            for item in os.listdir(diretorio):
                item_path = os.path.join(diretorio, item)
                try:
                    if os.path.isfile(item_path):
                        # Calcular tamanho do arquivo
                        tamanho = os.path.getsize(item_path)
                        os.unlink(item_path)
                        espaco_liberado += tamanho
                    elif os.path.isdir(item_path):
                        tamanho = NavegadoresCleaner._calcular_tamanho_diretorio(item_path)
                        shutil.rmtree(item_path, ignore_errors=True)
                        espaco_liberado += tamanho
                except (PermissionError, OSError):
                    # Ignorar arquivos que não podem ser excluídos
                    pass
                    
            return espaco_liberado
            
        except Exception as e:
            print(f"Erro ao limpar {diretorio}: {e}")
            return espaco_liberado
    
    @staticmethod
    def _calcular_tamanho_diretorio(diretorio):
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
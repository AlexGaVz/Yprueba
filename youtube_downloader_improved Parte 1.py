import sys
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Agregar debug desde el inicio
print("🚀 Iniciando YouTube Downloader Multi-Account Pro...")
print(f"📁 Directorio actual: {os.getcwd()}")
print(f"🐍 Python version: {sys.version}")

try:
    print("📦 Importando librerías básicas...")
    import tkinter as tk
    from tkinter import messagebox, filedialog, ttk
    print("✅ tkinter importado correctamente")
    
    import customtkinter as ctk
    print("✅ customtkinter importado correctamente")
    
    import threading
    print("✅ threading importado correctamente")
    
    import json
    print("✅ json importado correctamente")
    
    import tempfile
    print("✅ tempfile importado correctamente")
    
    import sqlite3
    print("✅ sqlite3 importado correctamente")
    
    import shutil
    print("✅ shutil importado correctamente")
    
    from pathlib import Path
    print("✅ pathlib importado correctamente")
    
    import re
    print("✅ re importado correctamente")
    
    import urllib.parse
    print("✅ urllib.parse importado correctamente")
    
    from io import BytesIO
    print("✅ BytesIO importado correctamente")
    
    import time
    import datetime
    print("✅ time/datetime importados correctamente")
    
    print("📦 Importando librerías externas...")
    
    try:
        import yt_dlp
        print("✅ yt-dlp importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando yt-dlp: {e}")
        print("💡 Instalando yt-dlp...")
        os.system("pip install yt-dlp")
        import yt_dlp
        print("✅ yt-dlp instalado e importado")
    
    try:
        import requests
        print("✅ requests importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando requests: {e}")
        print("💡 Instalando requests...")
        os.system("pip install requests")
        import requests
        print("✅ requests instalado e importado")
    
    try:
        from PIL import Image, ImageTk
        print("✅ PIL/Pillow importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando PIL: {e}")
        print("💡 Instalando Pillow...")
        os.system("pip install Pillow")
        from PIL import Image, ImageTk
        print("✅ Pillow instalado e importado")
    
    try:
        from cryptography.fernet import Fernet
        print("✅ cryptography importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando cryptography: {e}")
        print("💡 Instalando cryptography...")
        os.system("pip install cryptography")
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        print("✅ cryptography instalado e importado")
    
    print("✅ Todas las librerías importadas correctamente")

except Exception as e:
    print(f"❌ ERROR CRÍTICO en importaciones: {e}")
    import traceback
    traceback.print_exc()
    input("Presiona Enter para continuar...")
    sys.exit(1)

# Minimizar la consola en Windows
try:
    if sys.platform == "win32":
        import ctypes
        import ctypes.wintypes
        
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        
        hwnd = kernel32.GetConsoleWindow()
        if hwnd != 0:
            user32.ShowWindow(hwnd, 6)  # 6 = SW_MINIMIZE
            print("🪟 Consola minimizada")
except Exception as e:
    print(f"⚠️ No se pudo minimizar la consola: {e}")

class CookieManager:
    """🛡️ Gestor seguro de cookies con encriptación"""
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.cookies_dir = os.path.join(base_dir, "cookies")
        self.profiles_file = os.path.join(base_dir, "profiles.json")
        os.makedirs(self.cookies_dir, exist_ok=True)
        
        # Generar clave de encriptación única por usuario
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _get_or_create_key(self):
        """Generar o cargar clave de encriptación"""
        key_file = os.path.join(self.base_dir, ".key")
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                # Generar nueva clave basada en datos únicos del sistema
                password = f"YTDownloader_{os.getlogin()}_{os.getcwd()}".encode()
                salt = b'youtube_downloader_salt_2025'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password))
                
                with open(key_file, 'wb') as f:
                    f.write(key)
                return key
        except Exception as e:
            print(f"⚠️ Error con clave de encriptación: {e}")
            return Fernet.generate_key()
    
    def encrypt_data(self, data):
        """Encriptar datos"""
        try:
            if isinstance(data, str):
                data = data.encode()
            return self.cipher.encrypt(data)
        except Exception as e:
            print(f"❌ Error encriptando: {e}")
            return data
    
    def decrypt_data(self, encrypted_data):
        """Desencriptar datos"""
        try:
            return self.cipher.decrypt(encrypted_data).decode()
        except Exception as e:
            print(f"❌ Error desencriptando: {e}")
            return None
    
    def save_profile(self, profile_name, profile_data):
        """Guardar perfil de cookies encriptado"""
        try:
            profiles = self.load_profiles()
            
            # Encriptar el archivo de cookies
            if profile_data.get('cookies_file') and os.path.exists(profile_data['cookies_file']):
                with open(profile_data['cookies_file'], 'r', encoding='utf-8') as f:
                    cookies_content = f.read()
                
                encrypted_content = self.encrypt_data(cookies_content)
                encrypted_file = os.path.join(self.cookies_dir, f"{profile_name}_encrypted.dat")
                
                with open(encrypted_file, 'wb') as f:
                    f.write(encrypted_content)
                
                profile_data['encrypted_file'] = encrypted_file
                profile_data['created_at'] = datetime.datetime.now().isoformat()
                profile_data['last_validated'] = None
            
            profiles[profile_name] = profile_data
            
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)
                
            print(f"🔐 Perfil '{profile_name}' guardado y encriptado")
            
        except Exception as e:
            print(f"❌ Error guardando perfil: {e}")
    
    def load_profiles(self):
        """Cargar perfiles"""
        try:
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error cargando perfiles: {e}")
        return {}
    
    def get_cookies_file(self, profile_name):
        """Obtener archivo de cookies desencriptado temporal"""
        try:
            profiles = self.load_profiles()
            if profile_name not in profiles:
                return None
                
            profile = profiles[profile_name]
            encrypted_file = profile.get('encrypted_file')
            
            if not encrypted_file or not os.path.exists(encrypted_file):
                return None
            
            # Desencriptar a archivo temporal
            with open(encrypted_file, 'rb') as f:
                encrypted_content = f.read()
            
            cookies_content = self.decrypt_data(encrypted_content)
            if not cookies_content:
                return None
            
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
            temp_file.write(cookies_content)
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Error obteniendo cookies: {e}")
            return None
    
    def validate_cookies(self, profile_name):
        """🔍 Validar si las cookies siguen siendo válidas"""
        try:
            print(f"🔍 Validando cookies del perfil: {profile_name}")
            
            temp_cookies = self.get_cookies_file(profile_name)
            if not temp_cookies:
                return False
            
            # Probar cookies con una petición simple a YouTube
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'cookiefile': temp_cookies,
                'extract_flat': True
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Probar con un video público para verificar que las cookies funcionen
                    info = ydl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)
                    
                    # Si llegamos aquí, las cookies son válidas
                    profiles = self.load_profiles()
                    profiles[profile_name]['last_validated'] = datetime.datetime.now().isoformat()
                    
                    with open(self.profiles_file, 'w', encoding='utf-8') as f:
                        json.dump(profiles, f, indent=2, ensure_ascii=False)
                    
                    os.unlink(temp_cookies)  # Limpiar archivo temporal
                    print(f"✅ Cookies del perfil '{profile_name}' son válidas")
                    return True
                    
            except Exception as e:
                print(f"❌ Cookies del perfil '{profile_name}' no son válidas: {e}")
                os.unlink(temp_cookies)  # Limpiar archivo temporal
                return False
                
        except Exception as e:
            print(f"❌ Error validando cookies: {e}")
            return False
    
    def cleanup_expired(self):
        """🧹 Limpiar cookies expiradas"""
        try:
            profiles = self.load_profiles()
            expired_profiles = []
            
            for profile_name, profile_data in profiles.items():
                if not self.validate_cookies(profile_name):
                    expired_profiles.append(profile_name)
            
            for profile_name in expired_profiles:
                self.delete_profile(profile_name)
                print(f"🗑️ Perfil expirado eliminado: {profile_name}")
                
        except Exception as e:
            print(f"❌ Error limpiando cookies expiradas: {e}")
    
    def delete_profile(self, profile_name):
        """Eliminar perfil"""
        try:
            profiles = self.load_profiles()
            if profile_name in profiles:
                profile = profiles[profile_name]
                
                # Eliminar archivo encriptado
                encrypted_file = profile.get('encrypted_file')
                if encrypted_file and os.path.exists(encrypted_file):
                    os.unlink(encrypted_file)
                
                del profiles[profile_name]
                
                with open(self.profiles_file, 'w', encoding='utf-8') as f:
                    json.dump(profiles, f, indent=2, ensure_ascii=False)
                
                print(f"🗑️ Perfil '{profile_name}' eliminado")
                
        except Exception as e:
            print(f"❌ Error eliminando perfil: {e}")

class ScrollableFrame(ctk.CTkScrollableFrame):
    """Frame scrollable personalizado con scroll más rápido"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self._parent_canvas.yview_scroll(-8, "units")
        elif event.num == 5 or event.delta < 0:
            self._parent_canvas.yview_scroll(8, "units")

class IndependentScrollableFrame(ctk.CTkScrollableFrame):
    """Frame scrollable independiente que NO interfiere con el scroll principal"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self._setup_local_scroll()
        self._has_focus = False
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind_all_children()
    
    def bind_all_children(self):
        """Enlazar eventos de scroll a todos los widgets hijos"""
        def bind_recursive(widget):
            widget.bind("<Enter>", self._on_child_enter)
            widget.bind("<Leave>", self._on_child_leave)
            for child in widget.winfo_children():
                bind_recursive(child)
        
        self.after(100, lambda: bind_recursive(self))
    
    def _setup_local_scroll(self):
        """Configurar scroll SOLO para este frame cuando tiene foco"""
        self.bind("<MouseWheel>", self._on_local_mousewheel)
        self.bind("<Button-4>", self._on_local_mousewheel)
        self.bind("<Button-5>", self._on_local_mousewheel)
    
    def _on_enter(self, event):
        """Cuando el mouse entra en este frame"""
        self._has_focus = True
        self.focus_set()
        return "break"
    
    def _on_leave(self, event):
        """Cuando el mouse sale de este frame"""
        self._has_focus = False
        self.after(50, self._delayed_focus_out)
        return "break"
    
    def _on_child_enter(self, event):
        """Cuando el mouse entra en un hijo de este frame"""
        self._has_focus = True
        return "break"
        
    def _on_child_leave(self, event):
        """Cuando el mouse sale de un hijo de este frame"""
        self.after(10, self._check_if_really_left)
        return "break"
    
    def _check_if_really_left(self):
        """Verificar si el mouse realmente salió del frame completo"""
        try:
            x, y = self.winfo_pointerxy()
            widget = self.winfo_containing(x, y)
            
            if widget is None or not self._is_child_of(widget, self):
                self._has_focus = False
        except:
            self._has_focus = False
    
    def _is_child_of(self, widget, parent):
        """Verificar si un widget es hijo de otro"""
        try:
            current = widget
            while current:
                if current == parent:
                    return True
                current = current.master
            return False
        except:
            return False
    
    def _delayed_focus_out(self):
        """Focus out con delay para evitar parpadeo"""
        if not self._has_focus:
            try:
                self.master.focus_set()
            except:
                pass
    
    def _on_local_mousewheel(self, event):
        """Solo scrollear este frame si tiene foco"""
        if self._has_focus:
            if event.num == 4 or event.delta > 0:
                self._parent_canvas.yview_scroll(-3, "units")
            elif event.num == 5 or event.delta < 0:
                self._parent_canvas.yview_scroll(3, "units")
            return "break"

class YouTubeDownloader:
    def __init__(self):
        print("🎬 Inicializando YouTube Downloader Multi-Account Pro...")
        
        try:
            # Configurar tema
            print("🎨 Configurando tema...")
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            print("✅ Tema configurado")
            
            # Configuración y directorios
            print("⚙️ Configurando archivos...")
            self.config_dir = os.path.join(os.path.expanduser("~"), ".youtube_downloader")
            os.makedirs(self.config_dir, exist_ok=True)
            
            self.config_file = os.path.join(self.config_dir, "config.json")
            self.config = self.load_config()
            
            # Inicializar gestor de cookies
            self.cookie_manager = CookieManager(self.config_dir)
            print("✅ Configuración y gestor de cookies inicializados")
            
            # Obtener resolución de pantalla
            print("🖥️ Detectando resolución de pantalla...")
            temp_root = tk.Tk()
            screen_width = temp_root.winfo_screenwidth()
            screen_height = temp_root.winfo_screenheight()
            temp_root.destroy()
            print(f"✅ Resolución detectada: {screen_width}x{screen_height}")
            
            # Configurar ventana
            print("📐 Configurando ventana...")
            saved_geometry = self.config.get('window_geometry', None)
            if saved_geometry:
                window_width = saved_geometry['width']
                window_height = saved_geometry['height']
                pos_x = saved_geometry['x']
                pos_y = saved_geometry['y']
                print("✅ Usando tamaño guardado")
            else:
                window_width = min(int(screen_width * 0.7), 1200)
                window_height = min(int(screen_width * 0.6), 700)
                pos_x = (screen_width - window_width) // 2
                pos_y = (screen_height - window_height) // 2
                print("✅ Usando tamaño predeterminado")
            
            # Ventana principal
            print("🪟 Creando ventana principal...")
            self.root = ctk.CTk()
            self.root.title("🎬 YouTube Downloader Multi-Account Pro")
            self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
            self.root.minsize(800, 650)
            self.root.resizable(True, True)
            print("✅ Ventana principal creada")
            
            # Variables
            print("📝 Inicializando variables...")
            self.video_info = None
            self.download_path = self.config.get('download_path', os.path.join(os.path.expanduser("~"), "Downloads"))
            self.screen_width = screen_width
            self.screen_height = screen_height
            
            # Variables para perfiles múltiples
            self.current_profile = self.config.get('current_profile', None)
            self.auto_select_profile = self.config.get('auto_select_profile', True)
            
            # Variables para paneles colapsables
            self.accounts_visible = False
            self.folder_visible = False
            self.thumbnail_visible = False
            self.auto_visible = False
            print("✅ Variables inicializadas")
            
            print("🎨 Configurando interfaz...")
            self.setup_ui()
            print("✅ Interfaz configurada")
            
            # Configurar eventos
            print("🔧 Configurando eventos...")
            self.root.bind('<Configure>', self.on_window_resize)
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            print("✅ Eventos configurados")
            
            # Limpiar cookies expiradas en el inicio
            print("🧹 Limpiando cookies expiradas...")
            threading.Thread(target=self.cookie_manager.cleanup_expired, daemon=True).start()
            
            print(f"🖥️ Resolución detectada: {screen_width}x{screen_height}")
            print(f"📱 Ventana configurada: {window_width}x{window_height}")
            print("🎉 ¡Inicialización completada exitosamente!")
            
        except Exception as e:
            print(f"❌ ERROR CRÍTICO en inicialización: {e}")
            import traceback
            traceback.print_exc()
            input("Presiona Enter para continuar...")
            sys.exit(1)
        
    def load_config(self):
        """Cargar configuración desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print("⚙️ Configuración cargada desde archivo")
                    return config
        except Exception as e:
            print(f"⚠️ Error al cargar configuración: {e}")
        print("⚙️ Usando configuración predeterminada")
        return {}
    
    def save_config(self):
        """Guardar configuración incluyendo tamaño de ventana"""
        try:
            geometry = self.root.geometry()
            parts = geometry.split('+')
            size_part = parts[0]
            x = int(parts[1]) if len(parts) > 1 else 0
            y = int(parts[2]) if len(parts) > 2 else 0
            width, height = map(int, size_part.split('x'))
            
            config = {
                'download_path': self.download_path,
                'current_profile': self.current_profile,
                'auto_select_profile': self.auto_select_profile,
                'window_geometry': {
                    'width': width,
                    'height': height,
                    'x': x,
                    'y': y
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"💾 Configuración guardada (Tamaño: {width}x{height})")
            
        except Exception as e:
            print(f"⚠️ Error al guardar configuración: {e}")
    
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        print("👋 Cerrando aplicación...")
        try:
            self.save_config()
            self.root.destroy()
        except Exception as e:
            print(f"⚠️ Error al cerrar: {e}")
        
    def setup_ui(self):
        try:
            print("🎨 Configurando UI - Frame principal...")
            # Frame principal con scroll más rápido
            self.main_frame = ScrollableFrame(
                self.root,
                corner_radius=0,
                fg_color="transparent"
            )
            self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            print("🎨 Configurando UI - Header...")
            # Header
            header_frame = ctk.CTkFrame(self.main_frame)
            header_frame.pack(fill="x", padx=5, pady=(5, 8))
            
            title_label = ctk.CTkLabel(
                header_frame, 
                text="🎬 YouTube Downloader Multi-Account Pro", 
                font=ctk.CTkFont(size=20, weight="bold")
            )
            title_label.pack(pady=15)
            
            print("🎨 Configurando UI - Secciones colapsables...")
            # Secciones colapsables
            self.setup_accounts_section()
            self.setup_folder_section()
            self.setup_thumbnail_section()
            self.setup_auto_download_section()
            
            print("🎨 Configurando UI - URL Input...")
            # URL Input Section
            url_frame = ctk.CTkFrame(self.main_frame)
            url_frame.pack(fill="x", padx=5, pady=8)
            
            url_label = ctk.CTkLabel(
                url_frame, 
                text="📹 URL del Video:", 
                font=ctk.CTkFont(size=14, weight="bold")
            )
            url_label.pack(anchor="w", padx=15, pady=(12, 5))
            
            url_input_frame = ctk.CTkFrame(url_frame)
            url_input_frame.pack(fill="x", padx=15, pady=(0, 12))
            
            self.url_entry = ctk.CTkEntry(
                url_input_frame, 
                placeholder_text="Pega aquí la URL de YouTube...",
                font=ctk.CTkFont(size=12),
                height=35
            )
            self.url_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=8)
            
            self.analyze_btn = ctk.CTkButton(
                url_input_frame,
                text="🔍 Analizar",
                command=self.analyze_video,
                height=35,
                width=100,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            self.analyze_btn.pack(side="right", padx=(5, 10), pady=8)
            
            print("🎨 Configurando UI - Frames adicionales...")
            # Frames para información del video y opciones
            self.info_frame = ctk.CTkFrame(self.main_frame)
            self.progress_frame = ctk.CTkFrame(self.main_frame)
            self.progress_var = tk.StringVar(value="Listo para descargar")
            self.options_frame = ctk.CTkFrame(self.main_frame)
            
            print("✅ UI configurada completamente")
            
        except Exception as e:
            print(f"❌ ERROR en setup_ui: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def setup_accounts_section(self):
        """🎭 Sección de gestión de múltiples cuentas"""
        try:
            accounts_frame = ctk.CTkFrame(self.main_frame)
            accounts_frame.pack(fill="x", padx=5, pady=8)
            
            # Frame para botón principal y selector
            accounts_header = ctk.CTkFrame(accounts_frame)
            accounts_header.pack(fill="x", padx=15, pady=12)
            
            # Frame horizontal para selector y botón
            header_container = ctk.CTkFrame(accounts_header)
            header_container.pack(fill="x", pady=5)
            
            # Selector de perfil activo
            profile_frame = ctk.CTkFrame(header_container)
            profile_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            ctk.CTkLabel(
                profile_frame,
                text="📋 Perfil activo:",
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(side="left", padx=(10, 5))
            
            # Dropdown de perfiles
            self.profile_var = tk.StringVar()
            self.profile_dropdown = ctk.CTkComboBox(
                profile_frame,
                variable=self.profile_var,
                values=self.get_profile_names(),
                command=self.on_profile_changed,
                width=200,
                font=ctk.CTkFont(size=11)
            )
            self.profile_dropdown.pack(side="left", padx=5)
            
            # Botón para mostrar/ocultar opciones
            self.accounts_toggle_btn = ctk.CTkButton(
                header_container,
                text="🎭 Gestión de Cuentas",
                command=self.toggle_accounts_panel,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#2b2b2b",
                hover_color="#404040"
            )
            self.accounts_toggle_btn.pack(side="right", padx=(10, 0))
            
            # Frame colapsable para opciones de cuentas
            self.accounts_options_frame = ctk.CTkFrame(accounts_frame)
            self.setup_accounts_options()
            
            # Actualizar el dropdown con el perfil actual
            self.update_profile_dropdown()
            
        except Exception as e:
            print(f"❌ ERROR en setup_accounts_section: {e}")
            raise

    def setup_accounts_options(self):
        """Configurar las opciones de gestión de cuentas"""
        try:
            # Sección para extraer cookies
            extract_frame = ctk.CTkFrame(self.accounts_options_frame)
            extract_frame.pack(fill="x", padx=15, pady=(15, 10))
            
            extract_title = ctk.CTkLabel(
                extract_frame,
                text="🍪 Extraer Cookies desde Navegador",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            extract_title.pack(pady=(10, 5))
            
            # Frame para nombre del perfil
            name_frame = ctk.CTkFrame(extract_frame)
            name_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                name_frame,
                text="📝 Nombre del perfil:",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(10, 5))
            
            self.profile_name_entry = ctk.CTkEntry(
                name_frame,
                placeholder_text="Ej: YouTube Premium, Canal X Miembro...",
                font=ctk.CTkFont(size=11),
                width=300
            )
            self.profile_name_entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
            
            # Botones para extraer cookies
            buttons_container = ctk.CTkFrame(extract_frame)
            buttons_container.pack(fill="x", padx=10, pady=(5, 10))
            
            buttons_container.grid_columnconfigure(0, weight=1)
            buttons_container.grid_columnconfigure(1, weight=1)
            buttons_container.grid_columnconfigure(2, weight=1)
            
            chrome_btn = ctk.CTkButton(
                buttons_container,
                text="🌐 Chrome",
                command=lambda: self.extract_cookies_from_browser('chrome'),
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
            chrome_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            
            # Botón para Firefox
            firefox_btn = ctk.CTkButton(
                buttons_container,
                text="🦊 Firefox",
                command=lambda: self.extract_cookies_from_browser('firefox'),
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#FF7043",
                hover_color="#FF5722"
            )
            firefox_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            file_btn = ctk.CTkButton(
                buttons_container,
                text="📁 Archivo",
                command=self.load_cookies_from_file,
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#2196F3",
                hover_color="#1976D2"
            )
            file_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
            
            # Sección de gestión de perfiles
            manage_frame = ctk.CTkFrame(self.accounts_options_frame)
            manage_frame.pack(fill="x", padx=15, pady=(10, 15))
            
            manage_title = ctk.CTkLabel(
                manage_frame,
                text="⚙️ Gestión de Perfiles",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            manage_title.pack(pady=(10, 5))
            
            # Botones de gestión
            manage_buttons = ctk.CTkFrame(manage_frame)
            manage_buttons.pack(fill="x", padx=10, pady=(5, 10))
            
            manage_buttons.grid_columnconfigure(0, weight=1)
            manage_buttons.grid_columnconfigure(1, weight=1)
            manage_buttons.grid_columnconfigure(2, weight=1)
            
            validate_btn = ctk.CTkButton(
                manage_buttons,
                text="✅ Validar Actual",
                command=self.validate_current_profile,
                height=35,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#9C27B0",
                hover_color="#7B1FA2"
            )
            validate_btn.grid(row=0, column=0, padx=2, pady=5, sticky="ew")
            
            validate_all_btn = ctk.CTkButton(
                manage_buttons,
                text="🔍 Validar Todos",
                command=self.validate_all_profiles,
                height=35,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#FF9800",
                hover_color="#F57C00"
            )
            validate_all_btn.grid(row=0, column=1, padx=2, pady=5, sticky="ew")
            
            delete_btn = ctk.CTkButton(
                manage_buttons,
                text="🗑️ Eliminar",
                command=self.delete_current_profile,
                height=35,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#f44336",
                hover_color="#d32f2f"
            )
            delete_btn.grid(row=0, column=2, padx=2, pady=5, sticky="ew")
            
            # Checkbox para selección automática
            auto_frame = ctk.CTkFrame(manage_frame)
            auto_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            self.auto_select_var = tk.BooleanVar(value=self.auto_select_profile)
            auto_checkbox = ctk.CTkCheckBox(
                auto_frame,
                text="🧠 Selección inteligente automática de perfil",
                variable=self.auto_select_var,
                command=self.on_auto_select_changed,
                font=ctk.CTkFont(size=11)
            )
            auto_checkbox.pack(padx=10, pady=8)
            
            # Información de ayuda
            help_text = "💡 Chrome: Para YouTube Premium | Firefox: Para membresías de canal | Selección inteligente: Prueba Premium primero"
            help_label = ctk.CTkLabel(
                self.accounts_options_frame,
                text=help_text,
                font=ctk.CTkFont(size=10),
                text_color="gray70",
                wraplength=600
            )
            help_label.pack(pady=(0, 15), padx=15)
            
        except Exception as e:
            print(f"❌ ERROR en setup_accounts_options: {e}")
            raise

    def get_profile_names(self):
        """Obtener lista de nombres de perfiles"""
        try:
            profiles = self.cookie_manager.load_profiles()
            names = list(profiles.keys())
            if not names:
                names = ["Sin perfiles"]
            return names
        except:
            return ["Sin perfiles"]

    def update_profile_dropdown(self):
        """Actualizar el dropdown de perfiles"""
        try:
            names = self.get_profile_names()
            self.profile_dropdown.configure(values=names)
            
            # Seleccionar perfil actual o el primero disponible
            if self.current_profile and self.current_profile in names:
                self.profile_var.set(self.current_profile)
            elif names and names[0] != "Sin perfiles":
                self.profile_var.set(names[0])
                self.current_profile = names[0]
            else:
                self.profile_var.set("Sin perfiles")
                self.current_profile = None
                
        except Exception as e:
            print(f"❌ ERROR actualizando dropdown: {e}")

    def on_profile_changed(self, selected_profile):
        """Manejar cambio de perfil"""
        try:
            if selected_profile != "Sin perfiles":
                self.current_profile = selected_profile
                self.save_config()
                print(f"🔄 Perfil cambiado a: {selected_profile}")
            else:
                self.current_profile = None
        except Exception as e:
            print(f"❌ ERROR cambiando perfil: {e}")

    def on_auto_select_changed(self):
        """Manejar cambio en selección automática"""
        try:
            self.auto_select_profile = self.auto_select_var.get()
            self.save_config()
            print(f"🧠 Selección automática: {'activada' if self.auto_select_profile else 'desactivada'}")
        except Exception as e:
            print(f"❌ ERROR en auto select: {e}")

    def extract_cookies_from_browser(self, browser):
        """Extraer cookies desde Chrome o Firefox"""
        try:
            profile_name = self.profile_name_entry.get().strip()
            if not profile_name:
                messagebox.showerror("Error", "Por favor ingresa un nombre para el perfil")
                return
            
            print(f"🔄 Extrayendo cookies desde {browser.capitalize()}...")
            
            if browser == 'chrome':
                success = self._extract_chrome_cookies(profile_name)
            elif browser == 'firefox':
                success = self._extract_firefox_cookies(profile_name)
            else:
                messagebox.showerror("Error", "Navegador no soportado")
                return
            
            if success:
                self.update_profile_dropdown()
                # También actualizar el dropdown del canal automático si existe
                if hasattr(self, 'channel_profile_dropdown'):
                    self.channel_profile_dropdown.configure(values=self.get_profile_names())
                self.profile_name_entry.delete(0, 'end')
                messagebox.showinfo("Éxito", f"Perfil '{profile_name}' creado correctamente!")
            
        except Exception as e:
            print(f"❌ ERROR extrayendo cookies: {e}")
            messagebox.showerror("Error", f"Error extrayendo cookies: {str(e)}")

    def _extract_chrome_cookies(self, profile_name):
        """Extraer cookies desde Chrome"""
        try:
            # Rutas comunes de Chrome
            possible_paths = [
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"),
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"),
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Cookies"),
            ]
            
            chrome_cookies_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    chrome_cookies_path = path
                    break
            
            if not chrome_cookies_path:
                raise Exception("No se encontró la base de datos de cookies de Chrome")
            
            # Copiar la base de datos
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            shutil.copy2(chrome_cookies_path, temp_db.name)
            
            try:
                conn = sqlite3.connect(temp_db.name)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT name, value, host_key, path, expires_utc, is_secure 
                    FROM cookies 
                    WHERE host_key LIKE '%youtube.com%' OR host_key LIKE '%google.com%'
                """)
                
                cookies = cursor.fetchall()
                
                if cookies:
                    # Crear archivo temporal de cookies
                    temp_cookies_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
                    
                    temp_cookies_file.write("# Netscape HTTP Cookie File\n")
                    for cookie in cookies:
                        name, value, domain, path, expires, secure = cookie
                        line = f"{domain}\t{'TRUE' if domain.startswith('.') else 'FALSE'}\t{path}\t{'TRUE' if secure else 'FALSE'}\t{expires if expires else 0}\t{name}\t{value}\n"
                        temp_cookies_file.write(line)
                    
                    temp_cookies_file.close()
                    
                    # Guardar perfil
                    profile_data = {
                        'type': 'premium',
                        'browser': 'chrome',
                        'cookies_file': temp_cookies_file.name
                    }
                    
                    self.cookie_manager.save_profile(profile_name, profile_data)
                    
                    # Limpiar archivos temporales
                    os.unlink(temp_cookies_file.name)
                    conn.close()
                    os.unlink(temp_db.name)
                    
                    print(f"✅ Cookies de Chrome guardadas para perfil: {profile_name}")
                    return True
                else:
                    raise Exception("No se encontraron cookies de YouTube en Chrome")
                    
            except Exception as e:
                conn.close()
                os.unlink(temp_db.name)
                raise e
                
        except Exception as e:
            print(f"❌ Error extrayendo cookies de Chrome: {e}")
            messagebox.showerror("Error de Chrome", 
                f"No se pudieron extraer las cookies desde Chrome:\n{str(e)}\n\n"
                "Sugerencias:\n"
                "1. Cierra Chrome completamente\n"
                "2. Asegúrate de haber iniciado sesión en YouTube"
            )
            return False

    def _extract_firefox_cookies(self, profile_name):
        """Extraer cookies desde Firefox"""
        try:
            # Buscar perfiles de Firefox
            if sys.platform == "win32":
                firefox_dir = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
            elif sys.platform == "darwin":
                firefox_dir = os.path.expanduser("~/Library/Application Support/Firefox/Profiles")
            else:
                firefox_dir = os.path.expanduser("~/.mozilla/firefox")
            
            if not os.path.exists(firefox_dir):
                raise Exception("No se encontró la carpeta de perfiles de Firefox")
            
            # Buscar archivos cookies.sqlite en los perfiles
            cookies_files = []
            for root, dirs, files in os.walk(firefox_dir):
                for file in files:
                    if file == "cookies.sqlite":
                        cookies_files.append(os.path.join(root, file))
            
            if not cookies_files:
                raise Exception("No se encontraron archivos de cookies de Firefox")
            
            # Usar el archivo de cookies más reciente
            firefox_cookies_path = max(cookies_files, key=os.path.getmtime)
            
            # Copiar la base de datos
            temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_db.close()
            shutil.copy2(firefox_cookies_path, temp_db.name)
            
            try:
                conn = sqlite3.connect(temp_db.name)
                cursor = conn.cursor()
                
                # Firefox tiene una estructura diferente
                cursor.execute("""
                    SELECT name, value, host, path, expiry, isSecure 
                    FROM moz_cookies 
                    WHERE host LIKE '%youtube.com%' OR host LIKE '%google.com%'
                """)
                
                cookies = cursor.fetchall()
                
                if cookies:
                    # Crear archivo temporal de cookies
                    temp_cookies_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
                    
                    temp_cookies_file.write("# Netscape HTTP Cookie File\n")
                    for cookie in cookies:
                        name, value, domain, path, expires, secure = cookie
                        # Ajustar formato de dominio para Firefox
                        if not domain.startswith('.') and not domain.startswith('http'):
                            domain = f".{domain}"
                        line = f"{domain}\t{'TRUE' if domain.startswith('.') else 'FALSE'}\t{path}\t{'TRUE' if secure else 'FALSE'}\t{expires if expires else 0}\t{name}\t{value}\n"
                        temp_cookies_file.write(line)
                    
                    temp_cookies_file.close()
                    
                    # Guardar perfil
                    profile_data = {
                        'type': 'member',
                        'browser': 'firefox',
                        'cookies_file': temp_cookies_file.name
                    }
                    
                    self.cookie_manager.save_profile(profile_name, profile_data)
                    
                    # Limpiar archivos temporales
                    os.unlink(temp_cookies_file.name)
                    conn.close()
                    os.unlink(temp_db.name)
                    
                    print(f"✅ Cookies de Firefox guardadas para perfil: {profile_name}")
                    return True
                else:
                    raise Exception("No se encontraron cookies de YouTube en Firefox")
                    
            except Exception as e:
                conn.close()
                os.unlink(temp_db.name)
                raise e
                
        except Exception as e:
            print(f"❌ Error extrayendo cookies de Firefox: {e}")
            messagebox.showerror("Error de Firefox", 
                f"No se pudieron extraer las cookies desde Firefox:\n{str(e)}\n\n"
                "Sugerencias:\n"
                "1. Cierra Firefox completamente\n"
                "2. Asegúrate de haber iniciado sesión en YouTube\n"
                "3. Verifica que tengas membresías activas"
            )
            return False

    def load_cookies_from_file(self):
        """Cargar cookies desde un archivo"""
        try:
            profile_name = self.profile_name_entry.get().strip()
            if not profile_name:
                messagebox.showerror("Error", "Por favor ingresa un nombre para el perfil")
                return
            
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo de cookies",
                filetypes=[
                    ("Archivos de texto", "*.txt"),
                    ("Archivos JSON", "*.json"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if file_path:
                # Verificar contenido
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'youtube.com' not in content.lower() and 'google.com' not in content.lower():
                    raise Exception("El archivo no parece contener cookies de YouTube")
                
                # Guardar perfil
                profile_data = {
                    'type': 'file',
                    'browser': 'file',
                    'cookies_file': file_path
                }
                
                self.cookie_manager.save_profile(profile_name, profile_data)
                self.update_profile_dropdown()
                if hasattr(self, 'channel_profile_dropdown'):
                    self.channel_profile_dropdown.configure(values=self.get_profile_names())
                self.profile_name_entry.delete(0, 'end')
                
                messagebox.showinfo("Éxito", f"Perfil '{profile_name}' creado desde archivo!")
                
        except Exception as e:
            print(f"❌ ERROR cargando desde archivo: {e}")
            messagebox.showerror("Error", f"Error al cargar cookies: {str(e)}")

    def validate_current_profile(self):
        """Validar el perfil actual"""
        try:
            if not self.current_profile:
                messagebox.showwarning("Advertencia", "No hay perfil seleccionado")
                return
            
            self.progress_var.set("🔍 Validando cookies...")
            
            # Ejecutar validación en hilo separado
            thread = threading.Thread(target=self._validate_profile_thread, args=(self.current_profile,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"❌ ERROR validando perfil: {e}")

    def _validate_profile_thread(self, profile_name):
        """Hilo para validar perfil"""
        try:
            is_valid = self.cookie_manager.validate_cookies(profile_name)
            
            if is_valid:
                self.root.after(0, lambda: self.progress_var.set("✅ Cookies válidas"))
                self.root.after(0, lambda: messagebox.showinfo("Validación", f"Perfil '{profile_name}' es válido"))
            else:
                self.root.after(0, lambda: self.progress_var.set("❌ Cookies no válidas"))
                self.root.after(0, lambda: messagebox.showerror("Validación", f"Perfil '{profile_name}' no es válido o ha expirado"))
                
        except Exception as e:
            error_msg = f"Error validando perfil: {str(e)}"
            self.root.after(0, lambda: self.progress_var.set("❌ Error en validación"))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

    def validate_all_profiles(self):
        """Validar todos los perfiles"""
        try:
            profiles = self.cookie_manager.load_profiles()
            if not profiles:
                messagebox.showinfo("Info", "No hay perfiles para validar")
                return
            
            self.progress_var.set("🔍 Validando todos los perfiles...")
            
            # Ejecutar validación en hilo separado
            thread = threading.Thread(target=self._validate_all_profiles_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"❌ ERROR validando todos los perfiles: {e}")

    def _validate_all_profiles_thread(self):
        """Hilo para validar todos los perfiles"""
        try:
            profiles = self.cookie_manager.load_profiles()
            valid_count = 0
            invalid_profiles = []
            
            for profile_name in profiles.keys():
                is_valid = self.cookie_manager.validate_cookies(profile_name)
                if is_valid:
                    valid_count += 1
                else:
                    invalid_profiles.append(profile_name)
            
            total = len(profiles)
            
            # Mostrar resultados
            message = f"Validación completada:\n\n"
            message += f"✅ Válidos: {valid_count}/{total}\n"
            message += f"❌ Inválidos: {len(invalid_profiles)}/{total}\n"
            
            if invalid_profiles:
                message += f"\nPerfiles inválidos:\n"
                for profile in invalid_profiles:
                    message += f"• {profile}\n"
            
            self.root.after(0, lambda: self.progress_var.set(f"✅ Validación completa: {valid_count}/{total} válidos"))
            self.root.after(0, lambda: messagebox.showinfo("Validación Completa", message))
            
        except Exception as e:
            error_msg = f"Error validando perfiles: {str(e)}"
            self.root.after(0, lambda: self.progress_var.set("❌ Error en validación"))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

    def delete_current_profile(self):
        """Eliminar el perfil actual"""
        try:
            if not self.current_profile:
                messagebox.showwarning("Advertencia", "No hay perfil seleccionado")
                return
            
            # Confirmar eliminación
            response = messagebox.askyesno(
                "Confirmar Eliminación", 
                f"¿Estás seguro de que quieres eliminar el perfil '{self.current_profile}'?\n\nEsta acción no se puede deshacer."
            )
            
            if response:
                self.cookie_manager.delete_profile(self.current_profile)
                self.current_profile = None
                self.update_profile_dropdown()
                if hasattr(self, 'channel_profile_dropdown'):
                    self.channel_profile_dropdown.configure(values=self.get_profile_names())
                messagebox.showinfo("Eliminado", "Perfil eliminado correctamente")
                
        except Exception as e:
            print(f"❌ ERROR eliminando perfil: {e}")
            messagebox.showerror("Error", f"Error eliminando perfil: {str(e)}")

    def setup_folder_section(self):
        """Sección de carpeta colapsable"""
        try:
            folder_frame = ctk.CTkFrame(self.main_frame)
            folder_frame.pack(fill="x", padx=5, pady=8)
            
            folder_header = ctk.CTkFrame(folder_frame)
            folder_header.pack(fill="x", padx=15, pady=12)
            
            current_folder = self.download_path
            if len(current_folder) > 50:
                display_folder = f"...{current_folder[-47:]}"
            else:
                display_folder = current_folder
            
            self.folder_toggle_btn = ctk.CTkButton(
                folder_header,
                text=f"📁 Carpeta: {display_folder}",
                command=self.toggle_folder_panel,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#2b2b2b",
                hover_color="#404040"
            )
            self.folder_toggle_btn.pack(fill="x", pady=5)
            
            self.folder_options_frame = ctk.CTkFrame(folder_frame)
            self.setup_folder_options()
            
        except Exception as e:
            print(f"❌ ERROR en setup_folder_section: {e}")
            raise

    def setup_folder_options(self):
        """Configurar las opciones de carpeta"""
        try:
            path_display = ctk.CTkTextbox(
                self.folder_options_frame,
                height=60,
                font=ctk.CTkFont(size=11)
            )
            path_display.pack(fill="x", padx=15, pady=(15, 10))
            path_display.insert("1.0", self.download_path)
            path_display.configure(state="disabled")
            
            buttons_container = ctk.CTkFrame(self.folder_options_frame)
            buttons_container.pack(fill="x", padx=15, pady=(0, 15))
            
            buttons_container.grid_columnconfigure(0, weight=1)
            buttons_container.grid_columnconfigure(1, weight=1)
            
            change_folder_btn = ctk.CTkButton(
                buttons_container,
                text="📂 Cambiar Carpeta",
                command=self.select_download_path,
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#FF9800",
                hover_color="#F57C00"
            )
            change_folder_btn.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
            
            open_folder_btn = ctk.CTkButton(
                buttons_container,
                text="🗂️ Abrir Carpeta",
                command=self.open_download_folder,
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
            open_folder_btn.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")
            
            self.path_display = path_display
            
        except Exception as e:
            print(f"❌ ERROR en setup_folder_options: {e}")
            raise

    def setup_thumbnail_section(self):
        """Sección de miniatura colapsable"""
        try:
            thumbnail_frame = ctk.CTkFrame(self.main_frame)
            thumbnail_frame.pack(fill="x", padx=5, pady=8)
            
            thumbnail_header = ctk.CTkFrame(thumbnail_frame)
            thumbnail_header.pack(fill="x", padx=15, pady=12)
            
            self.thumbnail_toggle_btn = ctk.CTkButton(
                thumbnail_header,
                text="🖼️ Descargar Miniatura - Solo manual",
                command=self.toggle_thumbnail_panel,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#9C27B0",
                hover_color="#7B1FA2"
            )
            self.thumbnail_toggle_btn.pack(fill="x", pady=5)
            
            self.thumbnail_options_frame = ctk.CTkFrame(thumbnail_frame)
            self.setup_thumbnail_options()
            
        except Exception as e:
            print(f"❌ ERROR en setup_thumbnail_section: {e}")
            raise

    def setup_thumbnail_options(self):
        """Configurar las opciones de miniatura"""
        try:
            info_text = "💡 Descarga la miniatura del video ÚNICAMENTE cuando lo solicites manualmente (no automático)"
            info_label = ctk.CTkLabel(
                self.thumbnail_options_frame,
                text=info_text,
                font=ctk.CTkFont(size=10),
                text_color="gray70",
                wraplength=600
            )
            info_label.pack(pady=(15, 10), padx=15)
            
            buttons_container = ctk.CTkFrame(self.thumbnail_options_frame)
            buttons_container.pack(fill="x", padx=15, pady=(0, 15))
            
            buttons_container.grid_columnconfigure(0, weight=1)
            buttons_container.grid_columnconfigure(1, weight=1)
            buttons_container.grid_columnconfigure(2, weight=1)
            
            small_thumb_btn = ctk.CTkButton(
                buttons_container,
                text="🖼️ Pequeña (320x180)",
                command=lambda: self.download_thumbnail('small'),
                height=35,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#9C27B0",
                hover_color="#7B1FA2"
            )
            small_thumb_btn.grid(row=0, column=0, padx=2, pady=5, sticky="ew")
            
            medium_thumb_btn = ctk.CTkButton(
                buttons_container,
                text="🖼️ Mediana (480x360)",
                command=lambda: self.download_thumbnail('medium'),
                height=35,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#9C27B0",
                hover_color="#7B1FA2"
            )
            medium_thumb_btn.grid(row=0, column=1, padx=2, pady=5, sticky="ew")
            
            large_thumb_btn = ctk.CTkButton(
                buttons_container,
                text="🖼️ Grande (1280x720)",
                command=lambda: self.download_thumbnail('large'),
                height=35,
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#9C27B0",
                hover_color="#7B1FA2"
            )
            large_thumb_btn.grid(row=0, column=2, padx=2, pady=5, sticky="ew")
            
        except Exception as e:
            print(f"❌ ERROR en setup_thumbnail_options: {e}")
            raise

    def setup_auto_download_section(self):
        """🤖 NUEVA: Sección de descarga automática de canales"""
        try:
            auto_frame = ctk.CTkFrame(self.main_frame)
            auto_frame.pack(fill="x", padx=5, pady=8)
            
            # Frame para botón principal
            auto_header = ctk.CTkFrame(auto_frame)
            auto_header.pack(fill="x", padx=15, pady=12)
            
            self.auto_toggle_btn = ctk.CTkButton(
                auto_header,
                text="🤖 Descarga Automática de Canales - Configurar",
                command=self.toggle_auto_panel,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
            self.auto_toggle_btn.pack(fill="x", pady=5)
            
            # Frame colapsable para opciones automáticas
            self.auto_options_frame = ctk.CTkFrame(auto_frame)
            self.setup_auto_options()
            
        except Exception as e:
            print(f"❌ ERROR en setup_auto_download_section: {e}")
            raise


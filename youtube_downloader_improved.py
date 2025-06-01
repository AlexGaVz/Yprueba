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

    def setup_auto_options(self):
        """Configurar las opciones de descarga automática"""
        try:
            # Título
            auto_title = ctk.CTkLabel(
                self.auto_options_frame,
                text="🤖 Configuración de Descarga Automática por Canal",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            auto_title.pack(pady=(15, 10))
            
            # Frame para agregar canal
            add_channel_frame = ctk.CTkFrame(self.auto_options_frame)
            add_channel_frame.pack(fill="x", padx=15, pady=(10, 15))
            
            add_title = ctk.CTkLabel(
                add_channel_frame,
                text="➕ Agregar Nuevo Canal",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            add_title.pack(pady=(10, 5))
            
            # URL del canal
            url_frame = ctk.CTkFrame(add_channel_frame)
            url_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                url_frame,
                text="🔗 URL del canal:",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(10, 5))
            
            self.channel_url_entry = ctk.CTkEntry(
                url_frame,
                placeholder_text="https://www.youtube.com/@nombrecanal o https://www.youtube.com/c/nombrecanal",
                font=ctk.CTkFont(size=10),
                width=400
            )
            self.channel_url_entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
            
            # Carpeta del canal
            folder_frame = ctk.CTkFrame(add_channel_frame)
            folder_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                folder_frame,
                text="📁 Carpeta específica:",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(10, 5))
            
            self.channel_folder_entry = ctk.CTkEntry(
                folder_frame,
                placeholder_text="Carpeta donde se guardarán los videos de este canal",
                font=ctk.CTkFont(size=10),
                width=300
            )
            self.channel_folder_entry.pack(side="left", fill="x", expand=True, padx=(5, 5))
            
            browse_folder_btn = ctk.CTkButton(
                folder_frame,
                text="📂",
                command=self.browse_channel_folder,
                width=40,
                height=28,
                font=ctk.CTkFont(size=10)
            )
            browse_folder_btn.pack(side="right", padx=(5, 10))
            
            # Perfil a usar
            profile_frame = ctk.CTkFrame(add_channel_frame)
            profile_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                profile_frame,
                text="🎭 Perfil a usar:",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(10, 5))
            
            self.channel_profile_var = tk.StringVar()
            self.channel_profile_dropdown = ctk.CTkComboBox(
                profile_frame,
                variable=self.channel_profile_var,
                values=self.get_profile_names(),
                width=200,
                font=ctk.CTkFont(size=10)
            )
            self.channel_profile_dropdown.pack(side="left", padx=(5, 10))
            
            # Botón para agregar canal
            add_btn = ctk.CTkButton(
                add_channel_frame,
                text="➕ Agregar Canal",
                command=self.add_auto_channel,
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
            add_btn.pack(pady=(10, 15))
            
            # Lista de canales configurados
            channels_list_frame = ctk.CTkFrame(self.auto_options_frame)
            channels_list_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            channels_title = ctk.CTkLabel(
                channels_list_frame,
                text="📋 Canales Configurados",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            channels_title.pack(pady=(10, 5))
            
            # Scrollable frame para la lista
            self.channels_scroll_frame = ctk.CTkScrollableFrame(
                channels_list_frame,
                height=150
            )
            self.channels_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
            
            # Cargar canales existentes
            self.load_auto_channels()
            
            # Información de ayuda
            help_text = "💡 Los videos se numerarán automáticamente: '1. Título', '2. Título', etc.\n🖼️ Las miniaturas se numerarán: '1.1 Título', '2.1 Título', etc.\n📁 Carpetas vacías: Descarga TODO el canal desde el más antiguo al más reciente\n📈 Carpetas con contenido: Solo descarga videos nuevos"
            help_label = ctk.CTkLabel(
                self.auto_options_frame,
                text=help_text,
                font=ctk.CTkFont(size=10),
                text_color="gray70",
                wraplength=700
            )
            help_label.pack(pady=(0, 15), padx=15)
            
        except Exception as e:
            print(f"❌ ERROR en setup_auto_options: {e}")
            raise

    def toggle_accounts_panel(self):
        """Mostrar/ocultar el panel de gestión de cuentas"""
        try:
            if self.accounts_visible:
                self.accounts_options_frame.pack_forget()
                self.accounts_visible = False
            else:
                self.accounts_options_frame.pack(fill="x", padx=15, pady=(0, 12))
                self.accounts_visible = True
        except Exception as e:
            print(f"❌ ERROR en toggle_accounts_panel: {e}")

    def toggle_folder_panel(self):
        """Mostrar/ocultar el panel de opciones de carpeta"""
        try:
            if self.folder_visible:
                self.folder_options_frame.pack_forget()
                self.folder_visible = False
            else:
                self.folder_options_frame.pack(fill="x", padx=15, pady=(0, 12))
                self.folder_visible = True
        except Exception as e:
            print(f"❌ ERROR en toggle_folder_panel: {e}")

    def toggle_thumbnail_panel(self):
        """Mostrar/ocultar el panel de opciones de miniatura"""
        try:
            if self.thumbnail_visible:
                self.thumbnail_options_frame.pack_forget()
                self.thumbnail_visible = False
            else:
                self.thumbnail_options_frame.pack(fill="x", padx=15, pady=(0, 12))
                self.thumbnail_visible = True
        except Exception as e:
            print(f"❌ ERROR en toggle_thumbnail_panel: {e}")

    def toggle_auto_panel(self):
        """Mostrar/ocultar el panel de descarga automática"""
        try:
            if self.auto_visible:
                self.auto_options_frame.pack_forget()
                self.auto_visible = False
            else:
                self.auto_options_frame.pack(fill="x", padx=15, pady=(0, 12))
                self.auto_visible = True
        except Exception as e:
            print(f"❌ ERROR en toggle_auto_panel: {e}")

    def browse_channel_folder(self):
        """Explorar carpeta para el canal"""
        try:
            folder = filedialog.askdirectory(title="Seleccionar carpeta para este canal")
            if folder:
                self.channel_folder_entry.delete(0, 'end')
                self.channel_folder_entry.insert(0, folder)
        except Exception as e:
            print(f"❌ ERROR en browse_channel_folder: {e}")

    def add_auto_channel(self):
        """Agregar canal para descarga automática"""
        try:
            channel_url = self.channel_url_entry.get().strip()
            channel_folder = self.channel_folder_entry.get().strip()
            channel_profile = self.channel_profile_var.get()
            
            if not channel_url:
                messagebox.showerror("Error", "Ingresa la URL del canal")
                return
                
            if not channel_folder:
                messagebox.showerror("Error", "Selecciona una carpeta para el canal")
                return
                
            if not channel_profile or channel_profile == "Sin perfiles":
                messagebox.showerror("Error", "Selecciona un perfil válido")
                return
            
            # Crear carpeta si no existe
            os.makedirs(channel_folder, exist_ok=True)
            
            # Guardar configuración del canal con análisis inteligente
            auto_channels = self.load_auto_channels_config()
            
            channel_id = self.extract_channel_id(channel_url)
            if not channel_id:
                messagebox.showerror("Error", "URL de canal no válida")
                return
            
            # MEJORADO: Usar análisis inteligente para contadores iniciales
            existing_videos, existing_thumbnails = self.analyze_existing_files(channel_folder)
            current_video_count = max(existing_videos.keys()) if existing_videos else 0
            current_thumbnail_count = max(existing_thumbnails.keys()) if existing_thumbnails else 0
            
            auto_channels[channel_id] = {
                'url': channel_url,
                'folder': channel_folder,
                'profile': channel_profile,
                'last_video': None,
                'video_count': current_video_count,
                'thumbnail_count': current_thumbnail_count
            }
            
            self.save_auto_channels_config(auto_channels)
            self.refresh_channels_list()
            
            # Limpiar campos
            self.channel_url_entry.delete(0, 'end')
            self.channel_folder_entry.delete(0, 'end')
            
            messagebox.showinfo("Éxito", f"Canal agregado correctamente!\nCarpeta: {channel_folder}")
            
        except Exception as e:
            print(f"❌ ERROR en add_auto_channel: {e}")
            messagebox.showerror("Error", f"Error agregando canal: {str(e)}")

    def extract_channel_id(self, url):
        """Extraer ID del canal de YouTube"""
        try:
            patterns = [
                r'youtube\.com/channel/([^/?]+)',
                r'youtube\.com/c/([^/?]+)',
                r'youtube\.com/@([^/?]+)',
                r'youtube\.com/user/([^/?]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            return None
        except Exception as e:
            print(f"❌ ERROR en extract_channel_id: {e}")
            return None

    def analyze_existing_files(self, folder):
        """🔍 Analizar archivos existentes en la carpeta para evitar duplicados"""
        try:
            if not os.path.exists(folder):
                return {}, {}
            
            files = os.listdir(folder)
            existing_videos = {}  # {numero: titulo_limpio}
            existing_thumbnails = {}  # {numero: titulo_limpio}
            
            for file in files:
                # Analizar videos (formato: "numero. titulo.ext")
                video_match = re.match(r'^(\d+)\.\s*(.+)\.(mp4|webm|mkv|avi|mov)$', file, re.IGNORECASE)
                if video_match:
                    number = int(video_match.group(1))
                    title = video_match.group(2).strip()
                    # Limpiar título para comparación
                    clean_title = self.normalize_title_for_comparison(title)
                    existing_videos[number] = clean_title
                    print(f"📹 Video existente encontrado: {number}. {title}")
                
                # Analizar miniaturas (formato: "numero.1 titulo.jpg")
                thumb_match = re.match(r'^(\d+)\.1\s*(.+)\.jpg$', file, re.IGNORECASE)
                if thumb_match:
                    number = int(thumb_match.group(1))
                    title = thumb_match.group(2).strip()
                    # Limpiar título para comparación
                    clean_title = self.normalize_title_for_comparison(title)
                    existing_thumbnails[number] = clean_title
                    print(f"🖼️ Miniatura existente encontrada: {number}.1 {title}")
            
            print(f"📊 Análisis completo: {len(existing_videos)} videos, {len(existing_thumbnails)} miniaturas")
            return existing_videos, existing_thumbnails
            
        except Exception as e:
            print(f"❌ ERROR en analyze_existing_files: {e}")
            return {}, {}

    def normalize_title_for_comparison(self, title):
        """🧹 Normalizar título para comparación (sin caracteres especiales ni espacios extra)"""
        try:
            # Convertir a minúsculas y quitar espacios extra
            normalized = title.lower().strip()
            
            # Reemplazar caracteres especiales comunes por espacios
            normalized = re.sub(r'[<>"/\\?*|:]+', ' ', normalized)
            
            # Quitar espacios múltiples y convertir a un solo espacio
            normalized = re.sub(r'\s+', ' ', normalized).strip()
            
            return normalized
        except Exception as e:
            print(f"❌ ERROR en normalize_title_for_comparison: {e}")
            return title.lower().strip()

    def check_video_exists(self, video_title, existing_videos):
        """🔍 Verificar si un video ya existe comparando títulos"""
        try:
            clean_new_title = self.normalize_title_for_comparison(video_title)
            
            for number, existing_title in existing_videos.items():
                # Comparación exacta
                if clean_new_title == existing_title:
                    print(f"✅ Video ya existe: {number}. {existing_title}")
                    return True, number
                
                # Comparación de similitud (85% similar)
                similarity = self.calculate_title_similarity(clean_new_title, existing_title)
                if similarity >= 0.85:  # 85% de similitud
                    print(f"✅ Video similar existe ({similarity*100:.1f}%): {number}. {existing_title}")
                    return True, number
            
            return False, None
        except Exception as e:
            print(f"❌ ERROR en check_video_exists: {e}")
            return False, None

    def calculate_title_similarity(self, title1, title2):
        """📊 Calcular similitud entre dos títulos"""
        try:
            # Algoritmo simple de similitud basado en palabras comunes
            words1 = set(title1.split())
            words2 = set(title2.split())
            
            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union)
        except Exception as e:
            print(f"❌ ERROR en calculate_title_similarity: {e}")
            return 0.0

    def get_current_video_count(self, folder):
        """Obtener el número actual de videos en la carpeta"""
        try:
            if not os.path.exists(folder):
                return 0
            
            files = os.listdir(folder)
            video_numbers = []
            
            for file in files:
                # Buscar archivos que empiecen con número seguido de punto
                match = re.match(r'^(\d+)\.', file)
                if match and not re.match(r'^\d+\.\d+', file):  # Excluir miniaturas
                    video_numbers.append(int(match.group(1)))
            
            return max(video_numbers) if video_numbers else 0
        except Exception as e:
            print(f"❌ ERROR en get_current_video_count: {e}")
            return 0

    def get_current_thumbnail_count(self, folder):
        """Obtener el número actual de miniaturas en la carpeta"""
        try:
            if not os.path.exists(folder):
                return 0
            
            files = os.listdir(folder)
            thumbnail_numbers = []
            
            for file in files:
                # Buscar archivos que empiecen con número.número (miniaturas)
                match = re.match(r'^(\d+)\.(\d+)', file)
                if match:
                    thumbnail_numbers.append(int(match.group(1)))
            
            return max(thumbnail_numbers) if thumbnail_numbers else 0
        except Exception as e:
            print(f"❌ ERROR en get_current_thumbnail_count: {e}")
            return 0

    def load_auto_channels_config(self):
        """Cargar configuración de canales automáticos"""
        try:
            auto_config_file = os.path.join(self.config_dir, "auto_channels.json")
            if os.path.exists(auto_config_file):
                with open(auto_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error cargando configuración automática: {e}")
        return {}

    def save_auto_channels_config(self, config):
        """Guardar configuración de canales automáticos"""
        try:
            auto_config_file = os.path.join(self.config_dir, "auto_channels.json")
            with open(auto_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ ERROR guardando configuración automática: {e}")

    def load_auto_channels(self):
        """Cargar y mostrar canales automáticos"""
        try:
            auto_channels = self.load_auto_channels_config()
            self.refresh_channels_list()
        except Exception as e:
            print(f"❌ ERROR en load_auto_channels: {e}")

    def refresh_channels_list(self):
        """Refrescar la lista de canales"""
        try:
            # Limpiar lista actual
            for widget in self.channels_scroll_frame.winfo_children():
                widget.destroy()
            
            auto_channels = self.load_auto_channels_config()
            
            if not auto_channels:
                no_channels_label = ctk.CTkLabel(
                    self.channels_scroll_frame,
                    text="📭 No hay canales configurados",
                    font=ctk.CTkFont(size=11),
                    text_color="gray70"
                )
                no_channels_label.pack(pady=20)
                return
            
            for channel_id, config in auto_channels.items():
                self.create_channel_item(channel_id, config)
                
        except Exception as e:
            print(f"❌ ERROR en refresh_channels_list: {e}")

    def create_channel_item(self, channel_id, config):
        """Crear elemento de canal en la lista"""
        try:
            channel_frame = ctk.CTkFrame(self.channels_scroll_frame)
            channel_frame.pack(fill="x", padx=5, pady=2)
            
            # Información del canal
            info_frame = ctk.CTkFrame(channel_frame)
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # URL acortada
            url_display = config['url']
            if len(url_display) > 50:
                url_display = url_display[:47] + "..."
            
            url_label = ctk.CTkLabel(
                info_frame,
                text=f"🔗 {url_display}",
                font=ctk.CTkFont(size=10, weight="bold")
            )
            url_label.pack(anchor="w")
            
            folder_label = ctk.CTkLabel(
                info_frame,
                text=f"📁 {config['folder']}",
                font=ctk.CTkFont(size=9),
                text_color="gray70"
            )
            folder_label.pack(anchor="w")
            
            stats_text = f"🎭 {config['profile']} | 📹 Videos: {config['video_count']} | 🖼️ Miniaturas: {config['thumbnail_count']}"
            stats_label = ctk.CTkLabel(
                info_frame,
                text=stats_text,
                font=ctk.CTkFont(size=9),
                text_color="gray70"
            )
            stats_label.pack(anchor="w")
            
            # Botones
            buttons_frame = ctk.CTkFrame(channel_frame)
            buttons_frame.pack(side="right", padx=10, pady=8)
            
            check_btn = ctk.CTkButton(
                buttons_frame,
                text="🔍",
                command=lambda cid=channel_id: self.check_channel_updates(cid),
                width=30,
                height=25,
                font=ctk.CTkFont(size=10)
            )
            check_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑️",
                command=lambda cid=channel_id: self.delete_auto_channel(cid),
                width=30,
                height=25,
                font=ctk.CTkFont(size=10),
                fg_color="#f44336",
                hover_color="#d32f2f"
            )
            delete_btn.pack(side="left", padx=2)
            
        except Exception as e:
            print(f"❌ ERROR en create_channel_item: {e}")

    def delete_auto_channel(self, channel_id):
        """Eliminar canal automático"""
        try:
            response = messagebox.askyesno(
                "Confirmar Eliminación", 
                "¿Estás seguro de que quieres eliminar este canal de la descarga automática?"
            )
            
            if response:
                auto_channels = self.load_auto_channels_config()
                if channel_id in auto_channels:
                    del auto_channels[channel_id]
                    self.save_auto_channels_config(auto_channels)
                    self.refresh_channels_list()
                    messagebox.showinfo("Eliminado", "Canal eliminado de la descarga automática")
                    
        except Exception as e:
            print(f"❌ ERROR en delete_auto_channel: {e}")

    def check_channel_updates(self, channel_id):
        """Verificar y descargar nuevos videos del canal"""
        try:
            auto_channels = self.load_auto_channels_config()
            if channel_id not in auto_channels:
                return
            
            config = auto_channels[channel_id]
            
            self.progress_var.set("🔍 Verificando nuevos videos...")
            
            # Ejecutar en hilo separado
            thread = threading.Thread(target=self._check_channel_updates_thread, args=(channel_id, config))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"❌ ERROR en check_channel_updates: {e}")

    def _check_channel_updates_thread(self, channel_id, config):
        """🔍 MEJORADO: Verificar actualizaciones con descarga completa para carpetas vacías"""
        try:
            print(f"🔍 Verificando canal: {config['url']}")
            
            # Analizar archivos existentes ANTES de descargar
            existing_videos, existing_thumbnails = self.analyze_existing_files(config['folder'])
            
            # Verificar si la carpeta está vacía (sin videos)
            is_empty_folder = len(existing_videos) == 0
            
            if is_empty_folder:
                print("📁 Carpeta vacía detectada - Descarga completa desde el más antiguo")
                self.root.after(0, lambda: self.progress_var.set("📁 Carpeta vacía - Preparando descarga completa..."))
            else:
                print(f"📊 Carpeta con contenido - {len(existing_videos)} videos existentes")
                self.root.after(0, lambda: self.progress_var.set("🔍 Verificando videos nuevos..."))
            
            # Obtener cookies del perfil
            temp_cookies = self.cookie_manager.get_cookies_file(config['profile'])
            if not temp_cookies:
                self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudieron obtener cookies del perfil: {config['profile']}"))
                return
            
            # Configurar yt-dlp según si es carpeta vacía o no
            if is_empty_folder:
                # Para carpeta vacía: obtener TODOS los videos del canal
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'cookiefile': temp_cookies,
                    'extract_flat': True,
                    # No limitar cantidad para descarga completa
                }
            else:
                # Para carpeta con contenido: solo los últimos videos
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'cookiefile': temp_cookies,
                    'extract_flat': True,
                    'playlistend': 10,  # Solo últimos 10 para verificar nuevos
                }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Obtener información del canal
                    playlist_info = ydl.extract_info(config['url'], download=False)
                    
                # Limpiar archivo temporal
                os.unlink(temp_cookies)
                
                if 'entries' not in playlist_info:
                    self.root.after(0, lambda: messagebox.showinfo("Info", "No se encontraron videos en el canal"))
                    return
                
                # Filtrar entradas válidas
                valid_entries = [entry for entry in playlist_info['entries'] if entry and entry.get('id') and entry.get('title')]
                
                if not valid_entries:
                    self.root.after(0, lambda: messagebox.showinfo("Info", "No se encontraron videos válidos"))
                    return
                
                if is_empty_folder:
                    # CARPETA VACÍA: Procesar TODOS los videos desde el más antiguo
                    print(f"📥 Carpeta vacía - Procesando {len(valid_entries)} videos desde el más antiguo")
                    
                    # Invertir la lista para empezar por el más antiguo
                    videos_to_process = list(reversed(valid_entries))
                    
                    # Mostrar mensaje de confirmación
                    confirm_message = f"📁 Carpeta vacía detectada!\n\n"
                    confirm_message += f"🎬 Videos encontrados en el canal: {len(videos_to_process)}\n\n"
                    confirm_message += f"¿Descargar TODOS los videos desde el más antiguo hasta el más reciente?\n\n"
                    confirm_message += f"⚠️ Esto puede tomar mucho tiempo dependiendo del tamaño del canal."
                    
                    response = messagebox.askyesno(
                        "Descarga completa del canal", 
                        confirm_message,
                        icon='question'
                    )
                    
                    if not response:
                        self.root.after(0, lambda: self.progress_var.set("❌ Descarga completa cancelada"))
                        return
                    
                    # Procesar todos los videos
                    self._process_complete_channel_download(channel_id, config, videos_to_process)
                    
                else:
                    # CARPETA CON CONTENIDO: Solo verificar videos nuevos
                    new_videos_to_download = []
                    skipped_videos = []
                    
                    # Verificar cada video del canal
                    for entry in valid_entries:
                        video_title = entry.get('title', 'Video sin título')
                        
                        # Verificar si el video ya existe
                        exists, existing_number = self.check_video_exists(video_title, existing_videos)
                        
                        if exists:
                            skipped_videos.append({
                                'title': video_title,
                                'number': existing_number,
                                'id': entry.get('id')
                            })
                            print(f"⏭️ Saltando video existente: {video_title}")
                        else:
                            # Es un video nuevo
                            new_videos_to_download.append(entry)
                            print(f"📥 Video nuevo para descargar: {video_title}")
                    
                    # Mostrar estadísticas para carpeta con contenido
                    self._process_incremental_download(channel_id, config, new_videos_to_download, skipped_videos, existing_videos, existing_thumbnails)
                    
            except Exception as e:
                if os.path.exists(temp_cookies):
                    os.unlink(temp_cookies)
                error_msg = f"Error verificando canal: {str(e)}"
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                
        except Exception as e:
            print(f"❌ ERROR en _check_channel_updates_thread: {e}")

    def _process_complete_channel_download(self, channel_id, config, videos_to_process):
        """📥 NUEVA: Procesar descarga completa del canal desde el más antiguo"""
        try:
            total_videos = len(videos_to_process)
            downloaded_count = 0
            failed_count = 0
            
            print(f"🚀 Iniciando descarga completa: {total_videos} videos")
            
            # Mostrar progreso inicial
            self.root.after(0, lambda: self.progress_var.set(f"📥 Descargando canal completo: 0/{total_videos}"))
            
            for i, video_entry in enumerate(videos_to_process, 1):
                try:
                    video_title = video_entry.get('title', 'Video sin título')
                    print(f"📥 Descargando {i}/{total_videos}: {video_title}")
                    
                    # Actualizar progreso
                    progress_text = f"📥 Descargando {i}/{total_videos}: {video_title[:40]}..."
                    self.root.after(0, lambda pt=progress_text: self.progress_var.set(pt))
                    
                    # Descargar video (sin verificación de duplicados para carpeta vacía)
                    success = self._download_auto_video_complete(channel_id, config, video_entry, i)
                    
                    if success:
                        downloaded_count += 1
                        print(f"✅ {i}/{total_videos} - Descargado: {video_title}")
                    else:
                        failed_count += 1
                        print(f"❌ {i}/{total_videos} - Falló: {video_title}")
                    
                    # Pequeña pausa entre descargas para no sobrecargar
                    time.sleep(1)
                    
                except Exception as e:
                    failed_count += 1
                    print(f"❌ Error descargando video {i}/{total_videos}: {e}")
                    continue
            
            # Actualizar configuración final
            auto_channels = self.load_auto_channels_config()
            if videos_to_process:
                auto_channels[channel_id]['last_video'] = videos_to_process[-1]['id']  # Último video procesado
                auto_channels[channel_id]['video_count'] = downloaded_count
                auto_channels[channel_id]['thumbnail_count'] = downloaded_count
                self.save_auto_channels_config(auto_channels)
            
            # Mensaje final para descarga completa
            final_message = f"🎉 Descarga completa del canal finalizada!\n\n"
            final_message += f"📊 Estadísticas:\n"
            final_message += f"✅ Videos descargados: {downloaded_count}\n"
            final_message += f"❌ Videos fallidos: {failed_count}\n"
            final_message += f"📋 Total procesados: {total_videos}\n\n"
            final_message += f"📁 Ubicación: {config['folder']}"
            
            self.root.after(0, lambda: messagebox.showinfo("Descarga completa finalizada", final_message))
            self.root.after(0, lambda: self.progress_var.set(f"✅ Canal completo descargado: {downloaded_count}/{total_videos}"))
            
            # Refrescar la lista de canales para mostrar nuevos contadores
            self.root.after(0, self.refresh_channels_list)
            
        except Exception as e:
            print(f"❌ ERROR en _process_complete_channel_download: {e}")
            self.root.after(0, lambda: self.progress_var.set("❌ Error en descarga completa"))

    def _process_incremental_download(self, channel_id, config, new_videos_to_download, skipped_videos, existing_videos, existing_thumbnails):
        """📈 NUEVA: Procesar descarga incremental (solo videos nuevos)"""
        try:
            # Mostrar estadísticas
            stats_message = f"📊 Análisis del canal completado:\n\n"
            stats_message += f"🆕 Videos nuevos: {len(new_videos_to_download)}\n"
            stats_message += f"⏭️ Videos existentes (saltados): {len(skipped_videos)}\n"
            
            if not new_videos_to_download:
                stats_message += f"\n✅ Todos los videos ya están descargados"
                self.root.after(0, lambda: messagebox.showinfo("Canal actualizado", stats_message))
                self.root.after(0, lambda: self.progress_var.set("✅ Canal ya está actualizado"))
                return
            
            # Preguntar si descargar videos nuevos
            download_message = stats_message + f"\n¿Descargar los {len(new_videos_to_download)} videos nuevos?"
            response = messagebox.askyesno("Videos nuevos encontrados", download_message)
            
            if not response:
                self.root.after(0, lambda: self.progress_var.set("❌ Descarga cancelada por el usuario"))
                return
            
            # Descargar videos nuevos
            downloaded_count = 0
            for video_entry in new_videos_to_download:
                try:
                    success = self._download_auto_video_smart(channel_id, config, video_entry, existing_videos, existing_thumbnails)
                    if success:
                        downloaded_count += 1
                        # Actualizar listas de existentes para siguiente video
                        existing_videos, existing_thumbnails = self.analyze_existing_files(config['folder'])
                except Exception as e:
                    print(f"❌ Error descargando video {video_entry.get('title', 'Desconocido')}: {e}")
                    continue
            
            # Mensaje final
            final_message = f"✅ Descarga incremental completada!\n\n📥 Videos descargados: {downloaded_count}\n⏭️ Videos saltados: {len(skipped_videos)}"
            self.root.after(0, lambda: messagebox.showinfo("Descarga completada", final_message))
            self.root.after(0, lambda: self.progress_var.set(f"✅ {downloaded_count} videos nuevos descargados"))
            
        except Exception as e:
            print(f"❌ ERROR en _process_incremental_download: {e}")

    def _download_auto_video_complete(self, channel_id, config, video_entry, video_number):
        """📥 NUEVA: Descargar video para descarga completa (sin verificación de duplicados)"""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_entry['id']}"
            video_title = video_entry.get('title', 'Video sin título')
            
            print(f"📥 Descargando video completo #{video_number}: {video_title}")
            
            # Obtener información completa del video
            temp_cookies = self.cookie_manager.get_cookies_file(config['profile'])
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'cookiefile': temp_cookies,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
            
            # Limpiar título manteniendo : y |
            original_title = video_info.get('title', 'Video sin título')
            clean_title = re.sub(r'[<>"/\\?*]', '_', original_title)
            
            # Crear nombres con numeración secuencial
            video_filename = f"{video_number}. {clean_title}"
            thumbnail_filename = f"{video_number}.1 {clean_title}"
            
            # Paths completos
            video_path = os.path.join(config['folder'], f'{video_filename}.mp4')
            thumbnail_path = os.path.join(config['folder'], f'{thumbnail_filename}.jpg')
            
            # Verificar que no existan (por seguridad)
            if os.path.exists(video_path):
                print(f"⚠️ Video ya existe, saltando: {video_path}")
                os.unlink(temp_cookies)
                return False
            
            # Obtener MEJOR CALIDAD automáticamente
            video_formats = self._get_best_video_format(video_info)
            audio_formats = self._get_best_audio_format(video_info)
            
            if video_formats and audio_formats:
                # Usar mejor video + mejor audio
                format_selector = f"{video_formats['format_id']}+{audio_formats['format_id']}"
            elif video_formats:
                # Solo video (mejor calidad)
                format_selector = video_formats['format_id']
            else:
                # Fallback a mejor calidad disponible
                format_selector = 'best'
            
            print(f"🎯 Usando formato: {format_selector}")
            
            # Descargar video con numeración y mejor calidad
            ydl_opts_download = {
                'outtmpl': os.path.join(config['folder'], f'{video_filename}.%(ext)s'),
                'cookiefile': temp_cookies,
                'format': format_selector,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([video_url])
            
            # Descargar miniatura automáticamente
            if not os.path.exists(thumbnail_path):
                print(f"🖼️ Descargando miniatura: {thumbnail_filename}")
                self._download_auto_thumbnail_complete(video_info, config['folder'], thumbnail_filename)
            
            # Limpiar cookies temporales
            os.unlink(temp_cookies)
            
            print(f"✅ Video completo descargado: {video_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando video completo: {e}")
            # Limpiar cookies si hay error
            try:
                if 'temp_cookies' in locals() and os.path.exists(temp_cookies):
                    os.unlink(temp_cookies)
            except:
                pass
            return False

    def _download_auto_video_smart(self, channel_id, config, video_entry, existing_videos, existing_thumbnails):
        """🧠 NUEVA: Descargar video automáticamente con verificación inteligente de duplicados"""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_entry['id']}"
            video_title = video_entry.get('title', 'Video sin título')
            
            print(f"📥 Iniciando descarga inteligente: {video_title}")
            
            # Verificar nuevamente si existe (por si acaso)
            exists, existing_number = self.check_video_exists(video_title, existing_videos)
            if exists:
                print(f"⏭️ Video ya existe, saltando: {video_title}")
                return False
            
            # Actualizar contadores basándose en archivos reales
            auto_channels = self.load_auto_channels_config()
            
            # Recalcular contadores basándose en archivos existentes
            current_video_count = max(existing_videos.keys()) if existing_videos else 0
            current_thumbnail_count = max(existing_thumbnails.keys()) if existing_thumbnails else 0
            
            # Asignar siguiente número
            video_number = current_video_count + 1
            thumbnail_number = current_thumbnail_count + 1
            
            print(f"🔢 Asignando número: Video {video_number}, Miniatura {thumbnail_number}")
            
            # Obtener información completa del video
            temp_cookies = self.cookie_manager.get_cookies_file(config['profile'])
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'cookiefile': temp_cookies,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
            
            # Limpiar título manteniendo : y |
            original_title = video_info.get('title', 'Video sin título')
            clean_title = re.sub(r'[<>"/\\?*]', '_', original_title)
            
            # Crear nombres con numeración
            video_filename = f"{video_number}. {clean_title}"
            thumbnail_filename = f"{thumbnail_number}.1 {clean_title}"
            
            # Verificar que los archivos no existan ya (doble verificación)
            video_path = os.path.join(config['folder'], f'{video_filename}.mp4')
            thumbnail_path = os.path.join(config['folder'], f'{thumbnail_filename}.jpg')
            
            # Si por alguna razón ya existen, saltarlos
            if os.path.exists(video_path):
                print(f"⚠️ Archivo de video ya existe: {video_path}")
                os.unlink(temp_cookies)
                return False
                
            if os.path.exists(thumbnail_path):
                print(f"⚠️ Archivo de miniatura ya existe: {thumbnail_path}")
                # Continuar con video pero saltar miniatura
            
            # Descargar video con numeración y MEJOR CALIDAD
            self.root.after(0, lambda: self.progress_var.set(f"📥 Descargando: {video_number}. {clean_title[:50]}..."))
            
            # Obtener MEJOR CALIDAD automáticamente
            video_formats = self._get_best_video_format(video_info)
            audio_formats = self._get_best_audio_format(video_info)
            
            if video_formats and audio_formats:
                # Usar mejor video + mejor audio
                format_selector = f"{video_formats['format_id']}+{audio_formats['format_id']}"
            elif video_formats:
                # Solo video (mejor calidad)
                format_selector = video_formats['format_id']
            else:
                # Fallback a mejor calidad disponible
                format_selector = 'best'
            
            print(f"🎯 Usando formato: {format_selector}")
            
            ydl_opts_download = {
                'outtmpl': os.path.join(config['folder'], f'{video_filename}.%(ext)s'),
                'cookiefile': temp_cookies,
                'format': format_selector,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([video_url])
            
            # Descargar miniatura SOLO si no existe
            if not os.path.exists(thumbnail_path):
                print(f"🖼️ Descargando miniatura: {thumbnail_number}.1 {clean_title}")
                self.root.after(0, lambda: self.progress_var.set(f"🖼️ Descargando miniatura: {thumbnail_number}.1"))
                self._download_auto_thumbnail_smart(video_info, config['folder'], thumbnail_filename)
            else:
                print(f"⏭️ Miniatura ya existe: {thumbnail_path}")
            
            # Actualizar configuración con los nuevos contadores
            auto_channels[channel_id]['last_video'] = video_entry['id']
            auto_channels[channel_id]['video_count'] = video_number
            auto_channels[channel_id]['thumbnail_count'] = thumbnail_number
            self.save_auto_channels_config(auto_channels)
            
            # Limpiar cookies temporales
            os.unlink(temp_cookies)
            
            print(f"✅ Descargado exitosamente: {video_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando video automático inteligente: {e}")
            # Limpiar cookies si hay error
            try:
                if 'temp_cookies' in locals() and os.path.exists(temp_cookies):
                    os.unlink(temp_cookies)
            except:
                pass
            return False

    def _get_best_video_format(self, video_info):
        """🎯 NUEVA: Obtener el mejor formato de video automáticamente"""
        try:
            if not video_info or 'formats' not in video_info:
                return None
            
            video_formats = []
            
            for fmt in video_info['formats']:
                has_video = (
                    fmt.get('vcodec') and 
                    fmt.get('vcodec') != 'none' and 
                    fmt.get('vcodec') != 'null'
                ) or (
                    fmt.get('height') or 
                    fmt.get('width') or
                    'video' in str(fmt.get('format_note', '')).lower()
                )
                
                if has_video:
                    format_note = str(fmt.get('format_note', '')).lower()
                    is_premium = 'premium' in format_note
                    height = fmt.get('height', 0)
                    fps = fmt.get('fps', 0)
                    
                    video_formats.append({
                        'format_id': fmt.get('format_id'),
                        'height': height,
                        'fps': fps,
                        'is_premium': is_premium,
                        'quality_score': (10000 if is_premium else 0) + height + (fps * 10)
                    })
            
            if not video_formats:
                return None
            
            # Ordenar por calidad (Premium + resolución + fps)
            video_formats.sort(key=lambda x: x['quality_score'], reverse=True)
            
            best_format = video_formats[0]
            print(f"🎯 Mejor video: {best_format['format_id']} ({best_format['height']}p, {best_format['fps']}fps{', Premium' if best_format['is_premium'] else ''})")
            
            return best_format
            
        except Exception as e:
            print(f"❌ Error obteniendo mejor formato de video: {e}")
            return None

    def _get_best_audio_format(self, video_info):
        """🎯 NUEVA: Obtener el mejor formato de audio automáticamente"""
        try:
            if not video_info or 'formats' not in video_info:
                return None
            
            audio_formats = []
            
            for fmt in video_info['formats']:
                has_audio = (
                    fmt.get('acodec') and 
                    fmt.get('acodec') != 'none' and 
                    fmt.get('acodec') != 'null'
                ) or (
                    fmt.get('abr') or
                    'audio' in str(fmt.get('format_note', '')).lower()
                )
                
                if has_audio:
                    abr = fmt.get('abr', 0)
                    
                    audio_formats.append({
                        'format_id': fmt.get('format_id'),
                        'abr': abr,
                        'quality_score': abr
                    })
            
            if not audio_formats:
                return None
            
            # Ordenar por bitrate (mayor = mejor)
            audio_formats.sort(key=lambda x: x['quality_score'], reverse=True)
            
            best_format = audio_formats[0]
            print(f"🎯 Mejor audio: {best_format['format_id']} ({best_format['abr']}kbps)")
            
            return best_format
            
        except Exception as e:
            print(f"❌ Error obteniendo mejor formato de audio: {e}")
            return None

    def _download_auto_thumbnail_smart(self, video_info, folder, filename):
        """🖼️ MEJORADA: Descargar miniatura automática con verificación de existencia"""
        try:
            # Verificar si ya existe
            filepath = os.path.join(folder, f"{filename}.jpg")
            if os.path.exists(filepath):
                print(f"⏭️ Miniatura ya existe: {filepath}")
                return
            
            video_url = video_info.get('webpage_url', '')
            video_id = self.extract_video_id(video_url)
            
            if not video_id:
                print("❌ No se pudo extraer ID del video para miniatura")
                return
            
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            img_response = requests.get(thumbnail_url, headers=headers, timeout=30)
            img_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Miniatura automática guardada: {filepath}")
            
        except Exception as e:
            print(f"❌ Error descargando miniatura automática: {e}")

    def _download_auto_thumbnail_complete(self, video_info, folder, filename):
        """🖼️ NUEVA: Descargar miniatura para descarga completa"""
        try:
            video_url = video_info.get('webpage_url', '')
            video_id = self.extract_video_id(video_url)
            
            if not video_id:
                print("❌ No se pudo extraer ID del video para miniatura")
                return
            
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            img_response = requests.get(thumbnail_url, headers=headers, timeout=30)
            img_response.raise_for_status()
            
            filepath = os.path.join(folder, f"{filename}.jpg")
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Miniatura completa guardada: {filepath}")
            
        except Exception as e:
            print(f"❌ Error descargando miniatura completa: {e}")

    def update_folder_button(self):
        """Actualizar el texto del botón de carpeta"""
        try:
            current_folder = self.download_path
            if len(current_folder) > 50:
                display_folder = f"...{current_folder[-47:]}"
            else:
                display_folder = current_folder
                
            self.folder_toggle_btn.configure(text=f"📁 Carpeta: {display_folder}")
            
            if hasattr(self, 'path_display'):
                self.path_display.configure(state="normal")
                self.path_display.delete("1.0", "end")
                self.path_display.insert("1.0", self.download_path)
                self.path_display.configure(state="disabled")
        except Exception as e:
            print(f"❌ ERROR en update_folder_button: {e}")

    def extract_video_id(self, url):
        """Extraer ID del video de YouTube de la URL"""
        try:
            patterns = [
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
                r'youtube\.com/watch\?.*?v=([^&\n?#]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            return None
        except Exception as e:
            print(f"❌ ERROR en extract_video_id: {e}")
            return None

    # ===== FUNCIONES PRINCIPALES CON SELECCIÓN INTELIGENTE =====

    def analyze_video(self):
        """🧠 Analizar video con selección inteligente de perfil"""
        try:
            print("🔍 Analizando video con selección inteligente...")
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Por favor ingresa una URL válida")
                return
                
            self.analyze_btn.configure(state="disabled", text="Analizando...")
            
            # Limpiar secciones anteriores
            self.clear_previous_analysis()
            
            # Ejecutar en hilo separado
            thread = threading.Thread(target=self._analyze_video_thread, args=(url,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"❌ ERROR en analyze_video: {e}")
            messagebox.showerror("Error", f"Error al analizar video: {str(e)}")
            self.analyze_btn.configure(state="normal", text="🔍 Analizar")
        
    def clear_previous_analysis(self):
        """Limpiar análisis anterior"""
        try:
            for widget in self.info_frame.winfo_children():
                widget.destroy()
            for widget in self.options_frame.winfo_children():
                widget.destroy()
            for widget in self.progress_frame.winfo_children():
                widget.destroy()
                
            self.info_frame.pack_forget()
            self.options_frame.pack_forget()
            self.progress_frame.pack_forget()
        except Exception as e:
            print(f"❌ ERROR en clear_previous_analysis: {e}")
            
    def _analyze_video_thread(self, url):
        """🧠 Hilo para analizar video con selección inteligente"""
        try:
            print(f"🔍 Analizando URL: {url}")
            
            if self.auto_select_profile:
                print("🧠 Modo selección inteligente activado")
                success = self._smart_profile_selection(url)
                if not success:
                    self.root.after(0, lambda: self._show_error("No se pudo acceder al video con ningún perfil disponible"))
                    return
            else:
                print("👤 Usando perfil manual seleccionado")
                success = self._analyze_with_profile(url, self.current_profile)
                if not success:
                    self.root.after(0, lambda: self._show_error("Error al analizar video con el perfil actual"))
                    return
            
            # Actualizar UI en el hilo principal
            self.root.after(0, self._update_video_info)
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error en análisis: {error_msg}")
            self.root.after(0, lambda: self._show_error(f"Error al analizar el video: {error_msg}"))

    def _smart_profile_selection(self, url):
        """🧠 Selección inteligente de perfil: Premium primero, luego membresías"""
        try:
            profiles = self.cookie_manager.load_profiles()
            if not profiles:
                print("❌ No hay perfiles disponibles")
                return False
            
            # Separar perfiles por tipo
            premium_profiles = []
            member_profiles = []
            other_profiles = []
            
            for name, data in profiles.items():
                profile_type = data.get('type', 'other')
                if profile_type == 'premium':
                    premium_profiles.append(name)
                elif profile_type == 'member':
                    member_profiles.append(name)
                else:
                    other_profiles.append(name)
            
            # Orden de prioridad: Premium -> Miembros -> Otros
            profile_order = premium_profiles + member_profiles + other_profiles
            
            print(f"🎯 Orden de prueba: {profile_order}")
            
            for profile_name in profile_order:
                print(f"🔄 Probando con perfil: {profile_name}")
                
                try:
                    success = self._analyze_with_profile(url, profile_name)
                    if success:
                        print(f"✅ Éxito con perfil: {profile_name}")
                        self.current_profile = profile_name
                        
                        # Actualizar UI
                        self.root.after(0, lambda p=profile_name: self.profile_var.set(p))
                        self.root.after(0, self.save_config)
                        
                        return True
                    else:
                        print(f"❌ Falló con perfil: {profile_name}")
                        
                except Exception as e:
                    print(f"⚠️ Error con perfil {profile_name}: {e}")
                    continue
            
            print("❌ Ningún perfil funcionó")
            return False
            
        except Exception as e:
            print(f"❌ Error en selección inteligente: {e}")
            return False

    def _analyze_with_profile(self, url, profile_name):
        """Analizar video con un perfil específico"""
        try:
            if not profile_name:
                print("⚠️ Sin perfil para usar")
                return False
            
            # Obtener cookies del perfil
            temp_cookies = self.cookie_manager.get_cookies_file(profile_name)
            if not temp_cookies:
                print(f"❌ No se pudieron obtener cookies para: {profile_name}")
                return False
            
            # Configurar yt-dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'cookiefile': temp_cookies,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    self.video_info = ydl.extract_info(url, download=False)
                
                # Limpiar archivo temporal
                os.unlink(temp_cookies)
                
                print(f"✅ Video analizado con perfil '{profile_name}': {self.video_info.get('title', 'Sin título')}")
                
                # DEBUG: Información de formatos
                if self.video_info and 'formats' in self.video_info:
                    print(f"🔍 Total de formatos encontrados: {len(self.video_info['formats'])}")
                    
                    premium_count = 0
                    for fmt in self.video_info['formats']:
                        format_note = str(fmt.get('format_note', '')).lower()
                        if 'premium' in format_note:
                            premium_count += 1
                    
                    print(f"👑 Formatos Premium encontrados: {premium_count}")
                
                return True
                
            except Exception as e:
                # Limpiar archivo temporal en caso de error
                if os.path.exists(temp_cookies):
                    os.unlink(temp_cookies)
                
                error_str = str(e).lower()
                if any(keyword in error_str for keyword in ['private', 'unavailable', 'members only', 'sign in']):
                    print(f"🔒 Video requiere acceso especial (perfil: {profile_name})")
                    return False
                else:
                    print(f"❌ Error técnico con perfil {profile_name}: {e}")
                    return False
                
        except Exception as e:
            print(f"❌ Error analizando con perfil {profile_name}: {e}")
            return False
            
    def _update_video_info(self):
        """Actualizar información del video en la UI"""
        try:
            self.analyze_btn.configure(state="normal", text="🔍 Analizar")
            
            if not self.video_info:
                return
                
            print("🎨 Actualizando información del video en UI...")
                
            self.info_frame.pack(fill="x", padx=5, pady=8)
            
            # Título del video con indicador de perfil usado
            title_text = f"📹 {self.video_info.get('title', 'Sin título')}"
            if self.current_profile:
                profiles = self.cookie_manager.load_profiles()
                profile_type = profiles.get(self.current_profile, {}).get('type', 'unknown')
                if profile_type == 'premium':
                    title_text += " 👑"
                elif profile_type == 'member':
                    title_text += " 💎"
                else:
                    title_text += " 🔓"
            
            title_label = ctk.CTkLabel(
                self.info_frame,
                text=title_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                wraplength=self.screen_width - 100
            )
            title_label.pack(pady=(15, 5), padx=15)
            
            # Mostrar perfil usado
            if self.current_profile:
                profile_label = ctk.CTkLabel(
                    self.info_frame,
                    text=f"🎭 Accedido con: {self.current_profile}",
                    font=ctk.CTkFont(size=10),
                    text_color="gray70"
                )
                profile_label.pack(pady=(0, 10), padx=15)
            
            # Info adicional
            info_text = f"👤 {self.video_info.get('uploader', 'Desconocido')} | "
            info_text += f"⏱️ {self._format_duration(self.video_info.get('duration', 0))} | "
            info_text += f"👀 {self.video_info.get('view_count', 0):,} vistas"
            
            info_label = ctk.CTkLabel(
                self.info_frame,
                text=info_text,
                font=ctk.CTkFont(size=11),
                text_color="gray70"
            )
            info_label.pack(pady=(0, 15), padx=15)
            
            self._show_quality_options()
            
        except Exception as e:
            print(f"❌ ERROR en _update_video_info: {e}")
            import traceback
            traceback.print_exc()
            
    def _show_quality_options(self):
        """Mostrar opciones de calidad"""
        try:
            print("🎯 Mostrando opciones de calidad...")
            
            self.options_frame.pack(fill="x", padx=5, pady=8)
            
            options_title_text = "🎯 Opciones de Descarga"
            if self.current_profile:
                profiles = self.cookie_manager.load_profiles()
                profile_type = profiles.get(self.current_profile, {}).get('type', 'unknown')
                if profile_type == 'premium':
                    options_title_text += " (Premium 👑)"
                elif profile_type == 'member':
                    options_title_text += " (Miembro 💎)"
            
            options_title = ctk.CTkLabel(
                self.options_frame,
                text=options_title_text,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            options_title.pack(pady=(15, 10))
            
            # Obtener formatos
            try:
                print("🔍 Obteniendo formatos de video...")
                video_formats = self._get_video_formats()
                print(f"✅ Formatos de video obtenidos: {len(video_formats)}")
                
                print("🔍 Obteniendo formatos de audio...")
                audio_formats = self._get_audio_formats()
                print(f"✅ Formatos de audio obtenidos: {len(audio_formats)}")
                
            except Exception as e:
                print(f"❌ Error obteniendo formatos: {e}")
                video_formats = []
                audio_formats = []
            
            # Estadísticas
            stats_label = ctk.CTkLabel(
                self.options_frame,
                text=f"📊 {len(video_formats)} video | {len(audio_formats)} audio",
                font=ctk.CTkFont(size=10),
                text_color="gray70"
            )
            stats_label.pack(pady=(0, 10))
            
            # Variables para selección
            self.selected_video = tk.StringVar()
            self.selected_audio = tk.StringVar()
            
            if not video_formats and not audio_formats:
                error_label = ctk.CTkLabel(
                    self.options_frame,
                    text="❌ No se encontraron formatos disponibles",
                    font=ctk.CTkFont(size=12),
                    text_color="#ff6b6b"
                )
                error_label.pack(pady=15)
                return
            
            # Frame para las dos columnas
            columns_container = ctk.CTkFrame(self.options_frame)
            columns_container.pack(fill="x", padx=15, pady=10)
            
            # Columna Video
            video_column = ctk.CTkFrame(columns_container)
            video_column.pack(side="left", fill="both", expand=True, padx=(0, 8))
            
            video_title = ctk.CTkLabel(
                video_column,
                text=f"🎬 Video ({len(video_formats)})",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            video_title.pack(pady=(12, 8))
            
            video_scroll_frame = IndependentScrollableFrame(
                video_column, 
                height=200,
            )
            video_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 12))
            
            # Columna Audio
            audio_column = ctk.CTkFrame(columns_container)
            audio_column.pack(side="right", fill="both", expand=True, padx=(8, 0))
            
            audio_title = ctk.CTkLabel(
                audio_column,
                text=f"🎵 Audio ({len(audio_formats)})",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            audio_title.pack(pady=(12, 8))
            
            audio_scroll_frame = IndependentScrollableFrame(
                audio_column, 
                height=200,
            )
            audio_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 12))
            
            # Mostrar opciones de video
            if video_formats:
                print(f"🎬 Mostrando {len(video_formats)} formatos de video disponibles")
                for i, fmt in enumerate(video_formats):
                    try:
                        quality_text = f"ID:{fmt['format_id']} | {fmt['resolution']} ({fmt['ext']})"
                        
                        if fmt.get('fps'):
                            quality_text += f" | {fmt['fps']}fps"
                        
                        quality_text += f" | {fmt['filesize_mb']}"
                        
                        if fmt.get('is_premium', False):
                            quality_text += " | 👑 PREMIUM"
                            
                        radio = ctk.CTkRadioButton(
                            video_scroll_frame,
                            text=quality_text,
                            variable=self.selected_video,
                            value=fmt['format_id'],
                            font=ctk.CTkFont(size=9)
                        )
                        radio.pack(anchor="w", padx=8, pady=1, fill="x")
                        
                        if i == 0:
                            self.selected_video.set(fmt['format_id'])
                            
                    except Exception as e:
                        print(f"Error creando radio button para video {i}: {e}")
                        continue
            
            # Mostrar opciones de audio
            if audio_formats:
                print(f"🎵 Mostrando {len(audio_formats)} formatos de audio disponibles")
                for i, fmt in enumerate(audio_formats):
                    try:
                        quality_text = f"ID:{fmt['format_id']} | {fmt['quality_info']} ({fmt['ext']}) | {fmt['filesize_mb']}"
                            
                        radio = ctk.CTkRadioButton(
                            audio_scroll_frame,
                            text=quality_text,
                            variable=self.selected_audio,
                            value=fmt['format_id'],
                            font=ctk.CTkFont(size=9)
                        )
                        radio.pack(anchor="w", padx=8, pady=1, fill="x")
                        
                        if i == 0:
                            self.selected_audio.set(fmt['format_id'])
                            
                    except Exception as e:
                        print(f"Error creando radio button para audio {i}: {e}")
                        continue
            
            # Configurar scroll independiente
            self.root.after(100, lambda: video_scroll_frame.bind_all_children())
            self.root.after(100, lambda: audio_scroll_frame.bind_all_children())
                
            # Botones de descarga
            self._create_download_buttons()
            
            # Progress section
            self._create_progress_section()
            
            # Auto scroll al final
            self.root.after(100, lambda: self.main_frame._parent_canvas.yview_moveto(1.0))
            
        except Exception as e:
            print(f"❌ ERROR en _show_quality_options: {e}")
            import traceback
            traceback.print_exc()
        
    def _create_download_buttons(self):
        """CORREGIDO: Botones reordenados - Ambos, Video, Audio"""
        try:
            buttons_container = ctk.CTkFrame(self.options_frame)
            buttons_container.pack(fill="x", padx=15, pady=12)
            
            buttons_title = ctk.CTkLabel(
                buttons_container,
                text="⬇️ Descarga",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            buttons_title.pack(pady=(10, 8))
            
            # Checkbox para descargar miniatura con video
            checkbox_frame = ctk.CTkFrame(buttons_container)
            checkbox_frame.pack(fill="x", padx=15, pady=(0, 5))
            
            self.download_thumbnail_with_video = tk.BooleanVar(value=True)
            
            thumbnail_checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text="🖼️ Descargar miniatura automáticamente con el video",
                variable=self.download_thumbnail_with_video,
                font=ctk.CTkFont(size=11)
            )
            thumbnail_checkbox.pack(padx=10, pady=5)
            
            buttons_frame = ctk.CTkFrame(buttons_container)
            buttons_frame.pack(fill="x", padx=15, pady=(0, 12))
            
            buttons_frame.grid_columnconfigure(0, weight=1)
            buttons_frame.grid_columnconfigure(1, weight=1)
            buttons_frame.grid_columnconfigure(2, weight=1)
            
            # CORREGIDO: Reordenado - Ambos (izquierda), Video (centro), Audio (derecha)
            download_both_btn = ctk.CTkButton(
                buttons_frame,
                text="🎬🎵 Ambos",
                command=lambda: self.download('both'),
                height=35,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#FF6B6B",
                hover_color="#FF5252"
            )
            download_both_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")  # Columna 0 (izquierda)
            
            download_video_btn = ctk.CTkButton(
                buttons_frame,
                text="📥 Video",
                command=lambda: self.download('video'),
                height=35,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            download_video_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")  # Columna 1 (centro)
            
            download_audio_btn = ctk.CTkButton(
                buttons_frame,
                text="🎵 Audio",
                command=lambda: self.download('audio'),
                height=35,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            download_audio_btn.grid(row=0, column=2, padx=5, pady=10, sticky="ew")  # Columna 2 (derecha)
            
        except Exception as e:
            print(f"❌ ERROR en _create_download_buttons: {e}")
            
    def _create_progress_section(self):
        """Sección de progreso con progreso real"""
        try:
            self.progress_frame.pack(fill="x", padx=5, pady=8)
            
            progress_title = ctk.CTkLabel(
                self.progress_frame,
                text="📊 Estado",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            progress_title.pack(pady=(12, 8))
            
            self.progress_label = ctk.CTkLabel(
                self.progress_frame,
                textvariable=self.progress_var,
                font=ctk.CTkFont(size=11)
            )
            self.progress_label.pack(pady=5)
            
            self.progress_bar = ctk.CTkProgressBar(
                self.progress_frame,
                height=20
            )
            self.progress_bar.pack(fill="x", padx=15, pady=(5, 15))
            self.progress_bar.set(0)
            
        except Exception as e:
            print(f"❌ ERROR en _create_progress_section: {e}")
        
    def _get_video_formats(self):
        """Obtener formatos con Premium primero"""
        try:
            if not self.video_info or 'formats' not in self.video_info:
                print("❌ No hay video_info o formatos")
                return []
                
            video_formats = []
            
            for i, fmt in enumerate(self.video_info['formats']):
                try:
                    has_video = (
                        fmt.get('vcodec') and 
                        fmt.get('vcodec') != 'none' and 
                        fmt.get('vcodec') != 'null'
                    ) or (
                        fmt.get('height') or 
                        fmt.get('width') or
                        'video' in str(fmt.get('format_note', '')).lower()
                    )
                    
                    if has_video:
                        format_id = fmt.get('format_id', f'unknown_{i}')
                        ext = fmt.get('ext', 'mp4')
                        height = fmt.get('height', 0)
                        width = fmt.get('width', 0)
                        
                        format_note = str(fmt.get('format_note', '')).lower()
                        is_premium = 'premium' in format_note
                        
                        if height and width:
                            resolution = f"{width}x{height}"
                        elif height:
                            resolution = f"{height}p"
                        elif width:
                            resolution = f"{width}w"
                        else:
                            resolution = "unknown"
                        
                        filesize_mb = "N/A"
                        if fmt.get('filesize'):
                            size_mb = fmt['filesize'] / (1024*1024)
                            filesize_mb = f"{size_mb:.1f}MB"
                        elif fmt.get('filesize_approx'):
                            size_mb = fmt['filesize_approx'] / (1024*1024)
                            filesize_mb = f"~{size_mb:.1f}MB"
                        elif fmt.get('tbr') and self.video_info.get('duration'):
                            estimated_size = (fmt['tbr'] * self.video_info['duration'] * 1000) / (8 * 1024 * 1024)
                            filesize_mb = f"≈{estimated_size:.1f}MB"
                        
                        video_formats.append({
                            'format_id': format_id,
                            'ext': ext,
                            'height': height,
                            'width': width,
                            'resolution': resolution,
                            'filesize_mb': filesize_mb,
                            'quality_sort': height or 0,
                            'is_premium': is_premium,
                            'fps': fmt.get('fps', 0),
                            'format_note': fmt.get('format_note', '')
                        })
                        
                except Exception as e:
                    print(f"⚠️ Error procesando formato {i}: {e}")
                    continue
            
            # Ordenar poniendo Premium PRIMERO
            def sort_key(fmt):
                premium_priority = 10000 if fmt['is_premium'] else 0
                return (premium_priority, fmt.get('height', 0), fmt.get('fps', 0))
            
            video_formats.sort(key=sort_key, reverse=True)
            
            premium_count = sum(1 for fmt in video_formats if fmt['is_premium'])
            print(f"👑 Formatos Premium encontrados: {premium_count}")
            
            return video_formats
            
        except Exception as e:
            print(f"❌ ERROR en _get_video_formats: {e}")
            return []
            
    def _get_audio_formats(self):
        """Obtener formatos de audio"""
        try:
            if not self.video_info or 'formats' not in self.video_info:
                return []
                
            audio_formats = []
            
            for i, fmt in enumerate(self.video_info['formats']):
                try:
                    has_audio = (
                        fmt.get('acodec') and 
                        fmt.get('acodec') != 'none' and 
                        fmt.get('acodec') != 'null'
                    ) or (
                        fmt.get('abr') or
                        'audio' in str(fmt.get('format_note', '')).lower()
                    )
                    
                    if has_audio:
                        format_id = fmt.get('format_id', f'unknown_audio_{i}')
                        ext = fmt.get('ext', 'mp3')
                        abr = fmt.get('abr', 0)
                        
                        quality_info = f"{abr}kbps" if abr else "audio"
                        
                        filesize_mb = "N/A"
                        if fmt.get('filesize'):
                            size_mb = fmt['filesize'] / (1024*1024)
                            filesize_mb = f"{size_mb:.1f}MB"
                        elif fmt.get('filesize_approx'):
                            size_mb = fmt['filesize_approx'] / (1024*1024)
                            filesize_mb = f"~{size_mb:.1f}MB"
                        elif abr and self.video_info.get('duration'):
                            estimated_size = (abr * self.video_info['duration'] * 1000) / (8 * 1024 * 1024)
                            filesize_mb = f"≈{estimated_size:.1f}MB"
                        
                        audio_formats.append({
                            'format_id': format_id,
                            'ext': ext,
                            'abr': abr,
                            'quality_info': quality_info,
                            'filesize_mb': filesize_mb,
                            'quality_sort': abr or 0
                        })
                        
                except Exception as e:
                    print(f"⚠️ Error procesando formato de audio {i}: {e}")
                    continue
            
            audio_formats.sort(key=lambda x: x['quality_sort'], reverse=True)
            return audio_formats
            
        except Exception as e:
            print(f"❌ ERROR en _get_audio_formats: {e}")
            return []
            
    def download(self, download_type):
        """Función principal de descarga con miniatura condicional"""
        try:
            print(f"📥 Iniciando descarga tipo: {download_type}")
            
            if not self.video_info:
                messagebox.showerror("Error", "Primero analiza un video")
                return
                
            if not self.current_profile:
                messagebox.showerror("Error", "No hay perfil seleccionado")
                return
                
            download_path = self.download_path
            if not os.path.exists(download_path):
                messagebox.showerror("Error", "La carpeta de descarga no existe")
                return
                
            thread = threading.Thread(target=self._download_thread, args=(download_type, download_path))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"❌ ERROR en download: {e}")
            messagebox.showerror("Error", f"Error iniciando descarga: {str(e)}")
            
    def _download_thread(self, download_type, download_path):
        """Hilo de descarga con progreso real y miniatura condicional"""
        try:
            print(f"🔄 Hilo de descarga iniciado - Tipo: {download_type}")
            
            # Obtener cookies del perfil actual
            temp_cookies = self.cookie_manager.get_cookies_file(self.current_profile)
            if not temp_cookies:
                raise Exception("No se pudieron obtener cookies del perfil actual")
            
            # Configurar opciones de descarga
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'cookiefile': temp_cookies,
            }
            
            if download_type == 'video':
                selected_format = self.selected_video.get()
                ydl_opts['format'] = selected_format
                print(f"📹 Descargando video con formato ID: {selected_format}")
            elif download_type == 'audio':
                selected_format = self.selected_audio.get()
                ydl_opts['format'] = selected_format
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                print(f"🎵 Descargando audio con formato ID: {selected_format}")
            elif download_type == 'both':
                video_format = self.selected_video.get()
                audio_format = self.selected_audio.get()
                ydl_opts['format'] = f"{video_format}+{audio_format}"
                print(f"🎬🎵 Descargando video+audio con formatos ID: {video_format}+{audio_format}")
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_info['webpage_url']])
            
            # Limpiar archivo temporal de cookies
            os.unlink(temp_cookies)
            
            # Descargar miniatura automáticamente si está marcado
            if (download_type in ['video', 'both'] and 
                hasattr(self, 'download_thumbnail_with_video') and 
                self.download_thumbnail_with_video.get()):
                
                print("🖼️ Descargando miniatura automáticamente...")
                self.root.after(0, lambda: self.progress_var.set("🖼️ Descargando miniatura..."))
                self._download_thumbnail_sync('large')
                
            self.root.after(0, lambda: self._download_complete())
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error en descarga: {error_msg}")
            if "Sign in to confirm you're not a bot" in error_msg:
                error_msg += "\n\n💡 Este video requiere autenticación. Verifica tus cookies."
            self.root.after(0, lambda: self._show_error(f"Error en la descarga: {error_msg}"))
            
    def _progress_hook(self, d):
        """Hook de progreso que actualiza la barra"""
        try:
            if d['status'] == 'downloading':
                try:
                    percent = 0
                    if '_percent_str' in d:
                        percent_str = d['_percent_str'].strip()
                        if percent_str.endswith('%'):
                            try:
                                percent = float(percent_str[:-1]) / 100.0
                            except ValueError:
                                percent = 0
                    elif 'total_bytes' in d and 'downloaded_bytes' in d:
                        percent = d['downloaded_bytes'] / d['total_bytes']
                    elif 'total_bytes_estimate' in d and 'downloaded_bytes' in d:
                        percent = d['downloaded_bytes'] / d['total_bytes_estimate']
                    
                    speed = d.get('speed', 0)
                    speed_text = f"({speed/1024/1024:.1f} MB/s)" if speed else ""
                    
                    status_text = f"Descargando... {percent*100:.1f}% {speed_text}"
                    
                    self.root.after(0, lambda p=percent, s=status_text: self._update_progress(p, s))
                    
                except Exception as e:
                    print(f"Error en progress_hook: {e}")
                    self.root.after(0, lambda: self._update_progress(0, "Descargando..."))
                    
            elif d['status'] == 'finished':
                self.root.after(0, lambda: self._update_progress(1.0, "Procesando archivo final..."))
                
        except Exception as e:
            print(f"❌ ERROR en _progress_hook: {e}")
            
    def _update_progress(self, percent, status):
        """Actualizar la barra de progreso y el texto de estado"""
        try:
            percent = max(0, min(1, percent))
            self.progress_bar.set(percent)
            self.progress_var.set(status)
            self.root.update_idletasks()
        except Exception as e:
            print(f"❌ Error actualizando progreso: {e}")
        
    def _download_complete(self):
        """Manejar descarga completada"""
        try:
            self.progress_bar.set(1.0)
            self.progress_var.set("✅ ¡Descarga completada exitosamente!")
            messagebox.showinfo("Éxito", "¡Descarga completada exitosamente!")
            print("🎉 Descarga completada con éxito")
        except Exception as e:
            print(f"❌ ERROR en _download_complete: {e}")
        
    def _show_error(self, message):
        """Mostrar error en UI"""
        try:
            self.analyze_btn.configure(state="normal", text="🔍 Analizar")
            self.progress_var.set("❌ Error en la descarga")
            messagebox.showerror("Error", message)
            print(f"❌ Error mostrado: {message}")
        except Exception as e:
            print(f"❌ ERROR en _show_error: {e}")

    def _format_duration(self, seconds):
        """Formatear duración en formato legible"""
        try:
            if not seconds:
                return "Desconocido"
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return f"{minutes:02d}:{seconds:02d}"
        except Exception as e:
            print(f"❌ ERROR en _format_duration: {e}")
            return "Desconocido"

    def select_download_path(self):
        """Seleccionar carpeta de descarga"""
        try:
            path = filedialog.askdirectory(title="Seleccionar carpeta de descarga")
            if path:
                self.download_path = path
                self.save_config()
                self.update_folder_button()
                messagebox.showinfo("Carpeta Cambiada", f"Nueva carpeta de descarga:\n{path}")
        except Exception as e:
            print(f"❌ ERROR en select_download_path: {e}")
            messagebox.showerror("Error", f"Error al seleccionar carpeta: {str(e)}")

    def open_download_folder(self):
        """Abrir la carpeta de descarga en el explorador"""
        try:
            if os.path.exists(self.download_path):
                if sys.platform == "win32":
                    os.startfile(self.download_path)
                elif sys.platform == "darwin":
                    os.system(f"open '{self.download_path}'")
                else:
                    os.system(f"xdg-open '{self.download_path}'")
            else:
                messagebox.showerror("Error", "La carpeta de descarga no existe")
        except Exception as e:
            print(f"❌ ERROR en open_download_folder: {e}")
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{str(e)}")

    def download_thumbnail(self, size):
        """Descargar miniatura del video (manual)"""
        try:
            if not self.video_info:
                messagebox.showerror("Error", "Primero analiza un video para descargar su miniatura")
                return
            
            thread = threading.Thread(target=self._download_thumbnail_thread, args=(size,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"❌ ERROR en download_thumbnail: {e}")
            messagebox.showerror("Error", f"Error al descargar miniatura: {str(e)}")

    def _download_thumbnail_thread(self, size):
        """CORREGIDO: Hilo para descargar miniatura manual - CON alerta solo cuando es manual"""
        try:
            self.root.after(0, lambda: self.progress_var.set("🖼️ Descargando miniatura..."))
            
            video_url = self.video_info.get('webpage_url', '')
            video_id = self.extract_video_id(video_url)
            
            if not video_id:
                raise Exception("No se pudo extraer el ID del video")
            
            thumbnail_urls = {
                'small': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                'medium': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                'large': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            }
            
            thumbnail_url = thumbnail_urls.get(size, thumbnail_urls['large'])
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            img_response = requests.get(thumbnail_url, headers=headers, timeout=30)
            img_response.raise_for_status()
            
            # CORREGIDO: Usar el título original SIN modificar : y |
            video_title = self.video_info.get('title', 'video_thumbnail')
            safe_title = re.sub(r'[<>"/\\?*]', '_', video_title)  # Mantener : y |
            safe_title = safe_title.strip()
            
            # CORREGIDO: Sin sufijo también en manual
            filename = f"{safe_title}.jpg"
            filepath = os.path.join(self.download_path, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Miniatura guardada: {filepath}")
            
            # Mostrar alerta SOLO en descarga manual
            self.root.after(0, lambda: self.progress_var.set("✅ Miniatura descargada exitosamente!"))
            self.root.after(0, lambda: messagebox.showinfo(
                "Miniatura Descargada", 
                f"Miniatura descargada exitosamente:\n{filename}\n\nUbicación: {self.download_path}"
            ))
            
        except Exception as e:
            error_msg = f"Error al descargar miniatura: {str(e)}"
            print(f"❌ {error_msg}")
            self.root.after(0, lambda: self.progress_var.set("❌ Error descargando miniatura"))
            self.root.after(0, lambda: messagebox.showerror("Error de Miniatura", error_msg))

    def _download_thumbnail_sync(self, size):
        """CORREGIDO: Versión síncrona para usar en descarga automática - SIN alertas y con título original"""
        try:
            video_url = self.video_info.get('webpage_url', '')
            video_id = self.extract_video_id(video_url)
            
            if not video_id:
                raise Exception("No se pudo extraer el ID del video")
            
            thumbnail_urls = {
                'small': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                'medium': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                'large': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            }
            
            thumbnail_url = thumbnail_urls.get(size, thumbnail_urls['large'])
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            img_response = requests.get(thumbnail_url, headers=headers, timeout=30)
            img_response.raise_for_status()
            
            # CORREGIDO: Usar el título original SIN modificar caracteres especiales
            video_title = self.video_info.get('title', 'video_thumbnail')
            
            # CORREGIDO: Solo limpiar caracteres que Windows NO permite en nombres de archivo
            # Mantener : y | que SÍ están permitidos
            safe_title = re.sub(r'[<>"/\\?*]', '_', video_title)  # Removido : y |
            safe_title = safe_title.strip()
            
            # CORREGIDO: Solo el título, SIN sufijo de tamaño
            filename = f"{safe_title}.jpg"
            filepath = os.path.join(self.download_path, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Miniatura guardada: {filepath}")
            
            # CORREGIDO: Solo actualizar progreso, SIN mostrar alert/messagebox
            self.root.after(0, lambda: self.progress_var.set("✅ Miniatura descargada silenciosamente"))
            
            # NO mostrar messagebox automáticamente
            
        except Exception as e:
            raise e
        
    def on_window_resize(self, event):
        """Manejar redimensionamiento y guardar configuración"""
        try:
            if event.widget == self.root:
                self.root.update_idletasks()
                if hasattr(self, '_resize_timer'):
                    self.root.after_cancel(self._resize_timer)
                self._resize_timer = self.root.after(1000, self.save_config)
        except Exception as e:
            print(f"❌ ERROR en on_window_resize: {e}")
        
    def run(self):
        """Ejecutar la aplicación"""
        try:
            print("🚀 Iniciando YouTube Downloader Multi-Account Pro...")
            print("🎭 Gestión múltiple de cuentas (Premium + Membresías)")
            print("🧠 Selección inteligente automática de perfil")
            print("🦊 Soporte para Chrome y Firefox")
            print("🔐 Cookies encriptadas y validación automática")
            print("🛡️ Seguridad y privacidad mejoradas")
            print("🖱️ Scroll arreglado e interfaz optimizada")
            print("✅ Checkbox para miniatura automática")
            print("🤖 Descarga automática de canales con numeración")
            print("🔍 Sistema inteligente anti-duplicados")
            print("📁 Descarga completa para carpetas vacías")
            print("🎯 Mejor calidad automática para descargas automáticas")
            print("🎬 ¡Listo para usar!")
            print("=" * 50)
            self.root.mainloop()
        except Exception as e:
            print(f"❌ ERROR CRÍTICO en run(): {e}")
            import traceback
            traceback.print_exc()
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        print("🎬 Creando instancia de YouTubeDownloader Multi-Account...")
        app = YouTubeDownloader()
        print("✅ Instancia creada exitosamente")
        print("🎬 Ejecutando aplicación...")
        app.run()
    except Exception as e:
        print(f"❌ ERROR CRÍTICO en main: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 DIAGNÓSTICO:")
        print("1. Instala las librerías requeridas:")
        print("   pip install customtkinter yt-dlp requests pillow cryptography")
        print("2. Verifica que Python esté correctamente instalado")
        print("3. Intenta ejecutar el programa desde el terminal/CMD")
        input("\nPresiona Enter para salir...")
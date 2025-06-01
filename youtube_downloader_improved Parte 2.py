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
            

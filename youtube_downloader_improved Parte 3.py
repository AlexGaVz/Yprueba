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
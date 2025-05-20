import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from conn import get_connection


class ClubManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root  # Frame contenedor
        self.app = app_manager
        
        # Configurar el frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Variables de estado
        self.current_club = None
        self.clubs_data = []
        
        # Construir la interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_clubs_list()
        
        # Establecer focus inicial
        self.search_entry.focus()
    
    def _create_ui(self):
        """Construye toda la interfaz de usuario"""
        # Configuración del grid principal
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de búsqueda (fila 0)
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Botón para regresar al menú
        ctk.CTkButton(
            search_frame,
            text="← Menú",
            width=80,
            command=self.return_to_menu,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side="left", padx=(0, 10))
        
        # Componentes de búsqueda
        ctk.CTkLabel(search_frame, text="Buscar Club:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Nombre, código o responsable..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_clubs())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_clubs,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de clubs (columna 0)
        self._create_clubs_list()
        
        # Formulario de edición (columna 1)
        self._create_form()
        
        # Barra de estado (fila 2)
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def _create_clubs_list(self):
        """Crea el panel de lista de clubs"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=350)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera con contador
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.club_count_label = ctk.CTkLabel(
            header_frame,
            text="Clubs (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.club_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nuevo",
            width=80,
            command=self.new_club
        ).pack(side="right")
        
        # Lista con scroll
        self.list_scroll = ctk.CTkScrollableFrame(
            self.list_frame,
            height=550
        )
        self.list_scroll.pack(fill="both", expand=True)
    
    def _create_form(self):
        """Crea el formulario de edición"""
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=1, column=1, sticky="nsew")
        
        # Título del formulario
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Nuevo Club",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario según la tabla clubes
        fields = [
            {"label": "Código Club*", "var_name": "code_var", "required": True},
            {"label": "Nombre Club*", "var_name": "name_var", "required": True},
            {"label": "Responsable", "var_name": "responsable_var"},
            {"label": "Correo Contacto", "var_name": "email_var", "validate": "email"},
            {"label": "Estado*", "var_name": "status_var", "required": True},
            {"label": "Fecha Creación", "var_name": "creation_date_var", "validate": "date"},
            {"label": "Máx. Miembros", "var_name": "max_members_var", "validate": "number"},
            {"label": "Requisitos", "var_name": "requirements_var", "multiline": True},
            {"label": "Descripción", "var_name": "description_var", "multiline": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            # Label con asterisco para campos obligatorios
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            # Campo según tipo
            if field["var_name"] == "status_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Activo", "Inactivo", "En pausa"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field.get("multiline"):
                textbox = ctk.CTkTextbox(frame, height=60)
                textbox.pack(side="right", fill="x", expand=True)
                var.textbox = textbox
            else:
                entry = ctk.CTkEntry(frame)
                entry.pack(side="right", fill="x", expand=True)
                var.entry = entry
            
            self.form_vars[field["var_name"]] = var
        
        # Establecer valores por defecto
        self.form_vars["status_var"].set("Activo")
        self.form_vars["creation_date_var"].set(datetime.now().strftime("%Y-%m-%d"))
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=self.save_club,
            fg_color="#28a745"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.cancel_edit
        ).pack(side="left", padx=(0, 10))
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Eliminar",
            command=self.delete_club,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def update_clubs_list(self):
        """Actualiza la lista de clubs desde la base de datos"""
        # Limpiar lista actual
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        # Obtener datos
        self.clubs_data = self.get_clubs_from_db()
        self.club_count_label.configure(text=f"Clubs ({len(self.clubs_data)})")
        
        if not self.clubs_data:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron clubs",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for club in self.clubs_data:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Mostrar información básica
            text = f"{club.get('codigo_club', '')} - {club.get('nombre_club', '')}"
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            # Botón editar
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda c=club: self.load_club_data(c)
            ).pack(side="right", padx=2)
    
    def load_club_data(self, club):
        """Carga los datos de un club en el formulario"""
        self.current_club = club
        self.form_title.configure(text=f"Editando: {club.get('nombre_club', '')}")
        self.delete_btn.configure(state="normal")
        
        # Mapear datos a los campos
        field_mapping = {
            "code_var": club.get("codigo_club", ""),
            "name_var": club.get("nombre_club", ""),
            "responsable_var": club.get("responsable", ""),
            "email_var": club.get("correo_contacto", ""),
            "status_var": club.get("estado", "Activo"),
            "creation_date_var": club.get("fecha_creacion", ""),
            "max_members_var": str(club.get("max_miembros", "")),
            "requirements_var": club.get("requisitos", ""),
            "description_var": club.get("descripcion", "")
        }
        
        for var_name, value in field_mapping.items():
            if hasattr(self.form_vars[var_name], 'textbox'):
                # Validar que value no sea None ni otro tipo no string
                if value is None:
                    value = ""
                else:
                    value = str(value)
                self.form_vars[var_name].textbox.delete("1.0", "end")
                self.form_vars[var_name].textbox.insert("1.0", value)
            else:
                self.form_vars[var_name].set(value)

    
    def clear_form(self):
        """Limpia el formulario"""
        for var_name, var in self.form_vars.items():
            if hasattr(var, 'textbox'):
                var.textbox.delete("1.0", "end")
            else:
                var.set("")
        
        self.current_club = None
        self.form_title.configure(text="Nuevo Club")
        self.delete_btn.configure(state="disabled")
        self.form_vars["status_var"].set("Activo")
        self.form_vars["creation_date_var"].set(datetime.now().strftime("%Y-%m-%d"))
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []

        # Validar campos obligatorios (usando strip() para eliminar espacios en blanco)
        codigo = self.form_vars["code_var"].get().strip()
        nombre = self.form_vars["name_var"].get().strip()
        estado = self.form_vars["status_var"].get().strip()

        if not codigo:
            errors.append("El código del club es obligatorio")
        if not nombre:
            errors.append("El nombre del club es obligatorio")
        if not estado:
            errors.append("El estado es obligatorio")

        # Validar email si hay valor
        email = self.form_vars["email_var"].get().strip()
        if email:
            import re
            email_pattern = r"[^@]+@[^@]+\.[^@]+"
            if not re.match(email_pattern, email):
                errors.append("El correo electrónico no es válido")

        # Validar fecha creación (formato YYYY-MM-DD)
        fecha_str = self.form_vars["creation_date_var"].get().strip()
        if fecha_str:
            try:
                datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                errors.append("La fecha de creación debe tener formato AAAA-MM-DD")

        # Validar max miembros es número si no vacío
        max_miembros_str = self.form_vars["max_members_var"].get().strip()
        if max_miembros_str:
            if not max_miembros_str.isdigit():
                errors.append("Máx. Miembros debe ser un número entero positivo")

        # Validar que los campos multiline no contengan solo espacios (opcional)
        requisitos = self.form_vars["requirements_var"].textbox.get("1.0", "end").strip()
        descripcion = self.form_vars["description_var"].textbox.get("1.0", "end").strip()

        # Aquí podrías hacer validaciones extras si quieres...

        return errors


    
    def search_clubs(self):
        """Busca clubs según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_clubs_list()
            return
        
        # Obtener datos actualizados
        all_clubs = self.get_clubs_from_db()
        
        filtered = [
            club for club in all_clubs
            if (search_term in club.get("nombre_club", "").lower() or
                search_term in club.get("codigo_club", "").lower() or
                search_term in (club.get("responsable", "") or "").lower() or
                search_term in (club.get("correo_contacto", "") or "").lower())
        ]
        
        # Actualizar lista visual
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for club in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = f"{club.get('codigo_club', '')} - {club.get('nombre_club', '')}"
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda c=club: self.load_club_data(c)
            ).pack(side="right", padx=2)
        
        self.club_count_label.configure(text=f"Clubs ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda y muestra todos los clubs"""
        self.search_entry.delete(0, "end")
        self.update_clubs_list()
    
    def new_club(self):
        """Prepara el formulario para un nuevo club"""
        self.clear_form()
    
    def save_club(self):
        """Guarda los datos del club (versión corregida)"""
        if not self.validate_form():
            return
        
        # Obtener datos del formulario (usando strip() para limpiar espacios)
        club_data = {
            "codigo_club": self.form_vars["code_var"].get().strip(),
            "nombre_club": self.form_vars["name_var"].get().strip(),
            "responsable": self.form_vars["responsable_var"].get().strip() or None,
            "correo_contacto": self.form_vars["email_var"].get().strip() or None,
            "estado": self.form_vars["status_var"].get(),
            "fecha_creacion": self.form_vars["creation_date_var"].get().strip() or None,
            "max_miembros": int(self.form_vars["max_members_var"].get()) if self.form_vars["max_members_var"].get().strip() else None,
            "requisitos": self.form_vars["requirements_var"].textbox.get("1.0", "end-1c").strip() or None,
            "descripcion": self.form_vars["description_var"].textbox.get("1.0", "end-1c").strip() or None
        }
        
        try:
            if self.current_club:
                # Actualizar club existente
                club_data["id_club"] = self.current_club["id_club"]
                success = self.update_club_in_db(club_data)
                action = "actualizado"
            else:
                # Crear nuevo club
                success = self.insert_club_to_db(club_data)
                action = "creado"
            
            if success:
                messagebox.showinfo("Éxito", f"Club {action} correctamente")
                self.update_clubs_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", f"No se pudo {action} el club")
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def delete_club(self):
        """Elimina el club actual"""
        if not self.current_club:
            return
            
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar el club {self.current_club.get('nombre_club', '')}?\n\n"
            f"Código: {self.current_club.get('codigo_club', '')}\n"
            f"Responsable: {self.current_club.get('responsable', '')}",
            icon="warning"
        )
        
        if confirm:
            try:
                success = self.delete_club_from_db(self.current_club["id_club"])
                
                if success:
                    messagebox.showinfo("Éxito", "Club eliminado correctamente")
                    self.update_clubs_list()
                    self.clear_form()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el club")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar club: {str(e)}")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS DE BASE DE DATOS
    # ======================

    def get_clubs_from_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo_club, nombre_club, responsable, correo_contacto, estado, fecha_creacion, max_miembros, requisitos, descripcion FROM clubes")
        rows = cursor.fetchall()
        conn.close()

        clubs = []
        for row in rows:
            clubs.append({
                "codigo_club": row[0],
                "nombre_club": row[1],
                "responsable": row[2],
                "correo_contacto": row[3],
                "estado": row[4],
                "fecha_creacion": row[5].strftime("%Y-%m-%d") if row[5] else "",
                "max_miembros": row[6],
                "requisitos": row[7],
                "descripcion": row[8]
            })
        return clubs

        
    def insert_club_to_db(self, club_data):
        """Inserta un nuevo club en la base de datos"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            query = '''
                INSERT INTO clubes (
                    codigo_club, nombre_club, descripcion,
                    responsable, correo_contacto, estado,
                    fecha_creacion, max_miembros, requisitos
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            params = (
                club_data['codigo_club'],
                club_data['nombre_club'],
                club_data['descripcion'],
                club_data['responsable'],
                club_data['correo_contacto'],
                club_data['estado'],
                club_data['fecha_creacion'],
                club_data['max_miembros'],
                club_data['requisitos']
            )
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al insertar club: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def update_club_in_db(self, club_data):
        """Actualiza un club existente en la base de datos"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            query = '''
                UPDATE clubes SET 
                    codigo_club = %s,
                    nombre_club = %s,
                    descripcion = %s,
                    responsable = %s,
                    correo_contacto = %s,
                    estado = %s,
                    fecha_creacion = %s,
                    max_miembros = %s,
                    requisitos = %s
                WHERE id_club = %s
            '''
            params = (
                club_data['codigo_club'],
                club_data['nombre_club'],
                club_data['descripcion'],
                club_data['responsable'],
                club_data['correo_contacto'],
                club_data['estado'],
                club_data['fecha_creacion'],
                club_data['max_miembros'],
                club_data['requisitos'],
                club_data['id_club']
            )
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar club: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def delete_club_from_db(self, club_id):
        """Elimina un club de la base de datos"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM clubes WHERE id_club = %s"
            cursor.execute(query, (club_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar club: {str(e)}")
        finally:
            cursor.close()
            conn.close()
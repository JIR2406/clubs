import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

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
        
        # Campos del formulario
        fields = [
            {"label": "Código Club*", "var_name": "codigo_var", "required": True},
            {"label": "Nombre Club*", "var_name": "nombre_var", "required": True},
            {"label": "Responsable", "var_name": "responsable_var"},
            {"label": "Correo Contacto", "var_name": "correo_var", "validate": "email"},
            {"label": "Estado", "var_name": "estado_var"},
            {"label": "Fecha Creación", "var_name": "fecha_creacion_var", "validate": "date"},
            {"label": "Máx. Miembros", "var_name": "max_miembros_var", "validate": "number"},
            {"label": "Requisitos", "var_name": "requisitos_var", "multiline": True},
            {"label": "Descripción", "var_name": "descripcion_var", "multiline": True}
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
            if field["var_name"] == "estado_var":
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
        
        # Obtener datos (simulado)
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
            "codigo_var": club.get("codigo_club", ""),
            "nombre_var": club.get("nombre_club", ""),
            "responsable_var": club.get("responsable", ""),
            "correo_var": club.get("correo_contacto", ""),
            "estado_var": club.get("estado", "Activo"),
            "fecha_creacion_var": club.get("fecha_creacion", ""),
            "max_miembros_var": str(club.get("max_miembros", "")),
            "requisitos_var": club.get("requisitos", ""),
            "descripcion_var": club.get("descripcion", "")
        }
        
        for var_name, value in field_mapping.items():
            if hasattr(self.form_vars[var_name], 'textbox'):
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
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        # Validar campos obligatorios
        if not self.form_vars["codigo_var"].get():
            errors.append("El código del club es obligatorio")
        if not self.form_vars["nombre_var"].get():
            errors.append("El nombre del club es obligatorio")
        
        # Validar formato email
        email = self.form_vars["correo_var"].get()
        if email and "@" not in email:
            errors.append("El correo electrónico no es válido")
        
        # Validar fecha
        fecha = self.form_vars["fecha_creacion_var"].get()
        if fecha:
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                errors.append("La fecha debe estar en formato YYYY-MM-DD")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_clubs(self):
        """Busca clubs según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_clubs_list()
            return
        
        filtered = [
            club for club in self.clubs_data
            if (search_term in club.get("nombre_club", "").lower() or
                search_term in club.get("codigo_club", "").lower() or
                search_term in club.get("responsable", "").lower())
        ]
        
        # Actualizar lista visual
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for club in filtered:
            self._add_club_to_list(club)
        
        self.club_count_label.configure(text=f"Clubs ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda y muestra todos los clubs"""
        self.search_entry.delete(0, "end")
        self.update_clubs_list()
    
    def new_club(self):
        """Prepara el formulario para un nuevo club"""
        self.clear_form()
        self.form_vars["estado_var"].set("Activo")
        self.form_vars["fecha_creacion_var"].set(datetime.now().strftime("%Y-%m-%d"))
    
    def save_club(self):
        """Guarda los datos del club"""
        if not self.validate_form():
            return
        
        club_data = {
            "codigo_club": self.form_vars["codigo_var"].get(),
            "nombre_club": self.form_vars["nombre_var"].get(),
            "responsable": self.form_vars["responsable_var"].get(),
            "correo_contacto": self.form_vars["correo_var"].get(),
            "estado": self.form_vars["estado_var"].get(),
            "fecha_creacion": self.form_vars["fecha_creacion_var"].get(),
            "max_miembros": self.form_vars["max_miembros_var"].get(),
            "requisitos": self.form_vars["requisitos_var"].textbox.get("1.0", "end-1c"),
            "descripcion": self.form_vars["descripcion_var"].textbox.get("1.0", "end-1c")
        }
        
        if self.current_club:
            # Actualizar club existente
            messagebox.showinfo("Éxito", "Club actualizado correctamente")
        else:
            # Crear nuevo club
            messagebox.showinfo("Éxito", "Club creado correctamente")
        
        self.update_clubs_list()
        self.clear_form()
    
    def delete_club(self):
        """Elimina el club actual"""
        if not self.current_club:
            return
            
        if messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar el club {self.current_club.get('nombre_club', '')}?"
        ):
            messagebox.showinfo("Éxito", "Club eliminado correctamente")
            self.update_clubs_list()
            self.clear_form()
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()
    
    def get_clubs_from_db(self):
        """Simula obtener clubs de la base de datos"""
        # Datos de ejemplo - reemplazar con conexión real a BD
        return [
            {
                "codigo_club": "CLB001",
                "nombre_club": "Club de Futbol",
                "responsable": "Juan Pérez",
                "estado": "Activo",
                "fecha_creacion": "2023-01-15",
                "max_miembros": "50"
            },
            {
                "codigo_club": "CLB002",
                "nombre_club": "Club de Ajedrez",
                "responsable": "María García",
                "estado": "Activo",
                "fecha_creacion": "2023-02-20",
                "max_miembros": "30"
            }
        ]
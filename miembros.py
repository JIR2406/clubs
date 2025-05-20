import customtkinter as ctk
from tkinter import messagebox

class MemberManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root  # Frame contenedor
        self.app = app_manager
        self.current_member = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_members_list()

    def _create_ui(self):
        """Construye toda la interfaz gráfica"""
        # Configuración del grid principal
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de búsqueda con botón de regreso
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
        
        ctk.CTkLabel(search_frame, text="Buscar Estudiante:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Nombre, código o correo..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_members())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_members,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de estudiantes
        self._create_members_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_members_list(self):
        """Crea el panel de lista de estudiantes"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=350)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.member_count_label = ctk.CTkLabel(
            header_frame,
            text="Estudiantes (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.member_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nuevo",
            width=80,
            command=self.new_member
        ).pack(side="right")
        
        # Lista con scroll
        self.list_scroll = ctk.CTkScrollableFrame(
            self.list_frame,
            height=550
        )
        self.list_scroll.pack(fill="both", expand=True)
    
    def _create_form(self):
        """Crea el formulario de edición con appat y apmat"""
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=1, column=1, sticky="nsew")
        
        # Título del formulario
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Nuevo Estudiante",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario actualizados para appat/apmat
        fields = [
            {"label": "Código*", "var_name": "codigo_var", "required": True},
            {"label": "Nombre*", "var_name": "nombre_var", "required": True},
            {"label": "Apellido Paterno*", "var_name": "appat_var", "required": True},
            {"label": "Apellido Materno*", "var_name": "apmat_var", "required": True},
            {"label": "Correo*", "var_name": "correo_var", "required": True},
            {"label": "Teléfono", "var_name": "telefono_var"},
            {"label": "Fecha Nac.", "var_name": "fecha_nac_var"},
            {"label": "Carrera", "var_name": "carrera_var"},
            {"label": "Semestre", "var_name": "semestre_var"},
            {"label": "Estado*", "var_name": "estado_var", "required": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            if field["var_name"] == "estado_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Inscrito", "No inscrito", "Graduado", "Baja temporal"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            else:
                ctk.CTkEntry(
                    frame,
                    textvariable=var
                ).pack(side="right", fill="x", expand=True)
            
            self.form_vars[field["var_name"]] = var
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=self.save_member,
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
            command=self.delete_member,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_members_list(self):
        """Actualiza la lista de estudiantes mostrando appat y apmat"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        members = self.get_members_from_db()
        self.member_count_label.configure(text=f"Estudiantes ({len(members)})")
        
        if not members:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron estudiantes",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for member in members:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Mostrar ambos apellidos
            text = f"{member['codigo_estudiante']} - {member['nombre']} {member['appat']} {member['apmat']}"
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda m=member: self.load_member_data(m)
            ).pack(side="right", padx=2)
    
    def load_member_data(self, member):
        """Carga los datos de un estudiante en el formulario"""
        self.current_member = member
        self.form_title.configure(text=f"Editando: {member['nombre']} {member['appat']} {member['apmat']}")
        self.delete_btn.configure(state="normal")
        
        field_mapping = {
            "codigo_var": member.get("codigo_estudiante", ""),
            "nombre_var": member.get("nombre", ""),
            "appat_var": member.get("appat", ""),
            "apmat_var": member.get("apmat", ""),
            "correo_var": member.get("correo", ""),
            "telefono_var": member.get("telefono", ""),
            "fecha_nac_var": member.get("fecha_nacimiento", ""),
            "carrera_var": member.get("carrera", ""),
            "semestre_var": str(member.get("semestre", "")),
            "estado_var": member.get("estado_inscripcion", "Inscrito")
        }
        
        for var_name, value in field_mapping.items():
            self.form_vars[var_name].set(value)
    
    def clear_form(self):
        """Limpia el formulario"""
        for var in self.form_vars.values():
            var.set("")
        
        self.current_member = None
        self.form_title.configure(text="Nuevo Estudiante")
        self.delete_btn.configure(state="disabled")
        self.form_vars["estado_var"].set("Inscrito")
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        required_fields = ["codigo_var", "nombre_var", "appat_var", "apmat_var", "correo_var", "estado_var"]
        for field in required_fields:
            if not self.form_vars[field].get():
                field_name = field.replace("_var", "").replace("_", " ").title()
                errors.append(f"El campo {field_name} es obligatorio")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_members(self):
        """Busca estudiantes según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_members_list()
            return
        
        members = self.get_members_from_db()
        filtered = [
            m for m in members
            if (search_term in m['codigo_estudiante'].lower() or
                search_term in m['nombre'].lower() or
                search_term in m['appat'].lower() or
                search_term in m['apmat'].lower() or
                search_term in m['correo'].lower())
        ]
        
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for member in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = f"{member['codigo_estudiante']} - {member['nombre']} {member['appat']} {member['apmat']}"
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda m=member: self.load_member_data(m)
            ).pack(side="right", padx=2)
        
        self.member_count_label.configure(text=f"Estudiantes ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_entry.delete(0, "end")
        self.update_members_list()
    
    def new_member(self):
        """Prepara el formulario para nuevo estudiante"""
        self.clear_form()
        # Establecer valores por defecto si es necesario
        self.form_vars["semestre_var"].set("1")
    
    def save_member(self):
        """Guarda los datos del estudiante"""
        if not self.validate_form():
            return
        
        member_data = {
            "codigo_estudiante": self.form_vars["codigo_var"].get(),
            "nombre": self.form_vars["nombre_var"].get(),
            "appat": self.form_vars["appat_var"].get(),
            "apmat": self.form_vars["apmat_var"].get(),
            "correo": self.form_vars["correo_var"].get(),
            "telefono": self.form_vars["telefono_var"].get(),
            "fecha_nacimiento": self.form_vars["fecha_nac_var"].get(),
            "carrera": self.form_vars["carrera_var"].get(),
            "semestre": self.form_vars["semestre_var"].get(),
            "estado_inscripcion": self.form_vars["estado_var"].get()
        }
        
        if self.current_member:
            member_data["id_estudiante"] = self.current_member["id_estudiante"]
            success = self.save_member_to_db(member_data, is_update=True)
            action = "actualizado"
        else:
            success = self.save_member_to_db(member_data)
            action = "creado"
        
        if success:
            messagebox.showinfo("Éxito", f"Estudiante {action} correctamente")
            self.update_members_list()
            self.clear_form()
    
    def delete_member(self):
        """Elimina el estudiante actual"""
        if not self.current_member:
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar al estudiante:\n\n"
            f"{self.current_member['nombre']} {self.current_member['appat']} {self.current_member['apmat']}\n"
            f"Código: {self.current_member['codigo_estudiante']}",
            icon="warning"
        )
        
        if confirmacion:
            success = self.delete_member_from_db(self.current_member["id_estudiante"])
            
            if success:
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                self.update_members_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el estudiante")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS CRUD (VACÍOS)
    # ======================
    
    def get_members_from_db(self):
        """OBTENER ESTUDIANTES (implementar conexión real)"""
        # Retornar lista de diccionarios con la estructura de la tabla
        return []  # <-- Implementa tu lógica aquí
    
    def save_member_to_db(self, member_data, is_update=False):
        """GUARDAR ESTUDIANTE (implementar conexión real)"""
        # member_data: Dict con todos los campos del formulario
        # is_update: Boolean que indica si es actualización
        # Retornar True si fue exitoso
        return False  # <-- Implementa tu lógica aquí
    
    def delete_member_from_db(self, member_id):
        """ELIMINAR ESTUDIANTE (implementar conexión real)"""
        # member_id: ID del estudiante a eliminar
        # Retornar True si fue exitoso
        return False  # <-- Implementa tu lógica aquí
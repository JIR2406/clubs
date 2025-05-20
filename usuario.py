import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class UserManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_user = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_users_list()

    def _create_ui(self):
        """Construye la interfaz gráfica"""
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
        
        ctk.CTkLabel(search_frame, text="Buscar Usuarios:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Nombre, usuario, correo o rol..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_users())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_users,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de usuarios
        self._create_users_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_users_list(self):
        """Crea el panel de lista de usuarios"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.user_count_label = ctk.CTkLabel(
            header_frame,
            text="Usuarios (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.user_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nuevo",
            width=80,
            command=self.new_user
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
            text="Nuevo Usuario",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario según la tabla usuarios
        fields = [
            {"label": "Nombre Usuario*", "var_name": "username_var", "required": True},
            {"label": "Contraseña*", "var_name": "password_var", "required": True, "password": True},
            {"label": "Correo Electrónico*", "var_name": "email_var", "required": True},
            {"label": "Rol*", "var_name": "role_var", "required": True},
            {"label": "Estado*", "var_name": "status_var", "required": True},
            {"label": "ID Estudiante", "var_name": "student_id_var"},
            {"label": "Notas", "var_name": "notes_var", "multiline": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            if field["var_name"] == "role_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Administrador", "Coordinador"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] == "status_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Activo", "Inactivo", "Suspendido"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field.get("password"):
                entry = ctk.CTkEntry(
                    frame,
                    show="•",
                    textvariable=var
                )
                entry.pack(side="right", fill="x", expand=True)
                var.entry = entry  # Guardar referencia para poder mostrar/ocultar
                
                # Botón para mostrar/ocultar contraseña
                eye_btn = ctk.CTkButton(
                    frame,
                    text="👁",
                    width=30,
                    command=lambda e=entry: self.toggle_password_visibility(e)
                )
                eye_btn.pack(side="right", padx=(5, 0))
            elif field.get("multiline"):
                textbox = ctk.CTkTextbox(frame, height=60)
                textbox.pack(side="right", fill="x", expand=True)
                var.textbox = textbox
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
            command=self.save_user,
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
            command=self.delete_user,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def toggle_password_visibility(self, entry):
        """Alterna entre mostrar y ocultar la contraseña"""
        if entry.cget("show") == "":
            entry.configure(show="•")
        else:
            entry.configure(show="")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_users_list(self):
        """Actualiza la lista de usuarios"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        users = self.get_users_from_db()
        self.user_count_label.configure(text=f"Usuarios ({len(users)})")
        
        if not users:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron usuarios",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for user in users:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Formatear información para mostrar
            text = (f"{user['nombre_usuario']} - {user['correo']} "
                   f"({user['rol']}) - {user['estado']}")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda u=user: self.load_user_data(u)
            ).pack(side="right", padx=2)
    
    def load_user_data(self, user):
        """Carga los datos de un usuario en el formulario"""
        self.current_user = user
        self.form_title.configure(
            text=f"Editando Usuario #{user['id_usuario']}"
        )
        self.delete_btn.configure(state="normal")
        
        field_mapping = {
            "username_var": user.get("nombre_usuario", ""),
            "password_var": user.get("contrasena", ""),
            "email_var": user.get("correo", ""),
            "role_var": user.get("rol", "Coordinador"),
            "status_var": user.get("estado", "Activo"),
            "student_id_var": str(user.get("id_estudiante", "")),
            "notes_var": user.get("notas", "")
        }
        
        for var_name, value in field_mapping.items():
            if var_name == "notes_var":
                self.form_vars[var_name].textbox.delete("1.0", "end")
                self.form_vars[var_name].textbox.insert("1.0", value)
            else:
                self.form_vars[var_name].set(value)
    
    def clear_form(self):
        """Limpia el formulario"""
        for var_name, var in self.form_vars.items():
            if hasattr(var, 'textbox'):
                var.textbox.delete("1.0", "end")
            elif hasattr(var, 'entry'):
                var.entry.configure(show="•")
                var.set("")
            else:
                var.set("")
        
        self.current_user = None
        self.form_title.configure(text="Nuevo Usuario")
        self.delete_btn.configure(state="disabled")
        self.form_vars["role_var"].set("Coordinador")
        self.form_vars["status_var"].set("Activo")
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        required_fields = ["username_var", "password_var", "email_var", "role_var", "status_var"]
        for field in required_fields:
            if not self.form_vars[field].get():
                field_name = field.replace("_var", "").replace("_", " ").title()
                errors.append(f"El campo {field_name} es obligatorio")
        
        # Validar formato de email
        email = self.form_vars["email_var"].get()
        if email and "@" not in email:
            errors.append("El correo electrónico no es válido")
        
        # Validar que student_id sea numérico si existe
        student_id = self.form_vars["student_id_var"].get()
        if student_id:
            try:
                int(student_id)
            except ValueError:
                errors.append("El ID de estudiante debe ser un número")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_users(self):
        """Busca usuarios según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_users_list()
            return
        
        users = self.get_users_from_db()
        filtered = [
            u for u in users
            if (search_term in u['nombre_usuario'].lower() or
               search_term in u['correo'].lower() or
               search_term in u['rol'].lower() or
               search_term in u['estado'].lower() or
               search_term in str(u.get('id_estudiante', '')).lower())
        ]
        
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for user in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = (f"{user['nombre_usuario']} - {user['correo']} "
                   f"({user['rol']}) - {user['estado']}")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda u=user: self.load_user_data(u)
            ).pack(side="right", padx=2)
        
        self.user_count_label.configure(text=f"Usuarios ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_entry.delete(0, "end")
        self.update_users_list()
    
    def new_user(self):
        """Prepara el formulario para nuevo usuario"""
        self.clear_form()
    
    def save_user(self):
        """Guarda los datos del usuario"""
        if not self.validate_form():
            return
        
        user_data = {
            "nombre_usuario": self.form_vars["username_var"].get(),
            "contrasena": self.form_vars["password_var"].get(),
            "correo": self.form_vars["email_var"].get(),
            "rol": self.form_vars["role_var"].get(),
            "estado": self.form_vars["status_var"].get(),
            "id_estudiante": int(self.form_vars["student_id_var"].get()) if self.form_vars["student_id_var"].get() else None,
            "notas": self.form_vars["notes_var"].textbox.get("1.0", "end-1c") or None
        }
        
        if self.current_user:
            user_data["id_usuario"] = self.current_user["id_usuario"]
            success = self.save_user_to_db(user_data, is_update=True)
            action = "actualizado"
        else:
            success = self.save_user_to_db(user_data)
            action = "registrado"
        
        if success:
            messagebox.showinfo("Éxito", f"Usuario {action} correctamente")
            self.update_users_list()
            self.clear_form()
    
    def delete_user(self):
        """Elimina el usuario actual"""
        if not self.current_user:
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar este usuario?\n\n"
            f"Usuario: {self.current_user['nombre_usuario']}\n"
            f"Correo: {self.current_user['correo']}\n"
            f"Rol: {self.current_user['rol']}",
            icon="warning"
        )
        
        if confirmacion:
            success = self.delete_user_from_db(self.current_user["id_usuario"])
            
            if success:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.update_users_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS DE BASE DE DATOS (COMENTADOS)
    # ======================

    def get_users_from_db(self):
        """OBTENER USUARIOS DESDE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = '''
                SELECT u.*, 
                CONCAT(e.nombre, ' ', e.appat, ' ', e.apmat) AS nombre_estudiante
                FROM usuarios u
                LEFT JOIN estudiantes e ON u.id_estudiante = e.id_estudiante
                ORDER BY u.nombre_usuario
            '''
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios:\n{str(e)}")
            return []
        """
        # Datos de ejemplo (eliminar en implementación real)
        return [
            {
                "id_usuario": 1,
                "id_estudiante": 1,
                "nombre_usuario": "admin",
                "contrasena": "hashed_password",
                "correo": "admin@escuela.com",
                "rol": "Administrador",
                "estado": "Activo",
                "ultimo_acceso": "2023-05-15 14:30:00",
                "fecha_creacion": "2023-01-10",
                "fecha_actualizacion": "2023-05-15",
                "notas": "Usuario principal del sistema"
            },
            {
                "id_usuario": 2,
                "id_estudiante": 2,
                "nombre_usuario": "coordinador1",
                "contrasena": "hashed_password",
                "correo": "coordinador@escuela.com",
                "rol": "Coordinador",
                "estado": "Activo",
                "ultimo_acceso": "2023-06-20 10:15:00",
                "fecha_creacion": "2023-02-15",
                "fecha_actualizacion": "2023-06-20",
                "notas": "Coordinador del club de programación"
            }
        ]

    def save_user_to_db(self, user_data, is_update=False):
        """GUARDAR USUARIO EN BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            
            if is_update:
                query = '''UPDATE usuarios SET 
                          nombre_usuario = %s,
                          contrasena = IF(%s IS NULL OR %s = '', contrasena, %s),
                          correo = %s,
                          rol = %s,
                          estado = %s,
                          id_estudiante = %s,
                          notas = %s
                          WHERE id_usuario = %s
                '''
                params = (
                    user_data['nombre_usuario'],
                    user_data['contrasena'],
                    user_data['contrasena'],
                    user_data['contrasena'],
                    user_data['correo'],
                    user_data['rol'],
                    user_data['estado'],
                    user_data['id_estudiante'],
                    user_data['notas'],
                    user_data['id_usuario']
                )
            else:
                query = '''INSERT INTO usuarios (
                          nombre_usuario, contrasena, correo,
                          rol, estado, id_estudiante,
                          notas
                          ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
                params = (
                    user_data['nombre_usuario'],
                    user_data['contrasena'],
                    user_data['correo'],
                    user_data['rol'],
                    user_data['estado'],
                    user_data['id_estudiante'],
                    user_data['notas']
                )
            
            cursor.execute(query, params)
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al guardar usuario:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas

    def delete_user_from_db(self, user_id):
        """ELIMINAR USUARIO DE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            
            # Verificar si el usuario a eliminar es el mismo que está logueado
            if hasattr(self.app, 'current_user') and self.app.current_user and self.app.current_user['id_usuario'] == user_id:
                raise Exception("No puedes eliminar tu propio usuario mientras estás logueado")
            
            query = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query, (user_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al eliminar usuario:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas
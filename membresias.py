import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class MembershipManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_membership = None
        self.user = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_memberships_list()

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
        
        ctk.CTkLabel(search_frame, text="Buscar Membresía:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Estudiante, club o estado..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_memberships())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_memberships,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de membresías
        self._create_memberships_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_memberships_list(self):
        """Crea el panel de lista de membresías"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.membership_count_label = ctk.CTkLabel(
            header_frame,
            text="Membresías (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.membership_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nueva",
            width=80,
            command=self.new_membership
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
            text="Nueva Membresía",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario
        fields = [
            {"label": "Estudiante*", "var_name": "estudiante_var", "required": True},
            {"label": "Club*", "var_name": "club_var", "required": True},
            {"label": "Fecha Inscripción*", "var_name": "fecha_insc_var", "required": True},
            {"label": "Fecha Expiración", "var_name": "fecha_exp_var"},
            {"label": "Estado*", "var_name": "estado_var", "required": True},
            {"label": "Rol*", "var_name": "rol_var", "required": True}
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
                    values=["Activa", "Inactiva", "Suspendida", "En proceso"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] == "rol_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Miembro", "Coordinador", "Secretario", "Tesorero", "Asesor"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] in ["fecha_insc_var", "fecha_exp_var"]:
                ctk.CTkEntry(
                    frame,
                    textvariable=var,
                    placeholder_text="YYYY-MM-DD"
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
            command=self.save_membership,
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
            command=self.delete_membership,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_memberships_list(self):
        """Actualiza la lista de membresías"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        memberships = self.get_memberships_from_db()
        self.membership_count_label.configure(text=f"Membresías ({len(memberships)})")
        
        if not memberships:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron membresías",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for membership in memberships:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Formatear información para mostrar
            text = (f"{membership['nombre_estudiante']} en {membership['nombre_club']} - "
                   f"{membership['estado_membresia']} ({membership['rol']})")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda m=membership: self.load_membership_data(m)
            ).pack(side="right", padx=2)
    
    def load_membership_data(self, membership):
        """Carga los datos de una membresía en el formulario"""
        self.current_membership = membership
        self.form_title.configure(
            text=f"Editando: {membership['nombre_estudiante']} en {membership['nombre_club']}"
        )
        self.delete_btn.configure(state="normal")
        
        field_mapping = {
            "estudiante_var": membership.get("nombre_estudiante", ""),
            "club_var": membership.get("nombre_club", ""),
            "fecha_insc_var": membership.get("fecha_inscripcion", ""),
            "fecha_exp_var": membership.get("fecha_expiracion", ""),
            "estado_var": membership.get("estado_membresia", "En proceso"),
            "rol_var": membership.get("rol", "Miembro")
        }
        
        for var_name, value in field_mapping.items():
            self.form_vars[var_name].set(value)
    
    def clear_form(self):
        """Limpia el formulario"""
        for var in self.form_vars.values():
            var.set("")
        
        self.current_membership = None
        self.form_title.configure(text="Nueva Membresía")
        self.delete_btn.configure(state="disabled")
        self.form_vars["estado_var"].set("En proceso")
        self.form_vars["rol_var"].set("Miembro")
        self.form_vars["fecha_insc_var"].set(datetime.now().strftime("%Y-%m-%d"))
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        required_fields = ["estudiante_var", "club_var", "fecha_insc_var", "estado_var", "rol_var"]
        for field in required_fields:
            if not self.form_vars[field].get():
                field_name = field.replace("_var", "").replace("_", " ").title()
                errors.append(f"El campo {field_name} es obligatorio")
        
        # Validar formato de fechas
        fecha_insc = self.form_vars["fecha_insc_var"].get()
        fecha_exp = self.form_vars["fecha_exp_var"].get()
        
        try:
            if fecha_insc:
                datetime.strptime(fecha_insc, "%Y-%m-%d")
            if fecha_exp:
                datetime.strptime(fecha_exp, "%Y-%m-%d")
        except ValueError:
            errors.append("Las fechas deben estar en formato YYYY-MM-DD")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_memberships(self):
        """Busca membresías según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_memberships_list()
            return
        
        memberships = self.get_memberships_from_db()
        filtered = [
            m for m in memberships
            if (search_term in m['nombre_estudiante'].lower() or
                search_term in m['nombre_club'].lower() or
                search_term in m['estado_membresia'].lower() or
                search_term in m['rol'].lower())
        ]
        
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for membership in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = (f"{membership['nombre_estudiante']} en {membership['nombre_club']} - "
                   f"{membership['estado_membresia']} ({membership['rol']})")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda m=membership: self.load_membership_data(m)
            ).pack(side="right", padx=2)
        
        self.membership_count_label.configure(text=f"Membresías ({len(filtered)} encontradas)")
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_entry.delete(0, "end")
        self.update_memberships_list()
    
    def new_membership(self):
        """Prepara el formulario para nueva membresía"""
        self.clear_form()
    
    def save_membership(self):
        """Guarda los datos de la membresía"""
        if not self.validate_form():
            return
        
        membership_data = {
            "id_estudiante": self._get_student_id(self.form_vars["estudiante_var"].get()),
            "id_club": self._get_club_id(self.form_vars["club_var"].get()),
            "fecha_inscripcion": self.form_vars["fecha_insc_var"].get(),
            "fecha_expiracion": self.form_vars["fecha_exp_var"].get() or None,
            "estado_membresia": self.form_vars["estado_var"].get(),
            "rol": self.form_vars["rol_var"].get()
        }
        
        if self.current_membership:
            membership_data["id_membresia"] = self.current_membership["id_membresia"]
            success = self.save_membership_to_db(membership_data, is_update=True)
            action = "actualizada"
        else:
            success = self.save_membership_to_db(membership_data)
            action = "creada"
        
        if success:
            messagebox.showinfo("Éxito", f"Membresía {action} correctamente")
            self.update_memberships_list()
            self.clear_form()
    
    def delete_membership(self):
        """Elimina la membresía actual"""
        if not self.current_membership:
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar la membresía:\n\n"
            f"Estudiante: {self.current_membership['nombre_estudiante']}\n"
            f"Club: {self.current_membership['nombre_club']}\n"
            f"Rol: {self.current_membership['rol']}",
            icon="warning"
        )
        
        if confirmacion:
            success = self.delete_membership_from_db(self.current_membership["id_membresia"])
            
            if success:
                messagebox.showinfo("Éxito", "Membresía eliminada correctamente")
                self.update_memberships_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la membresía")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS DE BASE DE DATOS (COMENTADOS)
    # ======================

    def _get_student_id(self, student_name):
        """Obtiene ID de estudiante desde nombre (simulado)"""
        # En implementación real, harías una consulta a la base de datos
        # Ejemplo:
        # cursor = self.db_connection.cursor()
        # cursor.execute("SELECT id_estudiante FROM estudiantes WHERE CONCAT(nombre, ' ', appat, ' ', apmat) = %s", (student_name,))
        # result = cursor.fetchone()
        # return result[0] if result else None
        return 1  # Valor simulado para pruebas

    def _get_club_id(self, club_name):
        """Obtiene ID de club desde nombre (simulado)"""
        # Similar a _get_student_id pero para clubs
        return 1  # Valor simulado para pruebas

    def get_memberships_from_db(self):
        """OBTENER MEMBRESÍAS DESDE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = '''
                SELECT m.*, 
                CONCAT(e.nombre, ' ', e.appat, ' ', e.apmat) AS nombre_estudiante,
                c.nombre_club
                FROM membresias m
                JOIN estudiantes e ON m.id_estudiante = e.id_estudiante
                JOIN clubes c ON m.id_club = c.id_club
                ORDER BY nombre_estudiante, nombre_club
            '''
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar membresías:\n{str(e)}")
            return []
        """
        # Datos de ejemplo (eliminar en implementación real)
        return [
            {
                "id_membresia": 1,
                "id_estudiante": 1,
                "id_club": 1,
                "fecha_inscripcion": "2023-01-15",
                "fecha_expiracion": "2023-12-31",
                "estado_membresia": "Activa",
                "rol": "Miembro",
                "nombre_estudiante": "Juan Pérez López",
                "nombre_club": "Club de Programación"
            },
            {
                "id_membresia": 2,
                "id_estudiante": 2,
                "id_club": 2,
                "fecha_inscripcion": "2023-02-20",
                "fecha_expiracion": None,
                "estado_membresia": "En proceso",
                "rol": "Coordinador",
                "nombre_estudiante": "María García Sánchez",
                "nombre_club": "Club de Robótica"
            }
        ]

    def save_membership_to_db(self, membership_data, is_update=False):
        """GUARDAR MEMBRESÍA EN BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            
            if is_update:
                query = '''UPDATE membresias SET 
                          id_estudiante = %s, id_club = %s, 
                          fecha_inscripcion = %s, fecha_expiracion = %s,
                          estado_membresia = %s, rol = %s
                          WHERE id_membresia = %s'''
                params = (
                    membership_data['id_estudiante'],
                    membership_data['id_club'],
                    membership_data['fecha_inscripcion'],
                    membership_data['fecha_expiracion'],
                    membership_data['estado_membresia'],
                    membership_data['rol'],
                    membership_data['id_membresia']
                )
            else:
                query = '''INSERT INTO membresias (
                          id_estudiante, id_club, fecha_inscripcion,
                          fecha_expiracion, estado_membresia, rol
                          ) VALUES (%s, %s, %s, %s, %s, %s)'''
                params = (
                    membership_data['id_estudiante'],
                    membership_data['id_club'],
                    membership_data['fecha_inscripcion'],
                    membership_data['fecha_expiracion'],
                    membership_data['estado_membresia'],
                    membership_data['rol']
                )
            
            cursor.execute(query, params)
            self.db_connection.commit()
            return True
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al guardar membresía:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas

    def delete_membership_from_db(self, membership_id):
        """ELIMINAR MEMBRESÍA DE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            query = "DELETE FROM membresias WHERE id_membresia = %s"
            cursor.execute(query, (membership_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al eliminar membresía:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas
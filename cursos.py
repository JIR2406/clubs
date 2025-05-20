import customtkinter as ctk
from tkinter import messagebox

class CourseManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_course = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_courses_list()

    def _create_ui(self):
        """Construye la interfaz gráfica"""
        # Configuración del grid principal
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de búsqueda
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
        
        ctk.CTkLabel(search_frame, text="Buscar Cursos:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Código, nombre o departamento..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_courses())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_courses,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de cursos
        self._create_courses_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_courses_list(self):
        """Crea el panel de lista de cursos"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.course_count_label = ctk.CTkLabel(
            header_frame,
            text="Cursos (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.course_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nuevo",
            width=80,
            command=self.new_course
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
            text="Nuevo Curso",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario según la tabla cursos
        fields = [
            {"label": "Código Curso*", "var_name": "code_var", "required": True},
            {"label": "Nombre Curso*", "var_name": "name_var", "required": True},
            {"label": "Créditos", "var_name": "credits_var"},
            {"label": "Departamento", "var_name": "department_var"},
            {"label": "Descripción", "var_name": "description_var", "multiline": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            if field.get("multiline"):
                textbox = ctk.CTkTextbox(frame, height=80)
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
            command=self.save_course,
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
            command=self.delete_course,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_courses_list(self):
        """Actualiza la lista de cursos"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        courses = self.get_courses_from_db()
        self.course_count_label.configure(text=f"Cursos ({len(courses)})")
        
        if not courses:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron cursos",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for course in courses:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Formatear información para mostrar
            text = f"{course['codigo_curso']} - {course['nombre_curso']}"
            if course['creditos']:
                text += f" ({course['creditos']} créditos)"
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda c=course: self.load_course_data(c)
            ).pack(side="right", padx=2)
    
    def load_course_data(self, course):
        """Carga los datos de un curso en el formulario"""
        self.current_course = course
        self.form_title.configure(
            text=f"Editando Curso #{course['id_curso']}"
        )
        self.delete_btn.configure(state="normal")
        
        field_mapping = {
            "code_var": course.get("codigo_curso", ""),
            "name_var": course.get("nombre_curso", ""),
            "credits_var": str(course.get("creditos", "")),
            "department_var": course.get("departamento", ""),
            "description_var": course.get("descripcion", "")
        }
        
        for var_name, value in field_mapping.items():
            if var_name == "description_var":
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
        
        self.current_course = None
        self.form_title.configure(text="Nuevo Curso")
        self.delete_btn.configure(state="disabled")
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        required_fields = ["code_var", "name_var"]
        for field in required_fields:
            if not self.form_vars[field].get():
                field_name = field.replace("_var", "").replace("_", " ").title()
                errors.append(f"El campo {field_name} es obligatorio")
        
        # Validar que créditos sea numérico si existe
        credits = self.form_vars["credits_var"].get()
        if credits:
            try:
                int(credits)
            except ValueError:
                errors.append("Los créditos deben ser un número entero")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_courses(self):
        """Busca cursos según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_courses_list()
            return
        
        courses = self.get_courses_from_db()
        filtered = [
            c for c in courses
            if (search_term in c['codigo_curso'].lower() or
               search_term in c['nombre_curso'].lower() or
               search_term in (c['departamento'] or "").lower())
        ]
        
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for course in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = f"{course['codigo_curso']} - {course['nombre_curso']}"
            if course['creditos']:
                text += f" ({course['creditos']} créditos)"
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda c=course: self.load_course_data(c)
            ).pack(side="right", padx=2)
        
        self.course_count_label.configure(text=f"Cursos ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_entry.delete(0, "end")
        self.update_courses_list()
    
    def new_course(self):
        """Prepara el formulario para nuevo curso"""
        self.clear_form()
    
    def save_course(self):
        """Guarda los datos del curso"""
        if not self.validate_form():
            return
        
        course_data = {
            "codigo_curso": self.form_vars["code_var"].get(),
            "nombre_curso": self.form_vars["name_var"].get(),
            "descripcion": self.form_vars["description_var"].textbox.get("1.0", "end-1c") or None,
            "creditos": int(self.form_vars["credits_var"].get()) if self.form_vars["credits_var"].get() else None,
            "departamento": self.form_vars["department_var"].get() or None
        }
        
        if self.current_course:
            course_data["id_curso"] = self.current_course["id_curso"]
            success = self.save_course_to_db(course_data, is_update=True)
            action = "actualizado"
        else:
            success = self.save_course_to_db(course_data)
            action = "registrado"
        
        if success:
            messagebox.showinfo("Éxito", f"Curso {action} correctamente")
            self.update_courses_list()
            self.clear_form()
    
    def delete_course(self):
        """Elimina el curso actual"""
        if not self.current_course:
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar este curso?\n\n"
            f"Código: {self.current_course['codigo_curso']}\n"
            f"Nombre: {self.current_course['nombre_curso']}",
            icon="warning"
        )
        
        if confirmacion:
            success = self.delete_course_from_db(self.current_course["id_curso"])
            
            if success:
                messagebox.showinfo("Éxito", "Curso eliminado correctamente")
                self.update_courses_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el curso")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS DE BASE DE DATOS (COMENTADOS)
    # ======================

    def get_courses_from_db(self):
        """OBTENER CURSOS DESDE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = '''
                SELECT * FROM cursos
                ORDER BY nombre_curso
            '''
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cursos:\n{str(e)}")
            return []
        """
        # Datos de ejemplo (eliminar en implementación real)
        return [
            {
                "id_curso": 1,
                "codigo_curso": "PROG101",
                "nombre_curso": "Programación Básica",
                "descripcion": "Introducción a la programación con Python",
                "creditos": 4,
                "departamento": "Informática"
            },
            {
                "id_curso": 2,
                "codigo_curso": "BD202",
                "nombre_curso": "Bases de Datos",
                "descripcion": "Fundamentos de diseño y consulta de bases de datos",
                "creditos": 3,
                "departamento": "Informática"
            }
        ]

    def save_course_to_db(self, course_data, is_update=False):
        """GUARDAR CURSO EN BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            
            if is_update:
                query = '''UPDATE cursos SET 
                          codigo_curso = %s, nombre_curso = %s, 
                          descripcion = %s, creditos = %s,
                          departamento = %s
                          WHERE id_curso = %s'''
                params = (
                    course_data['codigo_curso'],
                    course_data['nombre_curso'],
                    course_data['descripcion'],
                    course_data['creditos'],
                    course_data['departamento'],
                    course_data['id_curso']
                )
            else:
                query = '''INSERT INTO cursos (
                          codigo_curso, nombre_curso, descripcion,
                          creditos, departamento
                          ) VALUES (%s, %s, %s, %s, %s)'''
                params = (
                    course_data['codigo_curso'],
                    course_data['nombre_curso'],
                    course_data['descripcion'],
                    course_data['creditos'],
                    course_data['departamento']
                )
            
            cursor.execute(query, params)
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al guardar curso:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas

    def delete_course_from_db(self, course_id):
        """ELIMINAR CURSO DE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            query = "DELETE FROM cursos WHERE id_curso = %s"
            cursor.execute(query, (course_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al eliminar curso:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class AcademicHistoryWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_record = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_records_list()

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
        
        ctk.CTkLabel(search_frame, text="Buscar Historial:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="ID Estudiante, Curso o Estado..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_records())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_records,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de registros
        self._create_records_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_records_list(self):
        """Crea el panel de lista de registros"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.record_count_label = ctk.CTkLabel(
            header_frame,
            text="Registros (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.record_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nuevo",
            width=80,
            command=self.new_record
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
            text="Nuevo Registro",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario según la tabla historial_academico
        fields = [
            {"label": "ID Estudiante*", "var_name": "student_id_var", "required": True},
            {"label": "ID Curso*", "var_name": "course_id_var", "required": True},
            {"label": "Calificación", "var_name": "grade_var"},
            {"label": "Fecha Inicio*", "var_name": "start_date_var", "required": True},
            {"label": "Fecha Fin", "var_name": "end_date_var"},
            {"label": "Periodo", "var_name": "period_var"},
            {"label": "Estado*", "var_name": "status_var", "required": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            if field["var_name"] == "status_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Aprobado", "Reprobado", "En curso", "Retirado"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
                var.set("En curso")
            elif field["var_name"] in ["start_date_var", "end_date_var"]:
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
            command=self.save_record,
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
            command=self.delete_record,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_records_list(self):
        """Actualiza la lista de registros"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        records = self.get_records_from_db()
        self.record_count_label.configure(text=f"Registros ({len(records)})")
        
        if not records:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron registros",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for record in records:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Formatear información para mostrar
            text = (f"Estudiante #{record['id_estudiante']} - Curso #{record['id_curso']} "
                   f"- {record['estado']} - Calif: {record['calificacion'] or 'N/A'}")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda r=record: self.load_record_data(r)
            ).pack(side="right", padx=2)
    
    def load_record_data(self, record):
        """Carga los datos de un registro en el formulario"""
        self.current_record = record
        self.form_title.configure(
            text=f"Editando Registro #{record['id_historial']}"
        )
        self.delete_btn.configure(state="normal")
        
        field_mapping = {
            "student_id_var": str(record.get("id_estudiante", "")),
            "course_id_var": str(record.get("id_curso", "")),
            "grade_var": str(record.get("calificacion", "")),
            "start_date_var": record.get("fecha_inicio", ""),
            "end_date_var": record.get("fecha_fin", ""),
            "period_var": record.get("periodo", ""),
            "status_var": record.get("estado", "En curso")
        }
        
        for var_name, value in field_mapping.items():
            self.form_vars[var_name].set(value)
    
    def clear_form(self):
        """Limpia el formulario"""
        for var in self.form_vars.values():
            var.set("")
        
        self.current_record = None
        self.form_title.configure(text="Nuevo Registro")
        self.delete_btn.configure(state="disabled")
        self.form_vars["status_var"].set("En curso")
        self.form_vars["start_date_var"].set(datetime.now().strftime("%Y-%m-%d"))
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        required_fields = ["student_id_var", "course_id_var", "start_date_var", "status_var"]
        for field in required_fields:
            if not self.form_vars[field].get():
                field_name = field.replace("_var", "").replace("_", " ").title()
                errors.append(f"El campo {field_name} es obligatorio")
        
        # Validar que los IDs sean numéricos
        try:
            int(self.form_vars["student_id_var"].get())
            int(self.form_vars["course_id_var"].get())
        except ValueError:
            errors.append("Los IDs de estudiante y curso deben ser números")
        
        # Validar formato de fechas
        date_fields = ["start_date_var", "end_date_var"]
        for field in date_fields:
            date_str = self.form_vars[field].get()
            if date_str:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    errors.append(f"La fecha {field.replace('_var', '')} debe estar en formato YYYY-MM-DD")
        
        # Validar calificación si existe
        grade = self.form_vars["grade_var"].get()
        if grade:
            try:
                grade_num = float(grade)
                if not (0 <= grade_num <= 10):
                    errors.append("La calificación debe estar entre 0 y 10")
            except ValueError:
                errors.append("La calificación debe ser un número válido")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_records(self):
        """Busca registros según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_records_list()
            return
        
        records = self.get_records_from_db()
        filtered = [
            r for r in records
            if (search_term in str(r['id_estudiante']).lower() or
               search_term in str(r['id_curso']).lower() or
               search_term in r['estado'].lower() or
               search_term in (r['periodo'] or "").lower())
        ]
        
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for record in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = (f"Estudiante #{record['id_estudiante']} - Curso #{record['id_curso']} "
                   f"- {record['estado']} - Calif: {record['calificacion'] or 'N/A'}")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda r=record: self.load_record_data(r)
            ).pack(side="right", padx=2)
        
        self.record_count_label.configure(text=f"Registros ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_entry.delete(0, "end")
        self.update_records_list()
    
    def new_record(self):
        """Prepara el formulario para nuevo registro"""
        self.clear_form()
    
    def save_record(self):
        """Guarda los datos del registro"""
        if not self.validate_form():
            return
        
        record_data = {
            "id_estudiante": int(self.form_vars["student_id_var"].get()),
            "id_curso": int(self.form_vars["course_id_var"].get()),
            "calificacion": float(self.form_vars["grade_var"].get()) if self.form_vars["grade_var"].get() else None,
            "fecha_inicio": self.form_vars["start_date_var"].get(),
            "fecha_fin": self.form_vars["end_date_var"].get() or None,
            "periodo": self.form_vars["period_var"].get() or None,
            "estado": self.form_vars["status_var"].get()
        }
        
        if self.current_record:
            record_data["id_historial"] = self.current_record["id_historial"]
            success = self.save_record_to_db(record_data, is_update=True)
            action = "actualizado"
        else:
            success = self.save_record_to_db(record_data)
            action = "registrado"
        
        if success:
            messagebox.showinfo("Éxito", f"Registro {action} correctamente")
            self.update_records_list()
            self.clear_form()
    
    def delete_record(self):
        """Elimina el registro actual"""
        if not self.current_record:
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar este registro?\n\n"
            f"Estudiante: #{self.current_record['id_estudiante']}\n"
            f"Curso: #{self.current_record['id_curso']}\n"
            f"Estado: {self.current_record['estado']}",
            icon="warning"
        )
        
        if confirmacion:
            success = self.delete_record_from_db(self.current_record["id_historial"])
            
            if success:
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.update_records_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS DE BASE DE DATOS (COMENTADOS)
    # ======================

    def get_records_from_db(self):
        """OBTENER REGISTROS DESDE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = '''
                SELECT h.*, 
                CONCAT(e.nombre, ' ', e.appat, ' ', e.apmat) AS nombre_estudiante,
                c.nombre_curso
                FROM historial_academico h
                JOIN estudiantes e ON h.id_estudiante = e.id_estudiante
                JOIN cursos c ON h.id_curso = c.id_curso
                ORDER BY h.fecha_inicio DESC
            '''
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros:\n{str(e)}")
            return []
        """
        # Datos de ejemplo (eliminar en implementación real)
        return [
            {
                "id_historial": 1,
                "id_estudiante": 101,
                "id_curso": 201,
                "calificacion": 8.5,
                "fecha_inicio": "2023-01-15",
                "fecha_fin": "2023-05-20",
                "periodo": "Primavera 2023",
                "estado": "Aprobado",
                "nombre_estudiante": "Juan Pérez López",
                "nombre_curso": "Programación Básica"
            },
            {
                "id_historial": 2,
                "id_estudiante": 102,
                "id_curso": 202,
                "calificacion": None,
                "fecha_inicio": "2023-08-20",
                "fecha_fin": None,
                "periodo": "Otoño 2023",
                "estado": "En curso",
                "nombre_estudiante": "María García Sánchez",
                "nombre_curso": "Base de Datos"
            }
        ]

    def save_record_to_db(self, record_data, is_update=False):
        """GUARDAR REGISTRO EN BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            
            if is_update:
                query = '''UPDATE historial_academico SET 
                          id_estudiante = %s, id_curso = %s, 
                          calificacion = %s, fecha_inicio = %s,
                          fecha_fin = %s, periodo = %s,
                          estado = %s
                          WHERE id_historial = %s'''
                params = (
                    record_data['id_estudiante'],
                    record_data['id_curso'],
                    record_data['calificacion'],
                    record_data['fecha_inicio'],
                    record_data['fecha_fin'],
                    record_data['periodo'],
                    record_data['estado'],
                    record_data['id_historial']
                )
            else:
                query = '''INSERT INTO historial_academico (
                          id_estudiante, id_curso, calificacion,
                          fecha_inicio, fecha_fin, periodo,
                          estado
                          ) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                params = (
                    record_data['id_estudiante'],
                    record_data['id_curso'],
                    record_data['calificacion'],
                    record_data['fecha_inicio'],
                    record_data['fecha_fin'],
                    record_data['periodo'],
                    record_data['estado']
                )
            
            cursor.execute(query, params)
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al guardar registro:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas

    def delete_record_from_db(self, record_id):
        """ELIMINAR REGISTRO DE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            query = "DELETE FROM historial_academico WHERE id_historial = %s"
            cursor.execute(query, (record_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al eliminar registro:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas
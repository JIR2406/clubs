import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PaymentManagementWindow:
    def __init__(self, root, app_manager):
        self.root = root
        self.app = app_manager
        self.current_payment = None
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Construir interfaz
        self._create_ui()
        
        # Cargar datos iniciales
        self.update_payments_list()

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
        
        ctk.CTkLabel(search_frame, text="Buscar Pagos:").pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Membresía, referencia o estado..."
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_payments())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_payments,
            width=100
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            width=100
        ).pack(side="left")
        
        # Lista de pagos
        self._create_payments_list()
        
        # Formulario de edición
        self._create_form()
        
        # Barra de estado
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Listo",
            anchor="w"
        )
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def _create_payments_list(self):
        """Crea el panel de lista de pagos"""
        self.list_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.list_frame.grid_propagate(False)
        
        # Cabecera
        header_frame = ctk.CTkFrame(self.list_frame)
        header_frame.pack(fill="x")
        
        self.payment_count_label = ctk.CTkLabel(
            header_frame,
            text="Pagos (0)",
            font=ctk.CTkFont(weight="bold")
        )
        self.payment_count_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            header_frame,
            text="+ Nuevo",
            width=80,
            command=self.new_payment
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
            text="Nuevo Pago",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.pack(pady=(0, 20))
        
        # Campos del formulario según la tabla pagos
        fields = [
            {"label": "Membresía*", "var_name": "membresia_var", "required": True},
            {"label": "Fecha Pago*", "var_name": "fecha_var", "required": True},
            {"label": "Monto*", "var_name": "monto_var", "required": True},
            {"label": "Método Pago*", "var_name": "metodo_var", "required": True},
            {"label": "Referencia", "var_name": "referencia_var"},
            {"label": "Periodo Cubierto", "var_name": "periodo_var"},
            {"label": "Estado*", "var_name": "estado_var", "required": True},
            {"label": "Notas", "var_name": "notas_var", "multiline": True}
        ]
        
        self.form_vars = {}
        
        for field in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            label_text = field["label"].replace("*", "") + (" *" if field.get("required") else "")
            ctk.CTkLabel(frame, text=label_text, width=120).pack(side="left")
            
            var = ctk.StringVar()
            
            if field["var_name"] == "metodo_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Efectivo", "Transferencia", "Tarjeta", "Beca"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] == "estado_var":
                ctk.CTkComboBox(
                    frame,
                    variable=var,
                    values=["Completo", "Pendiente", "Rechazado", "Reembolsado"],
                    state="readonly"
                ).pack(side="right", fill="x", expand=True)
            elif field["var_name"] == "fecha_var":
                ctk.CTkEntry(
                    frame,
                    textvariable=var,
                    placeholder_text="YYYY-MM-DD"
                ).pack(side="right", fill="x", expand=True)
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
            command=self.save_payment,
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
            command=self.delete_payment,
            fg_color="#dc3545",
            state="disabled"
        )
        self.delete_btn.pack(side="right")
    
    def return_to_menu(self):
        """Regresa al menú principal"""
        self.app.show_menu(self.app.current_user)
    
    def update_payments_list(self):
        """Actualiza la lista de pagos"""
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        payments = self.get_payments_from_db()
        self.payment_count_label.configure(text=f"Pagos ({len(payments)})")
        
        if not payments:
            ctk.CTkLabel(
                self.list_scroll,
                text="No se encontraron pagos",
                text_color="gray"
            ).pack(pady=20)
            return
        
        for payment in payments:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            # Formatear información para mostrar
            text = (f"Membresía #{payment['id_membresia']} - ${payment['monto']} "
                   f"({payment['metodo_pago']}) - {payment['estado_pago']}")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda p=payment: self.load_payment_data(p)
            ).pack(side="right", padx=2)
    
    def load_payment_data(self, payment):
        """Carga los datos de un pago en el formulario"""
        self.current_payment = payment
        self.form_title.configure(
            text=f"Editando Pago #{payment['id_pago']}"
        )
        self.delete_btn.configure(state="normal")
        
        field_mapping = {
            "membresia_var": str(payment.get("id_membresia", "")),
            "fecha_var": payment.get("fecha_pago", ""),
            "monto_var": str(payment.get("monto", "")),
            "metodo_var": payment.get("metodo_pago", "Efectivo"),
            "referencia_var": payment.get("referencia_pago", ""),
            "periodo_var": payment.get("periodo_cubierto", ""),
            "estado_var": payment.get("estado_pago", "Pendiente"),
            "notas_var": payment.get("notas", "")
        }
        
        for var_name, value in field_mapping.items():
            if var_name == "notas_var":
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
        
        self.current_payment = None
        self.form_title.configure(text="Nuevo Pago")
        self.delete_btn.configure(state="disabled")
        self.form_vars["fecha_var"].set(datetime.now().strftime("%Y-%m-%d"))
        self.form_vars["metodo_var"].set("Efectivo")
        self.form_vars["estado_var"].set("Pendiente")
    
    def validate_form(self):
        """Valida los campos del formulario"""
        errors = []
        
        required_fields = ["membresia_var", "fecha_var", "monto_var", "metodo_var", "estado_var"]
        for field in required_fields:
            if not self.form_vars[field].get():
                field_name = field.replace("_var", "").replace("_", " ").title()
                errors.append(f"El campo {field_name} es obligatorio")
        
        # Validar formato de fecha
        fecha = self.form_vars["fecha_var"].get()
        try:
            if fecha:
                datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            errors.append("La fecha debe estar en formato YYYY-MM-DD")
        
        # Validar que monto sea numérico
        try:
            float(self.form_vars["monto_var"].get())
        except ValueError:
            errors.append("El monto debe ser un valor numérico")
        
        if errors:
            messagebox.showerror("Errores en el formulario", "\n".join(errors))
            return False
        return True
    
    def search_payments(self):
        """Busca pagos según el criterio"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_payments_list()
            return
        
        payments = self.get_payments_from_db()
        filtered = [
            p for p in payments
            if (search_term in str(p['id_membresia']).lower() or
               search_term in p['referencia_pago'].lower() or
               search_term in p['estado_pago'].lower() or
               search_term in p['metodo_pago'].lower())
        ]
        
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
        
        for payment in filtered:
            frame = ctk.CTkFrame(self.list_scroll, height=45)
            frame.pack(fill="x", pady=2)
            
            text = (f"Membresía #{payment['id_membresia']} - ${payment['monto']} "
                   f"({payment['metodo_pago']}) - {payment['estado_pago']}")
            
            ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            ).pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(
                frame,
                text="Editar",
                width=60,
                command=lambda p=payment: self.load_payment_data(p)
            ).pack(side="right", padx=2)
        
        self.payment_count_label.configure(text=f"Pagos ({len(filtered)} encontrados)")
    
    def clear_search(self):
        """Limpia la búsqueda"""
        self.search_entry.delete(0, "end")
        self.update_payments_list()
    
    def new_payment(self):
        """Prepara el formulario para nuevo pago"""
        self.clear_form()
    
    def save_payment(self):
        """Guarda los datos del pago"""
        if not self.validate_form():
            return
        
        payment_data = {
            "id_membresia": int(self.form_vars["membresia_var"].get()),
            "fecha_pago": self.form_vars["fecha_var"].get(),
            "monto": float(self.form_vars["monto_var"].get()),
            "metodo_pago": self.form_vars["metodo_var"].get(),
            "referencia_pago": self.form_vars["referencia_var"].get() or None,
            "periodo_cubierto": self.form_vars["periodo_var"].get() or None,
            "estado_pago": self.form_vars["estado_var"].get(),
            "notas": self.form_vars["notas_var"].textbox.get("1.0", "end-1c") or None
        }
        
        if self.current_payment:
            payment_data["id_pago"] = self.current_payment["id_pago"]
            success = self.save_payment_to_db(payment_data, is_update=True)
            action = "actualizado"
        else:
            success = self.save_payment_to_db(payment_data)
            action = "registrado"
        
        if success:
            messagebox.showinfo("Éxito", f"Pago {action} correctamente")
            self.update_payments_list()
            self.clear_form()
    
    def delete_payment(self):
        """Elimina el pago actual"""
        if not self.current_payment:
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar este pago?\n\n"
            f"Membresía: #{self.current_payment['id_membresia']}\n"
            f"Monto: ${self.current_payment['monto']}\n"
            f"Fecha: {self.current_payment['fecha_pago']}",
            icon="warning"
        )
        
        if confirmacion:
            success = self.delete_payment_from_db(self.current_payment["id_pago"])
            
            if success:
                messagebox.showinfo("Éxito", "Pago eliminado correctamente")
                self.update_payments_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el pago")
    
    def cancel_edit(self):
        """Cancela la edición actual"""
        self.clear_form()

    # ======================
    # MÉTODOS DE BASE DE DATOS (COMENTADOS)
    # ======================

    def get_payments_from_db(self):
        """OBTENER PAGOS DESDE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = '''
                SELECT p.*, 
                CONCAT(e.nombre, ' ', e.appat, ' ', e.apmat) AS nombre_estudiante,
                c.nombre_club
                FROM pagos p
                JOIN membresias m ON p.id_membresia = m.id_membresia
                JOIN estudiantes e ON m.id_estudiante = e.id_estudiante
                JOIN clubes c ON m.id_club = c.id_club
                ORDER BY p.fecha_pago DESC
            '''
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pagos:\n{str(e)}")
            return []
        """
        # Datos de ejemplo (eliminar en implementación real)
        return [
            {
                "id_pago": 1,
                "id_membresia": 1,
                "fecha_pago": "2023-05-15",
                "monto": 150.00,
                "metodo_pago": "Transferencia",
                "referencia_pago": "TRF-12345",
                "periodo_cubierto": "Mayo 2023",
                "estado_pago": "Completo",
                "notas": "Pago completo del mes",
                "nombre_estudiante": "Juan Pérez López",
                "nombre_club": "Club de Programación"
            },
            {
                "id_pago": 2,
                "id_membresia": 2,
                "fecha_pago": "2023-06-20",
                "monto": 200.00,
                "metodo_pago": "Efectivo",
                "referencia_pago": "",
                "periodo_cubierto": "Junio 2023",
                "estado_pago": "Pendiente",
                "notas": "Pendiente de verificación",
                "nombre_estudiante": "María García Sánchez",
                "nombre_club": "Club de Robótica"
            }
        ]

    def save_payment_to_db(self, payment_data, is_update=False):
        """GUARDAR PAGO EN BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            
            if is_update:
                query = '''UPDATE pagos SET 
                          id_membresia = %s, fecha_pago = %s, 
                          monto = %s, metodo_pago = %s,
                          referencia_pago = %s, periodo_cubierto = %s,
                          estado_pago = %s, notas = %s
                          WHERE id_pago = %s'''
                params = (
                    payment_data['id_membresia'],
                    payment_data['fecha_pago'],
                    payment_data['monto'],
                    payment_data['metodo_pago'],
                    payment_data['referencia_pago'],
                    payment_data['periodo_cubierto'],
                    payment_data['estado_pago'],
                    payment_data['notas'],
                    payment_data['id_pago']
                )
            else:
                query = '''INSERT INTO pagos (
                          id_membresia, fecha_pago, monto,
                          metodo_pago, referencia_pago, periodo_cubierto,
                          estado_pago, notas
                          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                params = (
                    payment_data['id_membresia'],
                    payment_data['fecha_pago'],
                    payment_data['monto'],
                    payment_data['metodo_pago'],
                    payment_data['referencia_pago'],
                    payment_data['periodo_cubierto'],
                    payment_data['estado_pago'],
                    payment_data['notas']
                )
            
            cursor.execute(query, params)
            self.db_connection.commit()
            return True
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al guardar pago:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas

    def delete_payment_from_db(self, payment_id):
        """ELIMINAR PAGO DE BD (implementación comentada)"""
        """
        try:
            cursor = self.db_connection.cursor()
            query = "DELETE FROM pagos WHERE id_pago = %s"
            cursor.execute(query, (payment_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al eliminar pago:\n{str(e)}")
            return False
        """
        return True  # Simulación para pruebas
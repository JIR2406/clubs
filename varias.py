import customtkinter as ctk
from tkinter import messagebox

class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.menu_visible = True
        
        # Configuración del frame del menú
        self.configure(width=250, corner_radius=0, fg_color=("#f0f0f0", "#2b2b2b"))
        self.pack_propagate(False)
        self.pack(side="left", fill="y", padx=(0, 5))
        
        # Logo o título de la aplicación
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.logo_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        self.logo_label = ctk.CTkLabel(
            self.logo_frame, 
            text="Club Manager", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.logo_label.pack(fill="x", padx=10)
        
        # Separador
        ctk.CTkLabel(self, text="", height=2, fg_color=("#e0e0e0", "#3a3a3a")).pack(fill="x", pady=5)
        
        # Botones del menú
        menu_buttons = [
            {"text": "🏠 Gestión de Clubs", "command": self.mostrar_inicio},
            {"text": "👥 Gestión de Miembros", "command": self.mostrar_config},
            {"text": "💳 Gestión de Membresías", "command": self.mostrar_ventas},
            {"text": "⚙️ Configuración", "command": self.mostrar_configuracion},
            {"text": "❌ Cerrar Sesión", "command": self.cerrar_sesion}
        ]
        
        self.buttons = []
        for btn in menu_buttons:
            button = ctk.CTkButton(
                self,
                text=btn["text"],
                command=btn["command"],
                width=220,
                height=40,
                corner_radius=8,
                anchor="w",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color=("#e0e0e0", "#3a3a3a"),
                text_color=("#333333", "#f0f0f0")
            )
            button.pack(pady=5, padx=10)
            self.buttons.append(button)
        
        # Botón toggle del menú
        self.btn_toggle = ctk.CTkButton(
            self.parent, 
            text="☰", 
            command=self.toggle_menu, 
            width=40, 
            height=40,
            corner_radius=20,
            fg_color=("#f0f0f0", "#2b2b2b"),
            hover_color=("#e0e0e0", "#3a3a3a"),
            font=ctk.CTkFont(size=16)
        )
        self.btn_toggle.place(x=10, y=10)
        
        # Frame contenedor de las pantallas
        self.screen_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.screen_container.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Pantallas disponibles
        self.screens = {
            "inicio": self.create_inicio_screen(),
            "config": self.create_config_screen(),
            "ventas": self.create_ventas_screen(),
            "configuracion": self.create_configuracion_screen()
        }
        
        # Mostrar pantalla inicial
        self.show_screen("inicio")
        self.set_active_button(self.buttons[0])
        
        # Ajustar posición del toggle cuando cambia el tamaño de la ventana
        self.parent.bind("<Configure>", self.ajustar_posicion_toggle)
    
    def create_inicio_screen(self):
        """Crea y retorna la pantalla de gestión de clubs"""
        frame = ctk.CTkFrame(self.screen_container, fg_color="transparent")
        
        label = ctk.CTkLabel(
            frame, 
            text="Gestión de Clubs", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)
        
        # Aquí puedes añadir más widgets para esta pantalla
        btn_add = ctk.CTkButton(
            frame, 
            text="Agregar Club", 
            command=lambda: messagebox.showinfo("Info", "Agregar nuevo club")
        )
        btn_add.pack(pady=10)
        
        return frame
    
    def create_config_screen(self):
        """Crea y retorna la pantalla de gestión de miembros"""
        frame = ctk.CTkFrame(self.screen_container, fg_color="transparent")
        
        label = ctk.CTkLabel(
            frame, 
            text="Gestión de Miembros", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)
        
        # Aquí puedes añadir más widgets para esta pantalla
        btn_add = ctk.CTkButton(
            frame, 
            text="Agregar Miembro", 
            command=lambda: messagebox.showinfo("Info", "Agregar nuevo miembro")
        )
        btn_add.pack(pady=10)
        
        return frame
    
    def create_ventas_screen(self):
        """Crea y retorna la pantalla de gestión de membresías"""
        frame = ctk.CTkFrame(self.screen_container, fg_color="transparent")
        
        label = ctk.CTkLabel(
            frame, 
            text="Gestión de Membresías", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)
        
        # Aquí puedes añadir más widgets para esta pantalla
        btn_add = ctk.CTkButton(
            frame, 
            text="Agregar Membresía", 
            command=lambda: messagebox.showinfo("Info", "Agregar nueva membresía")
        )
        btn_add.pack(pady=10)
        
        return frame
    
    def create_configuracion_screen(self):
        """Crea y retorna la pantalla de configuración"""
        frame = ctk.CTkFrame(self.screen_container, fg_color="transparent")
        
        label = ctk.CTkLabel(
            frame, 
            text="Configuración del Sistema", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)
        
        # Aquí puedes añadir más widgets para esta pantalla
        theme_label = ctk.CTkLabel(frame, text="Tema:")
        theme_label.pack(pady=5)
        
        theme_option = ctk.CTkOptionMenu(
            frame, 
            values=["Claro", "Oscuro", "Sistema"],
            command=self.change_theme
        )
        theme_option.pack(pady=5)
        
        return frame
    
    def change_theme(self, choice):
        """Cambia el tema de la aplicación"""
        theme_map = {
            "Claro": "light",
            "Oscuro": "dark",
            "Sistema": "system"
        }
        ctk.set_appearance_mode(theme_map[choice])
    
    def show_screen(self, screen_name):
        """Muestra la pantalla seleccionada y oculta las demás"""
        for name, screen in self.screens.items():
            if name == screen_name:
                screen.pack(fill="both", expand=True)
            else:
                screen.pack_forget()
    
    def set_active_button(self, button):
        """Resalta el botón activo del menú"""
        for btn in self.buttons:
            btn.configure(
                fg_color="transparent",
                text_color=("#333333", "#f0f0f0")
            )
        
        button.configure(
            fg_color=("#3a7ebf", "#1f538d"),
            text_color=("#ffffff", "#ffffff")
        )
        self.active_button = button
    
    def mostrar_inicio(self):
        self.set_active_button(self.buttons[0])
        self.show_screen("inicio")
    
    def mostrar_config(self):
        self.set_active_button(self.buttons[1])
        self.show_screen("config")
    
    def mostrar_ventas(self):
        self.set_active_button(self.buttons[2])
        self.show_screen("ventas")
    
    def mostrar_configuracion(self):
        self.set_active_button(self.buttons[3])
        self.show_screen("configuracion")
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.parent.destroy()
    
    def toggle_menu(self):
        if self.menu_visible:
            self.pack_forget()
            self.menu_visible = False
            self.btn_toggle.configure(text="☰")
        else:
            self.pack(side="left", fill="y", padx=(0, 5))
            self.menu_visible = True
            self.btn_toggle.configure(text="☰")
        self.ajustar_posicion_toggle()
    
    def ajustar_posicion_toggle(self, event=None):
        if self.menu_visible:
            self.btn_toggle.place(x=260, y=10)
        else:
            self.btn_toggle.place(x=10, y=10)
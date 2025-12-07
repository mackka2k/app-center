import customtkinter as ctk
import threading
import json
import os
from tkinter import messagebox
from installer import AppInstaller

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AppCenterGUI(ctk.CTk):
    def __init__(self, config_path="apps.json"):
        super().__init__()

        self.title("App Center - Instant Installer")
        self.geometry("900x600")

        self.config_path = config_path
        self.installer = AppInstaller()
        self.categories = self._load_config()
        self.checkboxes = []
        self.selected_apps = []

        self._create_layout()
        self._load_categories_sidebar()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            messagebox.showerror("Error", f"Config file not found: {self.config_path}")
            return {}
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {e}")
            return {}

    def _create_layout(self):
        # Grid layout 1x2 used
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Categories", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=20)

        # Main Area (Scrollable)
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Select Apps")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Bottom Action Bar
        self.action_frame = ctk.CTkFrame(self, height=50)
        self.action_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.install_btn = ctk.CTkButton(self.action_frame, text="Install Selected", command=self.start_installation)
        self.install_btn.pack(side="right", padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.action_frame, text="Ready", anchor="w")
        self.status_label.pack(side="left", padx=20, pady=10)

    def _load_categories_sidebar(self):
        # For this simple view, we'll just list all apps in the main area grouped by headers
        # But we can add category filter buttons later if needed.
        # For now, let's just populate the main frame.
        self._populate_main_area()

    def _populate_main_area(self):
        row = 0
        for category, apps in self.categories.items():
            # Category Header
            cat_label = ctk.CTkLabel(self.main_frame, text=category.capitalize(), font=ctk.CTkFont(size=16, weight="bold"))
            cat_label.grid(row=row, column=0, sticky="w", padx=10, pady=(15, 5))
            row += 1

            # App Checkboxes
            for app in apps:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(self.main_frame, text=app['name'], variable=var)
                cb.grid(row=row, column=0, sticky="w", padx=20, pady=2)
                # Store reference to checkbox and app data
                self.checkboxes.append((cb, var, app))
                row += 1

    def start_installation(self):
        # Gather selected apps
        self.selected_apps = [app for cb, var, app in self.checkboxes if var.get()]
        
        if not self.selected_apps:
            messagebox.showinfo("Info", "No apps selected.")
            return

        # Disable button
        self.install_btn.configure(state="disabled", text="Installing...")
        
        # Start thread
        t = threading.Thread(target=self._run_install_process)
        t.start()

    def _run_install_process(self):
        total = len(self.selected_apps)
        for i, app in enumerate(self.selected_apps, 1):
            self.status_label.configure(text=f"Installing {i}/{total}: {app['name']}...")
            
            # We can't easily capture realtime stdout without more complex IPC, 
            # so we'll just run it and hope for the best, or modify installer to be callback-friendly.
            # For now, using the existing installer logic but we might miss error details in GUI.
            # Let's try to wrap it simply.
            try:
                self.installer._install_single_app(app['id'])
            except Exception as e:
                print(f"Error installing {app['name']}: {e}")

        self.status_label.configure(text="Installation Complete!")
        self.install_btn.configure(state="normal", text="Install Selected")
        messagebox.showinfo("Done", f"Finished processing {total} applications.")

if __name__ == "__main__":
    app = AppCenterGUI()
    app.mainloop()

import json
import json
import os
from typing import List, Dict, Any

class AppCenterUI:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.categories = self._load_config()

    def _load_config(self) -> Dict[str, List[Dict[str, str]]]:
        """Loads the app configuration from JSON file."""
        if not os.path.exists(self.config_path):
            print(f"Error: Config file not found at {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Failed to parse {self.config_path}")
            return {}

    def show_main_menu(self) -> List[Dict[str, str]]:
        """
        Displays the main menu and interactive selection.
        Returns a list of selected apps to install.
        """
        if not self.categories:
            print("No apps available.")
            return []

        selected_apps = []
        
        while True:
            self._clear_screen()
            print("=== App Center - Instant Installer ===")
            print("Select categories to browse (or 'all' to select individual apps from all categories):")
            
            category_names = list(self.categories.keys())
            for i, cat in enumerate(category_names, 1):
                print(f"{i}. {cat.capitalize()}")
            
            print("a. Install All Apps")
            print("q. Quit (or finish selection)")
            
            choice = input("\nEnter choice: ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == 'a':
                confirm = input("Are you sure you want to install ALL apps? (y/n): ").lower()
                if confirm == 'y':
                    for cat in self.categories.values():
                        selected_apps.extend(cat)
                    break
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(category_names):
                    cat_name = category_names[idx]
                    self._show_category_menu(cat_name, selected_apps)
            else:
                input("Invalid choice. Press Enter...")

        print(f"\nTotal apps selected: {len(selected_apps)}")
        if selected_apps:
            print("Selected apps:")
            for app in selected_apps:
                print(f" - {app['name']}")
            
            confirm = input("\nProceed with installation? (y/n): ").lower()
            if confirm != 'y':
                return []
                
        return selected_apps

    def _show_category_menu(self, category: str, selected_apps: List[Dict[str, str]]):
        """Shows apps in a specific category."""
        apps = self.categories[category]
        
        while True:
            self._clear_screen()
            print(f"=== Category: {category.capitalize()} ===")
            print("Select app number to toggle selection, or 'b' to go back.")
            
            for i, app in enumerate(apps, 1):
                is_selected = app in selected_apps
                status = "[x]" if is_selected else "[ ]"
                print(f"{i}. {status} {app['name']}")
                
            choice = input("\nEnter choice: ").strip().lower()
            
            if choice == 'b':
                break
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(apps):
                    app = apps[idx]
                    if app in selected_apps:
                        selected_apps.remove(app)
                    else:
                        selected_apps.append(app)
                else:
                    input("Invalid number. Press Enter...")
            
    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

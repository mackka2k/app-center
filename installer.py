import subprocess
import time

class AppInstaller:
    def __init__(self):
        self.winget_cmd = "winget"

    def install_apps(self, apps):
        """
        Installs a list of apps using winget.
        """
        total = len(apps)
        for i, app in enumerate(apps, 1):
            print(f"[{i}/{total}] Installing {app['name']}...")
            self._install_single_app(app['id'])
            print("-" * 40)
    
    def _install_single_app(self, app_id):
        """
        Installs a single app by ID.
        """
        try:
            # -e: Exact match
            # --silent: No interaction
            # --accept-package-agreements: Auto-accept agreements
            # --accept-source-agreements: Auto-accept source agreements
            cmd = [
                self.winget_cmd, "install",
                "-e", "--id", app_id,
                "--silent",
                "--accept-package-agreements",
                "--accept-source-agreements"
            ]
            
            # Run the command
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            print(f"Successfully installed {app_id}")
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {app_id}")
            print(f"Error: {e.stderr}")
        except FileNotFoundError:
            print("Error: 'winget' not found. Please ensure Windows App Installer is installed.")

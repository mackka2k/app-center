import argparse
from gui import AppCenterGUI

def main():
    parser = argparse.ArgumentParser(description="App Center - Instant App Installer")
    parser.add_argument("--config", default="apps.json", help="Path to configuration file")
    args = parser.parse_args()

    app = AppCenterGUI(config_path=args.config)
    app.mainloop()

if __name__ == "__main__":
    main()

import sys
from PyQt6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
import os

def load_stylesheet(app_instance, qss_file_path):
    """Loads an external QSS file and applies it to the application."""
    try:
        with open(qss_file_path, "r") as f:
            style_sheet = f.read()
            app_instance.setStyleSheet(style_sheet)
            print(f"Successfully loaded stylesheet from: {qss_file_path}")
    except FileNotFoundError:
        print(f"Warning: Stylesheet file not found at {qss_file_path}. Using default style.")
    except Exception as e:
        print(f"Error loading stylesheet: {e}")


def main() -> None:
    """
    Entry point for the application. Initializes the QApplication,
    displays the main window, and handles the app lifecycle.
    """
    app: QApplication = QApplication(sys.argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_file = os.path.join(script_dir, "nordic.qss")

    load_stylesheet(app, qss_file)

    # Create and show the main window
    window: MainWindow = MainWindow()
    window.show()

    # Exit the application when the event loop ends
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

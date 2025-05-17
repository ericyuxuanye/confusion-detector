import sys

from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main():
    """
    Entry point for the application. Initializes the QApplication,
    displays the main window, and handles the app lifecycle.
    """
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Exit the application when the event loop ends
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

"""
Entry point for the ProTranscriber application.
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import TranscriberApp

def main():
    """Initializes and runs the main PySide6 event loop."""
    app = QApplication(sys.argv)
    window = TranscriberApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
from app.main_window import WelcomeWindow
import sys
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    # Открываем приветственное окно
    window = WelcomeWindow()
    window.show()

    # Запуск главного цикла приложения
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

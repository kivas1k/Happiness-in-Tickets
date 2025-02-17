from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QPointF, QEasingCurve
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, \
    QTableWidget, QTableWidgetItem
from app.ticket_logic import read_and_analyze_tickets


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загружаем шрифт из файла. Это надо для всей визуальной части приложения
        font_path = "C:/Users/kivas1k/PycharmProjects/luck/assets/fonts/PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]  # Сохраняю шрифт, чтобы потом его использовать

        self.setWindowTitle("Happiness in Tickets")

        # Тут меняем размер окна на 4на3
        self.resize(1280, 1024)

        # Создаю основной виджет для окна
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout()

        # Приветственное сообщение для пользователя
        self.welcome_text = """
        Добро пожаловать в приложение "Счастье в билетах"!
        Это приложение предназначено для анализа счастливых билетов,
        вычисления статистики и проверки различных математических свойств.
        Загружайте файл с номерами билетов, и система проведет анализ,
        включая подсчет счастливых билетов, построение графиков и многое другое.
        """

        # Тут добавляю текст приветствия
        self.label = QLabel(self.welcome_text)
        self.label.setAlignment(Qt.AlignCenter)

        # Кнопка, которая запустит основной интерфейс
        self.start_button = QPushButton("Приступим")
        self.start_button.clicked.connect(self.show_main_interface)

        # Добавляю текст и кнопку на layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)

        # Применяю layout к основному виджету
        main_widget.setLayout(self.layout)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: #f5f5f5;
                font-family: {self.font_family}, Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }}
            QLabel {{
                color: #444;
                font-size: 16px;
                line-height: 1.6;
            }}
            QPushButton {{
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
            QVBoxLayout {{
                margin: 20px;
                padding: 20px;
                align-items: center;
            }}
        """)

    def show_main_interface(self):

        # Скрываю приветственный текст и кнопку, чтобы показать основной интерфейс
        self.label.setVisible(False)
        self.start_button.setVisible(False)

        # Гайд для пользователя, что делать дальше
        self.guide_text = """
        1. Нажмите 'Загрузить файл' чтобы выбрать файл с номерами билетов.
        2. После загрузки файла, таблицы отобразят все билеты и счастливые билеты.
        3. Проверьте результаты анализа для статистики и других свойств.
        """

        # Кнопка для загрузки файла с номерами билетов
        self.load_file_button = QPushButton("Загрузить файл")
        self.load_file_button.setEnabled(False)  # Отключаю кнопку, пока не пройдет 2 секу
        self.load_file_button.clicked.connect(self.choose_file_and_analyze)

        # Отображаю инструкцию
        self.guide_label = QLabel(self.guide_text)
        self.guide_label.setAlignment(Qt.AlignLeft)
        self.guide_label.setWordWrap(True)  # Разрешаю перенос строк

        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.layout.addWidget(self.guide_label)
        self.layout.addWidget(self.load_file_button)

        self.all_tickets_table = QTableWidget()
        self.layout.addWidget(self.all_tickets_table)

        self.lucky_tickets_table = QTableWidget()
        self.layout.addWidget(self.lucky_tickets_table)

        # Таймер для активации кнопки через 2 секу
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.enable_button)
        self.timer.start(2000)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: #f5f5f5;
                font-family: {self.font_family}, Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }}
            QLabel {{
                color: #444;
                font-size: 16px;
                line-height: 1.6;
            }}
            QPushButton {{
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
            }}
            QVBoxLayout {{
                margin: 20px;
                padding: 20px;
                align-items: center;
            }}
            QTableWidget {{
                width: 100%;
                border: 1px solid #ccc;
                margin-top: 20px;
                font-size: 14px;
                padding: 10px;
            }}
            QTableWidget::item {{
                padding: 5px;
                text-align: center;
            }}
            QHeaderView::section {{
                background-color: #007bff;
                color: white;
                padding: 10px;
                font-weight: bold;
            }}
        """)

    def enable_button(self):
        # Включаю кнопку загрузки файла после таймера
        self.load_file_button.setEnabled(True)
        self.timer.stop()

    def choose_file_and_analyze(self):
        # Скрываю инструкцию и отключаю кнопку, пока не выбрали файл
        self.guide_label.setVisible(False)
        self.load_file_button.setEnabled(False)

        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с билетами", "",
                                                   "Text Files (*.txt);;All Files (*)")

        if file_path:
            # Если файл выбран, выполняю анализ
            all_tickets, lucky_tickets = read_and_analyze_tickets(file_path)

            # Заполняю таблицы билетами
            self.fill_table(self.all_tickets_table, all_tickets)
            self.fill_table(self.lucky_tickets_table, lucky_tickets)

            # После анализа снова включаю кнопку
            self.load_file_button.setEnabled(True)
        else:
            # Если файл не выбран, показываю ошибку в таблице
            self.all_tickets_table.setRowCount(1)
            self.all_tickets_table.setColumnCount(1)
            self.all_tickets_table.setHorizontalHeaderLabels(["Ошибка"])
            self.all_tickets_table.setItem(0, 0, QTableWidgetItem("Файл не выбран."))

    def fill_table(self, table, tickets):
        # Функция для заполнения таблицы с билетами
        table.setRowCount(len(tickets))
        table.setColumnCount(2)  # Два столбца: Номер билета и его тип (Счастливый/Не счастливый)
        table.setHorizontalHeaderLabels(["Номер билета", "Тип"])

        for row, ticket in enumerate(tickets):
            table.setItem(row, 0, QTableWidgetItem(str(ticket)))
            table.setItem(row, 1, QTableWidgetItem("Счастливый" if self.is_lucky(ticket) else "Не счастливый"))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        # Отключаю редактирование ячеек, потому что они должны быть только для отображения
        table.setEditTriggers(QTableWidget.NoEditTriggers)

    def is_lucky(self, ticket):
        # Проверяю, является ли билет счастливым
        ticket_str = str(ticket)
        if len(ticket_str) == 6:
            first_half = sum(int(digit) for digit in ticket_str[:3])  # Сумма первой половины
            second_half = sum(int(digit) for digit in ticket_str[3:])  # Сумма второй половины
            return first_half == second_half  # Если суммы равны, билет счастливый
        return False


if __name__ == "__main__":
    app = QApplication([])
    window = WelcomeWindow()
    window.show()
    app.exec()

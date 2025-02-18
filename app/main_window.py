from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QTabWidget, QComboBox
)
from app.ticket_logic import (
    read_and_analyze_tickets,
    count_even_odd_tickets,
    count_lucky_tickets,
    is_lucky
)


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загружаем шрифт из файла
        font_path = "C:/Users/kivas1k/PycharmProjects/luck/assets/fonts/PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.setWindowTitle("Happiness in Tickets")
        self.showFullScreen()  # Запуск в полноэкранном режиме

        # Создаем центральный контейнер и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Добавляем кастомную панель управления окнами (title bar)
        self.title_bar = self.create_title_bar()
        self.main_layout.addWidget(self.title_bar)

        # Создаем QTabWidget для вкладок
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # Вкладка для анализа билетов
        self.analysis_tab = QWidget()
        self.analysis_layout = QVBoxLayout(self.analysis_tab)
        self.tabs.addTab(self.analysis_tab, "Анализ билетов")

        # Вкладка для настроек
        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.tabs.addTab(self.settings_tab, "Настройки")

        self.init_analysis_tab()
        self.init_settings_tab()

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
            }}
            /* Увеличиваем межстрочный интервал для многострочных меток */
            QLabel#welcomeLabel {{
                line-height: 1.8;
            }}
            /* Стилизация вкладок с 3D-эффектом */
            QTabBar::tab {{
                min-height: 40px;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop: 0 #E0E0E0, stop: 1 #A0A0A0);
                border: 1px solid #666666;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop: 0 #FFFFFF, stop: 1 #CCCCCC);
                border: 1px solid #666666;
                border-bottom: none;
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

    def create_title_bar(self):
        """Создает панель в верхней части окна с кнопками:
        свернуть, переключить режим и закрыть. Кнопки – это чистые квадраты (30×30)
        без текста внутри, с разными цветами и подсказками.
        """
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Метка с названием приложения слева
        title_label = QLabel("Happiness in Tickets")
        layout.addWidget(title_label)
        layout.addStretch()

        # Кнопка для сворачивания (минимизации) – жёлтый квадрат
        btn_minimize = QPushButton("")
        btn_minimize.setToolTip("Свернуть")
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.setStyleSheet("background-color: #FFBD2E; border: none; border-radius: 0;")
        btn_minimize.clicked.connect(self.showMinimized)
        layout.addWidget(btn_minimize)

        # Кнопка для переключения между полноэкранным и оконным режимом – зелёный квадрат
        self.btn_toggle = QPushButton("")
        self.btn_toggle.setToolTip("Перейти в оконный режим")
        self.btn_toggle.setFixedSize(30, 30)
        self.btn_toggle.setStyleSheet("background-color: #28C940; border: none; border-radius: 0;")
        self.btn_toggle.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(self.btn_toggle)

        # Кнопка для закрытия приложения – красный квадрат
        btn_close = QPushButton("")
        btn_close.setToolTip("Закрыть")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("background-color: #FF5F57; border: none; border-radius: 0;")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        return title_bar

    def toggle_fullscreen(self):
        """
        Переключает режим между полноэкранным и оконным.
        Обновляет подсказку кнопки в зависимости от текущего режима.
        """
        if self.isFullScreen():
            self.showNormal()
            self.btn_toggle.setToolTip("Перейти в полноэкранный режим")
        else:
            self.showFullScreen()
            self.btn_toggle.setToolTip("Перейти в оконный режим")

    def init_analysis_tab(self):
        """Инициализация вкладки для анализа билетов."""

        self.welcome_text = """
        <p style="line-height:1.8;">
        Добро пожаловать в приложение "Счастье в билетах"!<br>
        Это приложение предназначено для анализа счастливых билетов, вычисления статистики<br>
        и проверки различных математических свойств.<br>
        Загружайте файл с номерами билетов, и система проведет анализ,<br>
        включая подсчет счастливых билетов, построение графиков и многое другое.
        </p>
        """
        self.welcome_label = QLabel(self.welcome_text)
        self.welcome_label.setObjectName("welcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.analysis_layout.addWidget(self.welcome_label)

        # Кнопка для начала работы
        self.start_button = QPushButton("Приступим")
        self.start_button.clicked.connect(self.show_main_interface)
        self.analysis_layout.addWidget(self.start_button)

    def show_main_interface(self):
        """Переход к основному интерфейсу анализа после приветственного экрана."""
        self.welcome_label.hide()
        self.start_button.hide()

        # Инструкции для пользователя
        self.guide_text = """
        1. Нажмите 'Загрузить файл' чтобы выбрать файл с номерами билетов.<br>
        2. После загрузки файла, кнопки будут активны для подсчета статистики.<br>
        3. Выбирайте кнопки для получения результатов анализа.
        """
        self.guide_label = QLabel(self.guide_text)
        self.guide_label.setAlignment(Qt.AlignLeft)
        self.guide_label.setWordWrap(True)
        self.analysis_layout.addWidget(self.guide_label)

        # Кнопка для загрузки файла с билетами
        self.load_file_button = QPushButton("Загрузить файл")
        self.load_file_button.clicked.connect(self.choose_file_and_analyze)
        self.analysis_layout.addWidget(self.load_file_button)

        self.count_even_button = QPushButton("Посчитать четные билеты")
        self.count_odd_button = QPushButton("Посчитать нечетные билеты")
        self.count_lucky_button = QPushButton("Посчитать счастливые билеты")

        self.count_even_timer = QTimer()
        self.count_even_timer.timeout.connect(lambda: self.count_even_button.setEnabled(True))

        self.count_odd_timer = QTimer()
        self.count_odd_timer.timeout.connect(lambda: self.count_odd_button.setEnabled(True))

        self.count_lucky_timer = QTimer()
        self.count_lucky_timer.timeout.connect(lambda: self.count_lucky_button.setEnabled(True))

        self.count_even_button.clicked.connect(self.count_even_tickets)
        self.count_odd_button.clicked.connect(self.count_odd_tickets)
        self.count_lucky_button.clicked.connect(self.count_lucky_tickets)

        self.analysis_layout.addWidget(self.count_even_button)
        self.analysis_layout.addWidget(self.count_odd_button)
        self.analysis_layout.addWidget(self.count_lucky_button)

        self.all_tickets_table = QTableWidget()
        self.analysis_layout.addWidget(self.all_tickets_table)

        self.lucky_tickets_table = QTableWidget()
        self.analysis_layout.addWidget(self.lucky_tickets_table)

    def choose_file_and_analyze(self):
        """Открывает диалог выбора файла и запускает анализ билетов с помощью функций из ticket_logic."""
        self.guide_label.hide()
        self.load_file_button.setEnabled(False)

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл с билетами", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            all_tickets, lucky_tickets = read_and_analyze_tickets(file_path)

            self.fill_table(self.all_tickets_table, all_tickets)
            self.fill_table(self.lucky_tickets_table, lucky_tickets)

            self.load_file_button.setEnabled(True)
            self.count_even_button.setEnabled(True)
            self.count_odd_button.setEnabled(True)
            self.count_lucky_button.setEnabled(True)

    def fill_table(self, table, tickets):
        """Заполняет указанную таблицу данными билетов."""
        table.setRowCount(len(tickets))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Номер билета", "Тип"])

        for row, ticket in enumerate(tickets):
            table.setItem(row, 0, QTableWidgetItem(str(ticket)))
            table.setItem(row, 1, QTableWidgetItem("Счастливый" if is_lucky(ticket) else "Не счастливый"))

        table.resizeColumnsToContents()

    def count_even_tickets(self):
        """Подсчет четных билетов."""
        self.count_even_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        even_count = count_even_odd_tickets(all_tickets)[0]
        self.show_result(f"Четных билетов: {even_count}")
        self.count_even_timer.start(2000)

    def count_odd_tickets(self):
        """Подсчет нечетных билетов."""
        self.count_odd_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        odd_count = count_even_odd_tickets(all_tickets)[1]
        self.show_result(f"Нечетных билетов: {odd_count}")
        self.count_odd_timer.start(2000)

    def count_lucky_tickets(self):
        """Подсчет счастливых билетов."""
        self.count_lucky_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        lucky_count = count_lucky_tickets(all_tickets)
        self.show_result(f"Счастливых билетов: {lucky_count}")
        self.count_lucky_timer.start(2000)

    def show_result(self, result_text):
        """Отображает результат анализа в виде метки."""
        result_label = QLabel(result_text)
        self.analysis_layout.addWidget(result_label)

    def get_all_tickets_from_table(self):
        """Извлекает все номера билетов из таблицы."""
        tickets = []
        for row in range(self.all_tickets_table.rowCount()):
            ticket = self.all_tickets_table.item(row, 0).text()
            tickets.append(ticket)
        return tickets

    def init_settings_tab(self):
        """Инициализация вкладки с настройками (изменение разрешения окна)."""
        resolution_label = QLabel("Выберите разрешение:")
        self.settings_layout.addWidget(resolution_label)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "Full Screen", "1280x1024", "1920x1080", "1024x768", "800x600"
        ])
        self.settings_layout.addWidget(self.resolution_combo)

        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_resolution)
        self.settings_layout.addWidget(apply_button)

        self.settings_layout.addStretch()

    def apply_resolution(self):
        """Применяет выбранное разрешение к окну."""
        resolution = self.resolution_combo.currentText()
        if resolution == "Full Screen":
            self.showFullScreen()
            self.btn_toggle.setToolTip("Перейти в полноэкранный режим")
        else:
            self.showNormal()
            width, height = map(int, resolution.split('x'))
            self.resize(width, height)
            self.btn_toggle.setToolTip("Перейти в оконный режим")


if __name__ == "__main__":
    app = QApplication([])
    window = WelcomeWindow()
    window.show()
    app.exec()

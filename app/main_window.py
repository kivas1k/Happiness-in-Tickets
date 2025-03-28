from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontDatabase
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QTabWidget, QComboBox
)
from app.ticket_logic import (
    read_and_analyze_tickets,
    count_even_odd_tickets,
    count_lucky_tickets,
    is_lucky,
    count_palindromic_tickets,
    count_prime_tickets,
    count_divisible_tickets,
    is_cube,is_square,is_nth_power,
    find_lucky_ticket_intervals,
    calculate_lucky_density
)

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        font_path = "C:/Users/kivas1k/PycharmProjects/luck/assets/fonts/PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.setWindowTitle("Happiness in Tickets")
        self.showFullScreen()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = self.create_title_bar()
        self.main_layout.addWidget(self.title_bar)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.analysis_tab = QWidget()
        self.analysis_layout = QVBoxLayout(self.analysis_tab)
        self.tabs.addTab(self.analysis_tab, "Анализ билетов")

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
            QLabel#welcomeLabel {{
                line-height: 1.8;
            }}
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
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
                margin: 10px;       
                min-width: 120px; 
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
        свернуть, переключить режим и закрыть.
        """
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        title_label = QLabel("Happiness in Tickets")
        layout.addWidget(title_label)
        layout.addStretch()

        # Ж
        btn_minimize = QPushButton("")
        btn_minimize.setToolTip("Свернуть")
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.setStyleSheet("background-color: #FFBD2E; border: none; border-radius: 0;")
        btn_minimize.clicked.connect(self.showMinimized)
        layout.addWidget(btn_minimize)

        # З
        self.btn_toggle = QPushButton("")
        self.btn_toggle.setToolTip("Перейти в оконный режим")
        self.btn_toggle.setFixedSize(30, 30)
        self.btn_toggle.setStyleSheet("background-color: #28C940; border: none; border-radius: 0;")
        self.btn_toggle.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(self.btn_toggle)

        # К
        btn_close = QPushButton("")
        btn_close.setToolTip("Закрыть")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("background-color: #FF5F57; border: none; border-radius: 0;")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        return title_bar

    def toggle_fullscreen(self):
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

        self.start_button = QPushButton("Приступим")
        self.start_button.clicked.connect(self.show_main_interface)
        self.analysis_layout.addWidget(self.start_button)

    def show_main_interface(self):
        """Переход к основному интерфейсу анализа."""
        self.welcome_label.hide()
        self.start_button.hide()

        # Инструкция

        self.guide_text = """
        1. Нажмите 'Загрузить файл' чтобы выбрать файл с номерами билетов.<br>
        2. После загрузки файла, кнопки будут активны для подсчета статистики.<br>
        3. Выбирайте кнопки для получения результатов анализа.
        """

        self.guide_label = QLabel(self.guide_text)
        self.guide_label.setAlignment(Qt.AlignLeft)
        self.guide_label.setWordWrap(True)
        self.analysis_layout.addWidget(self.guide_label)

        self.load_file_button = QPushButton("Загрузить файл")
        self.load_file_button.clicked.connect(self.choose_file_and_analyze)
        self.analysis_layout.addWidget(self.load_file_button)

        button_row1 = QHBoxLayout()
        button_row2 = QHBoxLayout()
        button_row3 = QHBoxLayout()
        button_row4 = QHBoxLayout()
        button_row5 = QHBoxLayout()

        self.count_even_button = QPushButton("Посчитать четные билеты")
        self.count_odd_button = QPushButton("Посчитать нечетные билеты")
        button_row1.addWidget(self.count_even_button)
        button_row1.addWidget(self.count_odd_button)

        self.count_lucky_button = QPushButton("Посчитать счастливые билеты")
        self.count_palindrome_button = QPushButton("Посчитать палиндромные билеты")
        button_row2.addWidget(self.count_lucky_button)
        button_row2.addWidget(self.count_palindrome_button)

        self.count_prime_button = QPushButton("Посчитать простые билеты")
        self.count_divisible_button = QPushButton("Билеты, где одна половина делится на другую")
        button_row3.addWidget(self.count_prime_button)
        button_row3.addWidget(self.count_divisible_button)

        self.count_square_button = QPushButton("Проверить квадрат числа")
        self.count_cube_button = QPushButton("Проверить куб числа")
        self.count_power_button = QPushButton("Проверить степень числа")
        button_row4.addWidget(self.count_square_button)
        button_row4.addWidget(self.count_cube_button)
        button_row4.addWidget(self.count_power_button)

        self.count_find_lucky_ticket_intervals_button = QPushButton("Найти макс. и мин. промежутки")
        button_row5.addWidget(self.count_find_lucky_ticket_intervals_button)
        self.plot_density_button = QPushButton("Построить график плотности")
        button_row5.addWidget(self.plot_density_button)

        self.analysis_layout.addLayout(button_row1)
        self.analysis_layout.addLayout(button_row2)
        self.analysis_layout.addLayout(button_row3)
        self.analysis_layout.addLayout(button_row4)
        self.analysis_layout.addLayout(button_row5)

        self.reset_button = QPushButton("Сбросить всю историю запросов")
        self.analysis_layout.addWidget(self.reset_button)

        self.count_even_timer = QTimer()
        self.count_even_timer.timeout.connect(lambda: self.count_even_button.setEnabled(True))

        self.count_odd_timer = QTimer()
        self.count_odd_timer.timeout.connect(lambda: self.count_odd_button.setEnabled(True))

        self.count_lucky_timer = QTimer()
        self.count_lucky_timer.timeout.connect(lambda: self.count_lucky_button.setEnabled(True))

        self.count_palindrome_timer = QTimer()
        self.count_palindrome_timer.timeout.connect(lambda: self.count_palindrome_button.setEnabled(True))

        self.count_prime_timer = QTimer()
        self.count_prime_timer.timeout.connect(lambda: self.count_prime_button.setEnabled(True))

        self.count_divisible_timer = QTimer()
        self.count_divisible_timer.timeout.connect(lambda: self.count_divisible_button.setEnabled(True))

        self.count_square_timer = QTimer()
        self.count_square_timer.timeout.connect(lambda: self.count_square_button.setEnabled(True))

        self.count_cube_timer = QTimer()
        self.count_cube_timer.timeout.connect(lambda: self.count_cube_button.setEnabled(True))

        self.count_power_timer = QTimer()
        self.count_power_timer.timeout.connect(lambda: self.count_power_button.setEnabled(True))

        self.plot_density_timer = QTimer()
        self.plot_density_timer.timeout.connect(lambda: self.plot_density_button.setEnabled(True))

        self.count_find_lucky_ticket_intervals_timer = QTimer()
        self.count_find_lucky_ticket_intervals_timer.timeout.connect(
            lambda: self.count_find_lucky_ticket_intervals_button.setEnabled(True))

        self.count_even_button.clicked.connect(self.count_even_tickets)
        self.count_odd_button.clicked.connect(self.count_odd_tickets)
        self.count_lucky_button.clicked.connect(self.count_lucky_tickets)
        self.count_palindrome_button.clicked.connect(self.count_palindromic_tickets)
        self.count_prime_button.clicked.connect(self.count_prime_tickets)
        self.count_divisible_button.clicked.connect(self.count_divisible_tickets)
        self.plot_density_button.clicked.connect(self.plot_lucky_density)

        self.count_square_button.clicked.connect(self.check_square_tickets)
        self.count_cube_button.clicked.connect(self.check_cube_tickets)
        self.count_power_button.clicked.connect(self.check_power_tickets)

        self.count_find_lucky_ticket_intervals_button.clicked.connect(self.count_find_lucky_ticket_intervals)

        self.reset_button.clicked.connect(self.reset_all_data)

        self.all_tickets_table = QTableWidget()
        self.analysis_layout.addWidget(self.all_tickets_table)

        self.lucky_tickets_table = QTableWidget()
        self.analysis_layout.addWidget(self.lucky_tickets_table)

    def show_error(self, message):
        """Отображает сообщение об ошибке с красным цветом текста."""
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red; font-weight: bold;")
        self.analysis_layout.addWidget(error_label)

    def choose_file_and_analyze(self):
        """Открывает диалог выбора файла и запускает анализ билетов."""
        self.guide_label.hide()
        self.load_file_button.setEnabled(False)

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл с билетами", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            all_tickets, lucky_tickets = read_and_analyze_tickets(file_path)

            if len(all_tickets) == 0:
                self.show_error(
                    "Ошибка загрузки файла. Проверьте формат данных (файл должен содержать шестизначные числа).")
                self.load_file_button.setEnabled(True)
                return

            self.fill_table(self.all_tickets_table, all_tickets)
            self.fill_table(self.lucky_tickets_table, lucky_tickets)

            self.load_file_button.setEnabled(True)
            self.count_even_button.setEnabled(True)
            self.count_odd_button.setEnabled(True)
            self.count_lucky_button.setEnabled(True)
            self.count_palindrome_button.setEnabled(True)
            self.count_prime_button.setEnabled(True)
            self.count_divisible_button.setEnabled(True)
            self.count_square_button.setEnabled(True)
            self.count_cube_button.setEnabled(True)
            self.count_power_button.setEnabled(True)
            self.count_find_lucky_ticket_intervals_button.setEnabled(True)
            self.plot_density_button.setEnabled(True)

        self.load_file_button.setEnabled(True)

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

    def count_palindromic_tickets(self):
        """Подсчет палиндромных билетов."""
        self.count_palindrome_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        palindromic_count = count_palindromic_tickets(all_tickets)
        self.show_result(f"Палиндромных билетов: {palindromic_count}")
        self.count_palindrome_timer.start(2000)

    def count_prime_tickets(self):
        """Подсчет простых билетов."""
        self.count_prime_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        prime_count = count_prime_tickets(all_tickets)
        self.show_result(f"Простых билетов: {prime_count}")
        self.count_prime_timer.start(2000)

    def count_divisible_tickets(self):
        """Подсчет билетов, у которых одна половина делится на другую."""
        self.count_divisible_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        divisible_count = count_divisible_tickets(all_tickets)
        self.show_result(f"Билетов с делением одной половины на другую: {divisible_count}")
        QTimer.singleShot(2000, lambda: self.count_divisible_button.setEnabled(True))

    def check_square_tickets(self):
        """Проверяет, является ли номер билета квадратом числа."""
        self.count_square_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        square_tickets = [ticket for ticket in all_tickets if is_square(ticket)]
        self.show_result(f"Билетов, являющихся квадратом числа: {len(square_tickets)}")
        self.count_square_timer.start(2000)

    def check_cube_tickets(self):
        """Проверяет, является ли номер билета кубом числа."""
        self.count_cube_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        cube_tickets = [ticket for ticket in all_tickets if is_cube(ticket)]
        self.show_result(f"Билетов, являющихся кубом числа: {len(cube_tickets)}")
        self.count_cube_timer.start(2000)

    def check_power_tickets(self):
        """Проверяет, является ли номер билета n-ой степенью числа."""
        self.count_power_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        n, ok = QInputDialog.getInt(self, "Введите степень", "Введите степень n:", 2, 1, 100)
        if ok:
            power_tickets = [ticket for ticket in all_tickets if is_nth_power(ticket, n)]
            self.show_result(f"Билетов, являющихся {n}-ой степенью числа: {len(power_tickets)}")
        self.count_power_timer.start(2000)

    def count_find_lucky_ticket_intervals(self):
        """Находит и отображает самый короткий и самый длинный промежуток между счастливыми билетами."""
        self.count_find_lucky_ticket_intervals_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        lucky_tickets = [ticket for ticket in all_tickets if is_lucky(ticket)]

        if len(lucky_tickets) < 2:
            self.show_result("Недостаточно счастливых билетов для определения промежутков.")
        else:
            min_interval, max_interval = find_lucky_ticket_intervals(lucky_tickets)
            self.show_result(f"Самый короткий промежуток: {min_interval}, Самый длинный промежуток: {max_interval}")

        self.count_find_lucky_ticket_intervals_timer.start(2000)

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

    def reset_all_data(self):
        """Сбрасывает все данные: очищает таблицы, результаты и активирует кнопки одновременно."""

        self.count_even_button.setEnabled(False)
        self.count_odd_button.setEnabled(False)
        self.count_lucky_button.setEnabled(False)
        self.count_palindrome_button.setEnabled(False)
        self.count_prime_button.setEnabled(False)
        self.count_divisible_button.setEnabled(False)
        self.count_square_button.setEnabled(False)
        self.count_cube_button.setEnabled(False)
        self.count_power_button.setEnabled(False)
        self.count_find_lucky_ticket_intervals_button.setEnabled(False)

        for i in reversed(range(self.analysis_layout.count())):
            widget = self.analysis_layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget != self.guide_label:
                widget.deleteLater()

        QTimer.singleShot(2000, self.enable_all_buttons)

    def enable_all_buttons(self):
        """Включает все кнопки одновременно после сброса."""
        self.count_even_button.setEnabled(True)
        self.count_odd_button.setEnabled(True)
        self.count_lucky_button.setEnabled(True)
        self.count_palindrome_button.setEnabled(True)
        self.count_prime_button.setEnabled(True)
        self.count_divisible_button.setEnabled(True)
        self.count_square_button.setEnabled(True)
        self.count_cube_button.setEnabled(True)
        self.count_power_button.setEnabled(True)
        self.count_find_lucky_ticket_intervals_button.setEnabled(True)

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

    def plot_lucky_density(self):
        self.plot_density_button.setEnabled(False)
        all_tickets = self.get_all_tickets_from_table()
        if not all_tickets:
            self.show_result("Нет данных для построения графика.")
            self.plot_density_timer.start(2000)
            return

        from app.ticket_logic import calculate_lucky_density
        bin_centers, densities, bin_edges = calculate_lucky_density(all_tickets)

        if not bin_centers.size:
            self.show_result("Недостаточно данных для построения графика.")
            self.plot_density_timer.start(2000)
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=bin_centers, y=densities, ax=ax, palette="Blues_d", alpha=0.8)

        labels = [f"{int(bin_edges[i]):06d}-{int(bin_edges[i + 1]) - 1:06d}" for i in range(len(bin_edges) - 1)]
        ax.set_xticks(range(len(bin_centers)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title("Плотность счастливых билетов по диапазонам номеров")
        ax.set_xlabel("Диапазон номеров")
        ax.set_ylabel("Доля счастливых билетов")
        plt.tight_layout()

        plot_window = QMainWindow(self)
        plot_window.setWindowTitle("График плотности")
        plot_window.setCentralWidget(FigureCanvas(fig))
        plot_window.resize(1000, 600)
        plot_window.show()
        self.plot_density_timer.start(2000)

if __name__ == "__main__":
    app = QApplication([])
    window = WelcomeWindow()
    window.show()
    app.exec()

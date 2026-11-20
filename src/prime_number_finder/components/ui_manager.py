from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class UIManager:
    def __init__(self, window: QMainWindow, config: dict, themes: dict):
        self.window = window
        self.config = config
        self.themes = themes

        self.iterate_button = None
        self.most_recent_number_text = None
        self.most_recent_number = None
        self.most_recent_prime_text = None
        self.most_recent_prime = None
        self.check_button = None
        self.check_input = None
        self.theme_toggle = None

    def build_ui(self):
        self.window.setWindowTitle(self.config["window_title"])
        self.window.setFixedSize(
            self.config["window_size"]["width"], self.config["window_size"]["height"]
        )

        self.iterate_button = QPushButton("Iterate")

        self.most_recent_number_text = QLabel(
            "Most recent number checked: ", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.most_recent_number_text.setFixedWidth(
            self.config["input_widgets"]["width"]
        )

        self.most_recent_number = QLabel(alignment=Qt.AlignmentFlag.AlignRight)

        self.most_recent_prime_text = QLabel(
            "Most recent prime found: ", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.most_recent_prime_text.setFixedWidth(self.config["input_widgets"]["width"])

        self.most_recent_prime = QLabel(alignment=Qt.AlignmentFlag.AlignRight)

        self.check_button = QPushButton("Check for Primality")
        self.check_button.setFixedWidth(self.config["input_widgets"]["width"])

        self.check_input = QLineEdit()
        self.check_input.setValidator(QIntValidator(bottom=0))
        self.check_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.theme_toggle = QPushButton("Dark")
        self.theme_toggle.setFixedWidth(self.config["input_widgets"]["width"])

        page = QVBoxLayout()
        iterate = QGridLayout()
        numbers = QGridLayout()
        primes = QGridLayout()
        checks = QGridLayout()

        iterate.addWidget(self.theme_toggle, 0, 0, 1, 1)
        iterate.addWidget(self.iterate_button, 0, 1, 1, 1)

        numbers.addWidget(self.most_recent_number_text, 0, 0, 1, 1)
        numbers.addWidget(self.most_recent_number, 0, 1, 1, 2)

        primes.addWidget(self.most_recent_prime_text, 0, 0, 1, 1)
        primes.addWidget(self.most_recent_prime, 0, 1, 1, 2)

        checks.addWidget(self.check_button, 0, 0, 1, 1)
        checks.addWidget(self.check_input, 0, 1, 1, 2)

        page.addLayout(iterate)
        page.addLayout(numbers)
        page.addLayout(primes)
        page.addLayout(checks)

        gui = QWidget()
        gui.setLayout(page)
        self.window.setCentralWidget(gui)

    def apply_theme(self, theme_name: str):
        theme = self.themes[theme_name]
        general = self.themes["general"]

        main_stylesheet = f"""
            background-color: {theme["background-color"]};
            color: {theme["color"]};
            border: {theme["border"]};
            border-radius: {general["border-radius"]};
            padding: {general["padding"]};
        """
        widget_stylesheet = f"""
            background-color: {theme["widget-background-color"]};
        """

        self.window.setStyleSheet(main_stylesheet)

        for widget in [
            self.iterate_button,
            self.most_recent_number_text,
            self.most_recent_number,
            self.most_recent_prime_text,
            self.most_recent_prime,
            self.check_button,
            self.check_input,
            self.theme_toggle,
        ]:
            widget.setStyleSheet(widget_stylesheet)

        if theme_name == "dark":
            self.theme_toggle.setText("Dark")
        else:
            self.theme_toggle.setText("Light")

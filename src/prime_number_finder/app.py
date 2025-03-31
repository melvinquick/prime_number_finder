"""
Python program for finding/checking Prime Numbers.
"""

import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QGridLayout,
)

from .prime_checker import PrimeChecker
from .yaml_file_handler import YamlFileHandler
from .prime_file_handler import PrimeFileHandler

config_file = YamlFileHandler("resources/configs/config.yml")
config = config_file.load_yaml_file()

themes_file = YamlFileHandler("resources/configs/themes.yml")
themes = themes_file.load_yaml_file()


class PrimeNumberFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle(config["window_title"])
        self.setFixedSize(
            config["window_size"]["width"], config["window_size"]["height"]
        )

        # * Define normal variables
        self.prime_file_handler = PrimeFileHandler()
        self.current_number = self.prime_file_handler.load_current_number()
        self.check_number = int()
        self.prime_list = self.prime_file_handler.load_prime_numbers()
        self.prime_checker = PrimeChecker(self.prime_list)
        self.keep_iterating = False

        # * Create widgets and apply settings to them
        self.iterate_button = QPushButton("Iterate")

        self.iterate_timer = QTimer(self)
        self.iterate_timer.setInterval(10)

        self.most_recent_number_text = QLabel(
            "Most recent number checked: ", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.most_recent_number_text.setFixedWidth(config["input_widgets"]["width"])

        self.most_recent_number = QLabel(
            str(self.current_number), alignment=Qt.AlignmentFlag.AlignRight
        )

        self.most_recent_prime_text = QLabel(
            "Most recent prime found: ", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.most_recent_prime_text.setFixedWidth(config["input_widgets"]["width"])

        self.most_recent_prime = QLabel(
            str(self.prime_list[-1]), alignment=Qt.AlignmentFlag.AlignRight
        )

        self.check_button = QPushButton("Check for Primality")
        self.check_button.setFixedWidth(config["input_widgets"]["width"])

        self.check_input = QLineEdit(f"{self.current_number}")
        self.check_input.setValidator(QIntValidator(bottom=0))
        self.check_input.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.check_timer = QTimer(self)
        self.check_timer.setInterval(10)

        self.theme_toggle = QPushButton("Dark")
        self.theme_toggle.setFixedWidth(config["input_widgets"]["width"])

        self.check_click()

        # * Define button connections
        self.iterate_button.pressed.connect(self.iterate_click)
        self.iterate_timer.timeout.connect(self.iterate)
        self.check_button.pressed.connect(self.check_click)
        self.check_timer.timeout.connect(self.check_iterate)
        self.theme_toggle.pressed.connect(self.toggle_theme)

        # * Create layouts
        page = QVBoxLayout()
        iterate = QGridLayout()
        numbers = QGridLayout()
        primes = QGridLayout()
        checks = QGridLayout()

        # * Add widgets to layouts

        iterate.addWidget(self.theme_toggle, 0, 0, 1, 1)
        iterate.addWidget(self.iterate_button, 0, 1, 1, 1)

        numbers.addWidget(self.most_recent_number_text, 0, 0, 1, 1)
        numbers.addWidget(self.most_recent_number, 0, 1, 1, 2)

        primes.addWidget(self.most_recent_prime_text, 0, 0, 1, 1)
        primes.addWidget(self.most_recent_prime, 0, 1, 1, 2)

        checks.addWidget(self.check_button, 0, 0, 1, 1)
        checks.addWidget(self.check_input, 0, 1, 1, 2)

        # * Setup overall page layout and set default window theme
        page.addLayout(iterate)
        page.addLayout(numbers)
        page.addLayout(primes)
        page.addLayout(checks)

        gui = QWidget()
        gui.setLayout(page)

        self.setCentralWidget(gui)

        self.apply_theme(self.theme_toggle.text().lower())

    def iterate_click(self):
        self.keep_iterating = not self.keep_iterating
        if self.keep_iterating:
            self.iterate_button.setText("Stop Iterating")
            self.iterate_timer.start()
        else:
            self.iterate_button.setText("Iterate")
            self.iterate_timer.stop()

    def iterate(self):
        if self.keep_iterating:
            is_prime = self.prime_checker.prime_check(self.current_number)

            if is_prime is True:
                self.prime_file_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.prime_file_handler.save_current_number(self.current_number)
            self.most_recent_number.setText(str(self.current_number))

    def check_click(self):
        self.check_input_number_only = self.remove_non_ints(self.check_input.text())
        self.check_number = int(self.check_input_number_only)
        self.check_button.setText("Checking")

        if self.check_number <= self.current_number:
            if self.check_number in self.prime_list:
                self.check_input.setText(f"Prime: {self.check_input_number_only}")
            else:
                self.check_input.setText(f"Not Prime: {self.check_input_number_only}")
            self.check_button.setText("Check for Primality")
            self.check_timer.stop()
        else:
            self.check_timer.start()

    def check_iterate(self):
        if self.check_number > self.current_number:
            is_prime = self.prime_checker.prime_check(self.current_number)

            if is_prime is True:
                self.prime_file_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.prime_file_handler.save_current_number(self.current_number)
            self.most_recent_number.setText(str(self.current_number))

        self.check_click()

    def remove_non_ints(self, check_text):
        check_text = "".join(filter(str.isdigit, check_text))
        self.check_input.setText(check_text)
        return check_text

    def toggle_theme(self):
        if self.theme_toggle.text() == "Dark":
            self.theme_toggle.setText("Light")
            theme = self.theme_toggle.text()
        else:
            self.theme_toggle.setText("Dark")
            theme = self.theme_toggle.text()

        self.apply_theme(theme.lower())

    def apply_theme(self, theme):
        self.main_stylesheet = f"""
            background-color: {themes[theme]["background-color"]};
            color: {themes[theme]["color"]};
            border: {themes[theme]["border"]};
            border-radius: {themes["general"]["border-radius"]};
            padding: {themes["general"]["padding"]};
            """
        self.widget_stylesheet = f"""
            background-color: {themes[theme]["widget-background-color"]};
            """
        self.setStyleSheet(self.main_stylesheet)
        self.iterate_button.setStyleSheet(self.widget_stylesheet)
        self.most_recent_number_text.setStyleSheet(self.widget_stylesheet)
        self.most_recent_number.setStyleSheet(self.widget_stylesheet)
        self.most_recent_prime_text.setStyleSheet(self.widget_stylesheet)
        self.most_recent_prime.setStyleSheet(self.widget_stylesheet)
        self.check_button.setStyleSheet(self.widget_stylesheet)
        self.check_input.setStyleSheet(self.widget_stylesheet)
        self.theme_toggle.setStyleSheet(self.widget_stylesheet)

        (
            self.theme_toggle.setText("Dark")
            if theme == "dark"
            else self.theme_toggle.setText("Light")
        )


def main():
    app = QApplication(sys.argv)
    main_window = PrimeNumberFinder()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

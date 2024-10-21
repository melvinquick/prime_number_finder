import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from prime_checker import PrimeChecker
from config_handler import ConfigHandler
from file_handler import FileHandler

icon = ConfigHandler("images/placeholder.ico")

config_file = ConfigHandler("configs/config.yml")
config = config_file.load_yaml_file()

themes_file = ConfigHandler("configs/themes.yml")
themes = themes_file.load_yaml_file()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # * Set window default settings
        self.setWindowTitle(config["window_settings"]["title"])
        self.setMaximumSize(
            config["window_settings"]["min_width"],
            config["window_settings"]["min_height"],
        )
        self.setWindowIcon(QIcon(icon.get_file_path()))

        # * Define normal variables
        self.file_handler = FileHandler()
        self.current_number = self.file_handler.load_current_number()
        self.check_number = int()
        self.prime_list = self.file_handler.load_prime_numbers()
        self.prime_checker = PrimeChecker(self.prime_list)
        self.keep_iterating = False

        # * Create widgets and apply settings to them
        self.iterate_button = QPushButton("Iterate")

        self.iterate_timer = QTimer(self)
        self.iterate_timer.setInterval(10)

        self.most_recent_number_text = QLabel(
            f"Most recent number checked: ", alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.most_recent_number = QLabel(
            str(self.current_number), alignment=Qt.AlignmentFlag.AlignRight
        )

        self.most_recent_prime_text = QLabel(
            f"Most recent prime found: ", alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.most_recent_prime = QLabel(
            str(self.prime_list[-1]), alignment=Qt.AlignmentFlag.AlignRight
        )

        self.check_button = QPushButton("Check for Primality")

        self.check_input = QLineEdit(f"{self.current_number}")
        self.check_input.setValidator(QIntValidator(bottom=0))

        self.check_output = QLabel()

        self.check_timer = QTimer(self)
        self.check_timer.setInterval(10)

        self.check_click()

        # * Define button connections
        self.iterate_button.pressed.connect(self.iterate_click)
        self.iterate_timer.timeout.connect(self.iterate)
        self.check_button.pressed.connect(self.check_click)
        self.check_timer.timeout.connect(self.check_iterate)

        # * Create layouts
        self.page = QVBoxLayout()
        self.row_one = QHBoxLayout()
        self.row_two = QHBoxLayout()
        self.row_three = QHBoxLayout()
        self.row_four = QHBoxLayout()

        # * Add widgets to layouts
        self.row_one.addWidget(self.iterate_button)

        self.row_two.addWidget(self.most_recent_number_text)
        self.row_two.addWidget(self.most_recent_number)

        self.row_three.addWidget(self.most_recent_prime_text)
        self.row_three.addWidget(self.most_recent_prime)

        self.row_four.addWidget(self.check_button)
        self.row_four.addWidget(self.check_input)
        self.row_four.addWidget(self.check_output)

        # * Setup overall page layout and set default window theme
        self.page.addLayout(self.row_one)
        self.page.addLayout(self.row_two)
        self.page.addLayout(self.row_three)
        self.page.addLayout(self.row_four)

        self.gui = QWidget()
        self.gui.setLayout(self.page)

        self.setCentralWidget(self.gui)

        self.toggle_theme()

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

            if is_prime == True:
                self.file_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.file_handler.save_current_number(self.current_number)
            self.most_recent_number.setText(str(self.current_number))

    def check_click(self):
        self.check_number = int(self.check_input.text())
        self.check_button.setText("Checking")

        if self.check_number <= self.current_number:
            if self.check_number in self.prime_list:
                self.check_output.setText("is prime!")
            else:
                self.check_output.setText("is not prime!")
            self.check_button.setText("Check for Primality")
            self.check_timer.stop()
        else:
            self.check_timer.start()

    def check_iterate(self):
        if self.check_number > self.current_number:
            is_prime = self.prime_checker.prime_check(self.current_number)

            if is_prime == True:
                self.file_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.file_handler.save_current_number(self.current_number)
            self.most_recent_number.setText(str(self.current_number))

        self.check_click()

    def toggle_theme(self):
        self.theme = "Everforest-Light"
        self.apply_theme(self)
        for widget in self.findChildren(QWidget):  # * Apply theme to all child widgets
            self.apply_theme(widget)

    def apply_theme(self, widget):
        self.theme_stylesheet = f"""
            background-color: {themes[self.theme]['background-color']};
            color: {themes[self.theme]['color']};
            border: {themes[self.theme]['border']};
            border-radius: {themes['general']['border-radius']};
            padding: {themes['general']['padding']};
            """
        widget.setStyleSheet(self.theme_stylesheet)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

import os
from sys import argv, exit

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from .components.database_handler import DatabaseHandler
from .components.prime_checker import PrimeChecker
from .components.ui_manager import UIManager
from .components.yaml_file_handler import YamlFileHandler


class PrimeNumberFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(os.path.abspath(__file__))

        config_file = YamlFileHandler(
            os.path.join(base_dir, "resources/configs/config.yaml")
        )
        self.config = config_file.load_yaml_file()

        themes_file = YamlFileHandler(
            os.path.join(base_dir, "resources/styles/themes.yaml")
        )
        self.themes = themes_file.load_yaml_file()

        self.db_handler = DatabaseHandler()
        self.ui = UIManager(self, self.config, self.themes)

        self.current_number = self.db_handler.load_current_number()
        self.check_number = 0
        self.prime_list = self.db_handler.load_prime_numbers()
        self.prime_checker = PrimeChecker(self.prime_list)
        self.keep_iterating = False

        self.ui.build_ui()
        self.ui.most_recent_number.setText(str(self.current_number))
        self.ui.most_recent_prime.setText(
            str(self.prime_list[-1] if self.prime_list else 2)
        )
        self.ui.check_input.setText(f"{self.current_number}")

        self.iterate_timer = QTimer(self)
        self.iterate_timer.setInterval(10)

        self.check_timer = QTimer(self)
        self.check_timer.setInterval(10)

        self.ui.iterate_button.pressed.connect(self.iterate_click)
        self.iterate_timer.timeout.connect(self.iterate)
        self.ui.check_button.pressed.connect(self.check_click)
        self.check_timer.timeout.connect(self.check_iterate)
        self.ui.theme_toggle.pressed.connect(self.toggle_theme)

        self.ui.apply_theme("dark")
        self.check_click()
        self.show()

    def iterate_click(self):
        self.keep_iterating = not self.keep_iterating
        if self.keep_iterating:
            self.ui.iterate_button.setText("Stop Iterating")
            self.iterate_timer.start()
        else:
            self.ui.iterate_button.setText("Iterate")
            self.iterate_timer.stop()

    def iterate(self):
        if self.keep_iterating:
            is_prime = self.prime_checker.prime_check(self.current_number)
            if is_prime:
                self.db_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.ui.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.db_handler.save_current_number(self.current_number)
            self.ui.most_recent_number.setText(str(self.current_number))

    def check_click(self):
        check_input_number_only = self.remove_non_ints(self.ui.check_input.text())
        if not check_input_number_only:
            return
        try:
            self.check_number = int(check_input_number_only)
        except ValueError:
            return

        self.ui.check_button.setText("Checking")

        if self.check_number <= self.current_number:
            if self.check_number in self.prime_list:
                self.ui.check_input.setText(f"Prime: {check_input_number_only}")
            else:
                self.ui.check_input.setText(f"Not Prime: {check_input_number_only}")
            self.ui.check_button.setText("Check for Primality")
            self.check_timer.stop()
        else:
            self.check_timer.start()

    def check_iterate(self):
        if self.check_number > self.current_number:
            is_prime = self.prime_checker.prime_check(self.current_number)
            if is_prime:
                self.db_handler.save_found_prime(self.current_number)
                self.prime_list.append(self.current_number)
                self.ui.most_recent_prime.setText(str(self.current_number))

            self.current_number += 1
            self.db_handler.save_current_number(self.current_number)
            self.ui.most_recent_number.setText(str(self.current_number))

        if self.check_number <= self.current_number:
            self.check_click()

    def remove_non_ints(self, check_text):
        check_text = "".join(filter(str.isdigit, check_text))
        self.ui.check_input.setText(check_text)
        return check_text

    def toggle_theme(self):
        if self.ui.theme_toggle.text() == "Dark":
            self.ui.apply_theme("light")
        else:
            self.ui.apply_theme("dark")


def main():
    app = QApplication(argv)
    main_window = PrimeNumberFinder()
    exit(app.exec())


if __name__ == "__main__":
    main()

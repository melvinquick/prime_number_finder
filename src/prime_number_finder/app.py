import os
from sys import argv, exit

from PySide6.QtCore import QSettings, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow

from prime_number_finder.components.qss_file_handler import QssFileHandler
from prime_number_finder.components.yaml_file_handler import YamlFileHandler

from .components.about_dialog import AboutDialog
from .components.database_handler import DatabaseHandler
from .components.menubar import MenuBar
from .components.preferences_dialog import PreferencesDialog
from .components.prime_checker import PrimeChecker
from .components.theme_manager import ThemeManager
from .components.ui_manager import UIManager


class PrimeNumberFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.themes = YamlFileHandler(
            "../resources/styles/themes.yaml"
        ).load_yaml_file()
        qss = QssFileHandler("../resources/styles/styles.qss").load_qss_file()
        self.theme_manager = ThemeManager(self.themes, qss)

        config_dir = os.path.expanduser("~/.config/prime_number_finder")
        os.makedirs(config_dir, exist_ok=True)
        settings_path = os.path.join(config_dir, "settings.conf")
        self.settings = QSettings(settings_path, QSettings.Format.IniFormat)

        self.theme_name = self.settings.value("theme", ThemeManager.DEFAULT_THEME)

        self.db_handler = DatabaseHandler()
        self.ui = UIManager(self, {"window_title": "Prime Number Finder"})

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

        MenuBar(self, self.open_preferences, self.open_about, self.copy_recent_prime)

        self.iterate_timer = QTimer(self)
        self.iterate_timer.setInterval(10)
        self.iterate_timer.timeout.connect(self.iterate)

        self.check_timer = QTimer(self)
        self.check_timer.setInterval(10)
        self.check_timer.timeout.connect(self.check_iterate)

        self.result_hide_timer = QTimer(self)
        self.result_hide_timer.setSingleShot(True)
        self.result_hide_timer.timeout.connect(self.clear_result)

        self.ui.iterate_button.pressed.connect(self.iterate_click)
        self.ui.check_button.pressed.connect(self.check_click)
        self.ui.check_input.returnPressed.connect(self.check_click)

        self.apply_theme(self.theme_name)
        self.show()

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        qss = self.theme_manager.render(theme_name)
        QApplication.instance().setStyleSheet(qss)

    def open_preferences(self):
        dialog = PreferencesDialog(self.theme_manager, self.current_theme, self)
        dialog.theme_changed.connect(self.handle_theme_change)
        dialog.exec()

    def handle_theme_change(self, new_theme):
        if new_theme != self.current_theme:
            self.settings.setValue("theme", new_theme)
            self.apply_theme(new_theme)

    def open_about(self):
        dialog = AboutDialog(self.theme_manager, self.current_theme, self)
        dialog.exec()

    def copy_recent_prime(self):
        if not self.prime_list:
            return

        latest_prime = str(self.prime_list[-1])
        QGuiApplication.clipboard().setText(latest_prime)

        self.ui.result_label.setText(f"Copied {latest_prime} to clipboard!")
        self.ui.result_label.setObjectName("ResultNeutral")
        self.ui.result_label.style().unpolish(self.ui.result_label)
        self.ui.result_label.style().polish(self.ui.result_label)

        self.result_hide_timer.stop()
        self.result_hide_timer.start(3000)

    def iterate_click(self):
        self.keep_iterating = not self.keep_iterating
        if self.keep_iterating:
            self.ui.iterate_button.setText("Stop Iterating")
            self.iterate_timer.start()
        else:
            self.ui.iterate_button.setText("Start Iterating")
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

        self.ui.check_button.setText("Checking...")
        self.result_hide_timer.stop()
        self.ui.result_label.setText("")

        if self.check_number <= self.current_number:
            self._display_result()
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
            self._display_result()

    def _display_result(self):
        self.ui.check_button.setText("Check Primality")
        self.check_timer.stop()

        if self.check_number in self.prime_list:
            self.ui.result_label.setText("Prime")
            self.ui.result_label.setObjectName("ResultSuccess")
        else:
            self.ui.result_label.setText("Not Prime")
            self.ui.result_label.setObjectName("ResultDanger")

        self.ui.result_label.style().unpolish(self.ui.result_label)
        self.ui.result_label.style().polish(self.ui.result_label)

        self.result_hide_timer.start(6000)

    def clear_result(self):
        self.ui.result_label.setText("")

    def remove_non_ints(self, check_text):
        check_text = "".join(filter(str.isdigit, check_text))
        self.ui.check_input.setText(check_text)
        return check_text


def main():
    app = QApplication(argv)
    app.setApplicationName("Prime Number Finder")
    main_window = PrimeNumberFinder()
    exit(app.exec())


if __name__ == "__main__":
    main()

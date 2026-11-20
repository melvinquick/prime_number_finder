import os
import re

from .qss_file_handler import QssFileHandler
from .yaml_file_handler import YamlFileHandler


class ThemeManager:
    def __init__(self, base_dir):
        self.themes_file = os.path.join(base_dir, "resources/styles/themes.yaml")
        self.qss_file = os.path.join(base_dir, "resources/styles/styles.qss")

        self.themes = YamlFileHandler(self.themes_file).load_yaml_file()
        self.template = QssFileHandler(self.qss_file).load_qss_file()

    def render(self, theme_name):
        # Fallback to pnf_dark if the requested theme is missing
        theme = self.themes.get(theme_name)
        if not theme:
            theme = self.themes.get("pnf_dark", next(iter(self.themes.values())))

        qss = self.template

        for key, value in theme.items():
            qss = qss.replace(f"@{key}", value)

        qss = re.sub(r"@[\w-]+", "", qss)
        return qss

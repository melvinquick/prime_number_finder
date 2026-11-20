from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class PreferencesDialog(QDialog):
    theme_changed = Signal(str)

    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = current_theme

        self.setWindowTitle("Preferences")
        self.setFixedWidth(350)
        self.setStyleSheet(self.theme_manager.render(self.current_theme))

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Appearance Card
        appearance_card = QFrame()
        appearance_card.setObjectName("Card")
        card_layout = QVBoxLayout(appearance_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        title = QLabel("Appearance")
        title.setObjectName("DialogTitle")
        card_layout.addWidget(title)

        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setFixedWidth(60)

        self.theme_combo = QComboBox()
        for name in sorted(self.theme_manager.themes.keys()):
            # Format "pnf_dark" into "Prime Number Finder Dark"
            display_name = (
                name.replace("pnf", "prime number finder").replace("_", " ").title()
            )
            self.theme_combo.addItem(display_name, userData=name)

        idx = self.theme_combo.findData(self.current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)

        self.theme_combo.currentIndexChanged.connect(self._on_theme_selected)

        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo, 1)
        card_layout.addLayout(theme_row)
        layout.addWidget(appearance_card)

        layout.addStretch()

        # Footer Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("PrimaryButton")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def _on_theme_selected(self, index):
        new_theme = self.theme_combo.itemData(index)
        if new_theme and new_theme != self.current_theme:
            self.current_theme = new_theme
            self.setStyleSheet(self.theme_manager.render(self.current_theme))
            self.theme_changed.emit(self.current_theme)

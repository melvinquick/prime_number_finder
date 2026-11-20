from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class UIManager:
    def __init__(self, window: QMainWindow, config: dict):
        self.window = window
        self.config = config

        self.iterate_button = None
        self.most_recent_number = None
        self.most_recent_prime = None
        self.check_button = None
        self.check_input = None
        self.result_label = None

    def build_ui(self):
        self.window.setWindowTitle(self.config["window_title"])
        self.window.setMinimumSize(480, 400)
        self.window.resize(500, 450)

        # --- Stats Cards ---
        stats_layout = QHBoxLayout()

        num_card = QFrame()
        num_card.setObjectName("Card")
        num_layout = QVBoxLayout(num_card)
        num_title = QLabel("Latest Checked")
        num_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.most_recent_number = QLabel("2")
        self.most_recent_number.setObjectName("DialogTitle")
        self.most_recent_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_layout.addWidget(num_title)
        num_layout.addWidget(self.most_recent_number)

        prime_card = QFrame()
        prime_card.setObjectName("Card")
        prime_layout = QVBoxLayout(prime_card)
        prime_title = QLabel("Latest Prime")
        prime_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.most_recent_prime = QLabel("2")
        self.most_recent_prime.setObjectName("DialogTitle")
        self.most_recent_prime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prime_layout.addWidget(prime_title)
        prime_layout.addWidget(self.most_recent_prime)

        stats_layout.addWidget(num_card)
        stats_layout.addWidget(prime_card)

        # --- Check Primality Section ---
        check_card = QFrame()
        check_card.setObjectName("Card")
        # Allow this card to expand vertically
        check_card.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        check_layout = QVBoxLayout(check_card)
        check_layout.setContentsMargins(16, 16, 16, 16)
        check_layout.setSpacing(12)

        check_title = QLabel("Check a specific number")
        check_title.setObjectName("DialogTitle")
        check_title.setStyleSheet("font-size: 10pt; font-weight: 600;")
        check_layout.addWidget(check_title)

        # Input Row
        check_row = QHBoxLayout()
        self.check_input = QLineEdit()
        regex = QRegularExpression("^[0-9]+$")
        self.check_input.setValidator(QRegularExpressionValidator(regex))
        self.check_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.check_input.setFixedHeight(35)

        self.check_button = QPushButton("Check Primality")
        self.check_button.setFixedHeight(35)

        check_row.addWidget(self.check_input, 1)
        check_row.addWidget(self.check_button)
        check_layout.addLayout(check_row)

        # Result Label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFixedHeight(30)
        self.result_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        self.result_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        check_layout.addWidget(self.result_label)

        # Add a stretch inside the card so the content stays at the top when expanded
        check_layout.addStretch()

        # --- Iterate Section ---
        self.iterate_button = QPushButton("Start Iterating")
        self.iterate_button.setObjectName("PrimaryButton")
        self.iterate_button.setFixedHeight(40)

        # --- Main Layout ---
        page = QVBoxLayout()
        page.setContentsMargins(20, 20, 20, 20)
        page.setSpacing(20)

        # Order: Stats -> Expanding Check Card -> Bottom Button
        page.addLayout(stats_layout)
        page.addWidget(check_card)
        page.addWidget(self.iterate_button)

        gui = QWidget()
        gui.setLayout(page)
        self.window.setCentralWidget(gui)

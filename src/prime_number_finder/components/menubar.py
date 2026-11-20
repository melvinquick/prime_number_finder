from PySide6.QtGui import QAction


class MenuBar:
    def __init__(self, window, on_preferences, on_about, on_copy_prime):
        menubar = window.menuBar()

        # 1. File
        file_menu = menubar.addMenu("File")
        quit_action = QAction("Quit", window)
        quit_action.triggered.connect(window.close)
        file_menu.addAction(quit_action)

        # 2. Edit
        edit_menu = menubar.addMenu("Edit")
        copy_action = QAction("Copy Most Recent Prime", window)
        copy_action.triggered.connect(on_copy_prime)
        edit_menu.addAction(copy_action)

        # 3. Help
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", window)
        about_action.triggered.connect(on_about)
        help_menu.addAction(about_action)

        # 4. Preferences
        prefs_action = QAction("Preferences", window)
        prefs_action.triggered.connect(on_preferences)
        menubar.addAction(prefs_action)

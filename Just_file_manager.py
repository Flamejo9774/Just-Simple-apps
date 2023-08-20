#!/usr/bin/env python
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QAction, QDialog, QLabel, QMenu
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class AboutWindow(QDialog):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(300, 300, 200, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)

        layout = QVBoxLayout()

        label = QLabel("Just file manager\n{}\n© 2023–2023 Just simple Apps\n".format(version))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        link_label = QLabel('<a href="https://github.com/Flamejo9774/Just-apps">Other Just Simple Apps</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        link_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(link_label)

        self.setLayout(layout)



class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath("/")

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index("/"))
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)

        layout.addWidget(self.tree_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        more_menu = menu_bar.addMenu("More")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.open_about_window)
        more_menu.addAction(about_action)

    def open_about_window(self):
        about_version = "1.01.5"
        about_window = AboutWindow(about_version)
        about_window.exec_()

    def on_item_double_clicked(self, index):
        file_path = self.file_system_model.filePath(index)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[-1].lower()
            os.system(f"python3 Just_Text_Editor.py {file_path}")

def main():
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
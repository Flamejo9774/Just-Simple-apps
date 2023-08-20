import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QCheckBox, QMessageBox, QAction, QMenu, QLabel, QDialog
from PyQt5.QtCore import QFile, QTextStream, Qt

class AboutWindow(QDialog):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(300, 300, 200, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)

        layout = QVBoxLayout()

        label = QLabel("Just To Do\n{}\n© 2023–2023 Just Simple Apps\n".format(version))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        link_label = QLabel('<a href="https://github.com/Flamejo9774/Just-apps">Other Just Simple Apps</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        link_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(link_label)

        self.setLayout(layout)

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List App")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.todo_list = QListWidget()
        self.layout.addWidget(self.todo_list)

        self.input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.add_todo)
        self.input_layout.addWidget(self.input_field)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_todo)
        self.input_layout.addWidget(self.add_button)

        self.layout.addLayout(self.input_layout)

        self.load_todo_list()

        self.central_widget.setLayout(self.layout)

        self.init_menu()

    def init_menu(self):
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)

        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu("More")
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        about_window = AboutWindow("Version 1.0")
        about_window.exec_()

    def add_todo(self):
        todo_text = self.input_field.text()
        if todo_text:
            item = QListWidgetItem()
            todo_layout = QHBoxLayout()

            checkbox = QCheckBox(todo_text)
            checkbox.stateChanged.connect(self.save_todo_list)
            todo_layout.addWidget(checkbox)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, i=item: self.delete_todo_item(i))  # Connect the delete button signal
            todo_layout.addWidget(delete_button)

            todo_widget = QWidget()
            todo_widget.setLayout(todo_layout)

            item.setSizeHint(todo_widget.sizeHint())
            self.todo_list.addItem(item)
            self.todo_list.setItemWidget(item, todo_widget)
            self.input_field.clear()

            self.save_todo_list()

        else:
            QMessageBox.warning(self, "Empty Input", "Please enter a task.")

    def delete_todo_item(self, item):
        row = self.todo_list.row(item)
        self.todo_list.takeItem(row)
        self.save_todo_list()

    def save_todo_list(self):
        file = QFile("savedtodo.jstsmp")
        if file.open(QFile.WriteOnly | QFile.Text):
            stream = QTextStream(file)
            for index in range(self.todo_list.count()):
                widget_item = self.todo_list.itemWidget(self.todo_list.item(index))
                checkbox = widget_item.layout().itemAt(0).widget()
                task_text = checkbox.text()
                is_checked = checkbox.isChecked()
                stream << f"{task_text} | {'checked' if is_checked else 'unchecked'}\n"
            file.close()

    def load_todo_list(self):
        file = QFile("savedtodo.jstsmp")
        if file.exists() and file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            while not stream.atEnd():
                line = stream.readLine().strip()
                if line:
                    task_text, status = line.split(" | ")
                    item = QListWidgetItem()
                    todo_layout = QHBoxLayout()

                    checkbox = QCheckBox(task_text)
                    todo_layout.addWidget(checkbox)

                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, i=item: self.delete_todo_item(i))  # Connect the delete button signal
                    todo_layout.addWidget(delete_button)

                    todo_widget = QWidget()
                    todo_widget.setLayout(todo_layout)

                    item.setSizeHint(todo_widget.sizeHint())
                    self.todo_list.addItem(item)
                    self.todo_list.setItemWidget(item, todo_widget)

                    if status == "checked":
                        checkbox.setChecked(True)

            file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
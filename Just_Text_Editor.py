import sys
from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QMainWindow, QTextEdit, QScrollBar, QAction, QFileDialog, QMenuBar, QVBoxLayout, QWidget, QFontComboBox, QMenu, QWidgetAction
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtGui import QFont
import subprocess

class AboutWindow(QDialog):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(300, 300, 200, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)

        layout = QVBoxLayout()

        label = QLabel("Just Text Editor\n{}\n© 2023–2023 Just Simple Apps\n".format(version))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        link_label = QLabel('<a href="https://github.com/Flamejo9774/Just-apps">Other Just Simple Apps</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        link_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(link_label)

        self.setLayout(layout)
class texteditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Just Text Editor")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.scroll_bar = QScrollBar(Qt.Vertical)
        self.scroll_bar.setVisible(False)
        layout.addWidget(self.scroll_bar)

        self.central_widget.setLayout(layout)

        self.radius = 0

        self.init_menu()

        self.current_file = None
        self.update_title()

    def init_menu(self):
        menubar = self.menuBar()
        menu_color = menubar.palette().color(menubar.backgroundRole())

        file_menu = menubar.addMenu("File")

        about_action = QAction("about", self)
        about_action.triggered.connect(self.open_about_window)
        file_menu.addAction(about_action)

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut("Shift+Ctrl+S")
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        run_action = QAction("Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_python_script)
        file_menu.addAction(run_action)


        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.menu_background_color = QColor(menu_color)
        self.menu_background_color.setAlpha(200)

        font_menu = menubar.addMenu("Font")



        font_combo = QFontComboBox(self)
        font_combo.setCurrentFont(self.text_edit.font())
        font_combo.currentFontChanged.connect(self.change_font)
        font_widget_action = QWidgetAction(font_menu)
        font_widget_action.setDefaultWidget(font_combo)
        font_menu.addAction(font_widget_action)

        size_menu = font_menu.addMenu("Size")
        self.size_actions = []



        for size in range(8, 40, 2):
            size_action = QAction(f"{size}", self)
            size_action.setCheckable(True)
            size_action.triggered.connect(lambda checked, size=size: self.change_font_size(size))
            size_menu.addAction(size_action)
            self.size_actions.append(size_action)

        edit_menu = menubar.addMenu("Edit")

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        self.bold_action = QAction("Bold", self)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)
        edit_menu.addAction(self.bold_action)

        self.italic_action = QAction("Italic", self)
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.toggle_italic)
        edit_menu.addAction(self.italic_action)

        self.underline_action = QAction("Underline", self)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)
        edit_menu.addAction(self.underline_action)

        self.strikethrough_action = QAction("Strikethrough", self)
        self.strikethrough_action.setCheckable(True)
        self.strikethrough_action.triggered.connect(self.toggle_strikethrough)
        edit_menu.addAction(self.strikethrough_action)
    def open_about_window(self):
        about_version = "1.15.7"
        about_window = AboutWindow(about_version)
        about_window.exec_()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.menu_background_color))
        painter.drawRect(self.rect())

    def new_file(self):
        self.text_edit.clear()
        self.current_file = None
        self.update_title()
    def opencommandfile(self,file_name):
        if file_name:
            with open(file_name, "r") as file:
                self.text_edit.setPlainText(file.read())
                self.current_file = file_name
                self.update_title()
    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Text File", "","Text Files (*.txt);;Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "r") as file:
                self.text_edit.setPlainText(file.read())
                self.current_file = file_name
                self.update_title()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_edit.toPlainText())
        else:
            self.save_as_file()

    def save_as_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt);;Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.text_edit.toPlainText())
                self.current_file = file_name
                self.update_title()

    def update_title(self):
        if self.current_file:
            self.setWindowTitle(f"{self.current_file} - Just Text Editor")
        else:
            self.setWindowTitle("Untitled.txt - Just Text Editor")

    def change_font(self, font):
        self.text_edit.setCurrentFont(font)


    def toggle_bold(self):
        current_format = self.text_edit.currentCharFormat()
        if current_format.fontWeight() == QFont.Bold:
            current_format.setFontWeight(QFont.Normal)
        else:
            current_format.setFontWeight(QFont.Bold)
        self.text_edit.setCurrentCharFormat(current_format)
        self.bold_action.setChecked(current_format.fontWeight() == QFont.Bold)


    def toggle_italic(self):
        current_format = self.text_edit.currentCharFormat()
        current_format.setFontItalic(not current_format.fontItalic())
        self.text_edit.setCurrentCharFormat(current_format)
        self.italic_action.setChecked(current_format.fontItalic())

    def toggle_underline(self):
        current_format = self.text_edit.currentCharFormat()
        current_format.setFontUnderline(not current_format.fontUnderline())
        self.text_edit.setCurrentCharFormat(current_format)
        self.underline_action.setChecked(current_format.fontUnderline())

    def toggle_strikethrough(self):
        current_format = self.text_edit.currentCharFormat()
        current_format.setFontStrikeOut(not current_format.fontStrikeOut())
        self.text_edit.setCurrentCharFormat(current_format)
        self.strikethrough_action.setChecked(current_format.fontStrikeOut())
    def change_font_size(self, size):
        font = self.text_edit.currentFont()
        font.setPointSize(size)
        self.text_edit.setCurrentFont(font)
    def change_font(self, font):
        self.text_edit.setCurrentFont(font)
        self.update_font_action(font)

    def change_font_size(self, size):
        font = self.text_edit.currentFont()
        font.setPointSize(size)
        self.text_edit.setCurrentFont(font)
        self.update_size_checkmarks(size)

    def update_size_checkmarks(self, selected_size):
        for action in self.size_actions:
            action.setChecked(action.text() == str(selected_size))


    def run_python_script(self):
        if self.current_file and self.current_file.endswith(".py"):
            try:
                result = subprocess.run(["python", self.current_file], capture_output=True, text=True)
                output = result.stdout
                error = result.stderr

                if output:
                    print("Output:", output)
                if error:
                    print("Error:", error)
            except Exception as e:
                print("An error occurred:", str(e))
        else:
            print("No valid Python script selected to run.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = texteditor()
    window.setGeometry(200, 200, 600, 400)
    window.show()
    print(sys.argv)
    if len(sys.argv) != 2:
        pass
    else:
        text_file_name = sys.argv[1]
        window.opencommandfile(text_file_name)
    sys.exit(app.exec_())
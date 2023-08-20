#!/usr/bin/env python
import sys
import os
from PyQt5.QtCore import Qt, QTimer, QVariantAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QMenuBar, QMenu, QAction, QLabel, QHBoxLayout, QDialog

class SaveSlotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.save_text_fields = []

        grid_layout = QGridLayout()
        rows = 5
        cols = 3

        for i in range(rows):
            for j in range(cols):
                index = j * rows + i
                if index < 15:
                    text_field = QLineEdit()
                    self.save_text_fields.append(text_field)
                    label = QLabel(f"Save {index + 1}")
                    grid_layout.addWidget(label, i, j * 2)
                    grid_layout.addWidget(text_field, i, j * 2 + 1)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveToSaves)
        grid_layout.addWidget(save_button, rows, 0, 1, cols * 2)

        load_button = QPushButton("Load")
        load_button.clicked.connect(self.loadFromSaves)
        grid_layout.addWidget(load_button, rows + 1, 0, 1, cols * 2)

        self.message_label = QLabel()
        grid_layout.addWidget(self.message_label, rows + 2, 0, 1, cols * 2)

        self.layout.addLayout(grid_layout)


    def saveToSaves(self):
        with open("savedcalc.jstsmp", "w") as file:
            for text_field in self.save_text_fields:
                text = text_field.text()
                file.write(text + "\n")
        self.showMessage("Save successful.")

    def loadFromSaves(self):
        try:
            with open("savedcalc.jstsmp", "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if i < len(self.save_text_fields):
                        self.save_text_fields[i].setText(line.strip())
            self.showMessage("Load successful.")
        except FileNotFoundError:
            self.showMessage("No saved file found.")

    def showMessage(self, message):
        self.message_label.setText(message)
        self.message_label.setVisible(True)
        QTimer.singleShot(1000, self.hideMessage)

    def hideMessage(self):
        self.message_label.clear()
        self.message_label.setVisible(False)




class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(300, 300, 200, 150)

        layout = QVBoxLayout()


        # Add options widgets here
        # For example, you can add checkboxes, radio buttons, etc.

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveOptions)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def saveOptions(self):
        # Implement the saving of options here
        # This function will be triggered when the "Save" button is clicked
        pass

class AboutWindow(QDialog):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(300, 300, 200, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)

        layout = QVBoxLayout()

        label = QLabel("Just Calculator\n{}\n© 2023–2023 Just Simple Apps\n".format(version))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        link_label = QLabel('<a href="https://github.com/Flamejo9774/Just-apps">Other Just Simple Apps</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        link_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(link_label)

        self.setLayout(layout)

class CalculatorApp(QMainWindow):
    _instances = []
    version = "1.25.25"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.result_display = QLineEdit()
        layout.addWidget(self.result_display)

        self.createMenuBar()

        button_grid = [
            ['C', 'AC'         ],
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['^', '%']
        ]

        button_layout = QGridLayout()

        for row_idx, row in enumerate(button_grid):
            for col_idx, button_text in enumerate(row):
                button = QPushButton(button_text)
                button.clicked.connect(self.buttonClicked)
                button_layout.addWidget(button, row_idx, col_idx)

        layout.addLayout(button_layout)
        self.central_widget.setLayout(layout)

        self.current_input = ""
        self.pending_operator = ""
        self.result = None

    def createMenuBar(self):
        menubar = self.menuBar()

        # Create "more" menu
        more_menu = menubar.addMenu("More")
        new_action = QAction("New Window", self)
        new_action.triggered.connect(self.openNewWindow)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.openAboutWindow)
        options_action = QAction("Options", self)
        options_action.triggered.connect(self.openOptionsWindow)
        more_menu.addAction(new_action)
        more_menu.addAction(about_action)
        more_menu.addAction(options_action)

        # Create "saves" menu
        saves_menu = menubar.addMenu("Saves")
        save_slots_action = QAction("Save Slots", self)
        save_slots_action.triggered.connect(self.openSaveSlotsWindow)
        saves_menu.addAction(save_slots_action)

    def openSaveSlotsWindow(self):
        self.save_slots_widget = SaveSlotsWidget()
        self.save_slots_widget.show()



    def openOptionsWindow(self):
        options_window = OptionsWindow()
        options_window.exec_()

    def openNewWindow(self):
        new_window = CalculatorApp()
        new_window.show()
        self._instances.append(new_window)

    def openAboutWindow(self):
        about_window = AboutWindow(self.version)
        about_window.exec_()

    def buttonClicked(self):
        button = self.sender()
        button_text = button.text()

        if button_text == 'C':
            self.clearInput()
        elif button_text == 'AC':
            self.clearAll()
        elif button_text.isdigit() or button_text == '.':
            self.current_input += button_text
            self.result_display.setText(self.current_input)
        elif button_text in ['+', '-', '*', '/']:
            if self.current_input:
                self.pending_operator = button_text
                self.result = float(self.current_input)
                self.current_input = ""
                self.result_display.setText(self.pending_operator)
        elif button_text == '^':
            if self.current_input:
                self.pending_operator = '^'
                self.result = float(self.current_input)
                self.current_input = ""
                self.result_display.setText('^')
        elif button_text == '%':
            if self.current_input:
                self.pending_operator = '%'
                self.result = float(self.current_input)
                self.current_input = ""
                self.result_display.setText('%')
        elif button_text == '=':
            if self.pending_operator and self.current_input:
                if self.pending_operator == '+':
                    self.result += float(self.current_input)
                elif self.pending_operator == '-':
                    self.result -= float(self.current_input)
                elif self.pending_operator == '*':
                    self.result *= float(self.current_input)
                elif self.pending_operator == '/':
                    self.result /= float(self.current_input)
                elif self.pending_operator == '^':
                    self.result **= float(self.current_input)
                elif self.pending_operator == '%':
                    self.result %= float(self.current_input)
                self.result_display.setText(str(self.result))
                self.current_input = ""
                self.pending_operator = ""

    def clearInput(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.result_display.setText(self.current_input)

    def clearAll(self):
        self.current_input = ""
        self.pending_operator = ""
        self.result = None
        self.result_display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    calc.show()
    calc._instances.append(calc)
    sys.exit(app.exec_())

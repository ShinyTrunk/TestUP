import os
import sys
import logging
from datetime import datetime

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QAbstractItemView, \
    QHeaderView
from PyQt5.QtCore import QSize, Qt

from source.data.ui_designs.main_window_ui import Ui_MainWindow
from source.helpers.handler import Handler
from source.helpers.create_template import CreateTemplate

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.xlsx_path = ''
        logging.basicConfig(level=logging.INFO, filename="logs.txt", filemode="w")
        self.setupUi(self)
        self.initUI()
        self.tasks = []
        self.user_answers = []
        self.pointer = 0

    def initUI(self):
        main_window_icon = QPixmap("././static/img/main_window_online_learning_256x256.png")
        if main_window_icon.isNull():
            print("Error: QPixmap could not load the image.")
        self.setWindowIcon(QIcon(main_window_icon))
        self.setWindowTitle('TestUP')
        self.icon_lbl.setPixmap(main_window_icon)
        self.choose_file_btn.clicked.connect(self.choose_file)
        self.start_btn.clicked.connect(self.start_test)
        self.next_btn.clicked.connect(self.check_answer)
        self.get_hint_btn.clicked.connect(self.show_hint)
        self.get_template_btn.clicked.connect(self.install_template)
        self.back_to_menu_btn.clicked.connect(self.back_to_menu)

    def install_template(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        creator = CreateTemplate(os.path.join(desktop, 'Шаблон.xlsx'))
        creator.template_filling()

    def choose_file(self):
        self.xlsx_path = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', '*.xlsx')[0]
        handler = Handler(self.xlsx_path)
        function_response = handler.processing()
        if function_response != "Error":
            self.tasks = function_response
            self.choose_file_btn.setText(self.xlsx_path.split('/')[-1])
            self.start_btn.setEnabled(True)
        else:
            QMessageBox.critical(self, "Ошибка ", 'Ошибка импорта файла. Попробуйте ещё раз!', QMessageBox.Ok)

    def start_test(self):
        self.stack.setCurrentIndex(1)
        self.question_lbl.setText(self.tasks[self.pointer][0])

    def show_hint(self):
        self.hint_lbl.setText(self.tasks[self.pointer][2])

    def change_task(self):
        self.answer_lineedit.clear()
        self.hint_lbl.clear()
        self.question_lbl.setText(self.tasks[self.pointer][0])
        self.next_btn.setEnabled(True)

    def check_answer(self):
        self.results_table.setRowCount(len(self.tasks))
        self.results_table.setColumnCount(3)
        self.user_answers.append(self.answer_lineedit.text())
        self.pointer += 1
        count_correct_answers = 0
        if self.pointer == len(self.tasks):
            self.stack.setCurrentIndex(2)
            self.results_table.setHorizontalHeaderLabels(['Ваш ответ', 'Верный ответ', 'Вердикт'])
            for row in range(len(self.user_answers)):
                self.results_table.setItem(row, 0, QTableWidgetItem(self.user_answers[row]))
                self.results_table.setItem(row, 1, QTableWidgetItem(self.tasks[row][1]))
                if self.user_answers[row].lower() == self.tasks[row][1]:
                    self.results_table.setItem(row, 2, QTableWidgetItem('Верно'))
                    count_correct_answers += 1
                else:
                    self.results_table.setItem(row, 2, QTableWidgetItem('Неверно'))
            self.result_lbl.setText(f"Правильных ответов: {count_correct_answers}\n")
            for row in range(self.results_table.rowCount()):
                for column in range(self.results_table.columnCount()):
                    item = self.results_table.item(row, column)
                    item.setToolTip(item.text())
            self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        else:
            self.change_task()

    def back_to_menu(self):
        self.stack.setCurrentIndex(0)
        # self.tasks = []
        self.user_answers = []
        self.pointer = 0
        self.answer_lineedit.clear()

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton


class SearchDialog(QDialog):
    """ Dialog window for searching a student by name """

    def __init__(self, main_window):
        super().__init__()

        # get the main window object
        self.main_window = main_window

        # set window title and size
        self.setWindowTitle('Search Student')
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        # create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')

        button = QPushButton('Search')
        button.clicked.connect(self.search_student)

        # add widget to layout
        layout.addWidget(self.student_name)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        self.main_window.table.clearSelection()
        name = self.student_name.text()
        items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchContains)
        for item in items:
            self.main_window.table.item(item.row(), item.column()).setSelected(True)

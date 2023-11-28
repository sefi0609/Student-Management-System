from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel


class SearchDialog(QDialog):
    """ Dialog window for searching a student by name """

    def __init__(self, main_window):
        super().__init__()

        # get the main window object
        self.main_window = main_window

        # set window title and size
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        # create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')

        self.search_label = QLabel('Search By:')

        self.search_by = QComboBox()
        self.search_by.setToolTip('not case sensitive')
        self.search_by.addItems(['Exactly', 'Contains'])

        button = QPushButton('Search')
        button.clicked.connect(self.search_student)

        # add widget to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_by)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):

        # clear the selected cell of the table
        self.main_window.table.clearSelection()

        name = self.student_name.text()

        # get the items using the user preference
        match self.search_by.currentText():
            case 'Exactly':
                items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
            case 'Contains':
                items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchContains)

        # select the matching cells
        for item in items:
            self.main_window.table.item(item.row(), item.column()).setSelected(True)

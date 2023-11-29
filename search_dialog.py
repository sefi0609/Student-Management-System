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
        self.setFixedHeight(130)

        layout = QVBoxLayout()

        # create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')

        search_label = QLabel('Search By:')

        self.search_by = QComboBox()
        self.search_by.addItems(['Exactly', 'Contain'])
        self.search_by.setToolTip('not case sensitive')

        button = QPushButton('Search')
        button.clicked.connect(self.search_student)

        # add widget to layout
        layout.addWidget(self.student_name)
        layout.addWidget(search_label)
        layout.addWidget(self.search_by)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        # clear selected table cells
        self.main_window.table.clearSelection()

        name = self.student_name.text()

        # search by user reference
        match self.search_by.currentText():
            case 'Exactly':
                items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
            case 'Contain':
                items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchContains)

        # select the founded cells
        for item in items:
            self.main_window.table.item(item.row(), item.column()).setSelected(True)

from search_dialog import SearchDialog
from PyQt6.QtWidgets import QPushButton, QMainWindow, QTableWidget, QToolBar, QStatusBar, QTableWidgetItem
from PyQt6.QtGui import QAction, QIcon
from util import connect_to_db
from about_dialog import AboutDialog
from insert_dialog import InsertDialog
from delete_dialog import DeleteDialog
from edit_dialog import EditDialog


class MainWindow(QMainWindow):
    """ Main window for the application with all the functionality """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Student Management System')
        self.setMinimumSize(505, 400)

        # add menu items for the main window
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')
        edit_menu = self.menuBar().addMenu('&Edit')

        # create a widget
        add_student = QAction(QIcon('icons/add.png'), 'Add student', self)
        # connect the widget to a function, when the widget is clicked
        add_student.triggered.connect(self.insert)
        # add it to the menu bar
        file_menu.addAction(add_student)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        search = QAction(QIcon('icons/search.png'), 'Search', self)
        search.triggered.connect(self.search)
        edit_menu.addAction(search)

        # create a table widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile', 'Email'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # create toolbar and add elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addAction(add_student)
        toolbar.addAction(search)
        self.addToolBar(toolbar)

        # create a status bar and add elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        """ Load the students' data from the database """

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM students')
            result = cursor.fetchall()
            self.table.setRowCount(0)
            for row_num, row_data in enumerate(result):
                self.table.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        except Exception as e:
            print(f'Exception in MainWindow.load_data: {e}')
            raise e
        finally:
            cursor.close()
            conn.close()

        # the status bar needs to be hidden
        self.statusbar.setVisible(False)

    def cell_clicked(self):
        """ Show a status bar for every click on the table """

        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

        # the status bar needs to be visible
        self.statusbar.setVisible(True)

    def insert(self):
        dialog = InsertDialog(self)
        dialog.exec()

    def search(self):
        search_dialog = SearchDialog(self)
        search_dialog.exec()

    def edit(self):
        edit_dialog = EditDialog(self)
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog(self)
        delete_dialog.exec()

    @staticmethod
    def about():
        about_dialog = AboutDialog()
        about_dialog.exec()

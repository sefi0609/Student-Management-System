from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from util import connect_to_db, COURSES


class InsertDialog(QDialog):
    """ Dialog window to insert new student data """

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle('Enter New Student')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # create widgets
        self.name = QLineEdit()
        self.name.setPlaceholderText('Name')

        self.course = QComboBox()
        self.course.addItems(COURSES)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Mobile')

        self.email = QLineEdit()
        self.email.setPlaceholderText('Email')

        button = QPushButton('Add')
        button.clicked.connect(self.add_student)

        # add widgets to layout
        layout.addWidget(self.name)
        layout.addWidget(self.course)
        layout.addWidget(self.mobile)
        layout.addWidget(self.email)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        # add the new student data to the database
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            row = (self.name.text().title(), self.course.currentText(), self.mobile.text(), self.email.text())
            cursor.execute('INSERT INTO students (name, course, mobile, email) VALUES(%s,%s,%s,%s)', row)
            conn.commit()
        except Exception as e:
            print(f'Exception in InsertDialog.add_student: {e}')
            raise e
        finally:
            cursor.close()
            conn.close()

        # load the new data to the table
        self.main_window.load_data()
        self.close()

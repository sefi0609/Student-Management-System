from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from util import connect_to_db, COURSES


class EditDialog(QDialog):
    """ Edit window dialog to edit an existing student data """

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle('Update Student Data')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        row_index = self.main_window.table.currentRow()
        self.student_id = self.main_window.table.item(row_index, 0).text()

        # create widget
        layout = QVBoxLayout()

        # get student name from a selected row
        name = self.main_window.table.item(row_index, 1).text()
        self.name = QLineEdit(name)
        self.name.setPlaceholderText('Name')

        self.course = QComboBox()
        self.course.addItems(COURSES)

        # get course name from the selected row
        student_course = self.main_window.table.item(row_index, 2).text()
        self.course.setCurrentText(student_course)

        # get phone number from the selected row
        mobile = self.main_window.table.item(row_index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText('Mobile')

        # get email from the selected row
        email = self.main_window.table.item(row_index, 4).text()
        self.email = QLineEdit(email)
        self.email.setPlaceholderText('Email')

        button = QPushButton('Update')
        button.clicked.connect(self.update_student)

        # add widgets to layout
        layout.addWidget(self.name)
        layout.addWidget(self.course)
        layout.addWidget(self.mobile)
        layout.addWidget(self.email)
        layout.addWidget(button)

        # set the dialog window layout
        self.setLayout(layout)

    def update_student(self):
        # save updated data to the date base
        new_row = (self.name.text().title(), self.course.currentText(),
                   self.mobile.text(), self.email.text(), self.student_id)

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE students '
                           'SET name = %s, course = %s, mobile = %s, email = %s'
                           'WHERE id = %s', new_row)
            conn.commit()
        except Exception as e:
            print(f'Exception in EditDialog.update_student:  {e}')
            raise e
        finally:
            conn.close()

        # show updated data in the table
        self.main_window.load_data()
        self.close()

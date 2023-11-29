from PyQt6.QtWidgets import QDialog, QGridLayout, QPushButton, QLabel, QMessageBox
from util import connect_to_db


class DeleteDialog(QDialog):
    """ Delete window dialog to delete a student """

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle('Delete Student Data')
        self.setFixedHeight(100)
        self.setFixedWidth(200)

        # get student id
        row_index = self.main_window.table.currentRow()
        self.student_id = self.main_window.table.item(row_index, 0).text()

        layout = QGridLayout()

        # create widgets
        message = QLabel('Are you sure you want to delete?')

        yes_button = QPushButton('Yes')
        yes_button.clicked.connect(self.delete_student)

        no_button = QPushButton('No')
        no_button.clicked.connect(self.close)

        # add widgets to layout
        layout.addWidget(message, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

    def delete_student(self):
        # delete student from the database
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM students '
                           'WHERE id = %s;', (self.student_id,))
            conn.commit()
        except Exception as e:
            print(f'Exception in DeleteDialog.delete_student: {e}')
            raise e
        finally:
            cursor.close()
            conn.close()

        self.main_window.load_data()
        self.close()

        # show a confirmation message to the user
        confirmation_widget = QMessageBox()
        confirmation_widget.setText('The Student Was Successfully Deleted')
        confirmation_widget.setWindowTitle('Success')
        confirmation_widget.exec()

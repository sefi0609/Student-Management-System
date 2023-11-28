from PyQt6.QtWidgets import QMessageBox


class AboutDialog(QMessageBox):
    """ About window dialog to explain what you can do with this application """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('About')
        content = """
        This app was create for universities and colleges,
        to organize students data - name, course, mobile and email
        You can add, edit and delete students from the application
        This is a desktop app created with PyQt6
        """
        self.setText(content)

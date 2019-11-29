from PyQt5 import QtWidgets
import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()

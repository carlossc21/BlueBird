import sys
import urllib

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

from ui.mainwindow import Ui_MainWindow

    # Comprobamos que el usuario Tiene conexion a internet
def check_connection():
    try:
        urllib.request.urlopen('http://www.google.com')
        return True
    except:
        return False

if __name__ == '__main__':
    if check_connection():
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    else:
        app = QApplication([])
        msgBox = QMessageBox()
        msgBox.setText("Comprueba tu conexion a internet y vuelve a ejecutar la aplicación")
        msgBox.setWindowTitle("Sin conexión")
        msgBox.exec_()

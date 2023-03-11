from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLineEdit


class NameChooserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nombre de la lista")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        layout = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.returnPressed.connect(self.accept) # Conectar la señal returnPressed a accept
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)
        self.setStyleSheet('background-color:rgb(47, 44, 44); color:white; border:1px solid white;')


    def exec_(self):
        result = super().exec_()
        if result == QDialog.Accepted:
            return self.lineEdit.text()
        else:
            return ''
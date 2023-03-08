from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLineEdit


class NameChooserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo de cuadro de diálogo con QLineEdit")
        layout = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.returnPressed.connect(self.accept) # Conectar la señal returnPressed a accept
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

    def exec_(self):
        result = super().exec_()
        if result == QDialog.Accepted:
            return self.lineEdit.text()
        else:
            return ''
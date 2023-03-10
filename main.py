from PyQt5.QtWidgets import QApplication, QListWidget, QMenu, QListWidgetItem
from PyQt5.QtCore import Qt

class MiVentana(QListWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Agregar elementos al QListWidget
        self.addItem("Elemento 1")
        self.addItem("Elemento 2")
        self.addItem("Elemento 3")

        # Conectar el evento customContextMenuRequested a la función showContextMenu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        # Obtener el elemento seleccionado
        item = self.itemAt(pos)

        # Si no hay elementos seleccionados, salir
        if item is None:
            return

        # Crear una instancia de QMenu para nuestro menú contextual
        menu = QMenu(self)

        # Añadir acciones al menú contextual
        menu.addAction("Editar")
        menu.addAction("Eliminar")

        # Mostrar el menú contextual en la posición del cursor
        action = menu.exec_(self.mapToGlobal(pos))

        # Ejecutar la acción correspondiente al hacer clic en el menú contextual
        if action is not None:
            if action.text() == "Editar":
                self.editItem(item)
            elif action.text() == "Eliminar":
                self.takeItem(self.row(item))

if __name__ == '__main__':
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()

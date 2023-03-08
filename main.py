from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
from PyQt5.QtCore import Qt


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.inicializar_gui()

    def inicializar_gui(self):
        self.setWindowTitle("Ejemplo de menú de opciones")
        self.setGeometry(100, 100, 300, 200)

        boton = QPushButton("Haz clic derecho en mí", self)
        boton.setGeometry(50, 50, 200, 50)
        boton.setContextMenuPolicy(Qt.CustomContextMenu)
        boton.customContextMenuRequested.connect(self.mostrar_menu)

        self.show()

    def mostrar_menu(self, punto):
        menu = QMenu()
        cerrar_action = QAction("Cerrar", self)
        guardar_action = QAction("Guardar", self)
        menu.addAction(cerrar_action)
        menu.addAction(guardar_action)
        posicion_global = self.sender().mapToGlobal(punto)
        seleccion = menu.exec_(posicion_global)

        if seleccion == cerrar_action:
            self.close()
        elif seleccion == guardar_action:
            print("Guardando...")

if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaPrincipal()
    app.exec_()

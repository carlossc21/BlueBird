import os
import sys

import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, \
    QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import tempfile

from player.api import api


class Player:

    # Función para manejar el evento cuando la canción termina de reproducirse
    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            print("La canción ha terminado de reproducirse.")
            if (len(self.playlist) > 0):
                if (len(self.playlist) > self.contador):
                    response = requests.get(self.playlist[self.contador])

                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                        f.write(response.content)
                        temp_file = f.name
                        print(f"Archivo descargado y guardado en: {temp_file}")
                        self.reproductor.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file)))
                        self.reproductor.play()
                        self.contador = self.contador + 1

    def __init__(self):
        # super().__init__()
        if not os.path.exists('../ui/playlists'):
            os.makedirs('../ui/playlists')
        self.playlist = []
        self.contador = 0
        self.api = api()

        """# Configuración de ventana
        self.setWindowTitle("Reproductor de música")
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon("icon.png"))

        # Creación de widgets
        self.label_titulo = QLabel("Bienvenido al reproductor de música", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)

        self.list_canciones = QListWidget(self)

        self.btn_reproducir = QPushButton("Reproducir", self)
        self.btn_pausar = QPushButton("Pausar", self)
        self.btn_detener = QPushButton("Detener", self)

        # Configuración de layouts
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(self.label_titulo)
        layout_principal.addWidget(self.list_canciones)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_reproducir)
        layout_botones.addWidget(self.btn_pausar)
        layout_botones.addWidget(self.btn_detener)

        layout_principal.addLayout(layout_botones)

        # Conexión de señales y slots
        self.btn_reproducir.clicked.connect(self.reproducir_cancion)
        self.btn_pausar.clicked.connect(self.pausar_cancion)
        self.btn_detener.clicked.connect(self.detener_cancion)"""

        # Obtener lista de canciones de Deezer API
        self.canciones = self.obtener_canciones()
        for cancion in self.canciones:
            item = QListWidgetItem(cancion["title_short"])
            item.setData(Qt.UserRole, cancion["preview"])
            # self.list_canciones.addItem(item)

        # Configuración de reproductor
        self.reproductor = QMediaPlayer()
        self.reproductor.mediaStatusChanged.connect(self.handle_media_status)
        # self.reproducir_playlist('prueba')

    def get_playlist_content(self, playlist):
        with open("../ui/playlists/" + playlist, "r") as archivo:
            lineas = [linea.strip() for linea in archivo.readlines()]
        archivo.close()
        return lineas

    def get_playlists(self):
        files = os.listdir('../ui/playlists')

        return files

    def obtener_canciones(self):
        return self.api.obtener_canciones()

    def obtener_canciones_por_nombre(self, nombre_cancion):
       return self.api.obtener_canciones_por_nombre(nombre_cancion)

    def reproducir_cancion(self, url=None):

        # Obtener canción seleccionada
        #item = self.list_canciones.currentItem()
        #if(url==None):
            #url = item.data(Qt.UserRole)
        #self.añadir_cancion('prueba', url)

        # Cargar canción en reproductor y reproducir
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            temp_file = f.name
            print(f"Archivo descargado y guardado en: {temp_file}")
            self.reproductor.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file)))
            self.reproductor.play()

    def reproducir_playlist(self, playlist):
        self.reproductor.stop()
        with open("../ui/playlists/" + playlist, "r") as archivo:
            lineas = [linea.strip() for linea in archivo.readlines()]
            print(len(lineas))
            self.playlist = lineas
            self.contador = 0
        archivo.close()
        if(len(self.playlist)>0):
            response = requests.get(self.playlist[self.contador])
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(response.content)
                temp_file = f.name
                self.reproductor.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file)))
                self.reproductor.play()
                self.contador = self.contador + 1

    def pausar_cancion(self):
        self.reproductor.pause()

    def detener_cancion(self):
        self.reproductor.stop()

    def guardar_playlist(self, nombre):
        if not os.path.exists('../ui/playlists'):
            os.makedirs('../ui/playlists')

        with open('../ui/playlists/' + nombre, 'w') as archivo:
            archivo.write("")
            archivo.flush()
        archivo.close()

    def añadir_cancion(self, playlist, url_cancion):
        with open('../ui/playlists/' + playlist, 'a') as archivo:
            archivo.write(url_cancion + '\n')
            archivo.flush()
        archivo.close()


if __name__ == "__main__":
    # Configuración de aplicación
    app = QApplication(sys.argv)

    # Configuración de ventana
    ventana = Player()
    ventana.show()

    # Ejecución de aplicación
    sys.exit(app.exec_())

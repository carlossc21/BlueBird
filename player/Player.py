import os

import requests
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import tempfile

from player.api import api


class Player:

    # Función para manejar el evento cuando la canción termina de reproducirse
    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            if (len(self.playlist) > 0):
                if (len(self.playlist) > self.contador):
                    response = requests.get(self.playlist[self.contador].split('||')[0])

                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                        f.write(response.content)
                        temp_file = f.name
                        self.current_title = self.playlist[self.contador].split('||')[1]
                        self.current_artist = self.playlist[self.contador].split('||')[2]
                        self.reproductor.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file)))
                        self.reproductor.play()
                        self.contador = self.contador + 1

    def __init__(self):
        # super().__init__()
        if not os.path.exists('playlists'):
            os.makedirs('playlists')
        self.playlist = []
        self.contador = 0
        self.api = api()
        self.current_title = ''
        self.current_artist = ''

        # Configuración de reproductor
        self.reproductor = QMediaPlayer()
        self.reproductor.mediaStatusChanged.connect(self.handle_media_status)


    def get_playlist_content(self, playlist):
        with open("playlists/" + playlist, "r") as archivo:
            lineas = [linea.strip() for linea in archivo.readlines()]
        archivo.close()
        return lineas

    def obtener_favoritas(self):
        if os.path.exists('favoritas'):
            with open("favoritas", "r") as archivo:
                lineas = [linea.strip() for linea in archivo.readlines()]
            archivo.close()
            return lineas
        else:
            return []

    def get_playlists(self):
        files = os.listdir('playlists')

        return files

    def obtener_canciones(self):
        return self.api.obtener_canciones()

    def obtener_canciones_por_nombre(self, nombre_cancion):
        return self.api.obtener_canciones_por_nombre(nombre_cancion)

    def reproducir_cancion(self, url=None):
        # Eliminar la playlist actual para que no se siga reproduciendo al terminar la cancion seleccionada
        self.playlist = []
        # Cargar canción en reproductor y reproducir
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            temp_file = f.name
            self.reproductor.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file)))
            self.reproductor.play()

    def reproducir_playlist(self, playlist):
        self.reproductor.stop()
        with open("playlists/" + playlist, "r") as archivo:
            lineas = [linea.strip() for linea in archivo.readlines()]
            self.playlist = lineas
            self.contador = 0
        archivo.close()
        if (len(self.playlist) > 0):
            response = requests.get(self.playlist[self.contador].split('||')[0])
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(response.content)
                temp_file = f.name
                self.current_title = self.playlist[self.contador].split('||')[1]
                self.current_artist = self.playlist[self.contador].split('||')[2]
                self.reproductor.setMedia(QMediaContent(QUrl.fromLocalFile(temp_file)))
                self.reproductor.play()
                self.contador = self.contador + 1

    def borrar_playlist(self, nombre):
        os.remove('playlists/' + nombre)

    def pausar_cancion(self):
        self.reproductor.pause()

    def detener_cancion(self):
        self.reproductor.stop()

    def guardar_playlist(self, nombre):
        if not os.path.exists('playlists'):
            os.makedirs('playlists')

        with open('playlists/' + nombre, 'w') as archivo:
            archivo.write("")
            archivo.flush()
        archivo.close()

    def guardar_favoritas(self, datos):
        if not os.path.exists('favoritas'):
            with open('favoritas', 'w') as f:
                f.write('')
                f.flush()
            f.close()

        with open('favoritas', 'r') as a:
            lineas = a.readlines()
        if((datos+'\n') in lineas):
            a.close()
            return

        with open('favoritas', 'a') as archivo:
            archivo.write(datos + '\n')
            archivo.flush()
        archivo.close()

    def eliminar_favoritas(self, datos):
        with open('favoritas', "r+") as archivo:
            # Leer todas las líneas del archivo y guardarlas en una lista
            lineas = archivo.readlines()

            # Eliminar la línea deseada (por ejemplo, la segunda línea)
            del lineas[lineas.index((datos + '\n'))]

            # Volver al inicio del archivo
            archivo.seek(0)

            # Escribir de nuevo todas las líneas, excepto la eliminada
            for linea in lineas:
                archivo.write(linea)
            archivo.flush()

            # Truncar el resto del archivo (en caso de haber reducido su tamaño)
            archivo.truncate()
        archivo.close()

    def añadir_cancion(self, playlist, datos):
        with open('playlists/' + playlist, 'a') as archivo:
            archivo.write(datos + '\n')
            archivo.flush()
        archivo.close()

    def borrar_cancion(self, playlist, datos):
        with open('playlists/' + playlist, "r+") as archivo:
            # Leer todas las líneas del archivo y guardarlas en una lista
            lineas = archivo.readlines()

            # Eliminar la línea deseada (por ejemplo, la segunda línea)
            del lineas[lineas.index((datos + '\n'))]
            # Volver al inicio del archivo
            archivo.seek(0)

            # Escribir de nuevo todas las líneas, excepto la eliminada
            for linea in lineas:
                archivo.write(linea)
            archivo.flush()

            # Truncar el resto del archivo (en caso de haber reducido su tamaño)
            archivo.truncate()
        archivo.close()

    def descargar_cancion(self, url, nombre):
        response = requests.get(url)
        ruta_directorio = QFileDialog.getExistingDirectory(None, 'Selecciona un directorio')
        if(ruta_directorio == ''):
            return
        with open(ruta_directorio + '/' + nombre + '.mp3', 'wb') as f:
            f.write(response.content)
            f.flush()
        f.close()

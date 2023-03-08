import requests


class api:
    def obtener_canciones_por_nombre(self, nombre_cancion):
        # La URL de la API de Deezer para buscar canciones por nombre
        url = 'https://api.deezer.com/search?q={}'.format(nombre_cancion)

        # Realizamos la solicitud HTTP a la API
        respuesta = requests.get(url)

        # Si la solicitud fue exitosa, devolvemos los datos en formato JSON
        if respuesta.status_code == 200:
            return respuesta.json()['data']
        else:
            # Si hubo un error en la solicitud, mostramos un mensaje de error

            print('Error al obtener canciones: {}'.format(respuesta.status_code))
            return []

    def obtener_canciones(self):
        # Realizar petición a Deezer API
        response = requests.get("https://api.deezer.com/chart/0/tracks")

        # Obtener lista de canciones
        if response.status_code == 200:
            canciones = response.json()["data"]

            return canciones
        else:
            return []

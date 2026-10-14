import json
import os


# Capa de datos: el archivo json funciona como base de datos
class RepositorioJSON:
    def __init__(self, ruta=None):
        if ruta is None:
            carpeta = os.path.dirname(os.path.abspath(__file__))
            ruta = os.path.join(carpeta, "base_datos.json")
        self._ruta = ruta

    @property
    def ruta(self):
        return self._ruta

    # Guarda el diccionario completo en el archivo
    def guardar(self, datos):
        archivo = open(self._ruta, "w", encoding="utf-8")
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        archivo.close()

    # Lee el archivo, si no existe o esta danado devuelve un diccionario vacio
    def cargar(self):
        try:
            archivo = open(self._ruta, "r", encoding="utf-8")
            datos = json.load(archivo)
            archivo.close()
            return datos
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

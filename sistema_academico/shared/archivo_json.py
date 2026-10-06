import json
import os


class ArchivoJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON.

    Es la ÚNICA clase del sistema que toca el disco. No sabe qué es un
    Estudiante ni un Docente: solo recibe y devuelve listas de diccionarios.
    """

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)
        # PROCESO 7: la carpeta data/ se crea sola si no existe
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        # Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except (TypeError, OSError):
            # TypeError aparece si se intenta guardar un set: JSON no lo conoce
            return False

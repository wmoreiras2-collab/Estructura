import os

from shared.archivo_json import ArchivoJSON
from shared.validaciones import es_email_valido


class ControladorBase:
    """CONTROLADOR genérico: las 5 operaciones (crear, leer, buscar, editar, eliminar).

    Cada controlador concreto solo declara sus campos y sus reglas propias.
    Reglas que se cumplen en todo el archivo:
      - Cero print() y cero input(): el Controlador no habla con el usuario.
      - Toda operación devuelve una tupla (exito, mensaje) o datos.
      - Las validaciones ocurren ANTES de tocar el archivo.
    """

    NOMBRE = "registro"        # texto para los mensajes
    FINAL = "o"                # "o" -> creado, "a" -> creada
    ARCHIVO = ""               # nombre del .json dentro de data/
    MODELO = None              # clase del Modelo
    CAMPOS = ()                # TUPLA de campos (sin el id)
    OBLIGATORIOS = ()          # TUPLA de campos que no pueden ir vacíos
    BUSCABLES = ()             # TUPLA de campos donde se busca el texto
    UNICOS = ()                # TUPLA de campos que no pueden repetirse

    def __init__(self, carpeta_datos):
        self.gestor = ArchivoJSON(os.path.join(carpeta_datos, self.ARCHIVO))
        # LISTA de funciones f(id) -> mensaje | None que pueden impedir un borrado
        self.restricciones = []

    # ===================== AYUDAS INTERNAS =====================
    def agregar_restriccion(self, funcion):
        self.restricciones.append(funcion)

    def valores_usados(self, campo, excepto_id=None):
        """CONJUNTO con los valores ya usados de un campo (en minúsculas)."""
        return {
            str(registro.get(campo, "")).strip().lower()
            for registro in self.gestor.leer()
            if registro["id"] != excepto_id
        }

    def siguiente_id(self):
        ids = [registro["id"] for registro in self.gestor.leer()]
        return max(ids) + 1 if ids else 1

    def _posicion(self, registros, id_registro):
        for indice, registro in enumerate(registros):
            if registro["id"] == id_registro:
                return indice
        return None

    def _revisar(self, valores, excepto_id=None):
        """Devuelve un mensaje de error o None si todo está bien."""
        if "email" in valores and not es_email_valido(valores["email"]):
            return f"El email '{valores['email']}' no tiene un formato válido"
        error = self.validar(valores, excepto_id)
        if error:
            return error
        # Duplicados: búsqueda instantánea dentro de un CONJUNTO
        for campo in self.UNICOS:
            if campo in valores:
                if str(valores[campo]).strip().lower() in self.valores_usados(campo, excepto_id):
                    return f"Ya existe un {self.NOMBRE} con {campo} '{valores[campo]}'"
        return None

    # ---- ganchos que cada controlador concreto puede sobrescribir ----
    def convertir(self, valores):
        """Convierte textos a su tipo real (int, etc.). Lanza ValueError si falla."""
        return valores

    def validar(self, valores, excepto_id=None):
        """Reglas propias del controlador. Devuelve un mensaje de error o None."""
        return None

    def crear_objeto(self, id_registro, valores):
        return self.MODELO(id_registro, *[valores[campo] for campo in self.CAMPOS])

    def fila(self, objeto):
        """DICCIONARIO listo para que la Vista lo muestre en una tabla."""
        fila = objeto.a_diccionario()
        if hasattr(objeto, "obtener_nombre_completo"):
            fila["nombre_completo"] = objeto.obtener_nombre_completo()
        return fila

    # ===================== C · CREATE =====================
    def crear(self, datos):
        """datos: diccionario con las claves de CAMPOS. Devuelve (exito, mensaje)."""
        try:
            valores = {campo: str(datos.get(campo, "")).strip() for campo in self.CAMPOS}
            faltantes = [campo for campo in self.OBLIGATORIOS if not valores[campo]]
            if faltantes:
                return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"
            valores = self.convertir(valores)
            error = self._revisar(valores)
            if error:
                return False, error
            objeto = self.crear_objeto(self.siguiente_id(), valores)
            registros = self.gestor.leer()
            registros.append(objeto.a_diccionario())
            if not self.gestor.guardar(registros):
                return False, "No se pudo escribir el archivo"
            return True, f"{self.NOMBRE.capitalize()} cread{self.FINAL} con id {objeto.id}"
        except ValueError as error:
            return False, str(error)
        except Exception as error:
            return False, f"Error inesperado: {error}"

    # ===================== R · READ =====================
    def obtener_todos(self):
        """LISTA de objetos del Modelo."""
        return [self.MODELO.desde_diccionario(registro) for registro in self.gestor.leer()]

    def obtener_por_id(self, id_registro):
        for objeto in self.obtener_todos():
            if objeto.id == id_registro:
                return objeto
        return None

    # ===================== S · SEARCH =====================
    def buscar(self, termino):
        """Búsqueda lineal en los campos de BUSCABLES."""
        termino = str(termino).strip().lower()
        if not termino:
            return []
        encontrados = []
        for registro in self.gestor.leer():
            for campo in self.BUSCABLES:                  # recorro la TUPLA
                if termino in str(registro.get(campo, "")).lower():
                    encontrados.append(self.MODELO.desde_diccionario(registro))
                    break                                  # ya coincidió
        return encontrados

    # ===================== U · UPDATE =====================
    def actualizar(self, id_registro, cambios):
        """cambios: diccionario solo con los campos que se quieren modificar."""
        try:
            # DIFERENCIA DE CONJUNTOS: ¿mandaron un campo que no existe?
            desconocidos = set(cambios) - set(self.CAMPOS)
            if desconocidos:
                return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
            if not cambios:
                return False, "No se indicó ningún cambio"
            cambios = {campo: str(valor).strip() for campo, valor in cambios.items()}
            vacios = [c for c in cambios if c in self.OBLIGATORIOS and not cambios[c]]
            if vacios:
                return False, f"Estos campos no pueden quedar vacíos: {', '.join(vacios)}"
            registros = self.gestor.leer()
            posicion = self._posicion(registros, id_registro)
            if posicion is None:
                return False, f"No existe un {self.NOMBRE} con id {id_registro}"
            cambios = self.convertir(cambios)
            error = self._revisar(cambios, excepto_id=id_registro)
            if error:
                return False, error
            registros[posicion].update(cambios)
            if not self.gestor.guardar(registros):
                return False, "No se pudo escribir el archivo"
            return True, f"{self.NOMBRE.capitalize()} {id_registro} actualizad{self.FINAL} ({len(cambios)} campo/s)"
        except ValueError as error:
            return False, str(error)
        except Exception as error:
            return False, f"Error inesperado: {error}"

    # ===================== D · DELETE =====================
    def eliminar(self, id_registro):
        registros = self.gestor.leer()
        if self._posicion(registros, id_registro) is None:
            return False, f"No existe un {self.NOMBRE} con id {id_registro}"
        for restriccion in self.restricciones:
            motivo = restriccion(id_registro)
            if motivo:
                return False, f"No se puede eliminar: {motivo}"
        # LISTA NUEVA sin ese registro: nunca se borra mientras se recorre
        quedan = [registro for registro in registros if registro["id"] != id_registro]
        if not self.gestor.guardar(quedan):
            return False, "No se pudo escribir el archivo"
        return True, f"{self.NOMBRE.capitalize()} {id_registro} eliminad{self.FINAL}"

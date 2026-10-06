from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.validaciones import es_carnet_valido, convertir_numero, es_nota_valida
from .controlador_base import ControladorBase


class ControladorEstudiante(ControladorBase):
    NOMBRE = "estudiante"
    ARCHIVO = "estudiantes.json"
    MODELO = Estudiante
    CAMPOS = CAMPOS_ESTUDIANTE
    OBLIGATORIOS = CAMPOS_ESTUDIANTE
    BUSCABLES = ("nombre", "apellido", "email", "carnet")
    UNICOS = ("email", "carnet")          # los dos se revisan con un CONJUNTO

    def validar(self, valores, excepto_id=None):
        if "carnet" in valores and not es_carnet_valido(valores["carnet"]):
            return "El carnet debe tener al menos 4 caracteres, solo letras y números"
        return None

    def fila(self, estudiante):
        fila = super().fila(estudiante)
        fila["promedio"] = estudiante.obtener_promedio()
        return fila

    # Nombres que pide la guía; delegan en las operaciones genéricas
    crear_estudiante = ControladorBase.crear
    buscar_estudiantes = ControladorBase.buscar
    actualizar_estudiante = ControladorBase.actualizar
    eliminar_estudiante = ControladorBase.eliminar

    # ===================== OPERACIONES PROPIAS =====================
    def _con_estudiante(self, id_estudiante, accion):
        """Lee, aplica accion(estudiante) y guarda. Evita repetir código."""
        registros = self.gestor.leer()
        posicion = self._posicion(registros, id_estudiante)
        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        estudiante = Estudiante.desde_diccionario(registros[posicion])
        mensaje = accion(estudiante)
        registros[posicion] = estudiante.a_diccionario()
        if not self.gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, mensaje

    def agregar_nota(self, id_estudiante, materia, nota):
        materia = str(materia).strip()
        if not materia:
            return False, "La materia es obligatoria"
        valor = convertir_numero(nota)
        if not es_nota_valida(valor):
            return False, "La nota debe ser un número entre 0 y 20"
        if valor == int(valor):
            valor = int(valor)          # 18.0 se guarda como 18

        def accion(estudiante):
            estudiante.agregar_nota(materia, valor)
            return f"Nota {valor} agregada en {materia} (promedio: {estudiante.obtener_promedio()})"
        return self._con_estudiante(id_estudiante, accion)

    def inscribir_materia(self, id_estudiante, materia):
        materia = str(materia).strip()
        if not materia:
            return False, "La materia es obligatoria"

        def accion(estudiante):
            if materia in estudiante.materias:
                return f"Ya estaba inscrito en {materia}"
            estudiante.inscribir_materia(materia)
            return f"Inscrito en {materia}"
        return self._con_estudiante(id_estudiante, accion)

    def obtener_promedio(self, id_estudiante):
        estudiante = self.obtener_por_id(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        return True, estudiante.obtener_promedio()

    def materias_ofertadas(self):
        """CONJUNTO con todas las materias inscritas por todos los estudiantes."""
        todas = set()
        for estudiante in self.obtener_todos():
            todas |= estudiante.materias            # unión de conjuntos
        return todas

    def estudiantes_en_comun(self, id_a, id_b):
        """Devuelve (True, set de materias compartidas) o (False, mensaje)."""
        if id_a == id_b:
            return False, "Debe elegir dos estudiantes distintos"
        a = self.obtener_por_id(id_a)
        b = self.obtener_por_id(id_b)
        if a is None or b is None:
            return False, "Alguno de los dos ids no existe"
        return True, a.materias_en_comun(b)         # INTERSECCIÓN

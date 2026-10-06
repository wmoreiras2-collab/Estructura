from models import Curso, CAMPOS_CURSO
from shared.validaciones import convertir_entero
from .controlador_base import ControladorBase


class ControladorCurso(ControladorBase):
    """Un curso depende de los otros tres controladores (se los entrega main.py)."""

    NOMBRE = "curso"
    ARCHIVO = "cursos.json"
    MODELO = Curso
    CAMPOS = CAMPOS_CURSO
    OBLIGATORIOS = CAMPOS_CURSO
    BUSCABLES = ("codigo", "periodo")
    UNICOS = ("codigo",)
    CAMPOS_ENTEROS = ("id_asignatura", "id_docente", "cupo")

    def __init__(self, carpeta_datos, asignaturas, docentes, estudiantes):
        super().__init__(carpeta_datos)
        self.asignaturas = asignaturas
        self.docentes = docentes
        self.estudiantes = estudiantes

    def convertir(self, valores):
        convertidos = dict(valores)
        for campo in self.CAMPOS_ENTEROS:
            if campo in convertidos:
                numero = convertir_entero(convertidos[campo])
                if numero is None or numero < 1:
                    raise ValueError(f"'{campo}' debe ser un número entero mayor que 0")
                convertidos[campo] = numero
        return convertidos

    def validar(self, valores, excepto_id=None):
        if "id_asignatura" in valores and self.asignaturas.obtener_por_id(valores["id_asignatura"]) is None:
            return f"No existe una asignatura con id {valores['id_asignatura']}"
        if "id_docente" in valores and self.docentes.obtener_por_id(valores["id_docente"]) is None:
            return f"No existe un docente con id {valores['id_docente']}"
        if "cupo" in valores and excepto_id is not None:
            curso = self.obtener_por_id(excepto_id)
            if curso and valores["cupo"] < len(curso.estudiantes):
                return f"El cupo no puede ser menor que los {len(curso.estudiantes)} estudiantes ya inscritos"
        return None

    def fila(self, curso):
        fila = super().fila(curso)
        asignatura = self.asignaturas.obtener_por_id(curso.id_asignatura)
        docente = self.docentes.obtener_por_id(curso.id_docente)
        fila["asignatura"] = asignatura.nombre if asignatura else "(eliminada)"
        fila["docente"] = docente.obtener_nombre_completo() if docente else "(eliminado)"
        fila["inscritos"] = f"{len(curso.estudiantes)}/{curso.cupo}"
        return fila

    crear_curso = ControladorBase.crear
    buscar_cursos = ControladorBase.buscar
    actualizar_curso = ControladorBase.actualizar
    eliminar_curso = ControladorBase.eliminar

    # ===================== OPERACIONES PROPIAS =====================
    def inscribir_estudiante(self, id_curso, id_estudiante):
        registros = self.gestor.leer()
        posicion = self._posicion(registros, id_curso)
        if posicion is None:
            return False, f"No existe un curso con id {id_curso}"
        estudiante = self.estudiantes.obtener_por_id(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        curso = Curso.desde_diccionario(registros[posicion])
        if id_estudiante in curso.estudiantes:              # búsqueda en el CONJUNTO
            return False, "El estudiante ya está inscrito en este curso"
        if not curso.tiene_cupo():
            return False, "El curso no tiene cupos disponibles"
        curso.estudiantes.add(id_estudiante)
        registros[posicion] = curso.a_diccionario()
        if not self.gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        # La asignatura pasa a las materias del estudiante (conjunto, sin repetidos)
        asignatura = self.asignaturas.obtener_por_id(curso.id_asignatura)
        if asignatura:
            self.estudiantes.inscribir_materia(id_estudiante, asignatura.nombre)
        return True, (f"{estudiante.obtener_nombre_completo()} inscrito en {curso.codigo} "
                      f"({len(curso.estudiantes)}/{curso.cupo})")

    def retirar_estudiante(self, id_curso, id_estudiante):
        registros = self.gestor.leer()
        posicion = self._posicion(registros, id_curso)
        if posicion is None:
            return False, f"No existe un curso con id {id_curso}"
        curso = Curso.desde_diccionario(registros[posicion])
        if id_estudiante not in curso.estudiantes:
            return False, "El estudiante no está inscrito en este curso"
        curso.estudiantes.discard(id_estudiante)
        registros[posicion] = curso.a_diccionario()
        if not self.gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Estudiante {id_estudiante} retirado de {curso.codigo}"

    def detalle(self, id_curso):
        """Devuelve (fila, lista de TUPLAS (id, nombre, carnet)) o None."""
        curso = self.obtener_por_id(id_curso)
        if curso is None:
            return None
        inscritos = []
        for id_estudiante in sorted(curso.estudiantes):
            estudiante = self.estudiantes.obtener_por_id(id_estudiante)
            if estudiante:
                inscritos.append((estudiante.id, estudiante.obtener_nombre_completo(),
                                  estudiante.carnet))
        return self.fila(curso), inscritos

    # ---- restricciones de borrado: se registran en los otros controladores ----
    def _cursos_que_usan(self, campo, id_registro):
        return [r for r in self.gestor.leer() if r.get(campo) == id_registro]

    def bloqueo_docente(self, id_docente):
        usados = self._cursos_que_usan("id_docente", id_docente)
        return f"el docente dicta {len(usados)} curso(s)" if usados else None

    def bloqueo_asignatura(self, id_asignatura):
        usados = self._cursos_que_usan("id_asignatura", id_asignatura)
        return f"la asignatura se usa en {len(usados)} curso(s)" if usados else None

    def bloqueo_estudiante(self, id_estudiante):
        inscritos = [r for r in self.gestor.leer() if id_estudiante in r.get("estudiantes", [])]
        return f"el estudiante está inscrito en {len(inscritos)} curso(s)" if inscritos else None

import os

from controllers import (
    ControladorEstudiante, ControladorDocente, ControladorAsignatura, ControladorCurso,
)
from views import InterfazConsola


class SistemaAcademico:
    """PROCESO 6: integra Modelos, Controladores y Vista. Aquí no hay reglas de negocio."""

    def __init__(self, carpeta_datos=None):
        # La carpeta data/ queda junto a main.py, sin importar desde dónde se ejecute
        if carpeta_datos is None:
            carpeta_datos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

        self.estudiantes = ControladorEstudiante(carpeta_datos)
        self.docentes = ControladorDocente(carpeta_datos)
        self.asignaturas = ControladorAsignatura(carpeta_datos)
        self.cursos = ControladorCurso(carpeta_datos, self.asignaturas,
                                       self.docentes, self.estudiantes)

        # Integridad: no se puede borrar algo que un curso está usando
        self.estudiantes.agregar_restriccion(self.cursos.bloqueo_estudiante)
        self.docentes.agregar_restriccion(self.cursos.bloqueo_docente)
        self.asignaturas.agregar_restriccion(self.cursos.bloqueo_asignatura)

        self.interfaz = InterfazConsola(self.estudiantes, self.docentes,
                                        self.asignaturas, self.cursos)

    def ejecutar(self):
        self.interfaz.menu_principal()


if __name__ == "__main__":
    try:
        SistemaAcademico().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")

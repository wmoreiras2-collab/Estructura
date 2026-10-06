CAMPOS_CURSO = ("codigo", "id_asignatura", "id_docente", "periodo", "cupo")


class Curso:
    """MODELO: un curso une una asignatura, un docente y un grupo de estudiantes."""

    def __init__(self, id_curso, codigo, id_asignatura, id_docente, periodo, cupo,
                 estudiantes=None):
        self.id = id_curso
        self.codigo = codigo
        self.id_asignatura = id_asignatura
        self.id_docente = id_docente
        self.periodo = periodo        # ej: 2026-2
        self.cupo = cupo
        # CONJUNTO de ids de estudiantes: nadie puede inscribirse dos veces
        self.estudiantes = set(estudiantes) if estudiantes else set()

    def cupos_libres(self):
        return self.cupo - len(self.estudiantes)

    def tiene_cupo(self):
        return self.cupos_libres() > 0

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "id_asignatura": self.id_asignatura,
            "id_docente": self.id_docente,
            "periodo": self.periodo,
            "cupo": self.cupo,
            # set -> lista ordenada para poder guardarlo en JSON
            "estudiantes": sorted(self.estudiantes),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["codigo"], datos["id_asignatura"],
            datos["id_docente"], datos["periodo"], datos["cupo"],
            estudiantes=set(datos.get("estudiantes", [])),   # lista -> set
        )

    def __str__(self):
        return f"[{self.codigo}] {self.periodo} - {len(self.estudiantes)}/{self.cupo} inscritos"

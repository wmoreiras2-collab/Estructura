CAMPOS_ASIGNATURA = ("codigo", "nombre", "creditos")


class Asignatura:
    """MODELO: representa una asignatura (materia) del plan de estudios."""

    def __init__(self, id_asignatura, codigo, nombre, creditos):
        self.id = id_asignatura
        self.codigo = codigo          # ej: EDD101
        self.nombre = nombre
        self.creditos = creditos      # entero

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": self.creditos,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["id"], datos["codigo"], datos["nombre"], datos["creditos"])

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} ({self.creditos} créditos)"

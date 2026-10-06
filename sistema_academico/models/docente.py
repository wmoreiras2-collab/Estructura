CAMPOS_DOCENTE = ("nombre", "apellido", "email", "especialidad", "telefono")


class Docente:
    """MODELO: representa a un docente."""

    def __init__(self, id_docente, nombre, apellido, email, especialidad, telefono=""):
        self.id = id_docente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.especialidad = especialidad
        self.telefono = telefono

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "especialidad": self.especialidad,
            "telefono": self.telefono,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos.get("especialidad", ""),
            datos.get("telefono", ""),
        )

    def __str__(self):
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.especialidad}"

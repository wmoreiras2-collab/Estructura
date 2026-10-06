from models import Docente, CAMPOS_DOCENTE
from .controlador_base import ControladorBase


class ControladorDocente(ControladorBase):
    NOMBRE = "docente"
    ARCHIVO = "docentes.json"
    MODELO = Docente
    CAMPOS = CAMPOS_DOCENTE
    OBLIGATORIOS = ("nombre", "apellido", "email", "especialidad")   # teléfono es opcional
    BUSCABLES = ("nombre", "apellido", "email", "especialidad")
    UNICOS = ("email",)

    crear_docente = ControladorBase.crear
    buscar_docentes = ControladorBase.buscar
    actualizar_docente = ControladorBase.actualizar
    eliminar_docente = ControladorBase.eliminar

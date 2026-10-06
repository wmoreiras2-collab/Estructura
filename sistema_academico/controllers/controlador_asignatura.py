from models import Asignatura, CAMPOS_ASIGNATURA
from shared.validaciones import convertir_entero
from .controlador_base import ControladorBase

CREDITOS_MINIMOS = 1
CREDITOS_MAXIMOS = 10


class ControladorAsignatura(ControladorBase):
    NOMBRE = "asignatura"
    FINAL = "a"
    ARCHIVO = "asignaturas.json"
    MODELO = Asignatura
    CAMPOS = CAMPOS_ASIGNATURA
    OBLIGATORIOS = CAMPOS_ASIGNATURA
    BUSCABLES = ("codigo", "nombre")
    UNICOS = ("codigo",)

    def convertir(self, valores):
        convertidos = dict(valores)
        if "creditos" in convertidos:
            creditos = convertir_entero(convertidos["creditos"])
            if creditos is None or not CREDITOS_MINIMOS <= creditos <= CREDITOS_MAXIMOS:
                raise ValueError(
                    f"Los créditos deben ser un entero entre {CREDITOS_MINIMOS} y {CREDITOS_MAXIMOS}")
            convertidos["creditos"] = creditos
        return convertidos

    crear_asignatura = ControladorBase.crear
    buscar_asignaturas = ControladorBase.buscar
    actualizar_asignatura = ControladorBase.actualizar
    eliminar_asignatura = ControladorBase.eliminar

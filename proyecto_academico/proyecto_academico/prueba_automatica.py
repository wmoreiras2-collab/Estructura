"""Prueba automática de las reglas del negocio (no usa el menú, usa los controladores)."""
import os
import shutil
import tempfile

from models import Estudiante, Materia, Matricula
from views import EstudianteController, MateriaController, MatriculaController

carpeta = tempfile.mkdtemp()
try:
    est = EstudianteController(os.path.join(carpeta, "estudiantes.json"))
    mat = MateriaController(os.path.join(carpeta, "materias.json"))
    mac = MatriculaController(est, mat, os.path.join(carpeta, "matriculas.json"))

    def ok(titulo, resultado, esperado_exito):
        marca = "OK " if resultado[0] == esperado_exito else "FALLA"
        print(f"[{marca}] {titulo}: {resultado[1]}")
        assert resultado[0] == esperado_exito, titulo

    # ---------- Estudiantes ----------
    ok("crear estudiante", est.crear({"nombre": "ana", "apellido": "perez", "email": "ANA@U.edu",
                                      "carnet": "est2026001", "carrera": "software"}), True)
    ok("email repetido", est.crear({"nombre": "Luis", "apellido": "Mora", "email": "ana@u.edu",
                                    "carnet": "EST2026002"}), False)
    ok("carnet repetido", est.crear({"nombre": "Luis", "apellido": "Mora", "email": "luis@u.edu",
                                     "carnet": "EST2026001"}), False)
    ok("email inválido", est.crear({"nombre": "Luis", "apellido": "Mora", "email": "luis",
                                    "carnet": "EST2026002"}), False)
    ok("falta carnet", est.crear({"nombre": "Luis", "apellido": "Mora", "email": "luis@u.edu"}), False)
    ok("segundo estudiante", est.crear({"nombre": "Luis", "apellido": "Mora", "email": "luis@u.edu",
                                        "carnet": "EST2026002", "carrera": "Software"}), True)
    ok("actualizar carrera", est.actualizar(2, {"carrera": "sistemas"}), True)
    ok("actualizar campo invalido", est.actualizar(2, {"edad": "20"}), False)
    ok("actualizar con carnet duplicado", est.actualizar(2, {"carnet": "est2026001"}), False)
    assert len(est.buscar("est2026")) == 2 and len(est.buscar("zzz")) == 0
    assert est.carreras() == ["Sistemas", "Software"], est.carreras()
    print(est.obtener(1))

    # ---------- Materias ----------
    ok("crear materia", mat.crear({"nombre": "calculo i", "codigo": "mat101", "creditos": "4", "cupos": "2"}), True)
    ok("código repetido", mat.crear({"nombre": "Otra", "codigo": "MAT101", "creditos": "3"}), False)
    ok("créditos fuera de rango", mat.crear({"nombre": "Otra", "codigo": "FIS1", "creditos": "11"}), False)
    ok("cupos fuera de rango", mat.crear({"nombre": "Otra", "codigo": "FIS1", "creditos": "3", "cupos": "31"}), False)
    ok("materia sin cupos escritos", mat.crear({"nombre": "Fisica", "codigo": "FIS1", "creditos": "3"}), True)
    assert mat.obtener(2).cupos == Materia.CUPOS_MAXIMOS

    # ---------- Matrículas ----------
    ok("matricular 1", mac.crear({"estudiante_id": 1, "materia_id": 1, "periodo": "2026-1"}), True)
    assert mat.obtener(1).cupos == 1, "el cupo debe bajar"
    ok("matrícula doble", mac.crear({"estudiante_id": 1, "materia_id": 1, "periodo": "2026-1"}), False)
    ok("mismo estudiante y materia, otro periodo", mac.crear({"estudiante_id": 1, "materia_id": 1, "periodo": "2026-2"}), True)
    assert mat.obtener(1).cupos == 0
    ok("sin cupo", mac.crear({"estudiante_id": 2, "materia_id": 1, "periodo": "2026-1"}), False)
    ok("estudiante inexistente", mac.crear({"estudiante_id": 99, "materia_id": 2, "periodo": "2026-1"}), False)
    ok("materia inexistente", mac.crear({"estudiante_id": 1, "materia_id": 99, "periodo": "2026-1"}), False)
    assert [m.nombre for m in mat.materias_sin_cupo()] == ["Calculo I"]

    ok("nota valida", mac.registrar_nota(1, "16.5"), True)
    ok("nota > 20", mac.registrar_nota(1, "21"), False)
    ok("nota texto", mac.registrar_nota(1, "abc"), False)
    ok("nota 10", mac.registrar_nota(2, "10"), True)
    assert mac.obtener(1).estado() == "Aprobado" and mac.obtener(2).estado() == "Reprobado"
    assert mac.promedio_de_estudiante(1) == 13.25 and mac.promedio_de_estudiante(2) is None
    assert {k: len(v) for k, v in mac.matriculas_por_estudiante().items()} == {1: 2}
    print(mac.certificado(1))

    ok("retirar matricula", mac.retirar_matricula(2), True)
    assert mat.obtener(1).cupos == 1, "el cupo debe volver"

    # ---------- Persistencia ----------
    est2 = EstudianteController(os.path.join(carpeta, "estudiantes.json"))
    mat2 = MateriaController(os.path.join(carpeta, "materias.json"))
    mac2 = MatriculaController(est2, mat2, os.path.join(carpeta, "matriculas.json"))
    assert len(est2.leer()) == 2 and len(mat2.leer()) == 2 and len(mac2.leer()) == 1
    assert isinstance(est2.obtener(1), Estudiante) and isinstance(mac2.obtener(1), Matricula)
    print("\nTODAS LAS PRUEBAS PASARON")
finally:
    shutil.rmtree(carpeta)

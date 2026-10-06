"""Pruebas automáticas de los controladores. Ejecutar: python pruebas.py
Usan una carpeta temporal: no tocan tu carpeta data/."""
import json
import os
import tempfile

from main import SistemaAcademico

contador = {"ok": 0}


def verificar(descripcion, condicion):
    assert condicion, f"FALLÓ: {descripcion}"
    contador["ok"] += 1
    print(f"  ✓ {descripcion}")


def prueba():
    with tempfile.TemporaryDirectory() as carpeta:
        s = SistemaAcademico(carpeta)
        est, doc, asig, cur = s.estudiantes, s.docentes, s.asignaturas, s.cursos

        print("ESTUDIANTES")
        d = {"nombre": "Ana", "apellido": "Pérez", "email": "ana@escuela.edu", "carnet": "EST2026001"}
        verificar("crear estudiante", est.crear_estudiante(d)[0])
        verificar("email duplicado (sin importar mayúsculas)",
                  not est.crear({**d, "carnet": "EST2026009", "email": "ANA@escuela.edu"})[0])
        verificar("carnet duplicado", not est.crear({**d, "email": "otro@escuela.edu"})[0])
        verificar("email inválido", not est.crear({**d, "email": "ana", "carnet": "EST2026002"})[0])
        verificar("campo obligatorio vacío", not est.crear({**d, "nombre": ""})[0])
        verificar("crear segundo estudiante", est.crear(
            {"nombre": "Luis", "apellido": "García", "email": "luis@escuela.edu", "carnet": "EST2026002"})[0])
        verificar("buscar por carnet", len(est.buscar_estudiantes("2026002")) == 1)
        verificar("buscar texto vacío devuelve []", est.buscar("  ") == [])
        verificar("actualizar sin cambios falla", not est.actualizar(1, {})[0])
        verificar("actualizar campo desconocido falla", not est.actualizar(1, {"edad": "20"})[0])
        verificar("actualizar a email de otro falla", not est.actualizar(1, {"email": "luis@escuela.edu"})[0])
        verificar("actualizar su propio email sí", est.actualizar(1, {"email": "ana@escuela.edu"})[0])
        verificar("actualizar id inexistente falla", not est.actualizar(99, {"nombre": "X"})[0])

        print("NOTAS Y MATERIAS")
        for nota in ("21", "-1", "abc", "nan", "inf", ""):
            verificar(f"nota inválida '{nota}'", not est.agregar_nota(1, "Matemática", nota)[0])
        verificar("nota en id inexistente", not est.agregar_nota(99, "Matemática", "10")[0])
        verificar("nota 18", est.agregar_nota(1, "Matemática", "18")[0])
        verificar("nota 19,5 (coma decimal)", est.agregar_nota(1, "Matemática", "19,5")[0])
        verificar("nota 0 y 20 son válidas",
                  est.agregar_nota(1, "Inglés", "0")[0] and est.agregar_nota(1, "Inglés", "20")[0])
        verificar("promedio correcto", est.obtener_promedio(1) == (True, 14.38))
        verificar("Luis inscrito en Inglés", est.inscribir_materia(2, "Inglés")[0])
        verificar("materias en común = {Inglés}", est.estudiantes_en_comun(1, 2) == (True, {"Inglés"}))
        verificar("mismo estudiante dos veces falla", not est.estudiantes_en_comun(1, 1)[0])
        verificar("materias ofertadas sin repetir", est.materias_ofertadas() == {"Matemática", "Inglés"})

        print("PERSISTENCIA EN JSON")
        with open(os.path.join(carpeta, "estudiantes.json"), encoding="utf-8") as f:
            crudo = json.load(f)
        verificar("materias se guarda como lista ordenada", crudo[0]["materias"] == ["Inglés", "Matemática"])
        s2 = SistemaAcademico(carpeta)            # "reinicia" el programa
        ana = s2.estudiantes.obtener_por_id(1)
        verificar("al volver a leer, materias es set", ana.materias == {"Inglés", "Matemática"}
                  and isinstance(ana.materias, set))
        verificar("notas sobreviven al reinicio", ana.notas["Matemática"] == [18, 19.5])

        print("DOCENTES Y ASIGNATURAS")
        verificar("crear docente (teléfono opcional)", doc.crear_docente(
            {"nombre": "Daniel", "apellido": "Vera", "email": "dvera@unemi.edu.ec", "especialidad": "Programación"})[0])
        verificar("email de docente duplicado", not doc.crear(
            {"nombre": "X", "apellido": "Y", "email": "dvera@unemi.edu.ec", "especialidad": "Z"})[0])
        verificar("crear asignatura", asig.crear_asignatura(
            {"codigo": "EDD101", "nombre": "Estructura de Datos", "creditos": "4"})[0])
        verificar("código de asignatura duplicado", not asig.crear(
            {"codigo": "edd101", "nombre": "Otra", "creditos": "3"})[0])
        for cred in ("0", "11", "x", "2.5"):
            verificar(f"créditos inválidos '{cred}'", not asig.crear(
                {"codigo": f"C{cred}", "nombre": "N", "creditos": cred})[0])
        verificar("créditos guardados como entero", asig.obtener_por_id(1).creditos == 4)

        print("CURSOS")
        c = {"codigo": "EDD101-A", "id_asignatura": "1", "id_docente": "1", "periodo": "2026-2", "cupo": "1"}
        verificar("crear curso", cur.crear_curso(c)[0])
        verificar("curso con asignatura inexistente", not cur.crear({**c, "codigo": "Z", "id_asignatura": "9"})[0])
        verificar("curso con docente inexistente", not cur.crear({**c, "codigo": "Z", "id_docente": "9"})[0])
        verificar("curso con cupo 0", not cur.crear({**c, "codigo": "Z", "cupo": "0"})[0])
        verificar("curso con código duplicado", not cur.crear(c)[0])
        verificar("inscribir a Ana", cur.inscribir_estudiante(1, 1)[0])
        verificar("no se inscribe dos veces", not cur.inscribir_estudiante(1, 1)[0])
        verificar("sin cupo (cupo 1)", not cur.inscribir_estudiante(1, 2)[0])
        verificar("estudiante inexistente", not cur.inscribir_estudiante(1, 99)[0])
        verificar("subir cupo a 2", cur.actualizar(1, {"cupo": "2"})[0])
        verificar("inscribir a Luis (2/2)", cur.inscribir_estudiante(1, 2)[0])
        verificar("no se puede bajar el cupo por debajo de los inscritos",
                  not cur.actualizar(1, {"cupo": "1"})[0])
        verificar("retirar a Luis", cur.retirar_estudiante(1, 2)[0])
        verificar("detalle del curso", cur.detalle(1)[1] == [(1, "Ana Pérez", "EST2026001")])

        print("INTEGRIDAD")
        verificar("no borra docente con cursos", not doc.eliminar(1)[0])
        verificar("no borra asignatura con cursos", not asig.eliminar(1)[0])
        verificar("no borra estudiante inscrito", not est.eliminar(1)[0])
        verificar("retirar estudiante", cur.retirar_estudiante(1, 1)[0])
        verificar("ahora sí borra estudiante", est.eliminar_estudiante(1)[0])
        verificar("eliminar id inexistente falla", not est.eliminar(1)[0])
        verificar("borra curso, luego docente y asignatura",
                  cur.eliminar(1)[0] and doc.eliminar(1)[0] and asig.eliminar(1)[0])
        verificar("el id no se reutiliza mal (siguiente id)", est.siguiente_id() == 3)

        print("ARCHIVO DAÑADO")
        with open(os.path.join(carpeta, "docentes.json"), "w") as f:
            f.write("{esto no es json")
        verificar("JSON dañado se lee como lista vacía", doc.obtener_todos() == [])


if __name__ == "__main__":
    prueba()
    print(f"\n{contador['ok']} comprobaciones correctas ✔")

# Sistema Académico (MVC + JSON) — Estructura de Datos

## Cómo ejecutarlo
```
cd sistema_academico
python main.py          # (python3 main.py en Mac/Linux)
python pruebas.py       # pruebas automáticas (usan una carpeta temporal)
```
Solo usa la biblioteca estándar de Python 3.8+. La carpeta `data/` se crea sola.

## Estructura (PROCESOS 1 a 7 de la guía)
```
sistema_academico/
├── main.py                    PROCESO 6  Clase SistemaAcademico + menú principal
├── models/                    PROCESO 3  Estudiante (completo), Docente, Asignatura, Curso
├── controllers/               PROCESO 4  ControladorEstudiante / Docente / Asignatura / Curso
│   └── controlador_base.py               CRUD genérico que heredan los cuatro
├── views/
│   └── interfaz_consola.py    PROCESO 5  Clase InterfazConsola (único lugar con print/input)
├── shared/                    PROCESO 2  ArchivoJSON, validaciones, herramientas de consola
└── data/                      PROCESO 7  estudiantes.json, docentes.json, asignaturas.json, cursos.json
```
Cada carpeta tiene su `__init__.py` (PROCESO 1) para poder hacer `from models import Estudiante`.

## Colecciones usadas y por qué
| Colección | Dónde | Justificación |
|---|---|---|
| list | `obtener_todos()`, registros del JSON | Crece y se recorre en orden |
| tuple | `CAMPOS_*`, `OBLIGATORIOS`, retornos `(exito, mensaje)` | Datos fijos que nadie debe modificar |
| set | emails/carnets/códigos usados, `Estudiante.materias`, `Curso.estudiantes` | Sin repetidos y pregunta "¿ya existe?" instantánea |
| dict | cada registro, `Estudiante.notas`, menús `OPCIONES` | Acceso por clave; es la forma exacta del JSON |

## Lo que pide la Tarea 14 de la guía HTML (Estudiantes)
- Carnet sin repetir (set) → `ControladorEstudiante` (`UNICOS = ("email", "carnet")`)
- `agregar_nota(id, materia, nota)` con nota 0–20 → devuelve `(False, mensaje)` si no
- `materias_ofertadas()` → set con todas las materias, sin repetir
- `estudiantes_en_comun(id_a, id_b)` → intersección de conjuntos
- Menú: Agregar nota, Ver promedio, Materias en común (Gestión de estudiantes, opciones 7–11)
- El set `materias` se guarda como lista y vuelve a ser set al leer (probado en `pruebas.py`)

## Respuesta a la pregunta final de la guía
Para que buscar por email sea instantáneo se usa un **dict** `{email: registro}` (o un set si
solo interesa saber si existe). Se pierde: más memoria (guarda una estructura extra además de la
lista) y hay que mantenerlo sincronizado en cada crear/editar/eliminar; además solo acelera la
búsqueda **exacta**, no la parcial (`"ana" in texto`), que sigue siendo lineal.

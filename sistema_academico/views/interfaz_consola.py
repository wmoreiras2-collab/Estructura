from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info,
    confirmar, pausa,
)


class InterfazConsola:
    """VISTA: menús, input() y print(). No valida reglas ni abre archivos."""

    def __init__(self, estudiantes, docentes, asignaturas, cursos):
        self.estudiantes = estudiantes
        self.docentes = docentes
        self.asignaturas = asignaturas
        self.cursos = cursos

        # DICCIONARIO de configuración: cada entidad describe cómo se muestra.
        # columnas = lista de TUPLAS (encabezado, ancho, clave de la fila)
        self.entidades = {
            "estudiantes": {
                "titulo": "ESTUDIANTES", "singular": "estudiante",
                "controlador": estudiantes,
                "prompt_buscar": "Nombre, apellido, email o carnet: ",
                "columnas": [("ID", 5, "id"), ("CARNET", 13, "carnet"),
                             ("NOMBRE", 26, "nombre_completo"), ("EMAIL", 28, "email"),
                             ("PROM.", 7, "promedio")],
                "extras": [("Agregar nota", self.opcion_agregar_nota),
                           ("Inscribir en materia", self.opcion_inscribir_materia),
                           ("Ver promedio", self.opcion_ver_promedio),
                           ("Materias en común", self.opcion_materias_en_comun),
                           ("Materias ofertadas", self.opcion_materias_ofertadas)],
            },
            "docentes": {
                "titulo": "DOCENTES", "singular": "docente",
                "controlador": docentes,
                "prompt_buscar": "Nombre, apellido, email o especialidad: ",
                "columnas": [("ID", 5, "id"), ("NOMBRE", 26, "nombre_completo"),
                             ("EMAIL", 28, "email"), ("ESPECIALIDAD", 22, "especialidad")],
                "extras": [],
            },
            "asignaturas": {
                "titulo": "ASIGNATURAS", "singular": "asignatura",
                "controlador": asignaturas,
                "prompt_buscar": "Código o nombre: ",
                "columnas": [("ID", 5, "id"), ("CÓDIGO", 12, "codigo"),
                             ("NOMBRE", 38, "nombre"), ("CRÉDITOS", 10, "creditos")],
                "extras": [],
            },
            "cursos": {
                "titulo": "CURSOS", "singular": "curso",
                "controlador": cursos,
                "prompt_buscar": "Código o periodo: ",
                "columnas": [("ID", 5, "id"), ("CÓDIGO", 11, "codigo"),
                             ("ASIGNATURA", 22, "asignatura"), ("DOCENTE", 22, "docente"),
                             ("PERIODO", 9, "periodo"), ("INSCR.", 8, "inscritos")],
                "extras": [("Inscribir estudiante", self.opcion_inscribir_estudiante),
                           ("Retirar estudiante", self.opcion_retirar_estudiante),
                           ("Ver detalle del curso", self.opcion_detalle_curso)],
            },
        }

    # ===================== AYUDAS DE PANTALLA =====================
    def mostrar_resultado(self, exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    def pedir_id(self, texto="Id: "):
        """Devuelve un int o None (ya mostró el error)."""
        try:
            return int(input(texto))
        except ValueError:
            imprimir_error("El id debe ser un número entero")
            return None

    def mostrar_tabla(self, cfg, filas):
        columnas = cfg["columnas"]
        ancho_total = sum(ancho for _t, ancho, _c in columnas)
        print("".join(f"{titulo:<{ancho}}" for titulo, ancho, _c in columnas))
        print("-" * ancho_total)
        for fila in filas:
            print("".join(f"{str(fila.get(clave, ''))[:ancho - 1]:<{ancho}}"
                          for _t, ancho, clave in columnas))
        print("-" * ancho_total)
        imprimir_info(f"Total: {len(filas)} registro(s)")

    # ===================== CRUD GENÉRICO =====================
    def crear(self, cfg):
        imprimir_titulo(f"CREAR {cfg['singular'].upper()}")
        ctrl = cfg["controlador"]
        # Recorro la TUPLA de campos: si el Modelo cambia, el formulario se actualiza solo
        datos = {campo: input(f"{campo.replace('_', ' ').capitalize()}: ") for campo in ctrl.CAMPOS}
        self.mostrar_resultado(*ctrl.crear(datos))
        pausa()

    def ver_todos(self, cfg):
        imprimir_titulo(f"LISTA DE {cfg['titulo']}")
        ctrl = cfg["controlador"]
        objetos = ctrl.obtener_todos()
        if not objetos:
            imprimir_info("Todavía no hay registros. Use la opción 1 para crear el primero.")
        else:
            self.mostrar_tabla(cfg, [ctrl.fila(o) for o in objetos])
        pausa()

    def buscar(self, cfg):
        imprimir_titulo(f"BUSCAR {cfg['singular'].upper()}")
        ctrl = cfg["controlador"]
        termino = input(cfg["prompt_buscar"])
        encontrados = ctrl.buscar(termino)
        if not encontrados:
            imprimir_info(f"Ningún registro coincide con '{termino}'.")
        else:
            self.mostrar_tabla(cfg, [ctrl.fila(o) for o in encontrados])
        pausa()

    def ver_por_id(self, cfg):
        imprimir_titulo(f"VER {cfg['singular'].upper()} POR ID")
        ctrl = cfg["controlador"]
        id_registro = self.pedir_id()
        if id_registro is None:
            return pausa()
        objeto = ctrl.obtener_por_id(id_registro)
        if objeto is None:
            imprimir_error(f"No existe un {cfg['singular']} con id {id_registro}")
        else:
            # Recorro el DICCIONARIO del registro: clave y valor a la vez
            for clave, valor in ctrl.fila(objeto).items():
                if isinstance(valor, dict):
                    print(f"  {clave.capitalize():<16}:")
                    for subclave, subvalor in valor.items():
                        print(f"      {subclave}: {subvalor}")
                else:
                    print(f"  {clave.capitalize():<16}: {valor}")
        pausa()

    def actualizar(self, cfg):
        imprimir_titulo(f"ACTUALIZAR {cfg['singular'].upper()}")
        ctrl = cfg["controlador"]
        id_registro = self.pedir_id()
        if id_registro is None:
            return pausa()
        objeto = ctrl.obtener_por_id(id_registro)
        if objeto is None:
            imprimir_error(f"No existe un {cfg['singular']} con id {id_registro}")
            return pausa()
        imprimir_info(f"Editando: {objeto}")
        print("Deje en blanco el campo que no quiera cambiar.\n")
        cambios = {}
        for campo in ctrl.CAMPOS:
            actual = getattr(objeto, campo)
            nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo
        self.mostrar_resultado(*ctrl.actualizar(id_registro, cambios))
        pausa()

    def eliminar(self, cfg):
        imprimir_titulo(f"ELIMINAR {cfg['singular'].upper()}")
        ctrl = cfg["controlador"]
        id_registro = self.pedir_id()
        if id_registro is None:
            return pausa()
        objeto = ctrl.obtener_por_id(id_registro)
        if objeto is None:
            imprimir_error(f"No existe un {cfg['singular']} con id {id_registro}")
            return pausa()
        imprimir_info(f"Se eliminará: {objeto}")
        if confirmar("¿Confirma la eliminación?"):
            self.mostrar_resultado(*ctrl.eliminar(id_registro))
        else:
            imprimir_info("Operación cancelada")
        pausa()

    # ===================== OPCIONES PROPIAS: ESTUDIANTES =====================
    def opcion_agregar_nota(self):
        imprimir_titulo("AGREGAR NOTA")
        id_estudiante = self.pedir_id("Id del estudiante: ")
        if id_estudiante is None:
            return pausa()
        materia = input("Materia: ")
        nota = input("Nota (0 a 20): ")
        self.mostrar_resultado(*self.estudiantes.agregar_nota(id_estudiante, materia, nota))
        pausa()

    def opcion_inscribir_materia(self):
        imprimir_titulo("INSCRIBIR EN MATERIA")
        id_estudiante = self.pedir_id("Id del estudiante: ")
        if id_estudiante is None:
            return pausa()
        materia = input("Materia: ")
        self.mostrar_resultado(*self.estudiantes.inscribir_materia(id_estudiante, materia))
        pausa()

    def opcion_ver_promedio(self):
        imprimir_titulo("PROMEDIO DEL ESTUDIANTE")
        id_estudiante = self.pedir_id("Id del estudiante: ")
        if id_estudiante is None:
            return pausa()
        exito, resultado = self.estudiantes.obtener_promedio(id_estudiante)
        if exito:
            imprimir_info(f"Promedio general: {resultado}")
        else:
            imprimir_error(resultado)
        pausa()

    def opcion_materias_en_comun(self):
        imprimir_titulo("MATERIAS EN COMÚN")
        id_a = self.pedir_id("Id del primer estudiante: ")
        id_b = self.pedir_id("Id del segundo estudiante: ") if id_a is not None else None
        if id_a is None or id_b is None:
            return pausa()
        exito, resultado = self.estudiantes.estudiantes_en_comun(id_a, id_b)
        if not exito:
            imprimir_error(resultado)
        elif not resultado:
            imprimir_info("No comparten ninguna materia.")
        else:
            imprimir_exito(f"Materias en común: {', '.join(sorted(resultado))}")
        pausa()

    def opcion_materias_ofertadas(self):
        imprimir_titulo("MATERIAS OFERTADAS")
        materias = self.estudiantes.materias_ofertadas()
        if not materias:
            imprimir_info("Todavía no hay materias inscritas.")
        else:
            for materia in sorted(materias):        # un set no tiene orden: se ordena para mostrar
                print(f"  • {materia}")
            imprimir_info(f"Total: {len(materias)} materia(s) distinta(s)")
        pausa()

    # ===================== OPCIONES PROPIAS: CURSOS =====================
    def opcion_inscribir_estudiante(self):
        imprimir_titulo("INSCRIBIR ESTUDIANTE EN CURSO")
        id_curso = self.pedir_id("Id del curso: ")
        id_estudiante = self.pedir_id("Id del estudiante: ") if id_curso is not None else None
        if id_curso is None or id_estudiante is None:
            return pausa()
        self.mostrar_resultado(*self.cursos.inscribir_estudiante(id_curso, id_estudiante))
        pausa()

    def opcion_retirar_estudiante(self):
        imprimir_titulo("RETIRAR ESTUDIANTE DE CURSO")
        id_curso = self.pedir_id("Id del curso: ")
        id_estudiante = self.pedir_id("Id del estudiante: ") if id_curso is not None else None
        if id_curso is None or id_estudiante is None:
            return pausa()
        self.mostrar_resultado(*self.cursos.retirar_estudiante(id_curso, id_estudiante))
        pausa()

    def opcion_detalle_curso(self):
        imprimir_titulo("DETALLE DEL CURSO")
        id_curso = self.pedir_id("Id del curso: ")
        if id_curso is None:
            return pausa()
        resultado = self.cursos.detalle(id_curso)
        if resultado is None:
            imprimir_error(f"No existe un curso con id {id_curso}")
            return pausa()
        fila, inscritos = resultado
        print(f"  Curso      : {fila['codigo']} ({fila['periodo']})")
        print(f"  Asignatura : {fila['asignatura']}")
        print(f"  Docente    : {fila['docente']}")
        print(f"  Inscritos  : {fila['inscritos']}\n")
        for id_est, nombre, carnet in inscritos:        # desempaquetado de TUPLAS
            print(f"    {id_est:<4}{carnet:<14}{nombre}")
        if not inscritos:
            imprimir_info("Aún no hay estudiantes inscritos.")
        pausa()

    # ===================== MENÚS =====================
    def menu_crud(self, cfg):
        # DICCIONARIO de opciones: tecla -> (texto, función)
        opciones = {
            "1": ("Crear", lambda: self.crear(cfg)),
            "2": ("Ver todos", lambda: self.ver_todos(cfg)),
            "3": ("Buscar", lambda: self.buscar(cfg)),
            "4": ("Ver por id", lambda: self.ver_por_id(cfg)),
            "5": ("Actualizar", lambda: self.actualizar(cfg)),
            "6": ("Eliminar", lambda: self.eliminar(cfg)),
        }
        for numero, (texto, funcion) in enumerate(cfg["extras"], start=7):
            opciones[str(numero)] = (texto, funcion)
        while True:
            imprimir_titulo(f"GESTIÓN DE {cfg['titulo']}")
            for tecla, (texto, _funcion) in opciones.items():
                print(f"  {tecla}. {texto}")
            print("  0. Volver\n")
            tecla = input("Seleccione una opción: ").strip()
            if tecla == "0":
                return
            if tecla not in opciones:
                imprimir_error("Opción no válida")
                pausa()
                continue
            opciones[tecla][1]()

    def menu_principal(self):
        entidades = {"1": "estudiantes", "2": "docentes", "3": "asignaturas", "4": "cursos"}
        while True:
            imprimir_titulo("SISTEMA ACADÉMICO")
            for tecla, nombre in entidades.items():
                print(f"  {tecla}. {self.entidades[nombre]['titulo'].capitalize()}")
            print("  0. Salir\n")
            tecla = input("Seleccione una opción: ").strip()
            if tecla == "0":
                imprimir_info("¡Hasta luego! 👋")
                return
            if tecla not in entidades:
                imprimir_error("Opción no válida")
                pausa()
                continue
            self.menu_crud(self.entidades[entidades[tecla]])

#1
class Temperatura:
    def __init__(self):
        self.temperaturas = []

    def validar_temperatura(self, temperatura):
        return -50 <= temperatura <= 50

    def cargar_temperaturas(self, *args):
        for temperatura in args:
            if self.validar_temperatura(temperatura):
                self.temperaturas.append(temperatura)
        return self.temperaturas

    def promedio(self):
        if len(self.temperaturas) == 0:
            return 0
        return sum(self.temperaturas) / len(self.temperaturas)


t = Temperatura()

print(t.cargar_temperaturas(25, 30, 18, 40, 66, -99))
print(t.promedio())

#2
class RegistroProductos:
    def __init__(self):
        self.productos = set()
        self.orden = []

    def agregar_producto(self, producto):
        self.productos.add(producto)

        if producto not in self.orden:
            self.orden.append(producto)

    def contar_productos(self):
        return len(self.productos)

    def agregar_multiples(self, *args):
        for producto in args:
            self.agregar_producto(producto)


rp = RegistroProductos()

rp.agregar_multiples("Pan", "Leche", "Pan")

print(rp.orden)
print(rp.contar_productos())

#3
class Tienda:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, nombre, precio):
        self.productos[nombre] = precio

    def calcular_total(self):
        total = 0

        for precio in self.productos.values():
            total += precio

        return total

    def productos_por_rango(self, precio_min, precio_max):
        resultado = []

        for nombre, precio in self.productos.items():
            if precio_min <= precio <= precio_max:
                resultado.append(nombre)

        return resultado


t = Tienda()

t.agregar_producto("cuaderno", 2.50)
t.agregar_producto("mochila", 15.00)
t.agregar_producto("lapiz", 1.00)

print(t.calcular_total())
print(t.productos_por_rango(1, 5))

#4
class OrdenadorSecuencia:
    def ordenar_lista(self, lista):
        ordenada = []

        for numero in lista:
            ordenada.append(numero)

        ordenada.sort()

        return ordenada

    def ordenar_multiples(self, *listas):
        resultado = {}

        for lista in listas:
            original = tuple(lista)
            ordenada = self.ordenar_lista(lista)
            resultado[original] = ordenada

        return resultado


ord = OrdenadorSecuencia()

print(ord.ordenar_lista([3, 1, 2]))

print(ord.ordenar_multiples(
    [5, 2, 8],
    [9, 4, 1]
))

#5
class AnalizadorEdades:
    def __init__(self):
        self.menores = []
        self.mayores = []

    def es_mayor(self, edad):
        return edad >= 18

    def separar(self, *edades):
        self.menores = []
        self.mayores = []

        for edad in edades:
            if self.es_mayor(edad):
                self.mayores.append(edad)
            else:
                self.menores.append(edad)

        return {
            "menores": self.menores,
            "mayores": self.mayores
        }

    def cantidad_menores_mayores(self):
        return (len(self.menores), len(self.mayores))


ae = AnalizadorEdades()

print(ae.separar(12, 20, 15, 25, 17))
print(ae.cantidad_menores_mayores())

#6
class GestorCalificaciones:
    def __init__(self):
        self.calificaciones = []

    def registrar_calificacion(self, nota):
        self.calificaciones.append(nota)

    def minima(self):
        return min(self.calificaciones)

    def maxima(self):
        return max(self.calificaciones)

    def promedio(self):
        return sum(self.calificaciones) / len(self.calificaciones)

    def registrar_multiples(self, *notas):
        for nota in notas:
            self.registrar_calificacion(nota)


gc = GestorCalificaciones()

gc.registrar_multiples(8, 9, 7, 10)

print("Mínima:", gc.minima())
print("Máxima:", gc.maxima())
print("Promedio:", gc.promedio())

#7
class GestorProductos:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, nombre, precio):
        self.productos[nombre] = precio

    def productos_caros(self, precio_minimo):
        resultado = []

        for nombre, precio in self.productos.items():
            if precio >= precio_minimo:
                resultado.append(nombre)

        return resultado

    def precio_promedio(self):
        if len(self.productos) == 0:
            return 0

        suma = 0

        for precio in self.productos.values():
            suma += precio

        return suma / len(self.productos)


gp = GestorProductos()

gp.agregar_producto("Pan", 2)
gp.agregar_producto("Leche", 3)
gp.agregar_producto("Queso", 6)

print(gp.productos_caros(3))
print(gp.precio_promedio())

#8
class Grupos:
    def __init__(self):
        self.grupos = {}

    def crear_grupo(self, nombre_grupo):
        self.grupos[nombre_grupo] = []

    def agregar_estudiante(self, grupo, estudiante):
        if grupo in self.grupos:
            self.grupos[grupo].append(estudiante)

    def grupo_mayor_integrantes(self):
        mayor = None
        cantidad = 0

        for grupo, estudiantes in self.grupos.items():
            if len(estudiantes) > cantidad:
                cantidad = len(estudiantes)
                mayor = grupo

        return mayor


gr = Grupos()

gr.crear_grupo("Grupo 1")
gr.crear_grupo("Grupo 2")

gr.agregar_estudiante("Grupo 1", "Carlos")
gr.agregar_estudiante("Grupo 1", "María")
gr.agregar_estudiante("Grupo 2", "Pedro")

print(gr.grupo_mayor_integrantes())

#9
class AnalizadorPalabras:
    def __init__(self):
        self.palabra_mas_larga = ""

    def solo_vocales(self, letra):
        return letra.lower() in "aeiou"

    def contar_por_tipo(self, palabra):
        vocales = 0
        consonantes = 0
        digitos = 0

        for letra in palabra:
            if letra.isdigit():
                digitos += 1
            elif letra.isalpha():
                if self.solo_vocales(letra):
                    vocales += 1
                else:
                    consonantes += 1

        if len(palabra) > len(self.palabra_mas_larga):
            self.palabra_mas_larga = palabra

        return {
            "vocales": vocales,
            "consonantes": consonantes,
            "digitos": digitos
        }


ap = AnalizadorPalabras()

print(ap.contar_por_tipo("Programacion123"))
print(ap.palabra_mas_larga)

#10
class Actividades:
    def __init__(self):
        self.actividades = []

    def agregar_actividad(self, descripcion, importancia):
        self.actividades.append((descripcion, importancia))

    def actividades_importantes(self):
        resultado = []

        for actividad in self.actividades:
            if actividad[1] == "alta":
                resultado.append(actividad)

        return resultado

    def eliminar_actividad(self, descripcion):
        for actividad in self.actividades:
            if actividad[0] == descripcion:
                self.actividades.remove(actividad)
                break


a = Actividades()

a.agregar_actividad("Entrenar", "alta")
a.agregar_actividad("Ver televisión", "baja")
a.agregar_actividad("Estudiar Python", "alta")

print(a.actividades_importantes())

a.eliminar_actividad("Entrenar")

print(a.actividades)

#11
class ContadorProductos:
    def __init__(self):
        self.cantidades = {}

    def agregar_producto(self, producto):
        if producto in self.cantidades:
            self.cantidades[producto] += 1
        else:
            self.cantidades[producto] = 1

    def producto_mas_repetido(self):
        mayor = 0
        producto_mayor = None

        for producto, cantidad in self.cantidades.items():
            if cantidad > mayor:
                mayor = cantidad
                producto_mayor = producto

        return producto_mayor

    def cantidad_producto(self, producto):
        return self.cantidades.get(producto, 0)


cp = ContadorProductos()

cp.agregar_producto("pan")
cp.agregar_producto("leche")
cp.agregar_producto("pan")

print(cp.producto_mas_repetido())
print(cp.cantidad_producto("pan"))

#12
class GeneradorIntervalos:
    def crear_intervalo(self, inicio, fin):
        numeros = []

        for numero in range(inicio, fin + 1):
            numeros.append(numero)

        return tuple(numeros)

    def combinar_intervalos(self, *intervalos):
        elementos = set()

        for intervalo in intervalos:
            inicio = intervalo[0]
            fin = intervalo[1]

            for numero in range(inicio, fin + 1):
                elementos.add(numero)

        return sorted(elementos)


gi = GeneradorIntervalos()

print(gi.crear_intervalo(2, 5))
print(gi.combinar_intervalos((1, 4), (3, 6)))

#13
class MezcladorListas:
    def mezclar(self, lista1, lista2):
        resultado = []

        mayor = max(len(lista1), len(lista2))

        for i in range(mayor):
            if i < len(lista1):
                resultado.append(lista1[i])

            if i < len(lista2):
                resultado.append(lista2[i])

        return resultado

    def mezclar_varias(self, *listas):
        if len(listas) == 0:
            return []

        resultado = list(listas[0])

        for i in range(1, len(listas)):
            resultado = self.mezclar(resultado, listas[i])

        return resultado


ml = MezcladorListas()

print(ml.mezclar(["a", "b"], ["c", "d"]))
print(ml.mezclar_varias(["a", "b"], ["c", "d"], ["e", "f"]))

#14
class RegistroPuntajes:
    def __init__(self):
        self.puntajes = {}

    def registrar(self, jugador, puntaje):
        self.puntajes[jugador] = puntaje

    def jugadores_clasificados(self, puntaje_minimo):
        clasificados = []

        for jugador, puntaje in self.puntajes.items():
            if puntaje >= puntaje_minimo:
                clasificados.append(jugador)

        return clasificados

    def mejor_jugador(self):
        mejor_nombre = None
        mejor_puntaje = -1

        for jugador, puntaje in self.puntajes.items():
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_nombre = jugador

        return (mejor_nombre, mejor_puntaje)


rp = RegistroPuntajes()

rp.registrar("Juan", 80)
rp.registrar("Pedro", 65)
rp.registrar("Luis", 92)

print(rp.jugadores_clasificados(70))
print(rp.mejor_jugador())

#15
class AnalizadorMultiplos:
    def encontrar_multiplos(self, numero):
        multiplos = []

        for i in range(1, 6):
            multiplos.append(numero * i)

        return tuple(multiplos)

    def es_multiplo_de_diez(self, numero):
        return numero % 10 == 0

    def encontrar_varios_multiplos(self, *numeros):
        resultado = {}

        for numero in numeros:
            resultado[numero] = self.encontrar_multiplos(numero)

        return resultado


am = AnalizadorMultiplos()

print(am.encontrar_multiplos(4))
print(am.es_multiplo_de_diez(20))
print(am.encontrar_varios_multiplos(2, 3, 5))

#16
class CodificadorTexto:
    def __init__(self):
        self.historial = {}

    def modificar_letra(self, letra, desplazamiento):
        if letra.isalpha():
            codigo = ord(letra.lower()) - ord("a")
            nuevo_codigo = (codigo + desplazamiento) % 26
            return chr(nuevo_codigo + ord("a"))

        return letra

    def modificar_palabra(self, palabra, desplazamiento):
        resultado = ""

        for letra in palabra:
            resultado += self.modificar_letra(letra, desplazamiento)

        self.historial[palabra] = resultado

        return resultado


ct = CodificadorTexto()

print(ct.modificar_palabra("casa", 2))
print(ct.historial)

#17
class AgrupadorPrecios:
    def __init__(self):
        self.grupos = {}

    def clasificar_precio(self, precio):
        if precio <= 10:
            return "barato"
        elif precio <= 30:
            return "medio"
        elif precio <= 60:
            return "caro"
        else:
            return "muy caro"

    def agrupar_por_categoria(self, *precios):
        self.grupos = {
            "barato": [],
            "medio": [],
            "caro": [],
            "muy caro": []
        }

        for precio in precios:
            categoria = self.clasificar_precio(precio)
            self.grupos[categoria].append(precio)

        return self.grupos

    def precio_promedio_categoria(self, categoria):
        precios = self.grupos.get(categoria, [])

        if len(precios) == 0:
            return 0

        return sum(precios) / len(precios)


ap = AgrupadorPrecios()

print(ap.agrupar_por_categoria(5, 20, 45, 80))
print(ap.precio_promedio_categoria("caro"))

#18
import math


class CalculadorRecorrido:
    def __init__(self):
        self.recorridos = []

    def calcular_distancia(self, p1, p2):
        x1 = p1[0]
        y1 = p1[1]

        x2 = p2[0]
        y2 = p2[1]

        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        self.recorridos.append(distancia)

        return distancia

    def ubicacion_mas_cercana(self, referencia, *ubicaciones):
        ubicacion_cercana = None
        menor_distancia = float("inf")

        for ubicacion in ubicaciones:
            distancia = self.calcular_distancia(referencia, ubicacion)

            if distancia < menor_distancia:
                menor_distancia = distancia
                ubicacion_cercana = ubicacion

        return ubicacion_cercana


cr = CalculadorRecorrido()

print(cr.calcular_distancia((1, 1), (4, 5)))

print(cr.ubicacion_mas_cercana(
    (0, 0),
    (4, 4),
    (2, 1),
    (6, 3)
))

#19
class Almacen:
    def __init__(self):
        self.existencias = {}

    def agregar_existencia(self, articulo, cantidad):
        if articulo in self.existencias:
            self.existencias[articulo] += cantidad
        else:
            self.existencias[articulo] = cantidad

    def retirar_existencia(self, articulo, cantidad):
        if articulo in self.existencias and self.existencias[articulo] >= cantidad:
            self.existencias[articulo] -= cantidad
            return True

        return False

    def articulos_escasos(self, minimo):
        resultado = []

        for articulo, cantidad in self.existencias.items():
            if cantidad < minimo:
                resultado.append(articulo)

        return resultado


al = Almacen()

al.agregar_existencia("cuadernos", 40)
al.retirar_existencia("cuadernos", 25)

print(al.existencias)
print(al.articulos_escasos(20))

#20
class AnalizadorNombres:
    def __init__(self):
        self.nombres = set()

    def encontrar_nombres(self, texto, inicial):
        palabras = texto.split()
        resultado = []

        for palabra in palabras:
            palabra_limpia = palabra.strip(".,!?")

            if palabra_limpia.startswith(inicial):
                resultado.append(palabra_limpia)

        return resultado

    def agrupar_por_longitud(self, texto):
        palabras = texto.split()
        resultado = {}

        for palabra in palabras:
            palabra = palabra.strip(".,!?")
            longitud = len(palabra)

            if longitud not in resultado:
                resultado[longitud] = []

            resultado[longitud].append(palabra)

        return resultado

    def nombres_unicos(self, texto):
        palabras = texto.split()

        for palabra in palabras:
            palabra = palabra.strip(".,!?").lower()
            self.nombres.add(palabra)

        return self.nombres


an = AnalizadorNombres()

texto = "Carlos camina con Pedro"

print(an.encontrar_nombres(texto, "C"))
print(an.agrupar_por_longitud(texto))
print(an.nombres_unicos(texto))
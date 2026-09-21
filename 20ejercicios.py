# 20 EJERCICIOS PROPUESTOS - ESTRUCTURAS DE DATOS CON PYTHON


# 1. IVA + descuento del 10% antes del IVA

IVA = 0.15

precio = float(input("1. Precio sin IVA: $"))
descuento = precio * 0.10
precio_descuento = precio - descuento
iva = precio_descuento * IVA
total = precio_descuento + iva

print(f"Descuento: ${descuento:.2f}")
print(f"IVA: ${iva:.2f}")
print(f"Total: ${total:.2f}")



# 2. Par/impar + múltiplo de 3, 5 o ambos

num = int(input("\n2. Ingresa un número: "))

if num % 2 == 0:
    print(f"{num} es par")
else:
    print(f"{num} es impar")

if num % 3 == 0 and num % 5 == 0:
    print("Es múltiplo de 3 y de 5")
elif num % 3 == 0:
    print("Es múltiplo de 3")
elif num % 5 == 0:
    print("Es múltiplo de 5")
else:
    print("No es múltiplo de 3 ni de 5")



# 3. Segundos a hh:mm:ss

total = int(input("\n3. Segundos totales: "))

horas = total // 3600
resto = total % 3600
minutos = resto // 60
segundos = resto % 60

print(f"{horas:02d}:{minutos:02d}:{segundos:02d}")



# 4. De hh:mm:ss a segundos totales

tiempo = input("\n4. Ingresa el tiempo hh:mm:ss: ")
partes = tiempo.split(":")

horas = int(partes[0])
minutos = int(partes[1])
segundos = int(partes[2])

total_segundos = horas * 3600 + minutos * 60 + segundos

print("Segundos totales:", total_segundos)



# 5. Billetes de $50, $20, $10, $5 y $1

monto = int(input("\n5. Monto: $"))
resto = monto

b50 = resto // 50
resto = resto % 50

b20 = resto // 20
resto = resto % 20

b10 = resto // 10
resto = resto % 10

b5 = resto // 5
resto = resto % 5

b1 = resto // 1
resto = resto % 1

print(f"$50 x {b50}")
print(f"$20 x {b20}")
print(f"$10 x {b10}")
print(f"$5 x {b5}")
print(f"$1 x {b1}")



# 6. Monedas de $0.25, $0.10, $0.05 y $0.01
#    Se trabaja con centavos para evitar problemas con float.
monto = float(input("\n6. Monto para monedas: $"))
centavos = round(monto * 100)
resto = centavos

m25 = resto // 25
resto = resto % 25

m10 = resto // 10
resto = resto % 10

m5 = resto // 5
resto = resto % 5

m1 = resto // 1
resto = resto % 1

print(f"$0.25 x {m25}")
print(f"$0.10 x {m10}")
print(f"$0.05 x {m5}")
print(f"$0.01 x {m1}")



# 7. Suma de dígitos de un número de 3 cifras

num = int(input("\n7. Ingresa un número de 3 cifras: "))

centenas = num // 100
decenas = (num // 10) % 10
unidades = num % 10

suma = centenas + decenas + unidades

print("Suma:", suma)



# 8. Minutos a horas y minutos

minutos = int(input("\n8. Ingresa la cantidad de minutos: "))

horas = minutos // 60
minutos_restantes = minutos % 60

print(f"{horas} horas {minutos_restantes} minutos")


# 9. IMC

peso = float(input("\n9. Ingresa tu peso en kg: "))
estatura = float(input("Ingresa tu estatura en metros: "))

imc = peso / (estatura ** 2)

print(f"IMC: {imc:.2f}")



# 10. Redondear un decimal según cantidad de decimales
num = float(input("\n10. Ingresa un número decimal: "))
dec = int(input("Ingresa la cantidad de decimales: "))

print(round(num, dec))

# 11. Producto de $12 con descuentos

precio = 12
cantidad = int(input("\n11. Ingresa la cantidad de productos: "))

subtotal = precio * cantidad

if cantidad >= 10:
    descuento = 0.15
elif cantidad >= 5:
    descuento = 0.05
else:
    descuento = 0

total = subtotal - (subtotal * descuento)

print(f"Precio unitario: ${precio}")
print(f"Descuento: {descuento * 100:.0f}%")
print(f"Total: ${total:.2f}")



# 12. Calificador

class Calificador:
    def __init__(self):
        self.notas = []

    def validar_nota(self, nota):
        return 0 <= nota <= 100

    def cargar_notas(self, *args):
        for nota in args:
            if self.validar_nota(nota):
                self.notas.append(nota)
        return self.notas

    def promedio(self):
        if len(self.notas) == 0:
            return 0
        return sum(self.notas) / len(self.notas)


cal = Calificador()
cal.cargar_notas(85, 92, 78, 88)
print("\n12. Notas:", cal.notas)
print("Promedio:", cal.promedio())



# 13. Analizador de texto

class AnalizadorTexto:
    def __init__(self):
        self.palabras = set()
        self.orden = []

    def agregar_palabra(self, palabra):
        self.palabras.add(palabra)
        if palabra not in self.orden:
            self.orden.append(palabra)

    def contar_palabras(self):
        return len(self.palabras)

    def agregar_multiples(self, *args):
        for palabra in args:
            self.agregar_palabra(palabra)


texto = AnalizadorTexto()
texto.agregar_multiples("hola", "mundo", "hola", "python")

print("\n13. Palabras:", texto.orden)
print("Cantidad de palabras diferentes:", texto.contar_palabras())



# 14. Carrito de compras

class CarroCompras:
    def __init__(self):
        self.articulos = {}

    def agregar_articulo(self, nombre, precio):
        self.articulos[nombre] = precio

    def total_carrito(self):
        total = 0
        for precio in self.articulos.values():
            total += precio
        return total

    def articulos_por_rango(self, precio_min, precio_max):
        resultado = []
        for nombre, precio in self.articulos.items():
            if precio_min <= precio <= precio_max:
                resultado.append(nombre)
        return resultado


carro = CarroCompras()
carro.agregar_articulo("Pan", 2.50)
carro.agregar_articulo("Leche", 3.00)
carro.agregar_articulo("Queso", 5.50)

print("\n14. Total carrito:", carro.total_carrito())
print("Artículos entre $2 y $4:", carro.articulos_por_rango(2, 4))



# 15. Inversor de secuencia

class InversorSecuencia:
    def invertir_lista(self, lista):
        invertida = []

        for i in range(len(lista) - 1, -1, -1):
            invertida.append(lista[i])

        return invertida

    def invertir_multiples(self, *listas):
        resultado = {}

        for lista in listas:
            original = tuple(lista)
            invertida = self.invertir_lista(lista)
            resultado[original] = invertida

        return resultado


inversor = InversorSecuencia()

print("\n15. Lista invertida:", inversor.invertir_lista([1, 2, 3, 4]))
print("Varias listas:", inversor.invertir_multiples([1, 2, 3], [4, 5, 6]))

# 16. Analizador de números

class AnalizadorNumeros:
    def __init__(self):
        self.pares = []
        self.impares = []

    def es_par(self, numero):
        return numero % 2 == 0

    def separar(self, *numeros):
        self.pares = []
        self.impares = []

        for numero in numeros:
            if self.es_par(numero):
                self.pares.append(numero)
            else:
                self.impares.append(numero)

        return {
            "pares": self.pares,
            "impares": self.impares
        }

    def cantidad_pares_impares(self):
        return (len(self.pares), len(self.impares))


analizador = AnalizadorNumeros()

print("\n16. Separación:", analizador.separar(1, 2, 3, 4, 5, 6))
print("Cantidad:", analizador.cantidad_pares_impares())


# 17. Gestor de temperatura

class GestorTemperatura:
    def __init__(self):
        self.temperaturas = []

    def registrar_temperatura(self, temp):
        self.temperaturas.append(temp)

    def minima(self):
        return min(self.temperaturas)

    def maxima(self):
        return max(self.temperaturas)

    def promedio(self):
        return sum(self.temperaturas) / len(self.temperaturas)

    def registrar_multiples(self, *temps):
        for temp in temps:
            self.registrar_temperatura(temp)


temperatura = GestorTemperatura()
temperatura.registrar_multiples(20, 25, 18, 30)

print("\n17. Temperaturas:", temperatura.temperaturas)
print("Mínima:", temperatura.minima())
print("Máxima:", temperatura.maxima())
print("Promedio:", temperatura.promedio())


# 18. Gestor de personas

class GestorPersonas:
    def __init__(self):
        self.personas = {}

    def agregar_persona(self, nombre, edad):
        self.personas[nombre] = edad

    def personas_mayores(self, edad_minima):
        resultado = []

        for nombre, edad in self.personas.items():
            if edad >= edad_minima:
                resultado.append(nombre)

        return resultado

    def edad_promedio(self):
        if len(self.personas) == 0:
            return 0

        suma = 0

        for edad in self.personas.values():
            suma += edad

        return suma / len(self.personas)


personas = GestorPersonas()
personas.agregar_persona("Ana", 28)
personas.agregar_persona("Luis", 17)
personas.agregar_persona("Carlos", 22)

print("\n18. Personas:", personas.personas)
print("Mayores de 18:", personas.personas_mayores(18))
print("Edad promedio:", personas.edad_promedio())



# 19. Equipos

class Equipos:
    def __init__(self):
        self.equipos = {}

    def crear_equipo(self, nombre_equipo):
        self.equipos[nombre_equipo] = []

    def agregar_jugador(self, equipo, jugador):
        if equipo in self.equipos:
            self.equipos[equipo].append(jugador)

    def equipo_mayor_integrantes(self):
        mayor = None
        cantidad = 0

        for equipo, jugadores in self.equipos.items():
            if len(jugadores) > cantidad:
                cantidad = len(jugadores)
                mayor = equipo

        return mayor


equipos = Equipos()

equipos.crear_equipo("A")
equipos.crear_equipo("B")

equipos.agregar_jugador("A", "Juan")
equipos.agregar_jugador("A", "Pedro")
equipos.agregar_jugador("B", "Luis")

print("\n19. Equipos:", equipos.equipos)
print("Equipo con más integrantes:", equipos.equipo_mayor_integrantes())



# 20. Analizador de strings

class AnalizadorString:
    def __init__(self):
        self.texto_mas_largo = ""

    def solo_vocales(self, letra):
        return letra.lower() in "aeiou"

    def contar_por_tipo(self, texto):
        vocales = 0
        consonantes = 0
        digitos = 0

        for letra in texto:
            if letra.isdigit():
                digitos += 1
            elif letra.isalpha():
                if self.solo_vocales(letra):
                    vocales += 1
                else:
                    consonantes += 1

        if len(texto) > len(self.texto_mas_largo):
            self.texto_mas_largo = texto

        return {
            "vocales": vocales,
            "consonantes": consonantes,
            "digitos": digitos
        }


analizador_string = AnalizadorString()

print("\n20. Análisis:", analizador_string.contar_por_tipo("Hola123"))
print("Texto más largo:", analizador_string.texto_mas_largo)

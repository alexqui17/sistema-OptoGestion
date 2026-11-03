"""
SISTEMA OPTOGESTIÓN
Proyecto Final - Programación I

Sistema de consola para registrar, consultar y procesar pacientes
atendidos en jornadas universitarias de atención optométrica.

Estructuras y conceptos utilizados:
- Lista de diccionarios para almacenar los pacientes en memoria.
- Funciones para organizar cada módulo.
- Condicionales y ciclos para controlar el programa.
- Archivo JSON para conservar la información entre ejecuciones.
"""

import json
import os
from pathlib import Path

ARCHIVO_JSON = Path(__file__).resolve().parent / "pacientes.json"

# ---------------------------------------------------------
# MÓDULO DE ALMACENAMIENTO
# ---------------------------------------------------------

def cargar_pacientes():
    """
    Carga los pacientes guardados en pacientes.json.
    Si el archivo todavía no existe, devuelve una lista vacía.
    """
    pacientes = []  # Se inicia con una lista vacía, como solicita la guía.

    if os.path.exists(ARCHIVO_JSON):
        try:
            #para leer el archivo json y cargar los datos en las variables 
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            if isinstance(datos, list):
                pacientes = datos
            else:
                print("Advertencia: el JSON no contiene una lista. Se iniciará vacío.")

        except json.JSONDecodeError:
            print("Advertencia: pacientes.json está vacío o tiene un formato incorrecto.")
            print("Se iniciará una lista vacía.")
        except OSError as error:
            print(f"No fue posible leer el archivo: {error}")

    return pacientes


def guardar_pacientes(pacientes):

    try:
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:

            json.dump(
                pacientes,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        return True

    except PermissionError:
        print("ERROR: No hay permisos para modificar pacientes.json.")
        print("Verifique que el archivo no esté en modo Solo lectura.")
        print("Cierre el archivo si está abierto en otro programa.")
        return False

    except OSError as error:
        print(f"Error al guardar la información: {error}")
        return False


# ---------------------------------------------------------
# FUNCIONES DE VALIDACIÓN
# ---------------------------------------------------------

def solicitar_texto(mensaje):
    """Solicita un texto y evita que el usuario lo deje vacío."""
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Este campo no puede quedar vacío.")


def solicitar_edad():
    """Valida que la edad sea un número entero entre 1 y 120."""
    while True:
        try:
            edad = int(input("Edad (1 a 120 años): "))
            if 1 <= edad <= 120:
                return edad
            print("La edad debe estar entre 1 y 120 años.")
        except ValueError:
            print("Ingrese la edad utilizando números enteros.")


def solicitar_correccion():
    """
    Convierte una respuesta Sí/No en un valor booleano:
    Sí = True; No = False.
    """
    while True:
        respuesta = input("¿Utiliza corrección visual? (Sí/No): ").strip().lower()

        if respuesta in ("si", "sí", "s"):
            return True
        elif respuesta in ("no", "n"):
            return False
        else:
            print("Respuesta no válida. Escriba Sí o No.")


def solicitar_id(pacientes):
    """Solicita la identificación y verifica que no esté repetida."""

    while True:
        identificacion = input("Identificación del paciente: ").strip()

        if identificacion == "":
            print("La identificación no puede estar vacía.")
            continue

        existe = False

        for paciente in pacientes:
            if paciente["id"].upper() == identificacion.upper():
                existe = True
                break

        if existe:
            print("Esta identificación ya está registrada.")
        else:
            return identificacion


# ---------------------------------------------------------
# MÓDULO 1. REGISTRO DE PACIENTES
# ---------------------------------------------------------

def registrar_paciente(pacientes):
    """Solicita los datos y agrega un nuevo diccionario a la lista."""
    print("\n--- REGISTRO DE PACIENTE ---")

    identificacion = solicitar_id(pacientes)
    nombre = solicitar_texto("Nombre completo: ")
    edad = solicitar_edad()
    sexo = solicitar_texto("Sexo (F/M/O): ").upper()
    usa_correccion = solicitar_correccion()

    nuevo_paciente = {
        "id": identificacion,
        "nombre": nombre,
        "edad": edad,
        "sexo": sexo,
        "usa_correccion": usa_correccion
    }

    pacientes.append(nuevo_paciente)

    if guardar_pacientes(pacientes):
        print("\nPaciente registrado y guardado correctamente.")
        print(f"Identificación asignada: {identificacion}")
    else:
        
        print("\nEl paciente quedó en memoria, pero no se pudo guardar en el archivo.")


# ---------------------------------------------------------
# MÓDULO 2. CONSULTA DE PACIENTES
# ---------------------------------------------------------

def consultar_paciente(pacientes):
    """Busca un paciente por su identificacion y muestra sus datos."""
    print("\n--- CONSULTA DE PACIENTE ---")
    identificacion = solicitar_texto("Ingrese el numero de identificación  del paciente : ").upper()

    encontrado = None

    for paciente in pacientes:
        if paciente.get("id", "").upper() == identificacion:
            encontrado = paciente
            break

    if encontrado:
        print("\nInformación del paciente")
        print("-------------------------")
        print(f"ID: {encontrado.get('id', 'No registrado')}")
        print(f"Nombre: {encontrado.get('nombre', 'No registrado')}")
        print(f"Edad: {encontrado.get('edad', 'No registrada')}")
        print(f"Sexo: {encontrado.get('sexo', 'No registrado')}")
        correccion = "Sí" if encontrado.get("usa_correccion") is True else "No"
        print(f"Utiliza corrección visual: {correccion}")
    else:
        print(f"No se encontró un paciente con el ID {identificacion}.")


# ---------------------------------------------------------
# MÓDULO 3. MOSTRAR PACIENTES REGISTRADOS
# ---------------------------------------------------------
def mostrar_pacientes(pacientes):
    print("\n--- PACIENTES REGISTRADOS ---")

    if not pacientes:
        print("No hay pacientes registrados.")
        return

    for paciente in pacientes:
        print("------------------------------")
        print(f"Identificación: {paciente['id']}")
        print(f"Nombre: {paciente['nombre']}")
        print(f"Edad: {paciente['edad']}")
        print(f"Sexo: {paciente['sexo']}")

        if paciente['usa_correccion'] == True:
            print("Usa corrección visual: Sí")
        else:
            print("Usa corrección visual: No")

    print("------------------------------")


# ---------------------------------------------------------
# MÓDULO 4. PACIENTES CON CORRECCIÓN VISUAL
# ---------------------------------------------------------

def buscar_con_correccion(pacientes):
    """Muestra únicamente los pacientes cuyo campo es_correccion es True."""
    print("\n--- PACIENTES QUE UTILIZAN CORRECCIÓN VISUAL ---")

    encontrados = 0

    for paciente in pacientes:
        if paciente.get("usa_correccion") is True:
            print(f"- {paciente.get('nombre', 'Nombre no disponible')}")
            encontrados += 1

    if encontrados == 0:
        print("No hay pacientes registrados que utilicen corrección visual.")


# ---------------------------------------------------------
# MÓDULO 5. ESTADÍSTICAS DE LA JORNADA
# ---------------------------------------------------------

def generar_estadisticas(pacientes):
    """Calcula el total, la edad promedio y los usuarios de corrección."""
    print("\n--- ESTADÍSTICAS DE LA JORNADA ---")

    total_pacientes = len(pacientes)

    if total_pacientes == 0:
        print("No hay pacientes registrados.")
        print("No es posible calcular la edad promedio.")
        print("Pacientes que utilizan corrección visual: 0")
        return

    suma_edades = 0
    total_correccion = 0

    for paciente in pacientes:
        suma_edades += paciente["edad"]

        if paciente["usa_correccion"] is True:
            total_correccion += 1

    promedio_edad = suma_edades / total_pacientes

    print(f"Número total de pacientes: {total_pacientes}")
    print(f"Edad promedio: {promedio_edad:.2f} años")
    print(f"Pacientes que utilizan corrección visual: {total_correccion}")


# ---------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------

def mostrar_menu():
    """Imprime las opciones disponibles en el sistema."""
    print("\n" + "=" * 43)
    print("             SISTEMA OPTOGESTIÓN")
    print("=" * 43)
    print("1. Registrar paciente")
    print("2. Consultar paciente")
    print("3. Mostrar pacientes registrados")
    print("4. Buscar pacientes con corrección visual")
    print("5. Generar estadísticas")
    print("6. Salir")
    print("=" * 43)


def ejecutar_programa():
    """Controla el menú y mantiene el programa activo hasta elegir salir."""
    pacientes = cargar_pacientes()

    print("Bienvenido al sistema OptoGestión.")
    print(f"Pacientes cargados desde el archivo: {len(pacientes)}")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_paciente(pacientes)
        elif opcion == "2":
            consultar_paciente(pacientes)
        elif opcion == "3":
            mostrar_pacientes(pacientes)
        elif opcion == "4":
            buscar_con_correccion(pacientes)
        elif opcion == "5":
            generar_estadisticas(pacientes)
        elif opcion == "6":
            # Se guarda nuevamente antes de cerrar para conservar los registros.
            guardar_pacientes(pacientes)
            print("\nGracias por utilizar el sistema OptoGestión.")
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Seleccione un número del 1 al 6.")


# Esta condición permite ejecutar el programa desde este archivo.
if __name__ == "__main__":
    ejecutar_programa()

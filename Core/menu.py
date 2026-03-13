import os
from .db_requests import *

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nENTER para continuar...")


# -------------------------
# CLIENTES
# -------------------------

def registrar_cliente_menu():

    clear()

    nombre = input("Nombre cliente: ")
    telefono = input("Telefono: ")

    registrar_cliente(nombre, telefono)

    print("\nCliente registrado")
    pause()


def ver_clientes_menu():

    clear()

    clientes = obtener_clientes()

    if not clientes:
        print("No hay clientes registrados")

    for cid, nombre, telefono in clientes:
        print(f"ID:{cid} | {nombre} | {telefono}")

    pause()


# -------------------------
# ADMIN MENU
# -------------------------

def menu_admin():

    while True:

        clear()

        print("ADMINISTRACION\n")
        print("1 Registrar cliente")
        print("2 Ver clientes")
        print("0 Volver")

        op = input("> ")

        if op == "1":
            registrar_cliente_menu()

        elif op == "2":
            ver_clientes_menu()

        elif op == "0":
            break


# -------------------------
# INVENTARIO
# -------------------------

def agregar_repuesto_menu():

    clear()

    try:
        nombre = input("Nombre repuesto: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))

        agregar_repuesto(nombre, precio, stock)

        print("\nRepuesto agregado")

    except ValueError:
        print("\nError: precio o stock inválido")

    pause()


def ver_inventario_menu():

    clear()

    inventario = obtener_inventario()

    if not inventario:
        print("Inventario vacío")

    for rid, nombre, precio, stock in inventario:
        print(f"ID:{rid} | {nombre} | ${precio} | Stock:{stock}")

    pause()


def registrar_compra_menu():

    clear()

    try:
        repuesto = input("Repuesto: ")
        cantidad = int(input("Cantidad: "))
        costo = float(input("Costo: "))

        registrar_compra(repuesto, cantidad, costo)

        print("\nCompra registrada")

    except ValueError:
        print("\nDatos inválidos")

    pause()


def menu_inventario():

    while True:

        clear()

        print("INVENTARIO\n")
        print("1 Agregar repuesto")
        print("2 Ver inventario")
        print("3 Registrar compra")
        print("0 Volver")

        op = input("> ")

        if op == "1":
            agregar_repuesto_menu()

        elif op == "2":
            ver_inventario_menu()

        elif op == "3":
            registrar_compra_menu()

        elif op == "0":
            break


# -------------------------
# REPARACIONES
# -------------------------

def registrar_reparacion_menu():

    clear()

    cliente = input("Cliente: ")
    telefono = input("Telefono: ")
    modelo = input("Modelo telefono: ")
    imei = input("IMEI: ")
    problema = input("Problema: ")

    registrar_reparacion(cliente, telefono, modelo, imei, problema)

    print("\nReparacion registrada")
    pause()


def ver_reparaciones_menu():

    clear()

    reparaciones = obtener_reparaciones()

    if not reparaciones:
        print("No hay reparaciones")

    for r in reparaciones:
        print(r)

    pause()


def cambiar_estado_menu():

    try:

        id_rep = int(input("ID reparacion: "))
        estado = input("Nuevo estado: ")

        cambiar_estado(id_rep, estado)

        print("\nEstado actualizado")

    except ValueError:
        print("\nID inválido")

    pause()


def menu_reparaciones():

    while True:

        clear()

        print("SERVICIO TECNICO\n")
        print("1 Registrar reparacion")
        print("2 Ver reparaciones")
        print("3 Cambiar estado")
        print("0 Volver")

        op = input("> ")

        if op == "1":
            registrar_reparacion_menu()

        elif op == "2":
            ver_reparaciones_menu()

        elif op == "3":
            cambiar_estado_menu()

        elif op == "0":
            break

def main_menu():

    while True:

        clear()

        print("MENU PRINCIPAL\n")
        print("1 Administracion")
        print("2 Inventario / Compras")
        print("3 Servicio tecnico")
        print("0 Salir")

        op = input("> ")

        if op == "1":
            menu_admin()

        elif op == "2":
            menu_inventario()

        elif op == "3":
            menu_reparaciones()

        elif op == "0":
            break
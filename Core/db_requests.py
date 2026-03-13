import os
import sqlite3
import datetime


## [ BASE DE DATOS ]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE_DIR, "Data", "meistertech.db")
DB = "meistertech.db"

def db():
    return sqlite3.connect(DB)

## [ CREAR A DB ]
def init_db():

    conn = db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        telefono TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS inventario(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        stock INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS compras(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repuesto TEXT,
        cantidad INTEGER,
        costo REAL,
        fecha TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reparaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        telefono TEXT,
        modelo TEXT,
        imei TEXT,
        problema TEXT,
        estado TEXT,
        fecha TEXT
    )
    """)

    conn.commit()
    conn.close()


## [ REGISTROS ]
def registrar_cliente(nombre, telefono):

    conn = db()
    c = conn.cursor()

    c.execute(
        "INSERT INTO clientes(nombre,telefono) VALUES(?,?)",
        (nombre, telefono)
    )

    conn.commit()
    conn.close()


def obtener_clientes():

    conn = db()
    c = conn.cursor()

    c.execute("SELECT * FROM clientes")
    data = c.fetchall()

    conn.close()

    return data


## [ INVENTARIO ]
def agregar_repuesto(nombre, precio, stock):

    conn = db()
    c = conn.cursor()

    c.execute(
        "INSERT INTO inventario(nombre,precio,stock) VALUES(?,?,?)",
        (nombre, precio, stock)
    )

    conn.commit()
    conn.close()


def obtener_inventario():

    conn = db()
    c = conn.cursor()

    c.execute("SELECT * FROM inventario")
    data = c.fetchall()

    conn.close()

    return data


## [ COMPRAS ]
def registrar_compra(repuesto, cantidad, costo):

    fecha = datetime.date.today()

    conn = db()
    c = conn.cursor()

    c.execute(
        "INSERT INTO compras(repuesto,cantidad,costo,fecha) VALUES(?,?,?,?)",
        (repuesto, cantidad, costo, fecha)
    )

    c.execute(
        "UPDATE inventario SET stock = stock + ? WHERE nombre=?",
        (cantidad, repuesto)
    )

    conn.commit()
    conn.close()


# [ REPARACIONES ]
def registrar_reparacion(cliente, telefono, modelo, imei, problema):

    estado = "Recibido"
    fecha = datetime.date.today()

    conn = db()
    c = conn.cursor()

    c.execute("""
    INSERT INTO reparaciones(cliente,telefono,modelo,imei,problema,estado,fecha)
    VALUES(?,?,?,?,?,?,?)
    """, (cliente, telefono, modelo, imei, problema, estado, fecha))

    conn.commit()
    conn.close()


def obtener_reparaciones():

    conn = db()
    c = conn.cursor()

    c.execute("SELECT * FROM reparaciones")
    data = c.fetchall()

    conn.close()

    return data


def cambiar_estado(id_rep, estado):

    conn = db()
    c = conn.cursor()

    c.execute(
        "UPDATE reparaciones SET estado=? WHERE id=?",
        (estado, id_rep)
    )

    conn.commit()
    conn.close()
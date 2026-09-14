import sqlite3
from datetime import datetime

# Nombre del archivo donde se guardará la base de datos local
DB_NAME = "chat.db"

def inicializar_db():
    """
    Crea la base de datos y la tabla 'mensajes' si todavía no existen.
    Campos solicitados: id, contenido, fecha_envio, ip_cliente.
    """
    try:
        # Se conecta a la base de datos (si el archivo no existe, SQLite lo crea automáticamente)
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Sentencia SQL para crear la tabla
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            );
        """)
        
        # Confirmar los cambios y cerrar
        conexion.commit()
        conexion.close()
        print("[DB] Base de datos y tabla 'mensajes' inicializadas con éxito.")
    except sqlite3.Error as e:
        print(f"[DB ERROR] Error al inicializar la base de datos: {e}")
        raise e

def guardar_mensaje(contenido: str, ip_cliente: str) -> str:
    """
    Guarda un mensaje en la base de datos con la IP del cliente y el timestamp actual.
    Retorna la fecha y hora generada (timestamp) para responder al cliente.
    """
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Obtenemos la fecha y hora actual en formato legible YYYY-MM-DD HH:MM:SS
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertamos el registro de forma segura usando placeholders (?) para prevenir SQL Injection
        cursor.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?);
        """, (contenido, timestamp, ip_cliente))
        
        conexion.commit()
        conexion.close()
        print(f"[DB] Mensaje guardado correctamente en la DB (Timestamp: {timestamp})")
        return timestamp
    except sqlite3.Error as e:
        print(f"[DB ERROR] Error al guardar el mensaje en la base de datos: {e}")
        raise e

def obtener_mensajes():
    """
    Función auxiliar para consultar y verificar los mensajes almacenados.
    """
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, contenido, fecha_envio, ip_cliente FROM mensajes;")
        filas = cursor.fetchall()
        conexion.close()
        return filas
    except sqlite3.Error as e:
        print(f"[DB ERROR] Error al leer la base de datos: {e}")
        return []

# Si ejecutamos este archivo directamente, realizamos una prueba rápida
if __name__ == "__main__":
    print("--- Probando módulo de base de datos ---")
    inicializar_db()
    ts = guardar_mensaje("Mensaje de prueba", "127.0.0.1")
    print("Mensajes actuales en la base de datos:")
    for row in obtener_mensajes():
        print(f"ID: {row[0]} | Mensaje: '{row[1]}' | Fecha: {row[2]} | IP: {row[3]}")


import socket
import sys
from database import inicializar_db, guardar_mensaje
import sqlite3

# Configuración del Host y Puerto
HOST = '127.0.0.1'  # localhost
PUERTO = 5000

# ==========================================
# 1. Función para inicializar el socket
# ==========================================
def inicializar_socket(host=HOST, puerto=PUERTO):
    """
    Crea, configura y pone en escucha el socket del servidor.
    Maneja errores en caso de que el puerto ya esté ocupado.
    """
    try:
        # Configuración del socket TCP/IP (IPv4, orientada a conexión)
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Permitir la reutilización inmediata de la dirección/puerto
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Asociar el socket a la IP y puerto especificados
        servidor.bind((host, puerto))
        
        # Poner el servidor en modo de escucha para recibir conexiones entrantes
        servidor.listen()
        print(f"[*] Servidor iniciado y escuchando en {host}:{puerto}...")
        return servidor

    except OSError as e:
        # Manejo de error específico de puerto ocupado u error de red
        print(f"\n[ERROR DE RED] No se pudo inicializar el socket en {host}:{puerto}.")
        print(f"Detalle del error: {e}")
        print("Sugerencia: Comprobá si ya hay otra instancia del servidor corriendo en ese puerto.")
        sys.exit(1)

# ==========================================
# 2. Función para guardar cada mensaje en DB
# ==========================================
def guardar_mensaje_db(contenido, ip_cliente):
    """
    Llama al módulo de base de datos para registrar el mensaje.
    Maneja posibles errores en caso de que la DB no esté accesible.
    """
    try:
        # Guardar en SQLite y obtener el timestamp generado
        timestamp = guardar_mensaje(contenido, ip_cliente)
        return timestamp
    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo acceder o escribir en la base de datos: {e}")
        return None

# ==========================================
# 3. Función para recibir mensajes de un cliente
# ==========================================
def atender_cliente(conexion, direccion):
    """
    Recibe múltiples mensajes de un cliente conectado hasta que este
    envíe la palabra 'éxito' o se desconecte.
    """
    ip_cliente = direccion[0]
    puerto_cliente = direccion[1]
    print(f"\n[+] Cliente conectado desde: {ip_cliente}:{puerto_cliente}")

    try:
        while True:
            # Recibir datos del cliente (hasta 1024 bytes en cada lectura)
            datos = conexion.recv(1024)
            
            # Si datos está vacío, significa que el cliente cerró la conexión abruptamente
            if not datos:
                print(f"[-] El cliente {ip_cliente}:{puerto_cliente} se ha desconectado.")
                break
            
            mensaje = datos.decode('utf-8').strip()
            
            # Verificar si el cliente envió la palabra de salida 'éxito' (o variantes sin tilde)
            if mensaje.lower() in ['éxito', 'exito']:
                print(f"[*] El cliente {ip_cliente}:{puerto_cliente} solicitó finalizar la sesión ('éxito').")
                despedida = "Sesión finalizada. ¡Hasta luego!"
                conexion.sendall(despedida.encode('utf-8'))
                break

            print(f"[>] Mensaje recibido de {ip_cliente}: '{mensaje}'")
            
            # Guardar el mensaje en la base de datos SQLite
            timestamp = guardar_mensaje_db(mensaje, ip_cliente)
            
            if timestamp:
                # Responder con el formato requerido por la consigna: "Mensaje recibido: <timestamp>"
                respuesta = f"Mensaje recibido: {timestamp}"
            else:
                respuesta = "Error: No se pudo guardar el mensaje en la base de datos."

            # Enviar confirmación al cliente
            conexion.sendall(respuesta.encode('utf-8'))

    except ConnectionResetError:
        print(f"[-] Conexión restablecida abruptamente por el cliente {ip_cliente}:{puerto_cliente}.")
    finally:
        # Cerrar el socket de conexión particular con este cliente
        conexion.close()
        print(f"[*] Conexión cerrada con {ip_cliente}:{puerto_cliente}.")

# ==========================================
# 4. Función para aceptar conexiones continuas
# ==========================================
def aceptar_conexiones(servidor):
    """
    Bucle principal que acepta clientes entrantes.
    Permite atender clientes de forma secuencial y cerrar de forma limpia con Ctrl+C.
    """
    try:
        while True:
            # accept() bloquea hasta que un cliente se conecta
            conexion, direccion = servidor.accept()
            # Procesar la comunicación con el cliente conectado
            atender_cliente(conexion, direccion)
    except KeyboardInterrupt:
        print("\n[*] Servidor detenido manualmente por el usuario (Ctrl+C).")
    finally:
        servidor.close()
        print("[*] Socket del servidor cerrado correctamente.")

# ==========================================
# Punto de entrada principal
# ==========================================
def main():
    print("=== SERVIDOR DE CHAT TCP CON SQLITE ===")
    
    # 1. Aseguramos que la DB y la tabla 'mensajes' existan antes de recibir conexiones
    try:
        inicializar_db()
    except sqlite3.Error:
        print("[ERROR CRÍTICO] No se puede iniciar el servidor sin acceso a la base de datos.")
        sys.exit(1)

    # 2. Inicializar el socket en localhost:5000
    servidor = inicializar_socket(HOST, PUERTO)

    # 3. Iniciar el bucle de aceptación de conexiones
    aceptar_conexiones(servidor)

if __name__ == "__main__":
    main()

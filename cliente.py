import socket
import sys

# Configuración del servidor al que nos vamos a conectar
HOST = '127.0.0.1'  # localhost
PUERTO = 5000

def iniciar_cliente():
    """
    Crea el socket del cliente, se conecta al servidor y entra en un bucle interactivo
    para enviar múltiples mensajes hasta que el usuario escriba 'exit'.
    """
    # 1. Configuración del socket TCP/IP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 2. Conectarse al servidor en localhost:5000
        print(f"[*] Conectando al servidor en {HOST}:{PUERTO}...")
        cliente.connect((HOST, PUERTO))
        print("[+] ¡Conectado exitosamente al servidor!")
        print("[i] Escribe tus mensajes a continuación.")
        print("[i] Para finalizar la sesión, escribe: exit\n" + "-"*45)

        # 3. Bucle interactivo para enviar múltiples mensajes
        while True:
            mensaje = input("Vos > ").strip()

            # Evitar enviar mensajes completamente vacíos
            if not mensaje:
                continue

            # Enviar el mensaje codificado en bytes (UTF-8)
            cliente.sendall(mensaje.encode('utf-8'))

            # Esperar y recibir la respuesta del servidor
            datos_servidor = cliente.recv(1024)
            if not datos_servidor:
                print("[-] El servidor cerró la conexión inesperadamente.")
                break

            respuesta = datos_servidor.decode('utf-8')
            print(f"Servidor > {respuesta}")

            # Si el mensaje enviado fue 'exit' (o 'éxito'/'salir'), salimos del bucle
            if mensaje.lower() in ['exit', 'éxito', 'exito', 'salir']:
                print("-" * 45)
                print("[*] Desconectando y cerrando cliente...")
                break

    except ConnectionRefusedError:
        print(f"\n[ERROR] No se pudo conectar al servidor en {HOST}:{PUERTO}.")
    except KeyboardInterrupt:
        print("\n[*] Cliente cerrado por el usuario.")
    finally:
        # 4. Cerrar el socket al terminar
        cliente.close()
        print("[*] Conexión cerrada. Fin del programa.")

if __name__ == "__main__":
    iniciar_cliente()

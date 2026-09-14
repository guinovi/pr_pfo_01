# PFO-01
## Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos

* **Materia:** Programación sobre redes - 3° E
* **Alumno:** Novillo Guillermo Tadeo
* **Repositorio GitHub:** [https://github.com/guinovi/pr_pfo_01](https://github.com/guinovi/pr_pfo_01)

---

## Descripción
Implementación en Python de un sistema de comunicación cliente-servidor mediante sockets TCP/IP y persistencia de mensajes en una base de datos SQLite, aplicando buenas prácticas de modularización, comentarios descriptivos y manejo de excepciones.

## Estructura del Proyecto
* `servidor.py`: Inicializa el socket en `localhost:5000`, acepta conexiones, recibe mensajes en bucle, maneja errores de red/base de datos y responde con timestamp.
* `cliente.py`: Permite al usuario enviar múltiples mensajes interactivos al servidor hasta escribir `exit`. Muestra cada respuesta devuelta por el servidor.
* `database.py`: Módulo que administra la base de datos SQLite (`chat.db`) y la tabla `mensajes` (`id`, `contenido`, `fecha_envio`, `ip_cliente`).

## Requisitos
* Python 3.8 o superior (no requiere librerías externas, utiliza módulos estándar `socket`, `sqlite3`, `sys`, `datetime`).

## Instrucciones de Ejecución

### 1. Iniciar el Servidor
En una terminal:
```bash
python3 servidor.py
```

### 2. Iniciar el Cliente
En una segunda terminal:
```bash
python3 cliente.py
```

### 3. Finalizar la sesión
Escribe `exit` (o `éxito`) en la consola del cliente para cerrar la conexión ordenadamente.


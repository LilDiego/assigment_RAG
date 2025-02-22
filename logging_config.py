from loguru import logger
import os

# Crear carpeta de logs si no existe
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuración de loguru para rotación y retención
logger.add(os.path.join(log_dir, "logs.log"), rotation="1 week", retention="10 days", compression="zip", level="INFO")

# Función de ejemplo para registrar un evento
def log_event(message):
    logger.info(message)

# Función de error
def log_error(message):
    logger.error(message)

# Función para registrar tiempos
def log_timing(start_time, end_time, task_name):
    duration = end_time - start_time
    logger.info(f"Task '{task_name}' took {duration:.2f} seconds")

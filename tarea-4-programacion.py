"""
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
En un equipo conformado por cinco (5) estudiantes, deberán desarrollar un sistema integral orientado a objetos, sin uso de bases de datos, capaz de gestionar clientes, servicios y reservas para 
una empresa llamada Software FJ que ofrece varios tipos de servicios (reservas de salas, alquiler de equipos y asesorías especializadas). El objetivo de esta tarea es construir una aplicación estable, 
modular y extensible que implemente de forma rigurosa los principios de abstracción, herencia, polimorfismo, encapsulación y manejo avanzado de excepciones, garantizando que el sistema siga funcionando
aun cuando se presenten errores durante su ejecución.

El sistema debe incluir clases abstractas, clases derivadas, métodos sobrecargados, manejo de listas internas y validaciones estrictas, demostrando un diseño orientado a objetos completamente funcional. 
La información no debe almacenarse en bases de datos; toda la gestión debe hacerse mediante objetos, listas y manejo de archivos únicamente para el registro de eventos y errores.

Como parte esencial de la tarea, el sistema deberá incorporar manejo robusto de excepciones, incluyendo excepciones personalizadas, uso de bloques try/except, try/except/else, try/except/finally, y encadenamiento de excepciones. 
Cada error detectado debe registrarse en un archivo de logs, manteniendo la aplicación activa y estable en todo momento. El sistema debe ser capaz de manejar errores provenientes de datos inválidos, parámetros faltantes, 
operaciones no permitidas, intentos de reserva incorrectos, servicios no disponibles, cálculos inconsistentes y cualquier otra situación que pueda comprometer la operación normal de la aplicación.
El trabajo debe basarse en una arquitectura orientada a objetos, incluyendo al menos:

• Una clase abstracta que represente entidades generales del sistema.
• Una clase Cliente con validaciones robustas y encapsulación de datos personales.
• Una clase abstracta Servicio y al menos tres servicios especializados que hereden de ella, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y validar parámetros.
• Una clase Reserva que integre cliente, servicio, duración y estado, e implemente confirmación, cancelación y procesamiento con manejo de excepciones.
• Métodos sobrecargados (por ejemplo, diferentes variantes del cálculo de costos con impuestos, descuentos o parámetros opcionales).
• Un archivo de logs donde se registren todos los errores y eventos relevantes.

El sistema, sin utilizar ningún motor de base de datos, debe simular al menos 10 operaciones completas, incluyendo registros válidos e inválidos de clientes, creación correcta e incorrecta de servicios, 
y reservas exitosas y fallidas, demostrando la capacidad del programa para continuar funcionando ante errores graves y manejar excepciones de manera controlada y profesional.

El equipo debe entregar un único proyecto completamente funcional, organizado, documentado y capaz de ejecutarse sin interrupciones, demostrando la correcta aplicación de la programación orientada a objetos y
el manejo avanzado de excepciones en un entorno sin base de datos.

"""

import os
import datetime
from abc import ABC, abstractmethod

# CONFIGURACIÓN DE RUTAS Y SISTEMA DE LOGS PERSISTENTES

# Se obtiene la ruta absoluta de la carpeta donde se encuentra este archivo .py
# Esto evita errores de permisos o guardados en ubicaciones incorrectas del sistema.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Definición de la ruta completa del archivo de log en la misma carpeta del script
ARCHIVO_LOGS = os.path.join(BASE_DIR, "Registro_eventos")

def registrar_log(mensaje: str, tipo: str = "INFO"):
    """
    Registra eventos, advertencias y errores en un archivo de texto plano (Registro_eventos).
    
    Parámetros:
        mensaje (str): Texto descriptivo del evento u operación realizada.
        tipo (str): Categoría del log (ej: 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'SYSTEM').
    """
    # Formato de fecha y hora: YYYY-MM-DD HH:MM:SS
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Construcción de la línea de log estructurada
    log_entry = f"[{timestamp}] [{tipo}] {mensaje}\n"
    
    try:
        # Uso de 'with' para garantizar el cierre automático del archivo
        # Modo 'a' (append) para añadir nuevas líneas sin borrar el historial previo
        with open(ARCHIVO_LOGS, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        # En caso de fallo en disco, se muestra una alerta en consola sin detener el programa
        print(f"⚠️ Error al escribir en el archivo de registro (log): {e}")


# EXCEPCIONES PERSONALIZADAS DEL DOMINIO
class DatosInvalidosError(Exception):
    """
    Excepción lanzada cuando los datos ingresados por el usuario no cumplen
    con las reglas de validación de negocio (ej: nombre corto, correo sin '@', etc.).
    """
    pass

class ServicioNoDisponibleError(Exception):
    """
    Excepción lanzada cuando se intenta reservar o alquilar un servicio que no está activo.
    """
    pass
  
class ReservaError(Exception):
    """
    Excepción lanzada ante fallos en la confirmación, procesamiento o cancelación de reservas.
    """
    pass


# CLASE ABSTRACTA GENERAL: EntidadBase
class EntidadBase(ABC):
    """
    Clase abstracta general de la cual deben heredar todas las entidades del sistema
    (Cliente, Servicio, etc.) para garantizar un identificador único.
    """
    
    def __init__(self, id_entidad: int):
        """
        Inicializa el identificador protegido de la entidad.
        
        Parámetros:
            id_entidad (int): Número único que identifica a la entidad.
        """
        self._id_entidad = id_entidad

    @abstractmethod
    def obtener_identificador(self) -> int:
        """
        Método abstracto que obliga a todas las clases hijas a implementar la devolución
        de su ID único de forma pública.
        """
        pass


# FUNCIÓN DE AUTOINCREMENTO DINÁMICO DE IDs ÚNICOS
def generar_siguiente_id(lista_entidades) -> int:
    """
    Genera un nuevo ID único e incremental evaluando la lista de entidades actuales.
    Evita la duplicación de IDs al eliminar o agregar nuevos elementos.
    
    Parámetros:
        lista_entidades (list): Lista de objetos que heredan de EntidadBase.
        
    Retorna:
        int: Siguiente número de ID disponible (1 si la lista está vacía).
    """
    if not lista_entidades:
        return 1
    # Busca el valor máximo de ID en los objetos existentes y le suma 1
    return max(e.obtener_identificador() for e in lista_entidades) + 1



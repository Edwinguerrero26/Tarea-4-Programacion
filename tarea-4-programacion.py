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

import re # Importa el módulo re para usar expresiones regulares y validar datos como correo y teléfono.


class Cliente(EntidadBase):
    """Cliente con datos privados y propiedades de solo lectura."""

    def __init__(self, nombre: str, correo: str, telefono: str) -> None:
        super().__init__()  # Llama al constructor de la clase base "Entidad"

        # Verifica que el nombre sea un texto.
        # También elimina espacios al inicio y al final con strip()
        # y comprueba que tenga al menos 2 caracteres.
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise DatosInvalidosError("El nombre debe contener al menos dos caracteres.")

        # Verifica que el correo sea un texto.
        # Luego valida que tenga un formato válido, por ejemplo:
        # usuario@dominio.com
        if not isinstance(correo, str) or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", correo.strip()):
            raise DatosInvalidosError("El correo no es válido.")

        # Verifica que el teléfono sea un texto.
        # Luego valida que tenga un formato válido, por ejemplo:
        # +1234567890
        if not isinstance(telefono, str) or not re.fullmatch(r"\+?[0-9][0-9 ()-]{6,19}", telefono.strip()):
            raise DatosInvalidosError("El teléfono no es válido.")

    @property
    def nombre(self) -> str:
        # Permite leer el nombre del cliente sin permitir modificarlo directamente.
        return self.__nombre

    @property
    def correo(self) -> str:
        # Permite leer el correo del cliente de forma segura y solo lectura.
        return self.__correo

    @property
    def telefono(self) -> str:
        # Permite leer el teléfono del cliente sin cambiarlo desde fuera.
        return self.__telefono

    def descripcion(self) -> str:
        # Genera una descripción del cliente con su nombre, correo y teléfono.
        return f"Cliente: {self.nombre} ({self.correo}), teléfono: {self.telefono}"


# GESTIÓN DE SERVICIOS: CLASE ABSTRACTA

class Servicio(EntidadBase):
    """
    Clase abstracta que define la estructura base para cualquier servicio ofrecido por Software FJ.
    Hereda de EntidadBase para garantizar un ID único.
    """
    def __init__(self, id_entidad: int, nombre: str, costo_base: float, disponible: bool = True):
        super().__init__(id_entidad) # Llamada al constructor de la clase padre
        
        # Validaciones estrictas requeridas en la rúbrica
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre del servicio debe tener al menos 3 caracteres.")
        if not isinstance(costo_base, (int, float)) or costo_base < 0:
            raise DatosInvalidosError("El costo base no puede ser negativo.")
            
        self._nombre = nombre.strip()
        self._costo_base = float(costo_base)
        self._disponible = disponible

    # Cumplimiento del método abstracto heredado de EntidadBase
    def obtener_identificador(self) -> int:
        return self._id_entidad

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool):
        self._disponible = estado

    
    # MÉTODOS ABSTRACTOS (Para forzar polimorfismo)
   
    @abstractmethod
    def calcular_costo(self, impuesto: float = None, descuento: float = None) -> float:
        """ Método abstracto que sobrecargarán las clases hijas. """
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass

# CLASES HIJAS: HERENCIA, POLIMORFISMO Y SOBRECARGA

class ReservaSala(Servicio):
    """ Servicio 1: Reserva de salas físicas. """
    def __init__(self, id_entidad: int, nombre: str, costo_base: float, capacidad: int):
        super().__init__(id_entidad, nombre, costo_base)
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0.")
        self.__capacidad = capacidad

    # Polimorfismo y Sobrecarga mediante parámetros opcionales
    def calcular_costo(self, impuesto: float = None, descuento: float = None) -> float:
        registrar_log(f"Iniciando cálculo de costo para Sala '{self.nombre}'", "INFO")
        
        # Bloque robusto de excepciones (try/except/else/finally)
        try:
            if not self.disponible:
                raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible para reserva.")
            
            costo_total = self._costo_base
            
            # Lógica polimórfica: Las salas de más de 20 personas tienen un recargo del 10%
            if self.__capacidad > 20:
                costo_total *= 1.10

            # Aplicación de parámetros opcionales (Sobrecarga simulada)
            if descuento is not None:
                if descuento < 0 or descuento > 100:
                    raise DatosInvalidosError("El porcentaje de descuento es inválido.")
                costo_total -= costo_total * (descuento / 100)

            if impuesto is not None:
                if impuesto < 0:
                    raise DatosInvalidosError("El impuesto no puede ser negativo.")
                costo_total += costo_total * (impuesto / 100)

        except Exception as e:
            registrar_log(f"Error en cálculo de costo (Sala): {e}", "ERROR")
            raise # Encadenamiento: re-lanza el error para que la aplicación principal lo sepa
        else:
            # Se ejecuta solo si no hubo errores en el try
            registrar_log(f"Cálculo exitoso para Sala '{self.nombre}'. Total: {costo_total}", "INFO")
            return round(costo_total, 2)
        finally:
            # Se ejecuta siempre, haya error o no
            registrar_log(f"Finaliza operación de costeo para ID {self._id_entidad}", "SYSTEM")

    def descripcion(self) -> str:
        return f"[Sala] {self.nombre} - Capacidad: {self.__capacidad} personas."


class AlquilerEquipo(Servicio):
    """ Servicio 2: Alquiler de equipos tecnológicos. """
    def __init__(self, id_entidad: int, nombre: str, costo_base: float, requiere_deposito: bool):
        super().__init__(id_entidad, nombre, costo_base)
        self.__requiere_deposito = requiere_deposito

    # Polimorfismo: El cálculo es distinto al de las salas
    def calcular_costo(self, impuesto: float = None, descuento: float = None) -> float:
        registrar_log(f"Iniciando cálculo de costo para Equipo '{self.nombre}'", "INFO")
        try:
            if not self.disponible:
                raise ServicioNoDisponibleError(f"El equipo '{self.nombre}' está averiado o en uso.")
            
            costo_total = self._costo_base
            
            # Lógica polimórfica: Si requiere depósito, se suma un cargo fijo de 50.0 al costo base
            if self.__requiere_deposito:
                costo_total += 50.0

            if descuento is not None:
                costo_total -= costo_total * (descuento / 100)
            if impuesto is not None:
                costo_total += costo_total * (impuesto / 100)

        except Exception as e:
            registrar_log(f"Error en cálculo de costo (Equipo): {e}", "ERROR")
            raise
        else:
            return round(costo_total, 2)
        finally:
            registrar_log(f"Finaliza operación de costeo para ID {self._id_entidad}", "SYSTEM")

    def descripcion(self) -> str:
        deposito = "Sí" if self.__requiere_deposito else "No"
        return f"[Equipo] {self.nombre} - Requiere depósito: {deposito}."


class AsesoriaEspecializada(Servicio):
    """ Servicio 3: Asesorías con profesionales. """
    def __init__(self, id_entidad: int, nombre: str, costo_base: float, horas_estimadas: int):
        super().__init__(id_entidad, nombre, costo_base)
        if horas_estimadas <= 0:
            raise DatosInvalidosError("Las horas estimadas deben ser mínimo 1.")
        self.__horas_estimadas = horas_estimadas

    # Polimorfismo: El cálculo se multiplica por las horas
    def calcular_costo(self, impuesto: float = None, descuento: float = None) -> float:
        registrar_log(f"Iniciando cálculo de costo para Asesoría '{self.nombre}'", "INFO")
        try:
            if not self.disponible:
                raise ServicioNoDisponibleError(f"El asesor para '{self.nombre}' no tiene agenda disponible.")
            
            # Lógica polimórfica: El costo base es por hora
            costo_total = self._costo_base * self.__horas_estimadas

            if descuento is not None:
                costo_total -= costo_total * (descuento / 100)
            if impuesto is not None:
                costo_total += costo_total * (impuesto / 100)

        except Exception as e:
            registrar_log(f"Error en cálculo de costo (Asesoría): {e}", "ERROR")
            raise
        else:
            return round(costo_total, 2)
        finally:
              registrar_log(f"Finaliza operación de costeo para ID {self._id_entidad}", "SYSTEM")

    def descripcion(self) -> str:
        return f"[Asesoría] {self.nombre} - Duración: {self.__horas_estimadas} horas."
            
# GESTIÓN DE RESERVAS

class Reserva(EntidadBase):
    """
    Clase que gestiona las reservas del sistema Software FJ.
    Integra un cliente, un servicio, la duración y el estado de la reserva,
    implementando confirmación, cancelación y procesamiento.
    """

    def __init__(self, id_entidad: int, cliente: Cliente, servicio: Servicio, duracion: int = 1) -> None:
        super().__init__(id_entidad)

        # Validaciones de negocio
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "El cliente asociado a la reserva no es válido."
            )

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "El servicio asociado a la reserva no es válido."
            )

        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise DatosInvalidosError(
                "La duración de la reserva debe ser un número entero mayor a 0."
            )

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

        registrar_log(
            f"Reserva creada con ID {self._id_entidad} para el cliente "
            f"'{cliente.nombre}' con servicio '{servicio.nombre}'. "
            f"Estado inicial: Pendiente",
            "INFO"
        )

    # Implementación del método abstracto heredado de EntidadBase
    def obtener_identificador(self) -> int:
        return self._id_entidad

    # Propiedades de solo lectura
    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion(self) -> int:
        return self.__duracion

    @property
    def estado(self) -> str:
        return self.__estado

    # CONFIRMACIÓN DE RESERVA
    def confirmar(self) -> None:
        """
        Confirma la reserva únicamente si está pendiente
        y el servicio se encuentra disponible.
        """
        registrar_log(
            f"Intentando confirmar la reserva ID {self._id_entidad}",
            "INFO"
        )

        try:
            if self.__estado != "Pendiente":
                raise ReservaError(
                    f"No se puede confirmar la reserva ID {self._id_entidad} "
                    f"porque su estado actual es '{self.__estado}'."
                )

            if not self.__servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.__servicio.nombre}' "
                    "no está disponible actualmente."
                )

            self.__estado = "Confirmada"

        except Exception as e:
            registrar_log(
                f"Error al confirmar la reserva ID {self._id_entidad}: {e}",
                "ERROR"
            )
            raise

        else:
            registrar_log(
                f"Reserva ID {self._id_entidad} confirmada exitosamente.",
                "INFO"
            )

        finally:
            registrar_log(
                f"Finaliza proceso de confirmación para reserva ID "
                f"{self._id_entidad}",
                "SYSTEM"
            )

    # CANCELACIÓN DE RESERVA
    def cancelar(self) -> None:
        """
        Cancela la reserva siempre que no haya sido procesada
        ni se encuentre cancelada previamente.
        """
        registrar_log(
            f"Intentando cancelar la reserva ID {self._id_entidad}",
            "INFO"
        )

        try:
            if self.__estado == "Cancelada":
                raise ReservaError(
                    f"La reserva ID {self._id_entidad} "
                    "ya se encuentra cancelada."
                )

            if self.__estado == "Procesada":
                raise ReservaError(
                    f"No se puede cancelar la reserva ID {self._id_entidad} "
                    "porque ya fue procesada."
                )

            self.__estado = "Cancelada"

        except Exception as e:
            registrar_log(
                f"Error al cancelar la reserva ID {self._id_entidad}: {e}",
                "ERROR"
            )
            raise

        else:
            registrar_log(
                f"Reserva ID {self._id_entidad} cancelada exitosamente.",
                "INFO"
            )

        finally:
            registrar_log(
                f"Finaliza proceso de cancelación para reserva ID "
                f"{self._id_entidad}",
                "SYSTEM"
            )

    # PROCESAMIENTO DE RESERVA
    def procesar(self, impuesto: float = None, descuento: float = None) -> float:
        """
        Procesa la reserva, calcula el costo total mediante
        el método polimórfico del servicio y actualiza su estado.
        """

        registrar_log(
            f"Intentando procesar la reserva ID {self._id_entidad}",
            "INFO"
        )

        try:
            if self.__estado == "Cancelada":
                raise ReservaError(
                    f"No se puede procesar la reserva ID {self._id_entidad} "
                    "porque está cancelada."
                )

            if self.__estado == "Procesada":
                raise ReservaError(
                    f"La reserva ID {self._id_entidad} "
                    "ya fue procesada anteriormente."
                )

            if self.__estado != "Confirmada":
                raise ReservaError(
                    f"La reserva ID {self._id_entidad} debe estar confirmada "
                    f"antes de ser procesada. Estado actual: {self.__estado}."
                )

            # Validación de impuesto
            if impuesto is not None:
                if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or impuesto < 0:
                    raise DatosInvalidosError(
                        "El impuesto debe ser un número mayor o igual a 0."
                    )

            # Validación de descuento
            if descuento is not None:
                if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
                    raise DatosInvalidosError(
                        "El descuento debe estar entre 0 y 100."
                    )

            # Cálculo polimórfico del costo del servicio
            costo_parcial = self.__servicio.calcular_costo(
                impuesto=impuesto,
                descuento=descuento
            )

            # Multiplicación según la duración de la reserva
            costo_total = costo_parcial * self.__duracion

            self.__estado = "Procesada"

        except Exception as e:
            registrar_log(
                f"Error al procesar la reserva ID {self._id_entidad}: {e}",
                "ERROR"
            )
            raise

        else:
            registrar_log(
                f"Reserva ID {self._id_entidad} procesada con éxito. "
                f"Costo total: {costo_total}",
                "INFO"
            )

            return round(costo_total, 2)

        finally:
            registrar_log(
                f"Finaliza proceso de procesamiento para reserva ID "
                f"{self._id_entidad}",
                "SYSTEM"
            )

    # DESCRIPCIÓN DE RESERVA
    def descripcion(self) -> str:
        """
        Retorna una descripción detallada de la reserva.
        """
        return (
            f"[Reserva ID: {self._id_entidad}] "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} unidad(es) | "
            f"Estado: {self.__estado}"
        )

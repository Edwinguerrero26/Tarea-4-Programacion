prin(hello word)

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



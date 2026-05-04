""" INSTRUCCIONES: Se debe desarrollar un sistema integral orientado a objetos, sin uso de bases de datos,
capaz de gestionar clientes, servicios y reservas para una empresa
llamada (Software FJ) que ofrece varios tipos de servicios (reservas de
salas, alquiler de equipos y asesorías especializadas). El objetivo de esta
tarea es construir una aplicación estable, modular y extensible que
implemente de forma rigurosa los principios de abstracción, herencia,
polimorfismo, encapsulación y manejo avanzado de excepciones,
garantizando que el sistema siga funcionando aun cuando se presenten
errores durante su ejecución"""

"""El trabajo debe basarse en una arquitectura orientada a objetos,
incluyendo al menos:
• Una clase abstracta que represente entidades generales del
sistema. (Completado)
• Una clase Cliente con validaciones robustas y encapsulación de
datos personales. (Completado)
• Una clase abstracta Servicio y al menos tres servicios
especializados que hereden de ella, implementando polimorfismo y
métodos sobrescritos para calcular costos, describir servicios y
validar parámetros. (Revisar, ampliar, actualmente hay 3)
• Una clase Reserva que integre cliente, servicio, duración y estado,
e implemente confirmación, cancelación y procesamiento con
manejo de excepciones. (Completado)
• Métodos sobrecargados (por ejemplo, diferentes variantes del
cálculo de costos con impuestos, descuentos o parámetros
opcionales). (Completado)
3
• Un archivo de logs donde se registren todos los errores y eventos
relevantes. (Se crea el archivo, revisar funcionamiento)""" 

"""FALTA: 5 operaciones completas, Debugging, Revisar Logs, Organizacion (Modular, extensible), validacion estricta, Documento PDF"""
"""ADICIONALES: Interfaz grafica (ej tkinter), Inputs del usuario, Documentacion, +comentarios de linea"""

"""Nota: Recuerden revisar lo que ya esta implementado y trabajar desde ahi, cualquier correccion se debe especificar en el commit"""

"""Desarrollo de la actividad - Sistema Integral de Gestión de Clientes, Servicios y Reservas"""

# IMPORT

from abc import ABC, abstractmethod  # Permite crear clases abstractas
from datetime import datetime        # Manejo de fechas
import logging                       # Sistema de logs


# CONFIGURACIÓN DEL LOG

# Configura el archivo de logs donde se guardarán los errores y eventos
logging.basicConfig(
    filename="software_fj.log",      # Archivo de salida
    level=logging.INFO,              # Nivel mínimo de registro
    format="%(asctime)s - %(levelname)s - %(message)s"  # Formato del log
)


# EXCEPCIONES 

class SistemaError(Exception):
    """Clase base para errores del sistema"""
    pass


class ValidacionError(SistemaError):
    """Error cuando los datos no son válidos"""
    pass


class ReservaError(SistemaError):
    """Error relacionado con reservas"""
    pass


class ServicioError(SistemaError):
    """Error relacionado con servicios"""
    pass


# CLASE ABSTRACTA BASE

class Entidad(ABC):
    """Clase abstracta que representa una entidad del sistema"""

    def __init__(self, id):
        self._id = id  # Identificador protegido

    @abstractmethod
    def mostrar_info(self):
        """Método abstracto que debe implementar cada entidad"""
        pass


# CLASE CLIENTE

class Cliente(Entidad):
    """Clase que representa un cliente"""

    def __init__(self, id, nombre, email):
        super().__init__(id)  # Llama al constructor padre
        self.nombre = nombre  # Usa setter
        self.email = email    # Usa setter

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.isalpha():
            raise ValidacionError("Nombre inválido")
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValidacionError("Email inválido")
        self._email = valor

    def mostrar_info(self):
        return f"Cliente: {self._nombre}, Email: {self._email}"


# CLASE ABSTRACTA SERVICIO

class Servicio(ABC):
    """Clase abstracta para servicios"""

    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# SERVICIOS ESPECÍFICOS - hay 3

class ReservaSala(Servicio):
    """Servicio de reserva de salas"""

    def calcular_costo(self, horas, descuento=0): # Sobrecarga simulada
        if horas <= 0:
            raise ServicioError("Horas inválidas")
        costo = self.precio_base * horas
        return costo - (costo * descuento)

    def descripcion(self):
        return "Reserva de sala por horas"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos"""

    def calcular_costo(self, dias, seguro=False): #sobrecarga
        if dias <= 0:
            raise ServicioError("Días inválidos")
        costo = self.precio_base * dias
        if seguro:
            costo += 20  # Costo adicional por seguro
        return costo

    def descripcion(self):
        return "Alquiler de equipos tecnológicos"


class Asesoria(Servicio):
    """Servicio de asesorías"""

    def calcular_costo(self, horas, tipo="general"): #sobrcarga
        if horas <= 0:
            raise ServicioError("Horas inválidas")
        multiplicador = 1.5 if tipo == "especializada" else 1
        return self.precio_base * horas * multiplicador

    def descripcion(self):
        return "Asesoría profesional"


# CLASE RESERVA

class Reserva:
    """Clase que representa una reserva"""

    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"

# En esta parte se usa try, except, else, finally + implementa confirmar, cancelar, procesar
    def confirmar(self):
        """Confirma la reserva"""
        try:
            if self.estado != "pendiente":
                raise ReservaError("La reserva ya fue procesada")

            self.estado = "confirmada"
            logging.info("Reserva confirmada")

        except Exception as e:
            logging.error(f"Error al confirmar reserva: {e}")
            raise

    def cancelar(self):
        """Cancela la reserva"""
        try:
            self.estado = "cancelada"
            logging.info("Reserva cancelada")
        except Exception as e:
            logging.error(f"Error al cancelar: {e}")

    def procesar_pago(self):
        """Procesa el costo del servicio"""
        try:
            costo = self.servicio.calcular_costo(self.duracion)
        except Exception as e:
            raise ReservaError("Error en cálculo de pago") from e
        else:
            logging.info(f"Pago procesado: {costo}")
            return costo
        finally:
            logging.info("Intento de procesamiento finalizado")


# SISTEMA PRINCIPAL

class SistemaFJ:
    """Clase principal del sistema"""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        try:
            self.clientes.append(cliente)
            logging.info("Cliente agregado")
        except Exception as e:
            logging.error(f"Error agregando cliente: {e}")

    def agregar_servicio(self, servicio):
        try:
            self.servicios.append(servicio)
            logging.info("Servicio agregado")
        except Exception as e:
            logging.error(f"Error agregando servicio: {e}")

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            self.reservas.append(reserva)
            return reserva
        except Exception as e:
            logging.error(f"Error creando reserva: {e}")


# SIMULACIÓN (10 OPERACIONES)

def simulacion():
    sistema = SistemaFJ()

    # Crear servicios
    sala = ReservaSala("Sala", 50)
    equipo = AlquilerEquipo("Laptop", 30)
    asesoria = Asesoria("Consultoría", 100)

    sistema.agregar_servicio(sala)
    sistema.agregar_servicio(equipo)
    sistema.agregar_servicio(asesoria)

    # Lista de pruebas - deben ser 10, hay 5
    pruebas = [
        lambda: sistema.agregar_cliente(Cliente(1, "Dan", "dan@mail.com")),
        lambda: sistema.agregar_cliente(Cliente(2, "123", "error")),  # inválido
        lambda: sistema.crear_reserva(sistema.clientes[0], sala, 2),
        lambda: sistema.crear_reserva(sistema.clientes[0], equipo, -1),  # error
        lambda: sistema.crear_reserva(sistema.clientes[0], asesoria, 3),
    ]

    # Ejecutar operaciones con control de errores
    for i, prueba in enumerate(pruebas):
        try:
            resultado = prueba()

            if isinstance(resultado, Reserva):
                resultado.confirmar()
                print("Costo:", resultado.procesar_pago())

        except SistemaError as e:
            print(f"[Error controlado {i}]: {e}")
            logging.error(f"Error controlado: {e}")

        except Exception as e:
            print(f"[Error inesperado {i}]: {e}")
            logging.critical(f"Error crítico: {e}")


# EJECUCION, no se usaron bases de datos - datos temporales

if __name__ == "__main__":
    simulacion()




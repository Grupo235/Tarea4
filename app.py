"""
SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ
Programacion - Actividad 4 - Daniel Perez
==========================================
Sistema orientado a objetos para gestión de clientes, servicios y reservas.
Sin uso de bases de datos - toda la gestión mediante objetos y listas.
Incluye manejo avanzado de excepciones, registro de logs, interfaz gráfica (Tema oscuro). 
Abstracción, herencia, polimorfismo, encapsulación, Metodos sobrecargados.
"""

# IMPORTACIONES
from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, StringVar, IntVar, DoubleVar, BooleanVar
import threading

# CONFIGURACIÓN DEL SISTEMA DE LOGS
class LogManager:
    @staticmethod
    def configurar_logs():
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/software_fj_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger('SoftwareFJ')
        logger.setLevel(logging.DEBUG)
        return logger

logger = LogManager.configurar_logs()

# EXCEPCIONES PERSONALIZADAS - Dobrecarga
class SistemaFJException(Exception):
    def __init__(self, mensaje, codigo_error=None):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(self.mensaje)
        logger.error(f"Excepción del sistema: {mensaje} (Código: {codigo_error})")

class ValidacionError(SistemaFJException):
    def __init__(self, mensaje, campo=None):
        super().__init__(mensaje, "VAL-001")
        self.campo = campo
        logger.warning(f"Error de validación en campo '{campo}': {mensaje}")

class ClienteError(SistemaFJException):
    def __init__(self, mensaje):
        super().__init__(mensaje, "CLI-001")

class ServicioError(SistemaFJException):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SRV-001")

class ReservaError(SistemaFJException):
    def __init__(self, mensaje):
        super().__init__(mensaje, "RES-001")

class OperacionNoPermitidaError(SistemaFJException):
    def __init__(self, mensaje):
        super().__init__(mensaje, "OPR-001")

# CLASE ABSTRACTA BASE PARA ENTIDADES
class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad
        self._fecha_creacion = datetime.now()
        logger.debug(f"Entidad creada: {self.__class__.__name__} ID:{id_entidad}")
        
    # Encapsulamiento de datos
    @property
    def id(self):
        return self._id
    
    @property
    def fecha_creacion(self):
        return self._fecha_creacion
    
    @abstractmethod
    def mostrar_info(self):
        pass
    
    @abstractmethod
    def validar(self):
        pass

# CLASE CLIENTE CON VALIDACIONES ROBUSTAS
class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, email, telefono=None):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        logger.info(f"Cliente creado exitosamente: {nombre}")
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        try:
            if not valor:
                raise ValidacionError("El nombre no puede estar vacío", "nombre")
            if not isinstance(valor, str):
                raise ValidacionError("El nombre debe ser texto", "nombre")
            
            valor_limpio = valor.strip()
            if not valor_limpio:
                raise ValidacionError("El nombre no puede ser solo espacios", "nombre")
            
            if not all(c.isalpha() or c.isspace() or c in 'áéíóúÁÉÍÓÚñÑ' for c in valor_limpio):
                raise ValidacionError("El nombre solo puede contener letras y espacios", "nombre")
            
            if len(valor_limpio) < 2:
                raise ValidacionError("El nombre debe tener al menos 2 caracteres", "nombre")
            
            self._nombre = valor_limpio
            
        except ValidacionError:
            raise
        except Exception as e:
            logger.error(f"Error inesperado validando nombre: {e}")
            raise ValidacionError(f"Error validando nombre: {str(e)}", "nombre")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        try:
            if not valor:
                raise ValidacionError("El email no puede estar vacío", "email")
            
            valor = valor.strip().lower()
            
            if '@' not in valor:
                raise ValidacionError("El email debe contener @", "email")
            
            partes = valor.split('@')
            if len(partes) != 2:
                raise ValidacionError("Formato de email inválido", "email")
            
            nombre, dominio = partes
            
            if not nombre or not dominio:
                raise ValidacionError("Email incompleto", "email")
            
            if '.' not in dominio:
                raise ValidacionError("El dominio debe contener un punto", "email")
            
            if len(valor) > 100:
                raise ValidacionError("Email demasiado largo", "email")
            
            self._email = valor
            
        except ValidacionError:
            raise
        except Exception as e:
            logger.error(f"Error inesperado validando email: {e}")
            raise ValidacionError(f"Error validando email: {str(e)}", "email")
    
    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            self._telefono = None
            return
        
        try:
            valor_str = str(valor).strip()
            if not valor_str.isdigit():
                raise ValidacionError("El teléfono solo debe contener números", "telefono")
            if len(valor_str) < 7:
                raise ValidacionError("El teléfono debe tener al menos 7 dígitos", "telefono")
            self._telefono = valor_str
        except ValidacionError:
            raise
        except Exception as e:
            logger.error(f"Error validando teléfono: {e}")
            raise ValidacionError(f"Error validando teléfono: {str(e)}", "telefono")
    
    def mostrar_info(self):
        info = f"Cliente ID:{self._id} - Nombre: {self._nombre} - Email: {self._email}"
        if self._telefono:
            info += f" - Tel: {self._telefono}"
        return info
    
    def validar(self):
        try:
            if not self._nombre:
                raise ValidacionError("Cliente sin nombre", "nombre")
            if not self._email:
                raise ValidacionError("Cliente sin email", "email")
            return True
        except Exception as e:
            logger.error(f"Validación de cliente fallida: {e}")
            return False
    
    def __str__(self):
        return self.mostrar_info()

# CLASE ABSTRACTA SERVICIO
class Servicio(ABC):
    def __init__(self, nombre, precio_base, disponible=True):
        try:
            if not nombre:
                raise ServicioError("El servicio debe tener un nombre")
            if precio_base <= 0:
                raise ServicioError("El precio base debe ser positivo")
            
            self._nombre = nombre
            self._precio_base = precio_base
            self._disponible = disponible
            self._fecha_creacion = datetime.now()
            logger.debug(f"Servicio creado: {nombre}")
            
        except ServicioError:
            raise
        except Exception as e:
            logger.error(f"Error creando servicio: {e}")
            raise ServicioError(f"Error al crear servicio: {str(e)}")
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def precio_base(self):
        return self._precio_base
    
    @property
    def disponible(self):
        return self._disponible
    
    @disponible.setter
    def disponible(self, valor):
        self._disponible = valor
        logger.info(f"Servicio '{self._nombre}' disponible: {valor}")
    
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def descripcion(self):
        pass
    
    @abstractmethod
    def validar_parametros(self, *args, **kwargs):
        pass

# SERVICIOS ESPECIALIZADOS
class ReservaSala(Servicio):
    def __init__(self, nombre_sala, capacidad, precio_base=50):
        super().__init__(f"Sala {nombre_sala}", precio_base)
        self._capacidad = capacidad
        self._tipo_sala = "estándar"
    
    @property
    def capacidad(self):
        return self._capacidad
    
    def calcular_costo(self, horas, descuento=0, incluye_equipo=False):
        try:
            self.validar_parametros(horas, descuento, incluye_equipo)
            
            if not self._disponible:
                raise ServicioError(f"La sala '{self._nombre}' no está disponible")
            
            costo = self._precio_base * horas
            
            if descuento > 0:
                costo *= (1 - descuento)
            
            if incluye_equipo:
                costo += 25 * horas
            
            costo_con_impuesto = costo * 1.16
            
            logger.info(f"Costo calculado para {self._nombre}: ${costo_con_impuesto:.2f}")
            return round(costo_con_impuesto, 2)
            
        except ServicioError:
            raise
        except Exception as e:
            logger.error(f"Error calculando costo de sala: {e}")
            raise ServicioError(f"Error en cálculo de costo: {str(e)}")
    
    def calcular_costo_paquete(self, horas, num_personas):
        try:
            costo_base = self.calcular_costo(horas)
            if num_personas > self._capacidad * 0.8:
                return costo_base * 0.9
            return costo_base
        except Exception as e:
            logger.error(f"Error en cálculo de paquete: {e}")
            raise
    
    def descripcion(self):
        return (f"Reserva de {self._nombre} - Capacidad: {self._capacidad} personas - "
                f"Precio base: ${self._precio_base}/hora")
    
    def validar_parametros(self, horas, descuento=0, incluye_equipo=False):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioError("Las horas deben ser un número positivo")
        if horas > 24:
            raise ServicioError("No se puede reservar por más de 24 horas")
        if not isinstance(descuento, (int, float)) or descuento < 0 or descuento > 0.5:
            raise ServicioError("El descuento debe estar entre 0 y 0.5 (50%)")
        if not isinstance(incluye_equipo, bool):
            raise ServicioError("incluye_equipo debe ser booleano")

class AlquilerEquipo(Servicio):
    def __init__(self, tipo_equipo, marca, precio_base=30):
        super().__init__(f"Equipo {tipo_equipo}", precio_base)
        self._tipo_equipo = tipo_equipo
        self._marca = marca
    
    def calcular_costo(self, dias, seguro=False, cantidad=1):
        try:
            self.validar_parametros(dias, seguro, cantidad)
            
            if not self._disponible:
                raise ServicioError(f"El equipo '{self._nombre}' no está disponible")
            
            costo = self._precio_base * dias * cantidad
            
            if cantidad > 5:
                costo *= 0.85
            
            if seguro:
                costo += 20 * dias * cantidad
            
            costo_con_impuesto = costo * 1.19
            
            logger.info(f"Costo equipo calculado: ${costo_con_impuesto:.2f}")
            return round(costo_con_impuesto, 2)
            
        except ServicioError:
            raise
        except Exception as e:
            logger.error(f"Error calculando costo de equipo: {e}")
            raise ServicioError(f"Error en cálculo: {str(e)}")
    
    def descripcion(self):
        return f"Alquiler de {self._tipo_equipo} {self._marca} - ${self._precio_base}/día"
    
    def validar_parametros(self, dias, seguro=False, cantidad=1):
        if not isinstance(dias, int) or dias <= 0:
            raise ServicioError("Los días deben ser un número entero positivo")
        if dias > 30:
            raise ServicioError("Máximo 30 días de alquiler")
        if not isinstance(seguro, bool):
            raise ServicioError("seguro debe ser booleano")
        if not isinstance(cantidad, int) or cantidad < 1:
            raise ServicioError("La cantidad debe ser un entero positivo")

class Asesoria(Servicio):
    def __init__(self, especialidad, consultor, precio_base=100):
        super().__init__(f"Asesoría {especialidad}", precio_base)
        self._especialidad = especialidad
        self._consultor = consultor
        self._niveles = {"básico": 1, "intermedio": 1.3, "avanzado": 1.6, "especializado": 2.0}
    
    def calcular_costo(self, horas, nivel="básico", urgente=False):
        try:
            self.validar_parametros(horas, nivel, urgente)
            
            if not self._disponible:
                raise ServicioError(f"La asesoría '{self._nombre}' no está disponible")
            
            multiplicador = self._niveles.get(nivel, 1)
            costo = self._precio_base * horas * multiplicador
            
            if urgente:
                costo *= 1.5
            
            costo_final = costo * 1.10
            
            logger.info(f"Costo asesoría calculado: ${costo_final:.2f}")
            return round(costo_final, 2)
            
        except ServicioError:
            raise
        except Exception as e:
            logger.error(f"Error en cálculo de asesoría: {e}")
            raise ServicioError(f"Error en cálculo: {str(e)}")
    
    def descripcion(self):
        return (f"Asesoría en {self._especialidad} - Consultor: {self._consultor} - "
                f"${self._precio_base}/hora")
    
    def validar_parametros(self, horas, nivel="básico", urgente=False):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioError("Las horas deben ser un número positivo")
        if horas < 0.5:
            raise ServicioError("Mínimo 30 minutos de asesoría")
        if nivel not in self._niveles:
            raise ServicioError(f"Nivel inválido. Opciones: {list(self._niveles.keys())}")
        if not isinstance(urgente, bool):
            raise ServicioError("urgente debe ser booleano")

# CLASE RESERVA
class Reserva:
    ESTADOS_VALIDOS = ["pendiente", "confirmada", "en_proceso", "completada", "cancelada"]
    
    def __init__(self, cliente, servicio, duracion, parametros_adicionales=None):
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaError("Cliente inválido")
            if not isinstance(servicio, Servicio):
                raise ReservaError("Servicio inválido")
            if not cliente.validar():
                raise ReservaError("El cliente no es válido")
            
            self._cliente = cliente
            self._servicio = servicio
            self._duracion = duracion
            self._parametros = parametros_adicionales or {}
            self._estado = "pendiente"
            self._fecha_reserva = datetime.now()
            self._costo_total = None
            
            logger.info(f"Reserva creada: Cliente={cliente.nombre}, Servicio={servicio.nombre}")
            
        except ReservaError:
            raise
        except Exception as e:
            logger.error(f"Error creando reserva: {e}")
            raise ReservaError(f"Error al crear reserva: {str(e)}")
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def servicio(self):
        return self._servicio
    
    @property
    def costo_total(self):
        return self._costo_total
    
    def confirmar(self):
        try:
            logger.info(f"Intentando confirmar reserva para {self._cliente.nombre}")
            
            if self._estado == "confirmada":
                raise OperacionNoPermitidaError("La reserva ya está confirmada")
            if self._estado == "cancelada":
                raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada")
            if self._estado == "completada":
                raise OperacionNoPermitidaError("La reserva ya fue completada")
            
            if not self._servicio.disponible:
                raise ReservaError("El servicio no está disponible")
            
            self._costo_total = self._servicio.calcular_costo(
                self._duracion, **self._parametros
            )
            
        except (OperacionNoPermitidaError, ReservaError) as e:
            logger.error(f"Error al confirmar: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al confirmar: {e}")
            raise ReservaError("Error inesperado durante la confirmación") from e
        else:
            self._estado = "confirmada"
            logger.info(f"Reserva confirmada exitosamente. Costo: ${self._costo_total}")
            return True
        finally:
            logger.info(f"Proceso de confirmación finalizado. Estado: {self._estado}")
    
    def cancelar(self, motivo=None):
        try:
            if self._estado == "completada":
                raise OperacionNoPermitidaError("No se puede cancelar una reserva completada")
            
            estado_anterior = self._estado
            self._estado = "cancelada"
            
            if motivo:
                logger.info(f"Reserva cancelada. Motivo: {motivo}")
            else:
                logger.info("Reserva cancelada sin motivo especificado")
                
            return True
            
        except OperacionNoPermitidaError:
            raise
        except Exception as e:
            logger.error(f"Error cancelando reserva: {e}")
            self._estado = estado_anterior
            raise ReservaError("Error al cancelar la reserva") from e
    
    # Uso de try, except, else, finally
    def procesar_pago(self, metodo_pago="efectivo"):
        try:
            if self._estado != "confirmada":
                raise OperacionNoPermitidaError("La reserva debe estar confirmada para procesar el pago")
            
            if self._costo_total is None:
                self._costo_total = self._servicio.calcular_costo(
                    self._duracion, **self._parametros
                )
            
            logger.info(f"Procesando pago por ${self._costo_total:.2f} - Método: {metodo_pago}")
            
            self._estado = "completada"
            
        except OperacionNoPermitidaError:
            raise
        except Exception as e:
            logger.error(f"Error procesando pago: {e}")
            raise ReservaError("Error al procesar el pago") from e
        else:
            logger.info(f"Pago procesado exitosamente: ${self._costo_total:.2f}")
            return self._costo_total
        finally:
            logger.info("Proceso de pago finalizado")
    
    def mostrar_info(self):
        info = (f"Reserva - Cliente: {self._cliente.nombre}\n"
                f"Servicio: {self._servicio.descripcion()}\n"
                f"Duración: {self._duracion}\n"
                f"Estado: {self._estado}\n"
                f"Fecha: {self._fecha_reserva}")
        if self._costo_total:
            info += f"\nCosto Total: ${self._costo_total:.2f}"
        return info

# SISTEMA PRINCIPAL - Uso de Listas
class SistemaFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._total_operaciones = 0
        self._operaciones_exitosas = 0
        self._operaciones_fallidas = 0
        logger.info("Sistema Software FJ inicializado")
    
    @property
    def clientes(self):
        return self._clientes.copy()
    
    @property
    def servicios(self):
        return self._servicios.copy()
    
    @property
    def reservas(self):
        return self._reservas.copy()
    
    def agregar_cliente(self, cliente):
        try:
            if not isinstance(cliente, Cliente):
                raise ClienteError("El objeto no es un cliente válido")
            
            if any(c.id == cliente.id for c in self._clientes):
                raise ClienteError(f"Ya existe un cliente con ID {cliente.id}")
            
            self._clientes.append(cliente)
            self._total_operaciones += 1
            self._operaciones_exitosas += 1
            logger.info(f"Cliente agregado al sistema: {cliente.nombre}")
            return True
            
        except ClienteError:
            self._total_operaciones += 1
            self._operaciones_fallidas += 1
            raise
        except Exception as e:
            self._total_operaciones += 1
            self._operaciones_fallidas += 1
            logger.error(f"Error al agregar cliente: {e}")
            raise SistemaFJException(f"Error de sistema: {str(e)}")
    
    def agregar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise ServicioError("El objeto no es un servicio válido")
            
            self._servicios.append(servicio)
            self._total_operaciones += 1
            self._operaciones_exitosas += 1
            logger.info(f"Servicio agregado: {servicio.nombre}")
            return True
            
        except ServicioError:
            self._total_operaciones += 1
            self._operaciones_fallidas += 1
            raise
        except Exception as e:
            self._total_operaciones += 1
            self._operaciones_fallidas += 1
            logger.error(f"Error al agregar servicio: {e}")
            raise SistemaFJException(f"Error de sistema: {str(e)}")
    
    def crear_reserva(self, cliente, servicio, duracion, **parametros):
        try:
            if cliente not in self._clientes:
                raise ReservaError("El cliente no está registrado en el sistema")
            
            if servicio not in self._servicios:
                raise ReservaError("El servicio no está disponible en el sistema")
            
            reserva = Reserva(cliente, servicio, duracion, parametros)
            self._reservas.append(reserva)
            self._total_operaciones += 1
            self._operaciones_exitosas += 1
            
            return reserva
            
        except ReservaError:
            self._total_operaciones += 1
            self._operaciones_fallidas += 1
            raise
        except Exception as e:
            self._total_operaciones += 1
            self._operaciones_fallidas += 1
            logger.error(f"Error al crear reserva: {e}")
            raise SistemaFJException(f"Error de sistema: {str(e)}")
    
    def obtener_estadisticas(self):
        return {
            "total_clientes": len(self._clientes),
            "total_servicios": len(self._servicios),
            "total_reservas": len(self._reservas),
            "total_operaciones": self._total_operaciones,
            "operaciones_exitosas": self._operaciones_exitosas,
            "operaciones_fallidas": self._operaciones_fallidas,
            "tasa_exito": (self._operaciones_exitosas / self._total_operaciones * 100 
                          if self._total_operaciones > 0 else 0)
        }

# INTERFAZ GRÁFICA CON TKINTER
class AplicacionGUI:
    def __init__(self, root):
        self.root = root
        self.sistema = SistemaFJ()
        self.setup_ui()
        self.inicializar_datos_ejemplo()
    
    def setup_ui(self):
        # Configuración de la ventana principal
        self.root.title("Software FJ - Sistema de Gestión")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1e1e1e')
        
        # Configurar tema oscuro
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del tema oscuro
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        select_color = '#404040'
        accent_color = '#007acc'
        entry_bg = '#2d2d2d'
        button_bg = '#3c3c3c'
        
        # Configurar estilos de widgets
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#2d2d2d', 
                       foreground=fg_color, 
                       padding=[10, 5],
                       borderwidth=0)
        style.map('TNotebook.Tab', 
                 background=[('selected', '#3c3c3c')], 
                 foreground=[('selected', accent_color)])
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe', background=bg_color, foreground=fg_color, borderwidth=1)
        style.configure('TLabelframe.Label', background=bg_color, foreground=accent_color, 
                       font=('Arial', 10, 'bold'))
        
        style.configure('TButton', 
                       background=button_bg, 
                       foreground=fg_color, 
                       borderwidth=1,
                       padding=[10, 5],
                       relief='flat')
        style.map('TButton', 
                 background=[('active', accent_color), ('pressed', '#005a9e')],
                 foreground=[('active', fg_color)])
        
        style.configure('TEntry', 
                       fieldbackground=entry_bg, 
                       foreground=fg_color, 
                       insertcolor=fg_color,
                       borderwidth=1)
        
        style.configure('TCombobox', 
                       fieldbackground=entry_bg, 
                       background=button_bg,
                       foreground=fg_color, 
                       arrowcolor=fg_color)
        style.map('TCombobox', 
                 fieldbackground=[('readonly', entry_bg)],
                 background=[('readonly', button_bg)])
        
        style.configure('TCheckbutton', 
                       background=bg_color, 
                       foreground=fg_color)
        style.map('TCheckbutton', 
                 background=[('active', bg_color)])
        
        style.configure('TSeparator', background='#404040')
        
        # Estilo
        style.configure('Treeview', 
                       background=entry_bg,
                       foreground=fg_color,
                       fieldbackground=entry_bg,
                       borderwidth=0)
        style.configure('Treeview.Heading', 
                       background='#3c3c3c',
                       foreground=fg_color,
                       relief='flat',
                       font=('Arial', 9, 'bold'))
        style.map('Treeview', 
                 background=[('selected', accent_color)],
                 foreground=[('selected', fg_color)])
        style.map('Treeview.Heading',
                 background=[('active', '#4a4a4a')])
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_servicios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_log = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_clientes, text="👥 Clientes")
        self.notebook.add(self.tab_servicios, text="🔧 Servicios")
        self.notebook.add(self.tab_reservas, text="📅 Reservas")
        self.notebook.add(self.tab_log, text="📋 Log del Sistema")
        
        # Configurar cada pestaña
        self.setup_tab_clientes()
        self.setup_tab_servicios()
        self.setup_tab_reservas()
        self.setup_tab_log()
        
        # Barra de estado
        self.status_bar = ttk.Label(self.root, text="Sistema iniciado correctamente", 
                                   relief='flat',
                                   anchor='w',
                                   background='#007acc',
                                   foreground='#ffffff',
                                   padding=(10, 5))
        self.status_bar.pack(side='bottom', fill='x')
    
    def setup_tab_clientes(self):
        main_frame = ttk.Frame(self.tab_clientes, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        left_frame = ttk.LabelFrame(main_frame, text="Registrar Cliente", padding="10")
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        ttk.Label(left_frame, text="ID Cliente:").grid(row=0, column=0, sticky='w', pady=5)
        self.cliente_id_var = StringVar()
        ttk.Entry(left_frame, textvariable=self.cliente_id_var).grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Nombre:").grid(row=1, column=0, sticky='w', pady=5)
        self.cliente_nombre_var = StringVar()
        ttk.Entry(left_frame, textvariable=self.cliente_nombre_var, width=30).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        self.cliente_email_var = StringVar()
        ttk.Entry(left_frame, textvariable=self.cliente_email_var, width=30).grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Teléfono:").grid(row=3, column=0, sticky='w', pady=5)
        self.cliente_telefono_var = StringVar()
        ttk.Entry(left_frame, textvariable=self.cliente_telefono_var).grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Button(left_frame, text="Registrar Cliente", 
                  command=self.registrar_cliente).grid(row=4, column=0, columnspan=2, pady=20)
        
        right_frame = ttk.LabelFrame(main_frame, text="Clientes Registrados", padding="10")
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        columns = ('ID', 'Nombre', 'Email', 'Teléfono')
        self.tree_clientes = ttk.Treeview(right_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_clientes.heading(col, text=col)
        
        self.tree_clientes.column('ID', width=50)
        self.tree_clientes.column('Nombre', width=150)
        self.tree_clientes.column('Email', width=150)
        self.tree_clientes.column('Teléfono', width=100)
        
        self.tree_clientes.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree_clientes.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
    
    def setup_tab_servicios(self):
        main_frame = ttk.Frame(self.tab_servicios, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        servicios_frame = ttk.LabelFrame(main_frame, text="Agregar Servicios", padding="10")
        servicios_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Servicio de Sala
        sala_frame = ttk.Frame(servicios_frame, padding="5")
        sala_frame.pack(fill='x', pady=5)
        ttk.Label(sala_frame, text="🏢 Sala de Reuniones", font=('Arial', 10, 'bold'), 
                 foreground='#007acc').pack(anchor='w')
        ttk.Label(sala_frame, text="Nombre:").pack(anchor='w')
        self.sala_nombre_var = StringVar(value="Principal")
        ttk.Entry(sala_frame, textvariable=self.sala_nombre_var).pack(fill='x', pady=2)
        ttk.Label(sala_frame, text="Capacidad:").pack(anchor='w')
        self.sala_capacidad_var = StringVar(value="20")
        ttk.Entry(sala_frame, textvariable=self.sala_capacidad_var).pack(fill='x', pady=2)
        ttk.Label(sala_frame, text="Precio/hora:").pack(anchor='w')
        self.sala_precio_var = StringVar(value="50")
        ttk.Entry(sala_frame, textvariable=self.sala_precio_var).pack(fill='x', pady=2)
        ttk.Button(sala_frame, text="Agregar Sala", 
                  command=self.agregar_sala).pack(pady=10)
        
        ttk.Separator(servicios_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Servicio de Equipo
        equipo_frame = ttk.Frame(servicios_frame, padding="5")
        equipo_frame.pack(fill='x', pady=5)
        ttk.Label(equipo_frame, text="💻 Alquiler de Equipo", font=('Arial', 10, 'bold'),
                 foreground='#007acc').pack(anchor='w')
        ttk.Label(equipo_frame, text="Tipo:").pack(anchor='w')
        self.equipo_tipo_var = StringVar(value="Laptop")
        ttk.Entry(equipo_frame, textvariable=self.equipo_tipo_var).pack(fill='x', pady=2)
        ttk.Label(equipo_frame, text="Marca:").pack(anchor='w')
        self.equipo_marca_var = StringVar(value="Dell")
        ttk.Entry(equipo_frame, textvariable=self.equipo_marca_var).pack(fill='x', pady=2)
        ttk.Label(equipo_frame, text="Precio/día:").pack(anchor='w')
        self.equipo_precio_var = StringVar(value="30")
        ttk.Entry(equipo_frame, textvariable=self.equipo_precio_var).pack(fill='x', pady=2)
        ttk.Button(equipo_frame, text="Agregar Equipo", 
                  command=self.agregar_equipo).pack(pady=10)
        
        ttk.Separator(servicios_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Servicio de Asesoría
        asesoria_frame = ttk.Frame(servicios_frame, padding="5")
        asesoria_frame.pack(fill='x', pady=5)
        ttk.Label(asesoria_frame, text="🎓 Asesoría", font=('Arial', 10, 'bold'),
                 foreground='#007acc').pack(anchor='w')
        ttk.Label(asesoria_frame, text="Especialidad:").pack(anchor='w')
        self.asesoria_esp_var = StringVar(value="Tecnología")
        ttk.Entry(asesoria_frame, textvariable=self.asesoria_esp_var).pack(fill='x', pady=2)
        ttk.Label(asesoria_frame, text="Consultor:").pack(anchor='w')
        self.asesoria_consultor_var = StringVar(value="Ing. García")
        ttk.Entry(asesoria_frame, textvariable=self.asesoria_consultor_var).pack(fill='x', pady=2)
        ttk.Label(asesoria_frame, text="Precio/hora:").pack(anchor='w')
        self.asesoria_precio_var = StringVar(value="100")
        ttk.Entry(asesoria_frame, textvariable=self.asesoria_precio_var).pack(fill='x', pady=2)
        ttk.Button(asesoria_frame, text="Agregar Asesoría", 
                  command=self.agregar_asesoria).pack(pady=10)
        
        # Panel derecho - Servicios disponibles
        right_frame = ttk.LabelFrame(main_frame, text="Servicios Disponibles", padding="10")
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        self.lista_servicios = tk.Listbox(right_frame, height=15, width=40,
                                        bg='#2d2d2d',
                                        fg='#ffffff',
                                        selectbackground='#007acc',
                                        selectforeground='#ffffff',
                                        relief='flat',
                                        borderwidth=0)
        self.lista_servicios.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.lista_servicios.yview)
        scrollbar.pack(side='right', fill='y')
        self.lista_servicios.configure(yscrollcommand=scrollbar.set)
    
    def setup_tab_reservas(self):
        main_frame = ttk.Frame(self.tab_reservas, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        left_frame = ttk.LabelFrame(main_frame, text="Crear Reserva", padding="10")
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        ttk.Label(left_frame, text="Cliente:").grid(row=0, column=0, sticky='w', pady=5)
        self.reserva_cliente_var = StringVar()
        self.combo_clientes = ttk.Combobox(left_frame, textvariable=self.reserva_cliente_var, state='readonly')
        self.combo_clientes.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Servicio:").grid(row=1, column=0, sticky='w', pady=5)
        self.reserva_servicio_var = StringVar()
        self.combo_servicios = ttk.Combobox(left_frame, textvariable=self.reserva_servicio_var, state='readonly')
        self.combo_servicios.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Duración:").grid(row=2, column=0, sticky='w', pady=5)
        self.reserva_duracion_var = StringVar()
        ttk.Entry(left_frame, textvariable=self.reserva_duracion_var).grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Parámetros adicionales:").grid(row=3, column=0, sticky='w', pady=5)
        self.parametros_frame = ttk.Frame(left_frame)
        self.parametros_frame.grid(row=3, column=1, pady=5, padx=5)
        
        self.seguro_var = BooleanVar()
        ttk.Checkbutton(self.parametros_frame, text="Seguro", variable=self.seguro_var).pack(anchor='w')
        
        self.equipo_var = BooleanVar()
        ttk.Checkbutton(self.parametros_frame, text="Incluye equipo", variable=self.equipo_var).pack(anchor='w')
        
        self.urgente_var = BooleanVar()
        ttk.Checkbutton(self.parametros_frame, text="Urgente", variable=self.urgente_var).pack(anchor='w')
        
        ttk.Button(left_frame, text="Crear Reserva", 
                  command=self.crear_reserva).grid(row=4, column=0, columnspan=2, pady=20)
        
        right_frame = ttk.LabelFrame(main_frame, text="Reservas Realizadas", padding="10")
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        columns = ('Cliente', 'Servicio', 'Duración', 'Estado', 'Costo')
        self.tree_reservas = ttk.Treeview(right_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=100)
        
        self.tree_reservas.pack(fill='both', expand=True)
        
        acciones_frame = ttk.Frame(right_frame)
        acciones_frame.pack(fill='x', pady=10)
        
        ttk.Button(acciones_frame, text="Confirmar", 
                  command=self.confirmar_reserva).pack(side='left', padx=5)
        ttk.Button(acciones_frame, text="Procesar Pago", 
                  command=self.procesar_pago).pack(side='left', padx=5)
        ttk.Button(acciones_frame, text="Cancelar", 
                  command=self.cancelar_reserva).pack(side='left', padx=5)
    
    def setup_tab_log(self):
        main_frame = ttk.Frame(self.tab_log, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Registro de Actividades del Sistema", 
                 font=('Arial', 12, 'bold'),
                 foreground='#007acc').pack(pady=10)
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=20, width=80,
                                                bg='#2d2d2d',
                                                fg='#d4d4d4',
                                                insertbackground='#ffffff',
                                                relief='flat',
                                                borderwidth=0)
        self.log_text.pack(fill='both', expand=True, pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Actualizar Log", 
                  command=self.actualizar_log).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar Log", 
                  command=self.limpiar_log).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Mostrar Estadísticas", 
                  command=self.mostrar_estadisticas).pack(side='left', padx=5)
    
    def inicializar_datos_ejemplo(self):
        """Inicializa 10+ operaciones de ejemplo en el sistema"""
        try:
            logger.info("=== INICIANDO CARGA DE DATOS DE EJEMPLO (14 OPERACIONES) ===")
            
            # Operación 1: Agregar servicio de sala
            sala = ReservaSala("Principal", 20, 50)
            self.sistema.agregar_servicio(sala)
            
            # Operación 2: Agregar servicio de equipo
            equipo = AlquilerEquipo("Laptop", "Dell", 30)
            self.sistema.agregar_servicio(equipo)
            
            # Operación 3: Agregar servicio de asesoría
            asesoria = Asesoria("Tecnología", "Ing. García", 100)
            self.sistema.agregar_servicio(asesoria)
            
            # Operación 4: Agregar cliente válido 1
            cliente1 = Cliente(1, "Dan Pérez", "dan@email.com", "3011234567")
            self.sistema.agregar_cliente(cliente1)
            
            # Operación 5: Intentar agregar cliente con email inválido (FALLIDA)
            try:
                cliente_invalido = Cliente(2, "Vanessa López", "email_invalido")
                self.sistema.agregar_cliente(cliente_invalido)
            except ValidacionError as e:
                logger.info(f"Operación fallida controlada: {e}")
            
            # Operación 6: Agregar cliente válido 2
            cliente2 = Cliente(3, "Adri García", "adri@email.com", "3109876543")
            self.sistema.agregar_cliente(cliente2)
            
            # Operación 7: Crear reserva exitosa
            reserva1 = self.sistema.crear_reserva(cliente1, sala, 4)
            
            # Operación 8: Crear reserva de alquiler
            reserva2 = self.sistema.crear_reserva(cliente2, equipo, 5, seguro=True)
            
            # Operación 9: Confirmar reserva
            if reserva1:
                reserva1.confirmar()
            
            # Operación 10: Procesar pago
            if reserva1:
                reserva1.procesar_pago("tarjeta")
            
            # Operación 11: Intentar cancelar reserva ya completada (FALLIDA)
            try:
                if reserva1:
                    reserva1.cancelar("Ya no se necesita")
            except OperacionNoPermitidaError as e:
                logger.info(f"Operación fallida controlada: {e}")
            
            # Operación 12: Confirmar segunda reserva
            if reserva2:
                reserva2.confirmar()
            
            # Operación 13: Cancelar segunda reserva
            if reserva2:
                reserva2.cancelar("Cambio de planes")
            
            # Operación 14: Agregar servicio adicional
            sala_vip = ReservaSala("VIP", 10, 100)
            self.sistema.agregar_servicio(sala_vip)
            
            logger.info("=== CARGA DE DATOS COMPLETADA ===")
            
            self.actualizar_listas()
            self.actualizar_log()
            self.actualizar_status(f"Sistema listo - {self.sistema._total_operaciones} operaciones realizadas")
            
        except Exception as e:
            logger.error(f"Error inicializando datos: {e}")
            messagebox.showerror("Error", f"Error al inicializar datos: {e}")
    
    def actualizar_listas(self):
        """Actualiza todas las listas y combos de la interfaz"""
        self.lista_servicios.delete(0, tk.END)
        for servicio in self.sistema.servicios:
            self.lista_servicios.insert(tk.END, servicio.descripcion())
        
        clientes_nombres = [f"{c.id} - {c.nombre}" for c in self.sistema.clientes]
        self.combo_clientes['values'] = clientes_nombres
        
        servicios_nombres = [f"{s.nombre}" for s in self.sistema.servicios]
        self.combo_servicios['values'] = servicios_nombres
        
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        for cliente in self.sistema.clientes:
            self.tree_clientes.insert('', 'end', values=(
                cliente.id, cliente.nombre, cliente.email, 
                cliente.telefono if cliente.telefono else "N/A"
            ))
        
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        
        for reserva in self.sistema.reservas:
            self.tree_reservas.insert('', 'end', values=(
                reserva.cliente.nombre,
                reserva.servicio.nombre,
                reserva._duracion,
                reserva.estado,
                f"${reserva.costo_total:.2f}" if reserva.costo_total else "N/A"
            ))
    
    def actualizar_log(self):
        """Actualiza el visor de logs"""
        try:
            log_file = f"logs/software_fj_{datetime.now().strftime('%Y%m%d')}.log"
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(1.0, contenido[-5000:])
                self.log_text.see(tk.END)
        except Exception as e:
            self.log_text.insert(tk.END, f"Error al leer log: {e}\n")
    
    def limpiar_log(self):
        """Limpia el visor de logs"""
        self.log_text.delete(1.0, tk.END)
    
    def actualizar_status(self, mensaje):
        """Actualiza la barra de estado"""
        self.status_bar.config(text=mensaje)
    
    def registrar_cliente(self):
        """Registra un nuevo cliente desde el formulario"""
        try:
            id_cliente = self.cliente_id_var.get()
            nombre = self.cliente_nombre_var.get()
            email = self.cliente_email_var.get()
            telefono = self.cliente_telefono_var.get() or None
            
            if not id_cliente:
                raise ValidacionError("El ID del cliente es obligatorio")
            
            cliente = Cliente(int(id_cliente), nombre, email, telefono)
            self.sistema.agregar_cliente(cliente)
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente")
            self.actualizar_status(f"Cliente {nombre} registrado - {self.sistema._total_operaciones} ops totales")
            
            self.cliente_id_var.set("")
            self.cliente_nombre_var.set("")
            self.cliente_email_var.set("")
            self.cliente_telefono_var.set("")
            
        except ValidacionError as e:
            messagebox.showerror("Error de Validación", str(e))
            self.actualizar_status(f"Error: {e}")
            self.actualizar_log()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {e}")
            self.actualizar_status(f"Error inesperado")
            self.actualizar_log()
    
    def agregar_sala(self):
        try:
            nombre = self.sala_nombre_var.get()
            capacidad = int(self.sala_capacidad_var.get())
            precio = float(self.sala_precio_var.get())
            
            sala = ReservaSala(nombre, capacidad, precio)
            self.sistema.agregar_servicio(sala)
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Sala {nombre} agregada correctamente")
            self.actualizar_status(f"Sala {nombre} agregada - {self.sistema._total_operaciones} ops totales")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar sala: {e}")
            self.actualizar_log()
    
    def agregar_equipo(self):
        try:
            tipo = self.equipo_tipo_var.get()
            marca = self.equipo_marca_var.get()
            precio = float(self.equipo_precio_var.get())
            
            equipo = AlquilerEquipo(tipo, marca, precio)
            self.sistema.agregar_servicio(equipo)
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Equipo {tipo} agregado correctamente")
            self.actualizar_status(f"Equipo {tipo} agregado - {self.sistema._total_operaciones} ops totales")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar equipo: {e}")
            self.actualizar_log()
    
    def agregar_asesoria(self):
        try:
            especialidad = self.asesoria_esp_var.get()
            consultor = self.asesoria_consultor_var.get()
            precio = float(self.asesoria_precio_var.get())
            
            asesoria = Asesoria(especialidad, consultor, precio)
            self.sistema.agregar_servicio(asesoria)
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Asesoría en {especialidad} agregada correctamente")
            self.actualizar_status(f"Asesoría en {especialidad} agregada - {self.sistema._total_operaciones} ops totales")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar asesoría: {e}")
            self.actualizar_log()
    
    def crear_reserva(self):
        try:
            cliente_seleccion = self.reserva_cliente_var.get()
            if not cliente_seleccion:
                raise ValidacionError("Seleccione un cliente")
            
            cliente_id = int(cliente_seleccion.split(' - ')[0])
            cliente = next((c for c in self.sistema.clientes if c.id == cliente_id), None)
            
            if not cliente:
                raise ValidacionError("Cliente no encontrado")
            
            servicio_nombre = self.reserva_servicio_var.get()
            if not servicio_nombre:
                raise ValidacionError("Seleccione un servicio")
            
            servicio = next((s for s in self.sistema.servicios if s.nombre == servicio_nombre), None)
            
            if not servicio:
                raise ValidacionError("Servicio no encontrado")
            
            duracion = float(self.reserva_duracion_var.get())
            
            parametros = {}
            if self.seguro_var.get():
                parametros['seguro'] = True
            if self.equipo_var.get():
                parametros['incluye_equipo'] = True
            if self.urgente_var.get():
                parametros['urgente'] = True
            
            reserva = self.sistema.crear_reserva(cliente, servicio, duracion, **parametros)
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Reserva creada correctamente\n{reserva.mostrar_info()}")
            self.actualizar_status(f"Reserva creada para {cliente.nombre} - {self.sistema._total_operaciones} ops")
            
        except ValidacionError as e:
            messagebox.showerror("Error de Validación", str(e))
            self.actualizar_log()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva: {e}")
            self.actualizar_log()
    
    def confirmar_reserva(self):
        try:
            seleccion = self.tree_reservas.selection()
            if not seleccion:
                raise ValidacionError("Seleccione una reserva")
            
            index = self.tree_reservas.index(seleccion[0])
            reserva = self.sistema.reservas[index]
            
            reserva.confirmar()
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Reserva confirmada\nCosto: ${reserva.costo_total:.2f}")
            self.actualizar_status(f"Reserva confirmada - Costo: ${reserva.costo_total:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al confirmar: {e}")
            self.actualizar_log()
    
    def procesar_pago(self):
        try:
            seleccion = self.tree_reservas.selection()
            if not seleccion:
                raise ValidacionError("Seleccione una reserva")
            
            index = self.tree_reservas.index(seleccion[0])
            reserva = self.sistema.reservas[index]
            
            costo = reserva.procesar_pago("tarjeta")
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", f"Pago procesado: ${costo:.2f}")
            self.actualizar_status(f"Pago procesado: ${costo:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar pago: {e}")
            self.actualizar_log()
    
    def cancelar_reserva(self):
        try:
            seleccion = self.tree_reservas.selection()
            if not seleccion:
                raise ValidacionError("Seleccione una reserva")
            
            index = self.tree_reservas.index(seleccion[0])
            reserva = self.sistema.reservas[index]
            
            reserva.cancelar("Cancelado por usuario")
            
            self.actualizar_listas()
            self.actualizar_log()
            
            messagebox.showinfo("Éxito", "Reserva cancelada")
            self.actualizar_status("Reserva cancelada")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cancelar: {e}")
            self.actualizar_log()
    
    def mostrar_estadisticas(self):
        try:
            stats = self.sistema.obtener_estadisticas()
            mensaje = f"""
╔══════════════════════════════════════╗
║     ESTADÍSTICAS DEL SISTEMA        ║
╠══════════════════════════════════════╣
║ Clientes registrados:  {stats['total_clientes']:>11} ║
║ Servicios disponibles: {stats['total_servicios']:>11} ║
║ Reservas realizadas:   {stats['total_reservas']:>11} ║
║ Total operaciones:     {stats['total_operaciones']:>11} ║
║ Operaciones exitosas:  {stats['operaciones_exitosas']:>11} ║
║ Operaciones fallidas:  {stats['operaciones_fallidas']:>11} ║
║ Tasa de éxito:         {stats['tasa_exito']:>9.1f}% ║
╚══════════════════════════════════════╝
            """
            
            self.log_text.insert(tk.END, "\n" + mensaje + "\n")
            self.log_text.see(tk.END)
            self.actualizar_log()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener estadísticas: {e}")

# FUNCIÓN PRINCIPAL
def main():
    try:
        logger.info("="*60)
        logger.info("INICIANDO SISTEMA SOFTWARE FJ CON INTERFAZ")
        logger.info(f"Fecha: {datetime.now()}")
        logger.info("="*60)
        
        root = tk.Tk()
        
        try:
            root.iconbitmap(default='icon.ico')
        except:
            pass
        
        app = AplicacionGUI(root)
        
        def on_closing():
            if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
                logger.info("Aplicación cerrada por el usuario")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Error fatal en la aplicación: {e}")
        messagebox.showerror("Error Fatal", 
                           f"Error irrecuperable: {e}\nRevise los logs para más detalles.")
    finally:
        logger.info("SISTEMA FINALIZADO")

# Inicio
if __name__ == "__main__":
    main()
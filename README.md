# Software FJ - Sistema Integral de Gestión de Reservas

## Descripción del Proyecto

Software FJ es un sistema integral desarrollado en Python utilizando Programación Orientada a Objetos (POO). El proyecto tiene como objetivo gestionar clientes, servicios y reservas para una empresa ficticia llamada **Software FJ**, especializada en:

- Reservas de salas
- Alquiler de equipos
- Asesorías especializadas

El sistema fue diseñado sin utilizar bases de datos, gestionando toda la información mediante objetos, listas internas y archivos de logs para el registro de eventos y errores.

Además, el proyecto implementa manejo avanzado de excepciones para garantizar estabilidad y continuidad operativa aun cuando se presentan errores durante la ejecución.

---

# Características Principales

- Programación Orientada a Objetos (POO)
- Clases abstractas9
- Herencia
- Polimorfismo
- Encapsulación
- Validaciones robustas
- Manejo avanzado de excepciones
- Excepciones personalizadas
- Registro de eventos y errores mediante logs
- Simulación de operaciones válidas e inválidas
- Sistema modular y extensible
- Sin uso de bases de datos
- Interfaz en Tkinter

---

# Estructura del Sistema

El proyecto incluye las siguientes clases principales:

## Clase Abstracta `Entidad`
Representa entidades generales del sistema.

## Clase `Cliente`
Gestiona información de clientes con validaciones estrictas y encapsulación de datos.

## Clase Abstracta `Servicio`
Define la estructura general de los servicios ofrecidos por la empresa.

## Clase `Reserva`
Gestiona:
- Confirmación de reservas
- Cancelación
- Procesamiento de pagos
- Estados de la reserva
- Manejo de excepciones

## Clase `SistemaFJ`
Administra listas internas de:
- Clientes
- Servicios
- Reservas

---

# Manejo de Excepciones

El sistema implementa:

- `try / except`
- `try / except / else`
- `try / except / finally`
- Encadenamiento de excepciones
- Excepciones personalizadas

Errores controlados:
- Datos inválidos
- Emails incorrectos
- Reservas inválidas
- Servicios no disponibles
- Duraciones incorrectas
- Operaciones no permitidas

---

# Archivo de Logs

Todos los eventos y errores se registran automáticamente en Logs
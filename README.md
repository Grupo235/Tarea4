El trabajo debe basarse en una arquitectura orientada a objetos,
incluyendo al menos:
• Una clase abstracta que represente entidades generales del
sistema.
• Una clase Cliente con validaciones robustas y encapsulación de
datos personales.
• Una clase abstracta Servicio y al menos tres servicios
especializados que hereden de ella, implementando polimorfismo y
métodos sobrescritos para calcular costos, describir servicios y
validar parámetros.
• Una clase Reserva que integre cliente, servicio, duración y estado,
e implemente confirmación, cancelación y procesamiento con
manejo de excepciones.
• Métodos sobrecargados (por ejemplo, diferentes variantes del
cálculo de costos con impuestos, descuentos o parámetros
opcionales).
3
• Un archivo de logs donde se registren todos los errores y eventos
relevantes

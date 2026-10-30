from abc import ABC, abstractmethod
import logging

# 1. CONFIGURACIÓN DEL ARCHIVO DE LOGS
logging.basicConfig(
    filename='sistema_gestion.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)

# 2. EXCEPCIONES PERSONALIZADAS
class SoftwareFJException(Exception):
    """Excepción base para todas las anomalías de la empresa Software FJ"""
    pass

class ClienteInvalidoError(SoftwareFJException):
    """Se lanza cuando los datos del cliente violan las validaciones de encapsulado"""
    pass

class ServicioError(SoftwareFJException):
    """Se lanza ante fallos de parámetros o indisponibilidad en los servicios"""
    pass

class ReservaError(SoftwareFJException):
    """Se lanza cuando una regla de negocio del sistema de reservas se rompe"""
    pass


# 3. ARQUITECTURA DE CLASES ORIENTADA A OBJETOS
class EntidadSistema(ABC):
    """Clase abstracta que representa entidades generales del sistema"""
    def __init__(self, identificador: str):
        self._identificador = identificador

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass


class Cliente(EntidadSistema):
    """Clase Cliente con validaciones robustas y encapsulación"""
    def __init__(self, cedula: str, nombre: str, correo: str):
        super().__init__(cedula)
        self.nombre = nombre
        self.correo = correo  # Activa el setter de validación

    @property
    def cedula(self) -> str:
        return self._identificador

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        # Validación estricta del formato de correo electrónico
        if "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Estructura de correo inválida: '{valor}'")
        self._correo = valor

    def obtener_resumen(self) -> str:
        return f"Cliente: {self.nombre} [Cédula: {self.cedula}]"


class Servicio(ABC):
    """Clase abstracta base para los servicios de Software FJ"""
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass


# SERVICIO 1: Reserva de salas con descuento por volumen
class ReservaSala(Servicio):
    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ServicioError("Las horas de reserva de sala deben ser mayores a 0.")
        costo = self.costo_base * horas
        if horas > 5:  # Descuento comercial por exceso de horas
            costo *= 0.90
        return costo

    def describir_servicio(self) -> str:
        return f"Sala de reuniones - Código: {self.codigo}"


# SERVICIO 2: Alquiler de equipos con recargo fijo de mantenimiento
class AlquilerEquipo(Servicio):
    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ServicioError("Las horas de alquiler de equipo deben ser mayores a 0.")
        return (self.costo_base * horas) + 15.0  # Costo base + recargo tecnológico

    def describir_servicio(self) -> str:
        return f"Equipo de cómputo - Código: {self.codigo}"


# SERVICIO 3: Asesoría Especializada con Sobrecarga de Parámetros Opcionales
class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ServicioError("Las horas de asesoría especializada deben ser mayores a 0.")
        return self.costo_base * horas

    # Simulación de Método Sobrecargado usando argumentos opcionales avanzados (Descuentos/Impuestos)
    def calcular_costo_avanzado(self, horas: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        costo_base_calculado = self.calcular_costo(horas)
        costo_con_descuento = costo_base_calculado * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return costo_final

    def describir_servicio(self) -> str:
        return f"Asesoría técnica experta - Código: {self.codigo}"


class Reserva:
    """Clase transaccional que une al Cliente con el Servicio"""
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        if duracion_horas <= 0:
            raise ReservaError("Operación inválida: La duración debe ser mayor a 0 horas.")
        if duracion_horas > 24:
            raise ReservaError("Operación denegada: Las reservas de Software FJ no pueden superar las 24 horas.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "Pendiente"

    def confirmar(self):
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva previamente cancelada.")
        self.estado = "Confirmada"
        logging.info(f"CONFIRMACIÓN EXITOSA -> Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_servicio}")

    def cancelar(self):
        self.estado = "Cancelada"
        logging.info(f"CANCELACIÓN PROCESADA -> Cliente: {self.cliente.nombre}")


# 4. SIMULADOR DE OPERACIONES CON MANEJO AVANZADO DE EXCEPCIONES
def ejecutar_operacion(id_operacion: int, descripcion: str, accion_lambda):
    print(f"--- Operación #{id_operacion}: {descripcion} ---")
    try:
        # Se ejecuta la lógica de la prueba
        resultado = accion_lambda()
    except SoftwareFJException as e:
        # Captura de nuestras excepciones personalizadas
        print(f"[ERROR CONTROLADO] Se capturó un fallo esperado: {e}")
        logging.error(f"Operación #{id_operacion} Falló - Razón: {e}")
    except Exception as e:
        # Encadenamiento preventivo ante errores no previstos del sistema general
        print(f"[CRÍTICO] Error inesperado del sistema: {e}")
        logging.critical(f"Operación #{id_operacion} Error Crítico: {e}", exc_info=True)
    else:
        # Bloque ELSE exigido por la guía: se ejecuta si todo fue exitoso
        print(f"[ÉXITO] Operación realizada correctamente. Detalle: {resultado}")
        logging.info(f"Operación #{id_operacion} completada con éxito.")
    finally:
        # Bloque FINALLY exigido por la guía: se ejecuta siempre
        print(f"Limpieza de recursos de la Operación #{id_operacion} terminada.\n")


# 5. EJECUCIÓN CONTINUA DE LAS 10 OPERACIONES SIMULADAS (Garantiza estabilidad)
if __name__ == "__main__":
    print("=== INICIANDO SIMULACIÓN DE SOFTWARE FJ (10 OPERACIONES) ===\n")
    
    # Listas internas del sistema para simular base de datos volátil
    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # Operación 1: Registro Válido de Cliente
    ejecutar_operacion(1, "Registro de Cliente válido", lambda: [
        lista_clientes.append(Cliente("123456", "Luis Pérez", "luis@correo.com")),
        lista_clientes[0].obtener_resumen()
    ][-1])

    # Operación 2: Registro Inválido de Cliente (Correo incorrecto sin @ o .)
    ejecutar_operacion(2, "Registro de Cliente inválido (Error de correo)", lambda: 
        Cliente("789101", "Ana Gómez", "anagomezcorreo")
    )

    # Operación 3: Creación de Servicio Correcto (Sala de reuniones)
    ejecutar_operacion(3, "Creación de Servicio Válido (Sala)", lambda: [
        lista_servicios.append(ReservaSala("S01", "Sala de Juntas Premium", 50.0)),
        lista_servicios[0].describir_servicio()
    ][-1])

    # Operación 4: Creación de un Segundo Servicio Válido (Asesoría)
    ejecutar_operacion(4, "Creación de Servicio Válido (Asesoría)", lambda: [
        lista_servicios.append(AsesoriaEspecializada("A01", "Asesoría de Software Avanzado", 120.0)),
        lista_servicios[1].describir_servicio()
    ][-1])

    # Operación 5: Intento de Cálculo de Costo Inválido (Horas negativas en servicio)
    ejecutar_operacion(5, "Cálculo de costo inválido (Horas negativas)", lambda: 
        lista_servicios[0].calcular_costo(-3)
    )

    # Operación 6: Reserva Exitosa usando objetos existentes
    ejecutar_operacion(6, "Creación de Reserva Exitosa (4 horas)", lambda: [
        lista_reservas.append(Reserva(lista_clientes[0], lista_servicios[0], 4)),
        f"Reserva creada por {lista_reservas[0].cliente.nombre} con costo: ${lista_servicios[0].calcular_costo(4)}"
    ][-1])

    # Operación 7: Intento de Reserva Inválida (Excediendo el límite reglamentario de 24 horas)
    ejecutar_operacion(7, "Creación de Reserva Inválida (Límite superior > 24 horas)", lambda: 
        Reserva(lista_clientes[0], lista_servicios[0], 30)
    )

    # Operación 8: Confirmación de la Reserva Exitosa
    ejecutar_operacion(8, "Confirmación de Reserva Pendiente", lambda: [
        lista_reservas[0].confirmar(),
        f"Estado actual de la reserva: {lista_reservas[0].estado}"
    ][-1])

    # Operación 9: Cancelación y re-confirmación inválida (Rompe regla de negocio)
    ejecutar_operacion(9, "Intento de confirmar una reserva cancelada", lambda: [
        lista_reservas[0].cancelar(),
        lista_reservas[0].confirmar()
    ])

    # Operación 10: Demostración de Método Sobrecargado en Asesoría (Con Impuestos y Descuentos)
    ejecutar_operacion(10, "Cálculo Avanzado con Sobrecarga (Descuento del 10% e Impuesto del 19%)", lambda: 
        f"Costo final con sobrecarga avanzada: ${lista_servicios[1].calcular_costo_avanzado(horas=10, descuento=0.10, impuesto=0.19)}"
    )

    print("=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revisa el archivo 'sistema_gestion.log' generado en tu carpeta para ver los registros.")

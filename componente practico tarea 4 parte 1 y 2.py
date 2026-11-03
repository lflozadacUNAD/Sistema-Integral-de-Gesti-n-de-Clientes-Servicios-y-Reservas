# =====================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# ESCUELA DE CIENCIAS BÁSICAS TECNOLOGÍA E INGENIERÍA (ECBTI)
# CURSO: PROGRAMACIÓN (CÓDIGO: 213023)
# 
# EJERCICIO 1: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# DESARROLLADOR: Luis Fernando Lozada Castro (Simulación de Flujo Individual)
# FECHA: Octubre de 2026
# =====================================================================

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
        return (self.costo_base * horas) + 15.0  # Costo base + recargo de mantenimiento

    def describir_servicio(self) -> str:
        return f"Equipo de cómputo - Código: {self.codigo}"


# SERVICIO 3: Asesoría Especializada con Sobrecarga de Parámetros Opcionales
class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ServicioError("Las horas de asesoría especializada deben ser mayores a 0.")
        return self.costo_base * horas

    # Método Avanzado (Simula la sobrecarga con parámetros por defecto)
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


# =====================================================================
# EJECUCIÓN INTEGRADA: PARTE 1, PARTE 2 Y PARTE 3
# =====================================================================
if __name__ == "__main__":
    print("=== INICIANDO PRUEBA INTEGRADA (PARTES 1, 2 Y 3) ===\n")
    
    # -----------------------------------------------------------------
    # COMPONENTE: CLIENTES Y ENCAPSULAMIENTO (Partes 1 y 2)
    # -----------------------------------------------------------------
    print("--- [Fase 1] Validando Registro de Clientes ---")
    try:
        # 1. Registro Exitoso
        cliente_valido = Cliente("123456", "Luis Fernando Lozada", "luis@correo.com")
        print(f"[ÉXITO] Cliente registrado: {cliente_valido.obtener_resumen()}")
        
        # 2. Registro Inválido (Forzar excepción de encapsulamiento)
        print("Intentando registrar un correo sin estructura válida...")
        cliente_invalido = Cliente("789101", "Ana Gómez", "correo_invalido_sin_arroba")
        
    except ClienteInvalidoError as e:
        print(f"[ERROR CONTROLADO] Validación de cliente exitosa: {e}")
        logging.error(f"Fallo controlado en Clientes: {e}")

    # -----------------------------------------------------------------
    # COMPONENTE: SERVICIOS Y TRANSACCIONES (Parte 3)
    # -----------------------------------------------------------------
    print("\n--- [Fase 2] Validando Servicios y Costos ---")
    try:
        # Creación de instancias de los 3 servicios requeridos
        sala = ReservaSala("S01", "Sala de Juntas Premium", 50.0)
        computador = AlquilerEquipo("E01", "PC de Cómputo Desarrollo", 20.0)
        asesoria = AsesoriaEspecializada("A01", "Asesoría de Software Avanzado", 100.0)
        
        # Demostración de cálculos y descripciones
        print(f"[OK] {sala.describir_servicio()} | Costo 6h (Con dcto volumen): ${sala.calcular_costo(6)}")
        print(f"[OK] {computador.describir_servicio()} | Costo 3h (Con recargo mtto): ${computador.calcular_costo(3)}")
        print(f"[OK] {asesoria.describir_servicio()} | Costo Avanzado (Sobrecarga): ${asesoria.calcular_costo_avanzado(10, descuento=0.10, impuesto=0.19)}")

        print("\n--- [Fase 3] Validando Reglas de Negocio de Reservas ---")
        # 1. Creación y confirmación transaccional correcta
        reserva_valida = Reserva(cliente_valido, sala, 4)
        reserva_valida.confirmar()
        print(f"[ÉXITO] Reserva confirmada. Estado actual: {reserva_valida.estado}")
        
        # 2. Intento de romper regla de negocio (Reserva de más de 24 horas)
        print("Intentando generar una reserva de 30 horas...")
        reserva_invalida = Reserva(cliente_valido, computador, 30)

    except (ServicioError, ReservaError) as e:
        print(f"[ERROR CONTROLADO] Restricción de negocio activada: {e}")
        logging.error(f"Fallo controlado en Reservas: {e}")

    print("\n=== FIN DEL EJERCICIO HASTA LA PARTE 3 ===")
    print("Verifica el archivo 'sistema_gestion.log' para confirmar los registros de auditoría.")

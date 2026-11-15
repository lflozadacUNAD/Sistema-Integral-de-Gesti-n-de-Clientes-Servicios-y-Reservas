# =====================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# ESCUELA DE CIENCIAS BÁSICAS TECNOLOGÍA E INGENIERÍA (ECBTI)
# CURSO: PROGRAMACIÓN (CÓDIGO: 213023)
#
# EJERCICIO 1: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# DESARROLLADOR: Luis Fernando Lozada Castro
# FECHA: 22 de Noviembre de 2026
# =====================================================================

from abc import ABC, abstractmethod
from typing import overload, Optional
import logging
import os

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_LOG = os.path.join(RUTA_BASE, 'sistema_gestion.log')

# Configuración inicial del archivo de auditoría y errores
logging.basicConfig(
    filename=ARCHIVO_LOG,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8',
    force=True
)

# ---------------------------------------------------------------------
# JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ---------------------------------------------------------------------
class SoftwareFJException(Exception):
    """Excepción base para controlar los errores propios del sistema."""
    pass


class ClienteInvalidoError(SoftwareFJException):
    """Se dispara cuando los datos del cliente no cumplen las reglas de validación."""
    pass


class ServicioError(SoftwareFJException):
    """Se dispara por errores de configuración, horas inválidas o indisponibilidad."""
    pass


class ReservaError(SoftwareFJException):
    """Se dispara al incumplir reglas de negocio en la gestión de reservas."""
    pass


# ---------------------------------------------------------------------
# CLASES BASE Y ENTIDADES DEL SISTEMA
# ---------------------------------------------------------------------
class EntidadSistema(ABC):
    """Clase abstracta general para las entidades identificables del sistema."""

    def __init__(self, identificador: str):
        # Verificamos que el identificador no llegue vacío o solo con espacios
        if not identificador or not str(identificador).strip():
            raise SoftwareFJException("El identificador no puede estar vacío.")
        self._identificador = str(identificador).strip()

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna una cadena descriptiva de la entidad."""
        pass


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con validación en sus atributos."""

    def __init__(self, cedula: str, nombre: str, correo: str):
        # Validamos la cédula y encadenamos el error si falla el formato
        try:
            super().__init__(cedula)
            if not self._identificador.isdigit() or len(self._identificador) < 5:
                raise ValueError("La cédula debe tener al menos 5 dígitos numéricos.")
        except (SoftwareFJException, ValueError) as e:
            raise ClienteInvalidoError(f"Cédula de cliente inválida ('{cedula}').") from e

        # Invocamos los setters para validar nombre y correo desde el constructor
        self.nombre = nombre
        self.correo = correo

    @property
    def cedula(self) -> str:
        return self._identificador

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"El nombre '{valor}' es muy corto o inválido.")
        if not all(c.isalpha() or c.isspace() for c in valor.strip()):
            raise ClienteInvalidoError(f"El nombre '{valor}' no puede contener números ni símbolos.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        # Validación básica de estructura usuario@dominio.ext
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ClienteInvalidoError(f"Estructura de correo inválida: '{valor}'")
        self._correo = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente: {self.nombre} [Cédula: {self.cedula} | Correo: {self.correo}]"


# ---------------------------------------------------------------------
# JERARQUÍA DE SERVICIOS (POLIMORFISMO Y SOBRECARGA)
# ---------------------------------------------------------------------
class Servicio(ABC):
    """Clase abstracta base para los distintos servicios de Software FJ."""

    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, disponible: bool = True):
        if not codigo or not str(codigo).strip():
            raise ServicioError("El código del servicio es obligatorio.")
        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ServicioError("El nombre del servicio no puede estar vacío.")

        self.codigo = str(codigo).strip()
        self.nombre_servicio = str(nombre_servicio).strip()
        self.disponible = bool(disponible)

        # Convertimos y validamos el costo base encadenando posibles errores de tipo
        try:
            valor_costo = float(costo_base)
            if valor_costo <= 0:
                raise ValueError("El costo base debe ser mayor a cero.")
            self.costo_base = valor_costo
        except (TypeError, ValueError) as e:
            raise ServicioError(f"Costo base inválido ({costo_base}) en '{self.nombre_servicio}'.") from e

    def validar_horas(self, horas: int) -> int:
        """Comprueba que las horas sean un entero positivo."""
        try:
            if isinstance(horas, bool):
                raise TypeError("No se permiten valores booleanos como horas.")
            horas_int = int(horas)
            if horas_int <= 0:
                raise ValueError("La cantidad de horas debe ser mayor a 0.")
            return horas_int
        except (TypeError, ValueError) as e:
            raise ServicioError(f"Cantidad de horas inválida ({horas}) en '{self.nombre_servicio}'.") from e

    @abstractmethod
    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass


class ReservaSala(Servicio):
    """Servicio de alquiler de salas con descuento por volumen y sobrecarga."""

    @overload
    def calcular_costo(self, horas: int) -> float: ...

    @overload
    def calcular_costo(self, horas: int, descuento: float) -> float: ...

    @overload
    def calcular_costo(self, horas: int, descuento: float, impuesto: float) -> float: ...

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        horas_validas = self.validar_horas(horas)
        costo = self.costo_base * horas_validas

        # Si supera las 5 horas aplicamos un 10% de descuento automático
        if horas_validas > 5:
            costo *= 0.90
        if descuento > 0:
            costo *= (1 - descuento)
        if impuesto > 0:
            costo *= (1 + impuesto)

        return round(costo, 2)

    def describir_servicio(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Sala de reuniones '{self.nombre_servicio}' ({estado}) - Código: {self.codigo}"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos con cargo fijo por mantenimiento."""

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        horas_validas = self.validar_horas(horas)
        # Se suma un cargo fijo de $15.0 por alistamiento y mantenimiento
        costo = (self.costo_base * horas_validas) + 15.0
        costo = costo * (1 - descuento) * (1 + impuesto)
        return round(costo, 2)

    def describir_servicio(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Equipo de cómputo '{self.nombre_servicio}' ({estado}) - Código: {self.codigo}"


class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría técnica con cálculo sobrecargado."""

    @overload
    def calcular_costo(self, horas: int) -> float: ...

    @overload
    def calcular_costo(self, horas: int, descuento: float) -> float: ...

    @overload
    def calcular_costo(self, horas: int, descuento: float, impuesto: float) -> float: ...

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        horas_validas = self.validar_horas(horas)
        try:
            dcto = float(descuento)
            imp = float(impuesto)
            if not (0 <= dcto < 1) or imp < 0:
                raise ValueError("El descuento debe estar entre 0 y 1, y el impuesto no puede ser negativo.")
            subtotal = (self.costo_base * horas_validas) * (1 - dcto)
            return round(subtotal * (1 + imp), 2)
        except (TypeError, ValueError) as e:
            raise ServicioError("Error en los parámetros de cálculo de la asesoría.") from e

    def describir_servicio(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría técnica '{self.nombre_servicio}' ({estado}) - Código: {self.codigo}"


# ---------------------------------------------------------------------
# GESTIÓN TRANSACCIONAL DE RESERVAS
# ---------------------------------------------------------------------
class Reserva:
    """Gestiona el ciclo de vida de una reserva entre un cliente y un servicio."""

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaError("Se requieren instancias válidas de Cliente y Servicio.")
        if not servicio.disponible:
            raise ServicioError(f"El servicio '{servicio.nombre_servicio}' no se encuentra disponible.")

        try:
            horas = int(duracion_horas)
            if horas <= 0:
                raise ValueError("La duración debe ser mayor a 0 horas.")
            if horas > 24:
                raise ValueError("Las reservas no pueden exceder las 24 horas continuas.")
        except (TypeError, ValueError) as e:
            raise ReservaError(f"Duración de reserva inválida ({duracion_horas}h).") from e

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = horas
        self.estado = "Pendiente"
        self.valor_total: Optional[float] = None

    def confirmar(self):
        """Cambia el estado de la reserva a Confirmada si es válido hacerlo."""
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva que ya fue cancelada.")
        if self.estado == "Procesada":
            raise ReservaError("Esta reserva ya fue procesada anteriormente.")
        self.estado = "Confirmada"
        logging.info(f"CONFIRMACIÓN -> Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_servicio}")

    def procesar(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el valor final y cierra la reserva si está confirmada."""
        if self.estado != "Confirmada":
            raise ReservaError(f"No se puede procesar en estado '{self.estado}'. Debe confirmarse primero.")
        try:
            self.valor_total = self.servicio.calcular_costo(self.duracion_horas, descuento, impuesto)
            self.estado = "Procesada"
            logging.info(
                f"PROCESAMIENTO EXITOSO -> Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre_servicio} | Total: ${self.valor_total}"
            )
            return self.valor_total
        except ServicioError as e:
            raise ReservaError("Error al liquidar el costo de la reserva.") from e

    def cancelar(self):
        """Anula una reserva siempre que no haya sido procesada."""
        if self.estado == "Procesada":
            raise ReservaError("No se puede cancelar una reserva ya procesada.")
        self.estado = "Cancelada"
        logging.info(f"CANCELACIÓN -> Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_servicio}")

# ---------------------------------------------------------------------
# MOTOR DE EJECUCIÓN CONTROLADA
# ---------------------------------------------------------------------
def ejecutar_operacion(id_operacion: int, descripcion: str, funcion_prueba):
    """Ejecuta cada caso de prueba aislando fallos para no detener el sistema."""
    print(f"--- Operación #{id_operacion}: {descripcion} ---")
    try:
        resultado = funcion_prueba()
    except SoftwareFJException as e:
        causa = f" | Causa encadenada: {e.__cause__}" if e.__cause__ else ""
        print(f"[ERROR CONTROLADO] {e}{causa}")
        logging.error(f"Operación #{id_operacion} Falló - Razón: {e}{causa}")
    except Exception as e:
        print(f"[CRÍTICO] Error inesperado: {e}")
        logging.critical(f"Operación #{id_operacion} Error Crítico: {e}", exc_info=True)
    else:
        print(f"[ÉXITO] {resultado}")
        logging.info(f"Operación #{id_operacion} Exitosa - Detalle: {resultado}")
    finally:
        print(f"Cierre de ejecución para Operación #{id_operacion}.\n")


# ---------------------------------------------------------------------
# BLOQUE PRINCIPAL: SIMULACIÓN DE 12 OPERACIONES
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("=== INICIANDO SIMULACIÓN INTEGRAL SOFTWARE FJ ===\n")

    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    def op1_cliente_valido():
        c = Cliente("10987654", "Luis Pérez", "luis.perez@correo.com")
        lista_clientes.append(c)
        return c.obtener_resumen()

    def op2_cliente_cedula_invalida():
        return Cliente("ABC12", "Ana Gómez", "ana@correo.com")

    def op3_cliente_nombre_invalido():
        return Cliente("10987655", "Carlos 123", "carlos@correo.com")

    def op4_servicio_valido_sala():
        s = ReservaSala("S01", "Sala Ejecutiva Norte", 50.0, disponible=True)
        lista_servicios.append(s)
        return s.describir_servicio()

    def op5_servicio_creacion_invalida_costo():
        return AlquilerEquipo("E99", "Servidor Rack", -45.0)

    def op6_servicio_creacion_invalida_tipo():
        return AsesoriaEspecializada("A99", "Auditoría Seguridad", "cien_dolares")

    def op7_servicio_no_disponible():
        eq = AlquilerEquipo("E01", "Workstation GPU", 35.0, disponible=False)
        lista_servicios.append(eq)
        return eq.describir_servicio()

    def op8_demostracion_sobrecarga_explicita():
        asesoria = AsesoriaEspecializada("A01", "Arquitectura Cloud", 100.0)
        lista_servicios.append(asesoria)
        c1 = asesoria.calcular_costo(4)
        c2 = asesoria.calcular_costo(4, 0.10)
        c3 = asesoria.calcular_costo(4, 0.10, 0.19)
        return f"Sobrecarga verificada -> Base: ${c1} | Con dcto 10%: ${c2} | Con dcto + IVA 19%: ${c3}"

    def op9_reserva_confirmar_y_procesar_exitosa():
        res = Reserva(lista_clientes[0], lista_servicios[0], 6)
        res.confirmar()
        total = res.procesar(descuento=0.05, impuesto=0.19)
        lista_reservas.append(res)
        return f"Reserva {res.estado} para {res.cliente.nombre} | Total facturado: ${total}"

    def op10_procesar_reserva_sin_confirmar():
        res_pendiente = Reserva(lista_clientes[0], lista_servicios[0], 3)
        return res_pendiente.procesar()

    def op11_reserva_servicio_indisponible():
        return Reserva(lista_clientes[0], lista_servicios[1], 2)

    def op12_reserva_duracion_invalida_encadenada():
        return Reserva(lista_clientes[0], lista_servicios[0], "veinte")

    ejecutar_operacion(1, "Registro de Cliente válido con validaciones completas", op1_cliente_valido)
    ejecutar_operacion(2, "Validación Cliente: Cédula alfanumérica inválida (Encadenamiento)", op2_cliente_cedula_invalida)
    ejecutar_operacion(3, "Validación Cliente: Nombre con números inválidos", op3_cliente_nombre_invalido)
    ejecutar_operacion(4, "Creación válida de Servicio (Sala disponible)", op4_servicio_valido_sala)
    ejecutar_operacion(5, "Creación inválida de Servicio: Costo base negativo (Encadenamiento)", op5_servicio_creacion_invalida_costo)
    ejecutar_operacion(6, "Creación inválida de Servicio: Costo no numérico (Encadenamiento)", op6_servicio_creacion_invalida_tipo)
    ejecutar_operacion(7, "Registro de Servicio marcado como no disponible", op7_servicio_no_disponible)
    ejecutar_operacion(8, "Demostración explícita de sobrecarga de métodos (@overload)", op8_demostracion_sobrecarga_explicita)
    ejecutar_operacion(9, "Flujo completo: Creación, Confirmación y Procesamiento de Reserva", op9_reserva_confirmar_y_procesar_exitosa)
    ejecutar_operacion(10, "Error de negocio: Intentar procesar reserva sin confirmar", op10_procesar_reserva_sin_confirmar)
    ejecutar_operacion(11, "Error de disponibilidad: Reservar equipo fuera de servicio", op11_reserva_servicio_indisponible)
    ejecutar_operacion(12, "Error de parámetro: Duración corrupta en reserva (Encadenamiento)", op12_reserva_duracion_invalida_encadenada)

    print("=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revisa 'sistema_gestion.log' para verificar la auditoría completa.")
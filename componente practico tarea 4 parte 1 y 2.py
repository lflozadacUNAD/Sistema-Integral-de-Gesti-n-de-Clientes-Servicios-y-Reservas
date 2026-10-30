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
    

# ==========================================
# PRUEBA COMPLEMENTARIA - PARTE 1 Y 2
# ==========================================
if __name__ == "__main__":
    print("=== PROBANDO ENCAPSULAMIENTO DE LA PARTE 1 Y 2 ===")
    
    try:
        # 1. Crear un cliente con datos correctos
        cliente_valido = Cliente("123456", "Luis Fernando", "luis@correo.com")
        print(f"[ÉXITO] {cliente_valido.obtener_resumen()}")
        
        # 2. Intentar crear un cliente con correo inválido para forzar la excepción
        print("\nIntentando registrar correo inválido...")
        cliente_invalido = Cliente("789101", "Ana Gómez", "correo_sin_arroba")
        
    except ClienteInvalidoError as e:
        print(f"[ERROR CONTROLADO] Se lanzó la excepción esperada: {e}")
        logging.error(f"Error de validación controlado en la entrega: {e}")
        
    print("\n=== FIN DE LA PRUEBA DE LA PARTE 1 Y 2 ===")

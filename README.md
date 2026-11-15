# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto práctico correspondiente a la **Fase 4 del curso Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción del proyecto
Aplicación desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO) para gestionar clientes, servicios (reserva de salas, alquiler de equipos y asesorías especializadas) y reservas sin uso de bases de datos. El sistema garantiza continuidad operativa mediante el manejo avanzado de excepciones y registro de auditoría en archivos planos.

## Estructura del repositorio
* `componente practico tarea 4 final.py`: Código fuente principal con la arquitectura POO, validaciones, sobrecarga de métodos y el motor de simulación de 12 operaciones.
* `sistema_gestion.log`: Archivo generado automáticamente donde se registran los eventos exitosos y los errores controlados durante la ejecución.

## Conceptos implementados
* **Abstracción y Herencia:** Clases base abstractas (`EntidadSistema` y `Servicio`) con métodos abstractos implementados en clases derivadas.
* **Encapsulación:** Validación estricta de atributos mediante decoradores `@property` y setters en la clase `Cliente`.
* **Polimorfismo y Sobrecarga:** Cálculo diferenciado de tarifas según el tipo de servicio y uso de `@overload` para parámetros opcionales (descuentos e impuestos).
* **Manejo Avanzado de Excepciones:** Jerarquía de excepciones propias (`SoftwareFJException`), bloques `try / except / else / finally` y encadenamiento de errores (`raise ... from e`).

## Requisitos y ejecución
1. Tener instalado **Python 3.10** o superior.
2. Clonar el repositorio o descargar el archivo fuente.
3. Ejecutar desde la terminal:
   ```bash
   python "componente practico tarea 4 final.py"
   ```
4. Verificar la salida en consola y los registros generados en `sistema_gestion.log`.

## Autor
* **Luis Fernando Lozada Castro** - Programa de Ingeniería de Sistemas (ECBTI - UNAD).

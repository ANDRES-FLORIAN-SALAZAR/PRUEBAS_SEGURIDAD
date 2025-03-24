# Refactorización del Sistema de Gestión de Productos

## Introducción

Este informe documenta el proceso de refactorización de un sistema de gestión de productos en Python, aplicando los principios SOLID para mejorar la calidad del código y su mantenibilidad. También se incluye un análisis de las violaciones detectadas y las correcciones implementadas.

## Violaciones SOLID Identificadas

### 1. **Principio de Responsabilidad Única (SRP)**

- Antes: La clase `GestorProductos` manejaba tanto la persistencia de datos como la lógica de negocio.
- Corrección: Se introdujo la clase `GestorArchivo` para encargarse de la persistencia de datos.

### 2. **Principio de Abierto/Cerrado (OCP)**

- Antes: La creación de productos no permitía fácilmente la extensión a nuevos tipos de productos sin modificar la clase `Producto`.
- Corrección: Se creó la subclase `ProductoEspecial` para manejar descuentos sin modificar la clase base.

### 3. **Principio de Sustitución de Liskov (LSP)**

- Antes: `ProductoEspecial` sobrescribía el cálculo de precio, pero no respetaba completamente la estructura de `Producto`.
- Corrección: Se mantuvo la compatibilidad asegurando que `ProductoEspecial` solo extendiera funcionalidades sin alterar el comportamiento esperado.

### 4. **Principio de Segregación de Interfaces (ISP)**

- Antes: No existían interfaces claras para la gestión de productos.
- Corrección: Se introdujo `RepositorioProductos` como una interfaz abstracta para estandarizar las operaciones sobre productos.

### 5. **Principio de Inversión de Dependencias (DIP)**

- Antes: `GestorVentas` dependía directamente de `GestorProductos`.
- Corrección: Se introdujo la inyección de dependencias, permitiendo mayor flexibilidad y testabilidad.

## Correcciones Adicionales Identificadas con Ruff

### 1. **I001: Orden de Imports**

- Antes: Los imports no estaban organizados correctamente.
- Corrección: Se reordenaron en el siguiente orden:
  1. Módulos estándar de Python
  2. Módulos de terceros (si los hubiera)
  3. Módulos propios

### 2. **PLR0913: Demasiados argumentos en una función**

- Antes: `ProductoEspecial` tenía más de 5 argumentos en su `__init__`.
- Corrección: Se utilizó `dataclass` para evitar la necesidad de definir manualmente el constructor.

## Conclusión

La refactorización aplicada mejoró la separación de responsabilidades y la extensibilidad del sistema. Se logró mayor adherencia a los principios SOLID, facilitando la evolución y mantenimiento del código. Además, se resolvieron las advertencias detectadas por Ruff, mejorando la calidad del código en términos de estilo y legibilidad.

## Evidencia de las Correcciones

A continuación se incluyen capturas de pantalla con los resultados de Ruff antes y después de aplicar las correcciones:

![Error de orden de imports](./Pantallazos/1.png)

![Error de demasiados argumentos](./Pantallazos/2.png)

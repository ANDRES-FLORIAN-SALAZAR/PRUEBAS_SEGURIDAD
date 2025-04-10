"""Módulo para gestionar productos y ventas."""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass
class Producto:
    """Clase que representa un producto."""

    def __init__(
        self,
        producto_id: int,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> None:
        """Inicializa un nuevo producto."""
        self.producto_id = producto_id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    def calcular_precio_final(self) -> float:
        """Calcula el precio final del producto."""
        return self.precio

@dataclass
class ProductoEspecial(Producto):
    """Clase para productos con descuento."""

    def __init__ (
        self,
        producto_id: int,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
        descuento: float,
    ) -> None:
        """Inicializa un nuevo producto especial con descuento."""
        super().__init__(producto_id, nombre, precio, categoria, stock)
        self.descuento = descuento

    def calcular_precio_final(self) -> float:
        """Calcula el precio final del producto con descuento."""
        return self.precio * (1 - self.descuento)


class GestorArchivo:
    """Clase para gestionar archivos."""

    @staticmethod
    def cargar_datos(archivo: str) -> list:
        """Carga datos desde un archivo JSON."""
        ruta = Path(archivo)  # Convertimos la cadena a un objeto Path
        if not ruta.exists():
            return []
        try:
            with ruta.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error al leer el archivo {archivo}.")  # noqa: T201
            return []


@staticmethod
def guardar_datos(archivo: str, datos: list) -> None:
    """Guarda datos en un archivo JSON."""
    ruta = Path(archivo)
    with ruta.open("w", encoding="utf-8") as file:
        json.dump(datos, file, indent=4)


class GestorProductos:
    """Clase para gestionar productos."""

    def __init__(self, archivo_productos: str = "productos.txt") -> None:
        """Inicializa el gestor de productos."""
        self.archivo_productos = archivo_productos

    def listar_productos(self) -> list:
        """Lista todos los productos."""
        productos = GestorArchivo.cargar_datos(self.archivo_productos)
        return [Producto(**p) for p in productos]

    def registrar_producto(self, producto: Producto) -> None:
        """Registra un nuevo producto."""
        productos = GestorArchivo.cargar_datos(self.archivo_productos)
        if any(p["producto_id"] == producto.producto_id for p in productos):
            print("ERROR: Ya existe un producto con ese ID.")  # noqa: T201
            return
        productos.append(vars(producto))
        GestorArchivo.guardar_datos(self.archivo_productos, productos)

    def actualizar_producto(self, producto_id: int, **kwargs: any) -> bool:
        """Actualiza un producto existente."""
        productos = GestorArchivo.cargar_datos(self.archivo_productos)
        for producto in productos:
            if producto["producto_id"] == producto_id:
                producto.update(kwargs)
                GestorArchivo.guardar_datos(self.archivo_productos, productos)
                return True
        return False

    def eliminar_producto(self, producto_id: int) -> None:
        """Elimina un producto."""
        productos = GestorArchivo.cargar_datos(self.archivo_productos)
        productos = [p for p in productos if p["producto_id"] != producto_id]
        GestorArchivo.guardar_datos(self.archivo_productos, productos)


class GestorVentas:
    """Clase para gestionar ventas."""

    def __init__(
        self,
        archivo_ventas: str = "ventas.txt",
        gestor_productos: GestorProductos = None,
    ) -> None:
        """Inicializa el gestor de ventas."""
        self.archivo_ventas = archivo_ventas
        self.gestor_productos = gestor_productos or GestorProductos()

    def registrar_venta(self, producto_id: int, cantidad: int) -> bool:
        """Registra una nueva venta."""
        productos = self.gestor_productos.listar_productos()
        for producto in productos:
            if producto.producto_id == producto_id and producto.stock >= cantidad:
                producto.stock -= cantidad
                self.gestor_productos.actualizar_producto(
                    producto_id,
                    stock=producto.stock,
                )
                venta = {
                    "producto_id": producto_id,
                    "cantidad": cantidad,
                    "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "total": producto.calcular_precio_final() * cantidad,
                }
                ventas = GestorArchivo.cargar_datos(self.archivo_ventas)
                ventas.append(venta)
                GestorArchivo.guardar_datos(self.archivo_ventas, ventas)
                return True
        return False

    def generar_reporte(self) -> tuple:
        """Genera un reporte de ventas."""
        ventas = GestorArchivo.cargar_datos(self.archivo_ventas)
        total = sum(v["total"] for v in ventas)
        return ventas, total


class SistemaProductos:
    """Clase que maneja toda la aplicación."""

    def __init__(self) -> None:
        """Inicializa el sistema de productos."""
        self.gestor_productos = GestorProductos()
        self.gestor_ventas = GestorVentas(gestor_productos=self.gestor_productos)

    def ejecutar(self) -> None:
        """Ejecuta el sistema de productos."""
        while True:
            print("\n===== SISTEMA DE REGISTRO DE PRODUCTOS =====")  # noqa: T201
            print("1. Registrar producto")  # noqa: T201
            print("2. Consultar productos")  # noqa: T201
            print("3. Actualizar producto")  # noqa: T201
            print("4. Eliminar producto")  # noqa: T201
            print("5. Registrar venta")  # noqa: T201
            print("6. Generar reporte de ventas")  # noqa: T201
            print("7. Salir")  # noqa: T201
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                producto_id = int(input("ID: "))
                nombre = input("Nombre: ")
                precio = float(input("Precio: "))
                categoria = input("Categoría: ")
                stock = int(input("Stock: "))
                producto = Producto(producto_id, nombre, precio, categoria, stock)
                self.gestor_productos.registrar_producto(producto)
            elif opcion == "2":
                productos = self.gestor_productos.listar_productos()
                for p in productos:
                    print(vars(p))  # noqa: T201
            elif opcion == "3":
                producto_id = int(input("ID: "))
                nombre = input("Nuevo nombre (Enter para mantener): ")
                precio = input("Nuevo precio (Enter para mantener): ")
                stock = input("Nuevo stock (Enter para mantener): ")
                self.gestor_productos.actualizar_producto(
                    producto_id,
                    nombre=nombre or None,
                    precio=float(precio) if precio else None,
                    stock=int(stock) if stock else None,
                )
            elif opcion == "4":
                producto_id = int(input("ID del producto a eliminar: "))
                self.gestor_productos.eliminar_producto(producto_id)
            elif opcion == "5":
                producto_id = int(input("ID del producto vendido: "))
                cantidad = int(input("Cantidad: "))
                self.gestor_ventas.registrar_venta(producto_id, cantidad)
            elif opcion == "6":
                ventas, total = self.gestor_ventas.generar_reporte()
                print("Ventas:", ventas)  # noqa: T201
                print("Total:", total)  # noqa: T201
            elif opcion == "7":
                print("¡Gracias por usar el sistema!")  # noqa: T201
                break


if __name__ == "__main__":
    sistema = SistemaProductos()
    sistema.ejecutar()

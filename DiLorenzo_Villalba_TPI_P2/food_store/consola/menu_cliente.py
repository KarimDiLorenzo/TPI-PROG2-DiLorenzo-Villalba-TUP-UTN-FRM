from consola.entradas import leer_confirmacion, leer_entero
from consola.menu import Menu
from entidades.usuario import Usuario
from excepciones import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio


class MenuCliente(Menu):
    """Menú de consola exclusivo para usuarios con rol USUARIO (solo consulta)."""

    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self._categoria_servicio: CategoriaServicio = categoria_servicio
        self._producto_servicio: ProductoServicio = producto_servicio
        self._pedido_servicio: PedidoServicio = pedido_servicio

    def mostrar(self) -> bool:
        while True:
            print(
                f"\n=== FOOD STORE CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ==="
            )
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")

            opcion = input("Seleccione: ").strip()
            try:
                if opcion == "1":
                    self._ver_categorias()
                elif opcion == "2":
                    self._ver_productos_disponibles()
                elif opcion == "3":
                    self._ver_mis_pedidos()
                elif opcion == "4":
                    self._ver_mis_datos()
                elif opcion == "9":
                    print("Cerrando sesión...")
                    return True
                elif opcion == "0":
                    print("¡Gracias por visitar Food Store!")
                    return False
                else:
                    print("Error: Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Dato numérico inválido.")

    def _ver_categorias(self) -> None:
        categorias = self._categoria_servicio.listar()
        if not categorias:
            print("No hay categorías cargadas")
            return
        print("\n--- CATEGORÍAS ---")
        for cat in categorias:
            print(cat)

    def _ver_productos_disponibles(self) -> None:
        filtrar = leer_confirmacion("¿Desea filtrar por categoría? (S/N): ")
        if filtrar:
            self._ver_categorias()
            id_cat = leer_entero("Ingrese el ID de la categoría: ", minimo=1)
            if id_cat is not None:
                productos = self._producto_servicio.listar_por_categoria(
                    id_cat, solo_disponibles=True
                )
            else:
                productos = []
        else:
            productos = self._producto_servicio.listar_disponibles()

        if not productos:
            print("No hay productos disponibles.")
            return
        print("\n--- PRODUCTOS DISPONIBLES ---")
        for prod in productos:
            print(prod)

    def _ver_mis_pedidos(self) -> None:
        pedidos = self._pedido_servicio.listar_por_usuario(self._usuario)
        if not pedidos:
            print("No tienes pedidos registrados.")
            return
        print("\n--- MIS PEDIDOS ---")
        for ped in pedidos:
            print(
                f"[{ped.id}] Estado: {ped.estado.value} | "
                f"Forma de pago: {ped.forma_pago.value} | "
                f"Total: ${ped.total:.2f} | Fecha: {ped.fecha}"
            )
        ver_det = leer_confirmacion("\n¿Desea ver el detalle de un pedido? (S/N): ")
        if ver_det:
            id_ped = leer_entero("Ingrese el ID del pedido: ", minimo=1)
            if id_ped is not None:
                pedido = self._pedido_servicio.obtener_por_id_y_usuario(
                    id_ped, self._usuario
                )
                print(f"\n--- DETALLES DEL PEDIDO #{pedido.id} ---")
                for det in pedido.detalles:
                    print(f"  • {det}")
                print(f"TOTAL DEL PEDIDO: ${pedido.total:.2f}")

    def _ver_mis_datos(self) -> None:
        print("\n--- MIS DATOS ---")
        print(f"Nombre:   {self._usuario.nombre}")
        print(f"Apellido: {self._usuario.apellido}")
        print(f"Mail:     {self._usuario.mail}")
        print(f"Celular:  {self._usuario.celular}")
        print(f"Rol:      {self._usuario.rol.value}")

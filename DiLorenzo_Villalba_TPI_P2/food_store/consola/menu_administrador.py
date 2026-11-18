from consola.entradas import (
    leer_confirmacion,
    leer_entero,
    leer_flotante,
    leer_texto,
    seleccionar_enum,
)
from consola.menu import Menu
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class MenuAdministrador(Menu):
    """Menú de consola con gestión completa para usuarios con rol ADMIN."""

    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self._categoria_servicio: CategoriaServicio = categoria_servicio
        self._producto_servicio: ProductoServicio = producto_servicio
        self._usuario_servicio: UsuarioServicio = usuario_servicio
        self._pedido_servicio: PedidoServicio = pedido_servicio

    def mostrar(self) -> bool:
        while True:
            print(
                f"\n=== FOOD STORE ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ==="
            )
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")

            opcion = input("Seleccione: ").strip()
            if opcion == "1":
                self._submenu_categorias()
            elif opcion == "2":
                self._submenu_productos()
            elif opcion == "3":
                self._submenu_usuarios()
            elif opcion == "4":
                self._submenu_pedidos()
            elif opcion == "9":
                print("Cerrando sesión...")
                return True
            elif opcion == "0":
                print("¡Hasta luego!")
                return False
            else:
                print("Error: Opción fuera de rango.")

    # ---------------- CATEGORÍAS ----------------
    def _submenu_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")

            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_categorias()
                elif op == "2":
                    self._crear_categoria()
                elif op == "3":
                    self._editar_categoria()
                elif op == "4":
                    self._eliminar_categoria()
                elif op == "0":
                    break
                else:
                    print("Error: Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Entrada numérica inválida.")

    def _listar_categorias(self) -> None:
        categorias = self._categoria_servicio.listar()
        if not categorias:
            print("No hay categorías cargadas")
            return
        print("\nListado de Categorías:")
        for c in categorias:
            print(c)

    def _crear_categoria(self) -> None:
        nombre = leer_texto("Nombre de la categoría: ")
        descripcion = leer_texto("Descripción: ")
        nueva = self._categoria_servicio.crear(nombre=nombre, descripcion=descripcion)
        print(f"Éxito: Categoría creada correctamente con ID {nueva.id}.")

    def _editar_categoria(self) -> None:
        self._listar_categorias()
        id_cat = leer_entero("ID de la categoría a editar: ", minimo=1)
        if id_cat is None:
            return
        categoria = self._categoria_servicio.obtener_por_id(id_cat)
        print(f"Editando: {categoria}")
        nuevo_nombre = leer_texto(
            f"Nuevo nombre [{categoria.nombre}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        nueva_desc = leer_texto(
            f"Nueva descripción [{categoria.descripcion}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        self._categoria_servicio.editar(
            id_categoria=id_cat,
            nombre=nuevo_nombre if nuevo_nombre else None,
            descripcion=nueva_desc if nueva_desc else None,
        )
        print("Éxito: Categoría actualizada correctamente.")

    def _eliminar_categoria(self) -> None:
        self._listar_categorias()
        id_cat = leer_entero("ID de la categoría a eliminar: ", minimo=1)
        if id_cat is None:
            return
        categoria = self._categoria_servicio.obtener_por_id(id_cat)
        confirmar = leer_confirmacion(
            f"¿Confirma eliminar la categoría '{categoria.nombre}'? (S/N): "
        )
        if confirmar:
            self._categoria_servicio.eliminar(id_cat)
            print("Éxito: Categoría eliminada lógicamente.")
        else:
            print("Operación cancelada.")

    # ---------------- PRODUCTOS ----------------
    def _submenu_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")

            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_productos()
                elif op == "2":
                    self._crear_producto()
                elif op == "3":
                    self._editar_producto()
                elif op == "4":
                    self._eliminar_producto()
                elif op == "0":
                    break
                else:
                    print("Error: Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Entrada numérica inválida.")

    def _listar_productos(self) -> None:
        filtrar = leer_confirmacion("¿Desea filtrar por categoría? (S/N): ")
        if filtrar:
            self._listar_categorias()
            id_cat = leer_entero("Ingrese el ID de la categoría: ", minimo=1)
            productos = (
                self._producto_servicio.listar_por_categoria(id_cat)
                if id_cat is not None
                else []
            )
        else:
            productos = self._producto_servicio.listar()

        if not productos:
            print("No hay productos cargados.")
            return
        print("\nListado de Productos:")
        for p in productos:
            print(p)

    def _crear_producto(self) -> None:
        categorias = self._categoria_servicio.listar()
        if not categorias:
            print("Error: Primero debe existir al menos una categoría activa.")
            return
        nombre = leer_texto("Nombre del producto: ")
        descripcion = leer_texto("Descripción: ")
        precio = leer_flotante("Precio: ")
        stock = leer_entero("Stock inicial: ")
        imagen = leer_texto("Imagen (URL o archivo): ")
        disponible = leer_confirmacion("¿Está disponible? (S/N): ")
        self._listar_categorias()
        id_cat = leer_entero("ID de la categoría: ", minimo=1)

        if precio is None or stock is None or disponible is None or id_cat is None:
            return

        nuevo = self._producto_servicio.crear(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=imagen,
            disponible=disponible,
            id_categoria=id_cat,
        )
        print(f"Éxito: Producto creado correctamente con ID {nuevo.id}.")

    def _editar_producto(self) -> None:
        productos = self._producto_servicio.listar()
        if not productos:
            print("No hay productos cargados.")
            return
        for p in productos:
            print(p)
        id_prod = leer_entero("ID del producto a editar: ", minimo=1)
        if id_prod is None:
            return
        producto = self._producto_servicio.obtener_por_id(id_prod)
        print(f"Editando: {producto}")

        nombre = leer_texto(
            f"Nuevo nombre [{producto.nombre}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        descripcion = leer_texto(
            f"Nueva descripción [{producto.descripcion}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        precio = leer_flotante(
            f"Nuevo precio [{producto.precio:.2f}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        stock = leer_entero(
            f"Nuevo stock [{producto.stock}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        imagen = leer_texto(
            f"Nueva imagen [{producto.imagen}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        disponible = leer_confirmacion(
            f"¿Disponible? [{'S' if producto.disponible else 'N'}] (S/N o Enter para conservar): ",
            permitir_vacio=True,
        )
        self._listar_categorias()
        id_cat = leer_entero(
            f"Nuevo ID de categoría [{producto.categoria.id}] (Enter para conservar): ",
            minimo=1,
            permitir_vacio=True,
        )

        self._producto_servicio.editar(
            id_producto=id_prod,
            nombre=nombre if nombre else None,
            descripcion=descripcion if descripcion else None,
            precio=precio,
            stock=stock,
            imagen=imagen if imagen else None,
            disponible=disponible,
            id_categoria=id_cat,
        )
        print("Éxito: Producto actualizado correctamente.")

    def _eliminar_producto(self) -> None:
        productos = self._producto_servicio.listar()
        if not productos:
            print("No hay productos cargados.")
            return
        for p in productos:
            print(p)
        id_prod = leer_entero("ID del producto a eliminar: ", minimo=1)
        if id_prod is None:
            return
        producto = self._producto_servicio.obtener_por_id(id_prod)
        confirmar = leer_confirmacion(
            f"¿Confirma eliminar el producto '{producto.nombre}'? (S/N): "
        )
        if confirmar:
            self._producto_servicio.eliminar(id_prod)
            print("Éxito: Producto eliminado lógicamente.")
        else:
            print("Operación cancelada.")

    # ---------------- USUARIOS ----------------
    def _submenu_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")

            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_usuarios()
                elif op == "2":
                    self._crear_usuario()
                elif op == "3":
                    self._editar_usuario()
                elif op == "4":
                    self._eliminar_usuario()
                elif op == "0":
                    break
                else:
                    print("Error: Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Entrada numérica inválida.")

    def _listar_usuarios(self) -> None:
        usuarios = self._usuario_servicio.listar()
        if not usuarios:
            print("No hay usuarios cargados.")
            return
        print("\nListado de Usuarios:")
        for u in usuarios:
            print(u)

    def _crear_usuario(self) -> None:
        nombre = leer_texto("Nombre: ")
        apellido = leer_texto("Apellido: ")
        while True:
            mail = leer_texto("Mail: ")
            try:
                self._usuario_servicio.validar_mail_unico(mail)
                if "@" not in mail or "." not in mail:
                    print("Error: El mail debe contener '@' y '.'.")
                    continue
                break
            except FoodStoreError as e:
                print(f"Error: {e}. Por favor, ingrese otro mail.")

        celular = leer_texto("Celular: ")
        contrasenia = leer_texto("Contraseña: ")
        rol = seleccionar_enum(Rol, "Seleccione el Rol")
        if rol is None:
            return
        nuevo = self._usuario_servicio.crear(
            nombre=nombre,
            apellido=apellido,
            mail=mail,
            celular=celular,
            contrasenia=contrasenia,
            rol=rol,
        )
        print(f"Éxito: Usuario creado correctamente con ID {nuevo.id}.")

    def _editar_usuario(self) -> None:
        self._listar_usuarios()
        id_usr = leer_entero("ID del usuario a editar: ", minimo=1)
        if id_usr is None:
            return
        usuario = self._usuario_servicio.obtener_por_id(id_usr)
        print(f"Editando: {usuario}")

        nombre = leer_texto(
            f"Nuevo nombre [{usuario.nombre}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        apellido = leer_texto(
            f"Nuevo apellido [{usuario.apellido}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        mail = leer_texto(
            f"Nuevo mail [{usuario.mail}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        celular = leer_texto(
            f"Nuevo celular [{usuario.celular}] (Enter para conservar): ",
            permitir_vacio=True,
        )
        contrasenia = leer_texto(
            "Nueva contraseña (Enter para conservar): ",
            permitir_vacio=True,
        )
        rol = seleccionar_enum(
            Rol,
            f"Nuevo rol [{usuario.rol.value}]",
            permitir_vacio=True,
        )

        self._usuario_servicio.editar(
            id_usuario=id_usr,
            nombre=nombre if nombre else None,
            apellido=apellido if apellido else None,
            mail=mail if mail else None,
            celular=celular if celular else None,
            contrasenia=contrasenia if contrasenia else None,
            rol=rol,
        )
        print("Éxito: Usuario actualizado correctamente.")

    def _eliminar_usuario(self) -> None:
        self._listar_usuarios()
        id_usr = leer_entero("ID del usuario a eliminar: ", minimo=1)
        if id_usr is None:
            return
        usuario = self._usuario_servicio.obtener_por_id(id_usr)
        confirmar = leer_confirmacion(
            f"¿Confirma eliminar al usuario '{usuario.nombre} {usuario.apellido}'? (S/N): "
        )
        if confirmar:
            self._usuario_servicio.eliminar(id_usr, self._usuario)
            print("Éxito: Usuario eliminado lógicamente.")
        else:
            print("Operación cancelada.")

    # ---------------- PEDIDOS ----------------
    def _submenu_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---")
            print("1. Listar pedidos")
            print("2. Crear pedido")
            print("3. Actualizar estado / forma de pago")
            print("4. Eliminar pedido")
            print("0. Volver")

            op = input("Seleccione: ").strip()
            try:
                if op == "1":
                    self._listar_pedidos()
                elif op == "2":
                    self._crear_pedido()
                elif op == "3":
                    self._actualizar_pedido()
                elif op == "4":
                    self._eliminar_pedido()
                elif op == "0":
                    break
                else:
                    print("Error: Opción fuera de rango.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Entrada numérica inválida.")

    def _listar_pedidos(self) -> None:
        filtrar = leer_confirmacion("¿Desea filtrar pedidos por usuario? (S/N): ")
        if filtrar:
            self._listar_usuarios()
            id_usr = leer_entero("Ingrese el ID del usuario: ", minimo=1)
            if id_usr is None:
                return
            usr = self._usuario_servicio.obtener_por_id(id_usr)
            pedidos = self._pedido_servicio.listar_por_usuario(usr)
        else:
            pedidos = self._pedido_servicio.listar()

        if not pedidos:
            print("No hay pedidos registrados.")
            return
        print("\nListado de Pedidos:")
        for p in pedidos:
            print(p)

        ver_det = leer_confirmacion("\n¿Desea ver los detalles de un pedido? (S/N): ")
        if ver_det:
            id_ped = leer_entero("ID del pedido: ", minimo=1)
            if id_ped is not None:
                pedido = self._pedido_servicio.obtener_por_id(id_ped)
                print(f"\n--- DETALLES DEL PEDIDO #{pedido.id} ---")
                for det in pedido.detalles:
                    print(f"  • {det}")
                print(f"TOTAL: ${pedido.total:.2f}")

    def _crear_pedido(self) -> None:
        self._listar_usuarios()
        id_usr = leer_entero("ID del usuario cliente: ", minimo=1)
        if id_usr is None:
            return
        self._usuario_servicio.obtener_por_id(id_usr)

        forma_pago = seleccionar_enum(FormaPago, "Seleccione Forma de Pago")
        if forma_pago is None:
            return

        productos = self._producto_servicio.listar_disponibles()
        if not productos:
            print("Error: No hay productos disponibles con stock para crear pedidos.")
            return

        items: list[tuple[int, int]] = []
        while True:
            print("\nProductos disponibles:")
            for p in productos:
                print(p)
            id_prod = leer_entero("ID del producto a agregar: ", minimo=1)
            cantidad = leer_entero("Cantidad: ", minimo=1)
            if id_prod is not None and cantidad is not None:
                items.append((id_prod, cantidad))

            agregar_otro = leer_confirmacion("¿Desea agregar otro producto al pedido? (S/N): ")
            if not agregar_otro:
                break

        pedido = self._pedido_servicio.crear_pedido(
            id_usuario=id_usr,
            forma_pago=forma_pago,
            items=items,
        )
        print(
            f"Éxito: Pedido creado con ID {pedido.id} | Total: ${pedido.total:.2f}."
        )

    def _actualizar_pedido(self) -> None:
        pedidos = self._pedido_servicio.listar()
        if not pedidos:
            print("No hay pedidos registrados.")
            return
        for p in pedidos:
            print(p)
        id_ped = leer_entero("ID del pedido a actualizar: ", minimo=1)
        if id_ped is None:
            return
        pedido = self._pedido_servicio.obtener_por_id(id_ped)
        print(f"Actualizando: {pedido}")

        nuevo_estado = seleccionar_enum(
            Estado,
            f"Nuevo estado [{pedido.estado.value}]",
            permitir_vacio=True,
        )
        nueva_fp = seleccionar_enum(
            FormaPago,
            f"Nueva forma de pago [{pedido.forma_pago.value}]",
            permitir_vacio=True,
        )

        self._pedido_servicio.actualizar_pedido(
            id_pedido=id_ped,
            nuevo_estado=nuevo_estado,
            nueva_forma_pago=nueva_fp,
        )
        print("Éxito: Pedido actualizado correctamente.")

    def _eliminar_pedido(self) -> None:
        pedidos = self._pedido_servicio.listar()
        if not pedidos:
            print("No hay pedidos registrados.")
            return
        for p in pedidos:
            print(p)
        id_ped = leer_entero("ID del pedido a eliminar: ", minimo=1)
        if id_ped is None:
            return
        pedido = self._pedido_servicio.obtener_por_id(id_ped)
        confirmar = leer_confirmacion(
            f"¿Confirma eliminar el pedido #{pedido.id}? (S/N): "
        )
        if confirmar:
            self._pedido_servicio.eliminar(id_ped)
            print("Éxito: Pedido eliminado lógicamente.")
        else:
            print("Operación cancelada.")

from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones import (
    CredencialesInvalidasError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)


class UsuarioServicio:
    """Servicio encargado de gestionar la colección y autenticación de Usuario."""

    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []

    def listar(self) -> list[Usuario]:
        return [u for u in self._usuarios if not u.eliminado]

    def obtener_por_id(self, id_usuario: int) -> Usuario:
        for usuario in self._usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(
            f"No se encontró un usuario activo con id {id_usuario}."
        )

    def validar_mail_unico(self, mail: str, id_excluir: int | None = None) -> None:
        mail_norm = mail.strip().lower()
        for usuario in self._usuarios:
            if usuario.id != id_excluir and usuario.mail.lower() == mail_norm:
                raise DuplicadoError(f"El mail '{mail.strip()}' ya está registrado.")

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        self.validar_mail_unico(mail)
        nuevo = Usuario(
            nombre=nombre,
            apellido=apellido,
            mail=mail,
            celular=celular,
            contrasenia=contrasenia,
            rol=rol,
        )
        self._usuarios.append(nuevo)
        return nuevo

    def editar(
        self,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        usuario = self.obtener_por_id(id_usuario)
        if mail is not None and mail.strip() != "":
            self.validar_mail_unico(mail, id_excluir=usuario.id)
            usuario.mail = mail
        if nombre is not None and nombre.strip() != "":
            usuario.nombre = nombre
        if apellido is not None and apellido.strip() != "":
            usuario.apellido = apellido
        if celular is not None and celular.strip() != "":
            usuario.celular = celular
        if contrasenia is not None and contrasenia.strip() != "":
            usuario.cambiar_contrasenia(contrasenia)
        if rol is not None:
            usuario.rol = rol
        return usuario

    def eliminar(self, id_usuario: int, usuario_sesion: Usuario) -> None:
        usuario = self.obtener_por_id(id_usuario)
        if usuario == usuario_sesion:
            raise OperacionNoPermitidaError(
                "Un administrador no puede eliminarse a sí mismo con la sesión iniciada."
            )
        usuario.eliminado = True

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        mail_norm = mail.strip().lower()
        for usuario in self._usuarios:
            if usuario.mail.lower() == mail_norm:
                if not usuario.eliminado and usuario.verificar_contrasenia(contrasenia):
                    return usuario
                raise CredencialesInvalidasError("Mail o contraseña incorrectos")
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

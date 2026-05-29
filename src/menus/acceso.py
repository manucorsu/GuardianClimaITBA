# Funcionalidades utilizadas por el Menú de Acceso en main
from .. import csv_io
from ..password_strength import validar_password, criterios_strs
from ..choicer import choicer
from ..clear import clear
from ..types import OpcionesMenu
from pathlib import Path

path_csv_usuarios = Path("csv/usuarios_simulados.csv")
COLUMNAS_CSV_USUARIOS = ["username", "password_simulada"]

usuarios_simulados = csv_io.leer_o_crear(path_csv_usuarios, COLUMNAS_CSV_USUARIOS)


def registrar_usuario(username: str, password: str):
    username = username.strip().lower()
    if username == "":
        raise ValueError("El username no puede estar vacío.")
    for usuario in usuarios_simulados:
        if usuario["username"] == username:
            raise ValueError("El username ya existe. Por favor elige otro.")

    vp = validar_password(password, username)
    for criterio in criterios_strs:
        if vp[criterio] is not True:
            raise ValueError(
                f"El password no cumple el criterio de {criterio}: {criterios_strs[criterio]}"
            )

    usuarios_simulados.append({"username": username, "password_simulada": password})
    csv_io.escribir(path_csv_usuarios, COLUMNAS_CSV_USUARIOS, usuarios_simulados)
    return username


def registrar_usuario_prompt():
    clear()
    print("--Registrar usuario nuevo--")
    username = input("Nombre de usuario: ")
    password = ""
    while password == "":
        pw1 = input("Contraseña: ")
        pw2 = input("Repetir contraseña: ")
        if pw1 != pw2:
            print("Las contraseñas no coinciden. Por favor, volvé a intentarlo.")
        if pw1 == "":
            print("Debés ingresar una contraseña")
        else:
            password = pw1
    try:
        print("Registrando...", end="")
        ru = registrar_usuario(username, password)
        print("✅\nUsuario registrado exitosamente.\n")
        return ru
    except ValueError as ex:
        print(f"❌\n{ex}\n")


def login(username: str, password: str):
    username = username.strip().lower()
    for usuario in usuarios_simulados:
        if usuario["username"] == username and usuario["password_simulada"] == password:
            return username
    raise ValueError("Usuario o contraseña incorrecta.")


class OpcReintentarLogin(OpcionesMenu):
    REINTENTAR = "Reintentar"
    VOLVER_AL_MENU = "Volver al menú"


def login_prompt():
    clear()
    print("--Iniciar sesión--")
    u = None
    while u is None:
        try:
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            print("\nIniciando sesión...", end="")
            u = login(username, password)
            print("✅\nSesión iniciada exitosamente.\n")
        except ValueError as ex:
            print(f"❌\n{ex}\n")
            ch = choicer(list(OpcReintentarLogin))
            match (ch):
                case OpcReintentarLogin.REINTENTAR:
                    clear()
                    continue
                case OpcReintentarLogin.VOLVER_AL_MENU:
                    return None
    return u


class OpcMenuAcceso(OpcionesMenu):
    INICIAR_SESION = "Iniciar sesión"
    REGISTRAR_USUARIO = "Registrar nuevo usuario"
    SALIR = "Salir de la aplicación"


def menu_acceso():
    clear_menu_acceso = False
    username = None
    while username is None:
        if clear_menu_acceso:
            clear()
        else:
            clear_menu_acceso = True

        print("☀️  GuardiánClima ITBA ☀️\n")
        print("🚪 Menú de acceso\n")
        ch = choicer(list(OpcMenuAcceso))
        match (ch):
            case OpcMenuAcceso.INICIAR_SESION:
                username = login_prompt()
            case OpcMenuAcceso.REGISTRAR_USUARIO:
                username = registrar_usuario_prompt()
                clear_menu_acceso = False
            case OpcMenuAcceso.SALIR:
                print("Saliendo...")
                exit(0)
    return username

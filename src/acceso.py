# Funcionalidades utilizadas por el Menú de Acceso en main
from . import csv_io
from .password_strength import validar_password, criterios_strs
from .choicer import choicer

PATH_CSV_USUARIOS = "csv/usuarios_simulados.csv"
COLUMNAS_CSV_USUARIOS = ["username", "password_simulada"]

usuarios_simulados = csv_io.leer_o_crear(PATH_CSV_USUARIOS, COLUMNAS_CSV_USUARIOS)


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
    csv_io.escribir(PATH_CSV_USUARIOS, COLUMNAS_CSV_USUARIOS, usuarios_simulados)
    print("Usuario registrado exitosamente.")


def registrar_usuario_prompt():
    print("--Registrar usuario nuevo--")
    username = input("Nombre de usuario: ")
    password = ""
    while password == "":
        pw1 = input("Contraseña: ")
        pw2 = input("Repetir contraseña: ")
        if pw1 != pw2:
            print("Las contraseñas no coinciden. Por favor, volvé a intentarlo.")
        else:
            password = pw1
    try:
        print("Registrando...", end="")
        registrar_usuario(username, password)
        print("✅\nUsuario registrado exitosamente.\n")
    except ValueError as ex:
        print(f"❌\n{ex}")


def login(username: str, password: str):
    username = username.strip().lower()
    for usuario in usuarios_simulados:
        if usuario["username"] == username and usuario["password_simulada"] == password:
            return username
    raise ValueError("Usuario o contraseña incorrecta.")


def login_prompt():
    print("--Iniciar sesión--")
    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")
    u = None
    while u is None:
        try:
            print("Iniciando sesión...", end="")
            u = login(username, password)
            print("✅\nSesión iniciada exitosamente.\n")
        except ValueError as ex:
            print(f"❌\n{ex}")
            choice = choicer(["Reintentar", "Volver al menú"])
            if choice == 1:
                return None
    return u

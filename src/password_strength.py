from datetime import datetime

# Criterios (este diccionario se usa en mensajes de error):
criterios_strs = {
    "longitud": "No puede tener menos de 12 caracteres. Asegrate de que tu contraseña tenga al menos 12 caracteres para una mayor seguridad.",
    "contenido": "No puede contener el nombre de usuario, ser una contraseña común, contener el año actual o palabras relacionadas al clima o a la aplicación. Asegurate de que tu contraseña no incluya tu nombre de usuario, no sea una contraseña común (como '123456' o 'password'), no contenga el año actual, y no incluya palabras relacionadas al clima o a la aplicación para mejorar su seguridad.",
    "complejidad": "Debe mezclar diferentes tipos de caracteres (mayúsculas, minúsculas, números y símbolos). Asegurate de que tu contraseña incluya una combinación de mayúsculas, minúsculas, números y símbolos para aumentar su complejidad y resistencia a ataques.",
}

PASSWORDS_COMUNES = [
    "123456",
    "admin",
    "12345678",
    "123456789",
    "12345",
    "password",
    "Aa123456",
    "1234567890",
    "Pass@123",
    "admin123",
    "1234567",
    "123123",
    "111111",
    "12345678910",
    "P@ssw0rd",
    "Password",
    "Aa@123456",
    "admintelecom",
    "Admin@123",
    "112233",
]  #  fuente: la lista más reciente de https://en.wikipedia.org/wiki/List_of_the_most_common_passwords

PALABRAS_PROHIBIDAS = [
    "clima",
    "tiempo",
    "frio",
    "calor",
    "guardianclima",
    "itba",
    "climaitba",
    "guardianclimaitba",
]


def _longitud(password: str) -> bool:
    return len(password) >= 12


def _contenido(password: str, username: str) -> bool:
    def contiene_username(password: str, username: str) -> bool:
        return username.lower() in password.lower()

    def es_comun(password: str) -> bool:
        return password in PASSWORDS_COMUNES

    def contiene_el_anio_actual(password: str) -> bool:
        return str(datetime.now().year) in password

    def contiene_palabras_prohibidas(password: str) -> bool:
        lp = password.lower()
        for palabra in PALABRAS_PROHIBIDAS:
            if palabra.lower() in lp:
                return True
        return False

    return not (
        contiene_username(password, username)
        or es_comun(password)
        or contiene_el_anio_actual(password)
        or contiene_palabras_prohibidas(password)
    )


def _complejidad(password: str) -> bool:
    tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_simbolo = (
        False,
        False,
        False,
        False,
    )
    for c in password:
        if c.isupper():
            tiene_mayuscula = True
        elif c.islower():
            tiene_minuscula = True
        elif c.isdigit():
            tiene_numero = True
        else:
            tiene_simbolo = True
    return tiene_mayuscula and tiene_minuscula and tiene_numero and tiene_simbolo


def validar_password(password: str, username: str):
    return {
        "longitud": _longitud(password),
        "contenido": _contenido(password, username),
        "complejidad": _complejidad(password),
    }

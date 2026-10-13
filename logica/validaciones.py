# Funciones de validacion que usan las clases de la capa de logica
import re
from datetime import date, datetime

from logica.excepciones import ErrorValidacion


# Valida que el texto no este vacio y le quita los espacios sobrantes
def texto_no_vacio(valor, campo):
    if valor is None or str(valor).strip() == "":
        raise ErrorValidacion(f"El campo {campo} no puede estar vacío.")
    return str(valor).strip()


# Valida que el texto sean solo digitos con una longitud entre minimo y maximo
def solo_digitos(valor, campo, minimo, maximo):
    texto = texto_no_vacio(valor, campo)
    if not texto.isdigit():
        raise ErrorValidacion(f"El campo {campo} solo admite números.")
    if not minimo <= len(texto) <= maximo:
        raise ErrorValidacion(
            f"El campo {campo} debe tener entre {minimo} y {maximo} dígitos."
        )
    return texto


# Valida que el valor sea un numero (float) mayor a 0
def numero_mayor_0(valor, campo):
    try:
        numero = float(str(valor).replace(",", "."))
    except ValueError:
        raise ErrorValidacion(f"El campo {campo} debe ser un número.")
    if numero <= 0:
        raise ErrorValidacion(f"El campo {campo} debe ser mayor a 0.")
    return numero


# Valida el anio de nacimiento de la mascota (no puede ser a futuro)
def anio_valido(valor):
    try:
        anio = int(str(valor).strip())
    except ValueError:
        raise ErrorValidacion("El año de nacimiento debe ser un número.")
    anio_actual = date.today().year
    if not 1990 <= anio <= anio_actual:
        raise ErrorValidacion(
            f"El año de nacimiento debe estar entre 1990 y {anio_actual}."
        )
    return anio


# Valida el NIT con el formato 901456789-1
def validar_nit(valor):
    nit = texto_no_vacio(valor, "NIT")
    if re.fullmatch(r"\d{9}-\d", nit) is None:
        raise ErrorValidacion("El NIT debe tener el formato 901456789-1.")
    return nit


# Convierte un texto AAAA-MM-DD en un objeto date
def convertir_fecha(texto):
    try:
        return datetime.strptime(str(texto).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ErrorValidacion("La fecha debe tener el formato AAAA-MM-DD.")


# Convierte un texto HH:MM (24 horas) en un objeto time
def convertir_hora(texto):
    try:
        return datetime.strptime(str(texto).strip(), "%H:%M").time()
    except ValueError:
        raise ErrorValidacion(
            "La hora debe tener el formato HH:MM (24 horas).")


# Arma los codigos consecutivos como CIT-001 o FAC-001
def formatear_codigo(prefijo, numero):
    return f"{prefijo}-{numero:03d}"

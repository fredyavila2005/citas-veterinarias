# Excepciones personalizadas de la aplicacion de citas veterinarias


# Excepcion base: todas las demas heredan de esta, asi desde la
# presentacion basta con capturar ErrorClinica para mostrar el mensaje
class ErrorClinica(Exception):
    pass


# Se lanza cuando un dato digitado no cumple el formato esperado
class ErrorValidacion(ErrorClinica):
    pass


# Se lanza cuando se intenta registrar algo que ya existe (regla de negocio 7)
class ErrorDuplicado(ErrorClinica):
    pass


# Se lanza cuando se busca una clinica, cita, mascota, etc. que no existe
class ErrorNoEncontrado(ErrorClinica):
    pass


# Se lanza cuando un veterinario o una mascota ya tiene cita (reglas 2 y 3)
class ErrorDisponibilidad(ErrorClinica):
    pass


# Se lanza cuando la cita no esta en el estado que exige la operacion
# (reglas 4 y 5)
class ErrorCitaNoPermitida(ErrorClinica):
    pass

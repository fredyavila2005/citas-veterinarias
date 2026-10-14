# Parcial 2 - Programacion II: Citas veterinarias
#
# Estudiantes:
# Fredy Omar Avila Triana - 01251151005
# Andres Felipe Castilla Caselles - 01251151011
#
# Arquitectura en capas:
#   presentacion/ -> interfaz Gradio
#   logica/       -> clases del dominio y reglas de negocio
#   datos/        -> persistencia en json y datos de ejemplo
from datos.repositorio_json import RepositorioJSON
from logica.gestor_clinicas import GestorClinicas
from presentacion.interfaz import InterfazVeterinaria


class Main:
    def __init__(self):
        repositorio = RepositorioJSON()
        gestor = GestorClinicas(repositorio)
        self._interfaz = InterfazVeterinaria(gestor)

    def iniciar(self):
        self._interfaz.lanzar()


if __name__ == "__main__":
    Main().iniciar()

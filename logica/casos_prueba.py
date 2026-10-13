from logica.excepciones import ErrorClinica

NIT_HUELLITAS = "901456789-1"
NIT_PATITAS = "900987654-3"


# Ejecuta uno por uno los 5 casos de prueba del enunciado.
# Devuelve una lista de tuplas (caso, paso, exito, detalle) para mostrarla
# en la interfaz como evidencia.
def ejecutar_casos_prueba(gestor):
    resultados = []

    # Intenta una operacion y guarda si funciono o si fue rechazada
    def intentar(caso, paso, operacion):
        try:
            detalle = operacion()
            resultados.append((caso, paso, True, detalle))
        except ErrorClinica as error:
            resultados.append((caso, paso, False, str(error)))

    gestor.reiniciar()
    gestor.cargar_datos_ejemplo()

    # Caso 1: cita atendida con servicio adicional
    gestor.registrar_propietario(
        NIT_HUELLITAS, "1098765432", "Laura Méndez Plata", "3157894561",
        "Bucaramanga"
    )
    gestor.registrar_mascota(
        NIT_HUELLITAS, "1098765432", "Rocky", "Perro", "Criolla", 2023, 18
    )
    intentar(
        "Caso 1", "Programar consulta general",
        lambda: _texto_cita(gestor.programar_cita(
            NIT_HUELLITAS, "1098765432", "Rocky", "2026-11-10", "09:00", "CG"
        ))
    )
    intentar(
        "Caso 1", "Atender y agregar vacunación",
        lambda: _texto_factura(gestor.atender_cita("CIT-001", ["VAC"]))
    )

    # Caso 2: veterinario ocupado
    gestor.registrar_propietario(
        NIT_HUELLITAS, "1005678912", "Camila Duarte Serrano", "3204567812",
        "San Gil"
    )
    gestor.registrar_mascota(
        NIT_HUELLITAS, "1005678912", "Copito", "Conejo", "Cabeza de león",
        2025, 1.5
    )
    intentar(
        "Caso 2", "Desparasitación 9:00 con Juliana (ocupada)",
        lambda: _texto_cita(gestor.programar_cita(
            NIT_HUELLITAS, "1005678912", "Copito", "2026-11-10", "09:00",
            "DES", "63512478"
        ))
    )
    intentar(
        "Caso 2", "Desparasitación 10:00 con Juliana",
        lambda: _texto_cita(gestor.programar_cita(
            NIT_HUELLITAS, "1005678912", "Copito", "2026-11-10", "10:00",
            "DES", "63512478"
        ))
    )

    # Caso 3: cita cancelada
    gestor.registrar_propietario(
        NIT_PATITAS, "1102345678", "Andrés Rueda Ardila", "3016789023",
        "Piedecuesta"
    )
    gestor.registrar_mascota(
        NIT_PATITAS, "1102345678", "Luna", "Gato", "Siamés", 2022, 4
    )
    intentar(
        "Caso 3", "Programar ecografía",
        lambda: _texto_cita(gestor.programar_cita(
            NIT_PATITAS, "1102345678", "Luna", "2026-11-12", "15:00", "ECO"
        ))
    )
    intentar(
        "Caso 3", "Cancelar la cita el 11 de noviembre",
        lambda: f"La cita {gestor.cancelar_cita('CIT-003').codigo} quedó "
        f"Cancelada y no se genera factura."
    )

    # Caso 4: cancelacion no permitida
    intentar(
        "Caso 4", "Cancelar CIT-001 (ya atendida)",
        lambda: gestor.cancelar_cita("CIT-001").codigo
    )

    # Caso 5: consultas
    intentar(
        "Caso 5", "Citas de Huellitas el 10 de noviembre",
        lambda: " | ".join(
            f"{c.codigo}: {c.estado}"
            for c in gestor.citas_por_fecha(NIT_HUELLITAS, "2026-11-10")
        )
    )
    intentar(
        "Caso 5", "Historial de la gata Luna",
        lambda: " | ".join(
            f"{c.codigo}: {c.estado}"
            for c in gestor.historial_mascota(
                NIT_PATITAS, "1102345678", "Luna"
            )
        )
    )
    return resultados


def _texto_cita(cita):
    return (
        f"Cita {cita.codigo} programada con {cita.veterinario.nombre} "
        f"el {cita.fecha} a las {cita.hora.strftime('%H:%M')}."
    )


def _texto_factura(factura):
    return (
        f"Factura {factura.numero} por ${factura.total:,.0f}".replace(",", ".")
    )

# Funciones que arman los bloques HTML que se muestran en la interfaz
from html import escape


# Formatea un valor como pesos colombianos: $ 105.000
def formatear_pesos(valor):
    return f"$ {valor:,.0f}".replace(",", ".")


def aviso_ok(texto):
    return f'<div class="aviso aviso-ok">🐾 {escape(texto)}</div>'


def aviso_error(texto):
    return f'<div class="aviso aviso-error">⚠️ {escape(texto)}</div>'


# Encabezado de la aplicacion
def encabezado():
    return """
    <div class="carnet">
        <div class="huella">🐾</div>
        <div>
            <h1>Citas veterinarias</h1>
            <p>Parcial 2 · Programación II · Clínicas, mascotas y citas</p>
            <div class="equipo">
                <span>Fredy Omar Avila Triana · 01251151005</span>
                <span>Andres Felipe Castilla Caselles · 01251151011</span>
            </div>
        </div>
    </div>
    """


# Ficha con los datos de la clinica seleccionada
def ficha_clinica(clinica):
    if clinica is None:
        return (
            '<div class="ficha"><b>Ninguna clínica seleccionada</b>'
            '<small>Registre una clínica o cargue las clínicas de '
            'ejemplo en la primera pestaña.</small></div>'
        )
    return f"""
    <div class="ficha">
        <b>{escape(clinica.nombre)}</b>
        <small>NIT {escape(clinica.nit)} · DANE {escape(clinica.codigo_dane)}
        · {escape(clinica.municipio)}, {escape(clinica.departamento)}
        · {escape(clinica.direccion)}, barrio {escape(clinica.barrio)}</small>
    </div>
    """


# Factura de una cita atendida
def factura_html(factura):
    filas = ""
    for servicio in factura.servicios:
        filas += (
            f"<tr><td>{escape(servicio.codigo)}</td>"
            f"<td>{escape(servicio.nombre)}</td>"
            f'<td class="valor">{formatear_pesos(servicio.tarifa)}</td></tr>'
        )
    return f"""
    <div class="factura">
        <h3>Factura {escape(factura.numero)}</h3>
        <div>Fecha: {factura.fecha} ·
        Propietario: {escape(factura.propietario.nombre)}
        (C.C. {escape(factura.propietario.cedula)}) ·
        Mascota: {escape(factura.mascota.nombre)}</div>
        <table>
            <tr><th>Código</th><th>Servicio</th>
            <th class="valor">Tarifa</th></tr>
            {filas}
            <tr class="total"><td colspan="2">Valor total</td>
            <td class="valor">{formatear_pesos(factura.total)}</td></tr>
        </table>
    </div>
    """


# Lista de resultados de los casos de prueba
def casos_prueba_html(resultados):
    html = ""
    for caso, paso, exito, detalle in resultados:
        if exito:
            estado = '<span class="estado-ok">Aceptado</span>'
        else:
            estado = '<span class="estado-rechazo">Rechazado</span>'
        html += (
            f'<div class="paso"><div class="caso">{escape(caso)}</div>'
            f"<div><b>{escape(paso)}</b> · {estado}<br>"
            f"{escape(detalle)}</div></div>"
        )
    return html

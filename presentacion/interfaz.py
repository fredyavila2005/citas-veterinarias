import gradio as gr

from logica.casos_prueba import ejecutar_casos_prueba
from logica.excepciones import ErrorClinica
from presentacion import vistas_html as vistas
from presentacion.estilos import CSS_INTERFAZ

ENCABEZADOS_CITAS = [
    "Código", "Fecha", "Hora", "Mascota", "Propietario", "Veterinario",
    "Servicio", "Estado"
]


# Capa de presentacion: interfaz Gradio. Solo se comunica con el gestor.
class InterfazVeterinaria:
    def __init__(self, gestor):
        self._gestor = gestor
        self._demo = None

    # ------------------------------------------------------------------
    # Opciones de los desplegables (etiqueta, valor)
    # ------------------------------------------------------------------
    def _opciones_clinicas(self):
        return [
            (f"{c.nombre} · NIT {c.nit}", c.nit)
            for c in self._gestor.clinicas
        ]

    def _clinica_o_none(self, nit):
        try:
            return self._gestor.buscar_clinica(nit)
        except ErrorClinica:
            return None

    def _opciones_veterinarios(self, clinica):
        opciones = [("Asignar automáticamente", "")]
        for v in clinica.veterinarios:
            opciones.append(
                (f"{v.nombre} · {v.tarjeta_profesional}", v.cedula))
        return opciones

    def _opciones_servicios(self, clinica):
        return [
            (f"{s.codigo} · {s.nombre} · {vistas.formatear_pesos(s.tarifa)}",
             s.codigo)
            for s in clinica.servicios
        ]

    def _opciones_propietarios(self, clinica):
        return [
            (f"{p.nombre} · C.C. {p.cedula}", p.cedula)
            for p in clinica.propietarios
        ]

    def _opciones_citas(self, clinica):
        return [
            (f"{c.codigo} · {c.fecha} {c.hora.strftime('%H:%M')} · "
             f"{c.mascota.nombre} · {c.estado}", c.codigo)
            for c in clinica.citas
        ]

    # Convierte una lista de citas en filas para la tabla
    def _filas_citas(self, citas):
        filas = []
        for c in citas:
            filas.append([
                c.codigo, str(c.fecha), c.hora.strftime("%H:%M"),
                c.mascota.nombre, c.propietario.nombre,
                c.veterinario.nombre, c.servicio.nombre, c.estado
            ])
        return filas

    # ------------------------------------------------------------------
    # Refresco de la pantalla
    # ------------------------------------------------------------------
    # Actualiza el selector de clinicas, opcionalmente con un valor
    def refrescar_clinicas(self, nit_actual=None):
        opciones = self._opciones_clinicas()
        valores = [valor for _, valor in opciones]
        if nit_actual not in valores:
            nit_actual = valores[0] if valores else None
        return gr.update(choices=opciones, value=nit_actual)

    # Actualiza todos los componentes que dependen de la clinica activa
    def refrescar_dependientes(self, nit):
        clinica = self._clinica_o_none(nit)
        if clinica is None:
            vacio = gr.update(choices=[], value=None)
            return (
                vacio, vacio, gr.update(choices=[], value=[]), vacio, vacio,
                vacio, vacio, vacio, [], [], [], vistas.ficha_clinica(None)
            )
        servicios = self._opciones_servicios(clinica)
        propietarios = self._opciones_propietarios(clinica)
        citas = self._opciones_citas(clinica)
        return (
            gr.update(choices=self._opciones_veterinarios(clinica), value=""),
            gr.update(choices=servicios, value=None),
            gr.update(choices=servicios, value=[]),
            gr.update(choices=propietarios, value=None),
            gr.update(choices=propietarios, value=None),
            gr.update(choices=citas, value=None),
            gr.update(choices=citas, value=None),
            gr.update(choices=propietarios, value=None),
            [[v.cedula, v.nombre, v.tarjeta_profesional]
             for v in clinica.veterinarios],
            [[s.codigo, s.nombre, vistas.formatear_pesos(s.tarifa)]
             for s in clinica.servicios],
            [[p.cedula, p.nombre, p.telefono, p.municipio,
              ", ".join(m.nombre for m in p.mascotas)]
             for p in clinica.propietarios],
            vistas.ficha_clinica(clinica)
        )

    # Lista las mascotas del propietario escogido
    def cambiar_mascotas(self, nit, cedula):
        try:
            clinica = self._gestor.buscar_clinica(nit)
            propietario = clinica.buscar_propietario(cedula)
            opciones = [m.nombre for m in propietario.mascotas]
        except ErrorClinica:
            opciones = []
        return gr.update(choices=opciones, value=None)

    # ------------------------------------------------------------------
    # Acciones (cada una devuelve el aviso que se muestra al usuario)
    # ------------------------------------------------------------------
    def accion_registrar_clinica(self, nit, nombre, dane, municipio,
                                 departamento, direccion, barrio):
        try:
            clinica = self._gestor.registrar_clinica(
                nit, nombre, dane, municipio, departamento, direccion, barrio
            )
        except ErrorClinica as error:
            return vistas.aviso_error(str(error)), gr.update()
        aviso = vistas.aviso_ok(f"Clínica {clinica.nombre} registrada.")
        return aviso, self.refrescar_clinicas(clinica.nit)

    def accion_cargar_ejemplo(self, nit_actual):
        cargadas = self._gestor.cargar_datos_ejemplo()
        if cargadas == 0:
            aviso = vistas.aviso_error(
                "Las clínicas de ejemplo ya estaban cargadas."
            )
        else:
            aviso = vistas.aviso_ok(
                f"Se cargaron {cargadas} clínicas de ejemplo con sus "
                f"veterinarios y catálogos."
            )
        return aviso, self.refrescar_clinicas(nit_actual)

    def accion_registrar_veterinario(self, nit, cedula, nombre, tarjeta):
        try:
            v = self._gestor.registrar_veterinario(
                nit, cedula, nombre, tarjeta)
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return vistas.aviso_ok(f"Veterinario {v.nombre} registrado.")

    def accion_registrar_servicio(self, nit, codigo, nombre, tarifa):
        try:
            s = self._gestor.registrar_servicio(nit, codigo, nombre, tarifa)
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return vistas.aviso_ok(f"Servicio {s.nombre} agregado al catálogo.")

    def accion_registrar_propietario(self, nit, cedula, nombre, telefono,
                                     municipio):
        try:
            p = self._gestor.registrar_propietario(
                nit, cedula, nombre, telefono, municipio
            )
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return vistas.aviso_ok(f"Propietario {p.nombre} registrado.")

    def accion_registrar_mascota(self, nit, cedula, nombre, especie, raza,
                                 anio, peso):
        try:
            m = self._gestor.registrar_mascota(
                nit, cedula, nombre, especie, raza, anio, peso
            )
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return vistas.aviso_ok(f"Mascota {m.nombre} registrada.")

    def accion_programar(self, nit, cedula, mascota, fecha, hora, servicio,
                         cedula_vet):
        try:
            c = self._gestor.programar_cita(
                nit, cedula, mascota, fecha, hora, servicio, cedula_vet or ""
            )
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return vistas.aviso_ok(
            f"Cita {c.codigo} programada con {c.veterinario.nombre} para "
            f"{c.mascota.nombre} el {c.fecha} a las "
            f"{c.hora.strftime('%H:%M')}."
        )

    def accion_cancelar(self, codigo):
        try:
            c = self._gestor.cancelar_cita(codigo)
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return vistas.aviso_ok(
            f"La cita {c.codigo} fue cancelada. No se genera factura."
        )

    def accion_atender(self, codigo, adicionales):
        try:
            factura = self._gestor.atender_cita(codigo, adicionales)
        except ErrorClinica as error:
            return vistas.aviso_error(str(error))
        return (
            vistas.aviso_ok(f"Cita {codigo} atendida.")
            + vistas.factura_html(factura)
        )

    def accion_consultar_fecha(self, nit, fecha):
        try:
            citas = self._gestor.citas_por_fecha(nit, fecha)
        except ErrorClinica as error:
            return vistas.aviso_error(str(error)), []
        if not citas:
            return vistas.aviso_ok("No hay citas en esa fecha."), []
        return vistas.aviso_ok(f"{len(citas)} cita(s) encontradas."), \
            self._filas_citas(citas)

    def accion_consultar_historial(self, nit, cedula, mascota):
        try:
            citas = self._gestor.historial_mascota(nit, cedula, mascota)
        except ErrorClinica as error:
            return vistas.aviso_error(str(error)), []
        if not citas:
            return vistas.aviso_ok(f"{mascota} aún no tiene citas."), []
        return vistas.aviso_ok(f"Historial de {mascota}."), \
            self._filas_citas(citas)

    def accion_casos_prueba(self, nit_actual):
        resultados = ejecutar_casos_prueba(self._gestor)
        return (
            vistas.casos_prueba_html(resultados),
            self.refrescar_clinicas(nit_actual)
        )

    def accion_reiniciar(self):
        self._gestor.reiniciar()
        return (
            vistas.aviso_ok("Se borraron todos los datos."),
            self.refrescar_clinicas(None)
        )

    # ------------------------------------------------------------------
    # Construccion de la pantalla
    # ------------------------------------------------------------------
    def construir(self):
        # En Gradio 6 el css va en launch, en versiones anteriores en Blocks
        self._gradio_nuevo = int(gr.__version__.split(".")[0]) >= 6
        opciones = {"css": CSS_INTERFAZ, "theme": gr.themes.Soft()}
        argumentos_blocks = {"title": "Citas veterinarias"}
        if not self._gradio_nuevo:
            argumentos_blocks.update(opciones)
        self._opciones_launch = opciones if self._gradio_nuevo else {}

        with gr.Blocks(**argumentos_blocks) as demo:
            gr.HTML(vistas.encabezado())

            with gr.Row():
                dd_clinica = gr.Dropdown(
                    label="Clínica de trabajo",
                    choices=self._opciones_clinicas(),
                    value=None, scale=2
                )
                ficha = gr.HTML(vistas.ficha_clinica(None), scale=3)

            with gr.Tabs():
                # ---------------- 1. Clinicas ----------------
                with gr.Tab("🏥 Clínicas"):
                    with gr.Row():
                        c_nit = gr.Textbox(
                            label="NIT", placeholder="901456789-1")
                        c_nombre = gr.Textbox(label="Nombre de la clínica")
                        c_dane = gr.Textbox(
                            label="Código DANE", placeholder="68679")
                    with gr.Row():
                        c_municipio = gr.Textbox(label="Municipio")
                        c_departamento = gr.Textbox(label="Departamento")
                    with gr.Row():
                        c_direccion = gr.Textbox(label="Dirección")
                        c_barrio = gr.Textbox(label="Barrio")
                    with gr.Row():
                        btn_clinica = gr.Button(
                            "Registrar clínica", variant="primary")
                        btn_ejemplo = gr.Button(
                            "Cargar clínicas de ejemplo", variant="secondary")
                    out_clinica = gr.HTML()

                # ---------------- 2. Veterinarios y servicios ----------------
                with gr.Tab("🩺 Veterinarios y servicios"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Nuevo veterinario")
                            v_cedula = gr.Textbox(label="Cédula")
                            v_nombre = gr.Textbox(label="Nombre completo")
                            v_tarjeta = gr.Textbox(
                                label="Tarjeta profesional",
                                placeholder="TP-18452")
                            btn_vet = gr.Button(
                                "Registrar veterinario", variant="primary")
                            out_vet = gr.HTML()
                        with gr.Column():
                            gr.Markdown("### Nuevo servicio")
                            s_codigo = gr.Textbox(
                                label="Código", placeholder="CG")
                            s_nombre = gr.Textbox(label="Nombre del servicio")
                            s_tarifa = gr.Textbox(
                                label="Tarifa", placeholder="60000")
                            btn_serv = gr.Button(
                                "Agregar al catálogo", variant="primary")
                            out_serv = gr.HTML()
                    with gr.Row():
                        tabla_vets = gr.Dataframe(
                            headers=[
                                "Cédula", "Nombre", "Tarjeta profesional"],
                            label="Veterinarios de la clínica",
                            interactive=False
                        )
                        tabla_servicios = gr.Dataframe(
                            headers=["Código", "Servicio", "Tarifa"],
                            label="Catálogo de servicios",
                            interactive=False
                        )

                # ---------------- 3. Propietarios y mascotas ----------------
                with gr.Tab("🐶 Propietarios y mascotas"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Nuevo propietario")
                            p_cedula = gr.Textbox(label="Cédula de ciudadanía")
                            p_nombre = gr.Textbox(label="Nombre completo")
                            p_telefono = gr.Textbox(label="Teléfono")
                            p_municipio = gr.Textbox(
                                label="Municipio de residencia")
                            btn_prop = gr.Button(
                                "Registrar propietario", variant="primary")
                            out_prop = gr.HTML()
                        with gr.Column():
                            gr.Markdown("### Nueva mascota")
                            m_propietario = gr.Dropdown(
                                label="Propietario", choices=[])
                            m_nombre = gr.Textbox(label="Nombre de la mascota")
                            with gr.Row():
                                m_especie = gr.Textbox(
                                    label="Especie", placeholder="Perro")
                                m_raza = gr.Textbox(label="Raza")
                            with gr.Row():
                                m_anio = gr.Textbox(
                                    label="Año de nacimiento",
                                    placeholder="2023")
                                m_peso = gr.Textbox(
                                    label="Peso (kg)", placeholder="18")
                            btn_masc = gr.Button(
                                "Registrar mascota", variant="primary")
                            out_masc = gr.HTML()
                    tabla_props = gr.Dataframe(
                        headers=[
                            "Cédula",
                            "Nombre",
                            "Teléfono",
                            "Municipio",
                            "Mascotas"],
                        label="Propietarios de la clínica",
                        interactive=False
                    )

                # ---------------- 4. Programar cita ----------------
                with gr.Tab("📅 Programar cita"):
                    with gr.Row():
                        k_propietario = gr.Dropdown(
                            label="Propietario", choices=[])
                        k_mascota = gr.Dropdown(label="Mascota", choices=[])
                    with gr.Row():
                        k_fecha = gr.Textbox(
                            label="Fecha (AAAA-MM-DD)",
                            placeholder="2026-11-10")
                        k_hora = gr.Textbox(
                            label="Hora (HH:MM)", placeholder="09:00")
                    with gr.Row():
                        k_servicio = gr.Dropdown(label="Servicio", choices=[])
                        k_vet = gr.Dropdown(label="Veterinario", choices=[])
                    btn_cita = gr.Button("Programar cita", variant="primary")
                    out_cita = gr.HTML()

                # ---------------- 5. Cancelar ----------------
                with gr.Tab("❌ Cancelar cita"):
                    x_cita = gr.Dropdown(label="Cita", choices=[])
                    btn_cancelar = gr.Button("Cancelar cita", variant="stop")
                    out_cancelar = gr.HTML()

                # ---------------- 6. Atender ----------------
                with gr.Tab("💉 Atender y facturar"):
                    a_cita = gr.Dropdown(label="Cita", choices=[])
                    a_adicionales = gr.CheckboxGroup(
                        label="Servicios adicionales durante la atención",
                        choices=[]
                    )
                    btn_atender = gr.Button(
                        "Atender cita y generar factura", variant="primary")
                    out_atender = gr.HTML()

                # ---------------- 7. Consultas ----------------
                with gr.Tab("🔎 Consultas"):
                    gr.Markdown("### Citas de la clínica en una fecha")
                    with gr.Row():
                        q_fecha = gr.Textbox(
                            label="Fecha (AAAA-MM-DD)",
                            placeholder="2026-11-10")
                        btn_fecha = gr.Button(
                            "Consultar fecha", variant="primary")
                    out_fecha = gr.HTML()
                    tabla_fecha = gr.Dataframe(
                        headers=ENCABEZADOS_CITAS, interactive=False)

                    gr.Markdown("### Historial de una mascota")
                    with gr.Row():
                        h_propietario = gr.Dropdown(
                            label="Propietario", choices=[])
                        h_mascota = gr.Dropdown(label="Mascota", choices=[])
                        btn_historial = gr.Button(
                            "Ver historial", variant="primary")
                    out_historial = gr.HTML()
                    tabla_historial = gr.Dataframe(
                        headers=ENCABEZADOS_CITAS, interactive=False)

                # ---------------- 8. Casos de prueba ----------------
                with gr.Tab("🧪 Casos de prueba"):
                    gr.Markdown(
                        "Borra los datos, carga las clínicas de ejemplo y "
                        "ejecuta los 5 casos del enunciado en orden."
                    )
                    with gr.Row():
                        btn_casos = gr.Button(
                            "Ejecutar los 5 casos", variant="primary")
                        btn_reiniciar = gr.Button(
                            "Borrar todos los datos", variant="stop")
                    out_casos = gr.HTML()

            # ---------------- Conexion de eventos ----------------
            salidas_dep = [
                k_vet, k_servicio, a_adicionales, m_propietario,
                k_propietario, x_cita, a_cita, h_propietario,
                tabla_vets, tabla_servicios, tabla_props, ficha
            ]

            dd_clinica.change(
                self.refrescar_dependientes, [dd_clinica], salidas_dep
            )

            btn_clinica.click(
                self.accion_registrar_clinica,
                [c_nit, c_nombre, c_dane, c_municipio, c_departamento,
                 c_direccion, c_barrio],
                [out_clinica, dd_clinica]
            )
            btn_ejemplo.click(
                self.accion_cargar_ejemplo, [dd_clinica],
                [out_clinica, dd_clinica]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_vet.click(
                self.accion_registrar_veterinario,
                [dd_clinica, v_cedula, v_nombre, v_tarjeta], [out_vet]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_serv.click(
                self.accion_registrar_servicio,
                [dd_clinica, s_codigo, s_nombre, s_tarifa], [out_serv]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_prop.click(
                self.accion_registrar_propietario,
                [dd_clinica, p_cedula, p_nombre, p_telefono, p_municipio],
                [out_prop]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_masc.click(
                self.accion_registrar_mascota,
                [dd_clinica, m_propietario, m_nombre, m_especie, m_raza,
                 m_anio, m_peso], [out_masc]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            k_propietario.change(
                self.cambiar_mascotas, [dd_clinica, k_propietario], [k_mascota]
            )
            h_propietario.change(
                self.cambiar_mascotas, [dd_clinica, h_propietario],
                [h_mascota]
            )

            btn_cita.click(
                self.accion_programar,
                [dd_clinica, k_propietario, k_mascota, k_fecha, k_hora,
                 k_servicio, k_vet], [out_cita]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_cancelar.click(
                self.accion_cancelar, [x_cita], [out_cancelar]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_atender.click(
                self.accion_atender, [a_cita, a_adicionales], [out_atender]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            btn_fecha.click(
                self.accion_consultar_fecha, [dd_clinica, q_fecha],
                [out_fecha, tabla_fecha]
            )
            btn_historial.click(
                self.accion_consultar_historial,
                [dd_clinica, h_propietario, h_mascota],
                [out_historial, tabla_historial]
            )

            btn_casos.click(
                self.accion_casos_prueba, [dd_clinica],
                [out_casos, dd_clinica]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)
            btn_reiniciar.click(
                self.accion_reiniciar, None, [out_casos, dd_clinica]
            ).then(self.refrescar_dependientes, [dd_clinica], salidas_dep)

            # Al abrir la pagina se muestran las clinicas ya guardadas
            demo.load(
                self.refrescar_clinicas, [dd_clinica], [dd_clinica]
            )

        self._demo = demo
        return demo

    def lanzar(self):
        if self._demo is None:
            self.construir()
        self._demo.launch(**self._opciones_launch)

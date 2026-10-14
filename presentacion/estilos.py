# Estilos de la interfaz: paleta veterinaria (verde agua, azul cielo,
# amarillo girasol) con tipografia redondeada y amable
# Tipografias de Google Fonts (se separa en varias lineas por el PEP8)
FUENTES = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700"
    "&display=swap');\n"
)

CSS_INTERFAZ = FUENTES + """

:root {
    --v-pino: #0f4c5c;
    --v-mar: #1b7f8c;
    --v-menta: #d8f0e8;
    --v-cielo: #e6f3fb;
    --v-girasol: #f6c453;
    --v-coral: #e76f51;
    --v-papel: #f7fbfa;
    --v-borde: #b9dcd3;
    --v-texto: #17323a;
}

html, body, .gradio-container, .gradio-container.gradio-container {
    background: var(--v-papel) !important;
    color: var(--v-texto) !important;
    font-family: 'Nunito', sans-serif !important;
}
.gradio-container { max-width: 1180px !important; margin: 0 auto !important; }
footer { display: none !important; }

/* Encabezado tipo carnet de la clinica */
.carnet {
    display: grid;
    grid-template-columns: 96px 1fr;
    gap: 22px;
    align-items: center;
    background: linear-gradient(120deg, #0f4c5c 0%, #1b7f8c 100%);
    border-radius: 26px 26px 26px 6px;
    padding: 26px 30px;
    margin: 6px 0 18px;
    color: #ffffff;
    border-bottom: 6px solid var(--v-girasol);
}
.carnet .huella {
    width: 96px; height: 96px;
    background: var(--v-girasol);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 48px;
    box-shadow: 0 0 0 6px rgba(255,255,255,0.18);
}
.carnet h1 {
    font-family: 'Fredoka', sans-serif;
    font-size: 36px; font-weight: 700;
    margin: 0 0 4px; color: #ffffff;
}
.carnet p { margin: 0; color: #d8f0e8; font-size: 15px; }
.carnet .equipo { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.carnet .equipo span {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 999px; padding: 4px 12px; font-size: 12px;
}
@media (max-width: 700px) {
    .carnet { grid-template-columns: 1fr; }
}

/* Ficha de la clinica activa */
.ficha {
    background: var(--v-menta);
    border: 2px dashed var(--v-mar);
    border-radius: 18px;
    padding: 14px 18px;
    color: var(--v-pino);
}
.ficha b { font-family: 'Fredoka', sans-serif; font-size: 18px; }
.ficha small { display: block; margin-top: 2px; color: #3b6b66; }

/* Pestanas */
button[role="tab"] {
    font-family: 'Fredoka', sans-serif !important;
    font-weight: 600 !important;
    color: var(--v-mar) !important;
    font-size: 15px !important;
}
button[role="tab"][aria-selected="true"] {
    color: var(--v-pino) !important;
    border-color: var(--v-girasol) !important;
}

.block, .form, .panel, .gr-group {
    background: #ffffff !important;
    border-color: var(--v-borde) !important;
    border-radius: 16px !important;
}
label span, .block-label {
    color: var(--v-pino) !important;
    font-weight: 700 !important;
}
input, textarea, select {
    background: var(--v-papel) !important;
    color: var(--v-texto) !important;
    border: 1.5px solid var(--v-borde) !important;
    border-radius: 12px !important;
}
input:focus, textarea:focus {
    border-color: var(--v-mar) !important;
    box-shadow: 0 0 0 3px rgba(27,127,140,0.2) !important;
}

button.primary {
    background: var(--v-mar) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Fredoka', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border-radius: 999px !important;
}
button.primary:hover { background: var(--v-pino) !important; }
button.secondary {
    background: var(--v-girasol) !important;
    border: none !important;
    color: var(--v-pino) !important;
    font-family: 'Fredoka', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 999px !important;
}
button.stop {
    background: var(--v-coral) !important;
    border: none !important;
    color: #ffffff !important;
    border-radius: 999px !important;
}

/* Mensajes */
.aviso {
    border-radius: 14px; padding: 12px 16px; font-weight: 600;
    border-left: 8px solid;
}
.aviso-ok { background: #e3f6ec; border-color: #2a9d6f; color: #14513a; }
.aviso-error {
    background: #fdece6;
    border-color: var(--v-coral);
    color: #7a2a14;
}

/* Factura */
.factura {
    background: #ffffff;
    border: 2px solid var(--v-pino);
    border-radius: 18px;
    padding: 18px 22px;
    margin-top: 10px;
}
.factura h3 {
    font-family: 'Fredoka', sans-serif;
    margin: 0 0 4px;
    color: var(--v-pino);
}
.factura table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.factura td, .factura th {
    padding: 7px 4px;
    border-bottom: 1px dashed var(--v-borde);
    text-align: left;
}
.factura td.valor, .factura th.valor { text-align: right; }
.factura .total td {
    font-weight: 800;
    font-size: 18px;
    border-bottom: none;
    color: var(--v-pino);
}

/* Casos de prueba */
.paso {
    display: grid; grid-template-columns: 90px 1fr; gap: 12px;
    background: #ffffff; border: 1.5px solid var(--v-borde);
    border-radius: 14px; padding: 10px 14px; margin-bottom: 8px;
}
.paso .caso {
    font-family: 'Fredoka', sans-serif; font-weight: 600;
    color: var(--v-pino);
}
.paso .estado-ok { color: #2a9d6f; font-weight: 700; }
.paso .estado-rechazo { color: var(--v-coral); font-weight: 700; }
"""

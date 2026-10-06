const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak, BorderStyle } = require("docx");

const MONO = "Consolas", SANS = "Calibri", MUTED = "5B6676", ACC = "1F5F8B";
const p = (runs, o = {}) => new Paragraph({ spacing: { after: 60 }, ...o, children: runs });
const t = (text, o = {}) => new TextRun({ text, font: SANS, size: 20, ...o });
const code = (text, tag) => p([new TextRun({ text, font: MONO, size: 17 }),
  ...(tag ? [t("   " + tag, { size: 16, color: tag.startsWith("no") || tag.includes("A26") || tag === "gestión" ? "9A5B00" : "1D7A4C", bold: true })] : [])],
  { indent: { left: 240 }, spacing: { after: 30 } });
const h = (title, meta) => p([t(title, { bold: true, size: 23, color: ACC }), t("   " + meta, { size: 17, color: MUTED })],
  { spacing: { before: 200, after: 70 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "DDE2E8", space: 2 } } });
const nota = (text) => p([t(text, { size: 17, color: MUTED, italics: true })], { indent: { left: 240 } });
const kv = (k, v) => p([t(k + ": ", { bold: true, size: 18 }), t(v, { size: 18 })], { indent: { left: 240 }, spacing: { after: 30 } });

const hoja = [
  p([t("REM A04 · SECCIONES P–U · 2026", { size: 16, color: MUTED, bold: true })], { spacing: { after: 0 } }),
  p([t("Registro de actividades de epidemiología", { bold: true, size: 32 })], { spacing: { after: 40 } }),
  p([t("Actividad literal que alimenta cada casilla (REM Comentado Serie A 2026 · Maestro de Actividades). ", { size: 17, color: MUTED }),
     t("Q · R · S habilitadas: registrar ya.  ", { size: 17, bold: true, color: "1D7A4C" }),
     t("P · T · U: pedir habilitación.", { size: 17, bold: true, color: "9A5B00" })]),

  h("Q · Quimioprofilaxis para bloqueo", "Box / Pacientes citados · 18 actividades"),
  code("Entrega de quimioprofilaxis para bloqueo epidemiológico - [insumo] - [destino]"),
  kv("Insumo", "Vacunas · Inmunoglobulinas · Medicamentos antibioticos · Medicamentos antivirales · Medicamentos antiparasitarios · Otros medicamentos"),
  kv("Destino", "Lugar de trabajo · Institución · A grupo comunitario"),
  nota("Una actividad por insumo y destino. El rango etario sale del paciente."),

  h("R · Toma de muestras para vigilancia", "Box / Pacientes citados"),
  ...["sangre tomadas", "coprocultivos tomadas", "frotis hisopado nasofaríngeo", "aspirado tomadas", "hisopado de lesión cutáneas tomadas"]
    .map(s => code("Toma de muestras para vigilancia epidemiológica - N° muestras de " + s)),

  h("S · Seguimiento de casos y contactos", "Box / Pacientes citados"),
  p([t("Prefijo: ", { size: 17, color: MUTED }), new TextRun({ text: "Seguimiento de casos y contactos/expuestos via telefonica y visitas de seguimientos de casos y contactos/expuestos - ", font: MONO, size: 16 })], { indent: { left: 240 } }),
  ...["Llamadas - N° de llamadas a casos", "Llamadas - N° de llamadas a contactos/expuestos", "Seguimiento - N° de Visitas de seguimiento a casos", "Seguimiento - N° de Visitas de seguimiento a contactos/ expuestos"]
    .map(s => code("… " + s)),

  h("P · Encuesta epidemiológica", "Registro Atención Comunitaria"),
  code("Encuesta epidemiológica - Visita epidemiológica", "solo Enfermero/a"),
  code("Encuesta epidemiológica - A lugar de trabajo", "no habilitada"),
  code("Encuesta epidemiológica - A colegios, salas cuna, jardín infantil", "no habilitada"),
  code("Encuesta epidemiológica - A grupo comunitario", "no habilitada"),
  nota("Columnas según «Profesionales que participaron»: un profesional más un técnico va en «Un profesional»; dos o más profesionales más un técnico, en «Dos o más»."),

  h("T · Búsqueda activa institucional (BAI)", "Registro Atención Comunitaria · 9 actividades · no habilitadas"),
  code("Busqueda activa institucional (BAI) de casos - BAI [evento] - [registros]"),
  kv("Evento", "sarampión rubéola · febriles · otros eventos epidemiologicos"),
  kv("Registros revisados", "Menor de 100 registros · 100 a 250 registros · Mayor de 250 registros"),

  h("U · Búsqueda activa comunitaria (BAC)", "Registro Atención Comunitaria · no habilitadas"),
  code("Busqueda activa comunitaria (BAC) de casos - BAC febriles"),
  code("Busqueda activa comunitaria (BAC) de casos - BAC otros eventos epidemiológicos"),
  nota("T y U: en «Entidad comunitaria» se indica el centro donde se hace el registro."),

  h("No alimentan el A04", "gestión, o de otra hoja del REM"),
  code("Otras visitas integrales - Visita epidemiológica (Individual)", "cuenta en A26·B"),
  code("AG_Investigación Epidemiológica · AG_Búsqueda activa de casos de ENO", "gestión"),
  code("AG_Encuesta Epidemiológica - Con/Sin Riesgo · AG_Notificación … · AG_Visita epidemiológica …", "gestión"),
];

const par = (text, o = {}) => p([t(text, { size: 22 })], { spacing: { after: 140 }, ...o });
const item = (n, runs) => p([t(n + ". ", { size: 22, bold: true }), ...runs.map(r => typeof r === "string" ? t(r, { size: 22 }) : r)],
  { indent: { left: 360, hanging: 260 }, spacing: { after: 100 } });
const b = (s) => t(s, { size: 22, bold: true });

const solicitud = [
  new Paragraph({ children: [new PageBreak()] }),
  p([t("CESFAM Dr. Luis Ferrada Urzúa", { size: 20, color: MUTED })], { spacing: { after: 240 } }),
  p([t("Asunto: ", { bold: true, size: 24 }), t("Regularización del registro de actividades de epidemiología (REM A04, secciones P a U)", { size: 24 })], { spacing: { after: 280 } }),
  par("Las actividades de epidemiología se realizan, pero no hay actividad habilitada para registrar varias de ellas. Hoy se registran como actividades de gestión, y el REM A04 P a U se reporta en 0."),
  par("Se solicita habilitar en RAYEN, en el Registro de Atención Comunitaria:"),
  item(1, [b("Sección P: "), "«Encuesta epidemiológica - A lugar de trabajo», «- A colegios, salas cuna, jardín infantil» y «- A grupo comunitario»."]),
  item(2, [b("Sección P: "), "extender «Encuesta epidemiológica - Visita epidemiológica» a los estamentos que realizan la actividad (hoy, solo Enfermero/a)."]),
  item(3, [b("Sección T: "), "las 9 actividades «Busqueda activa institucional (BAI) de casos», es decir, 3 eventos (sarampión rubéola, febriles, otros eventos) por 3 rangos de registros revisados."]),
  item(4, [b("Sección U: "), "«Busqueda activa comunitaria (BAC) de casos - BAC febriles» y «- BAC otros eventos epidemiológicos»."]),
  par("Referencias: REM Comentado Serie A 2026 (15-04-2026), hoja A04, y Maestro de Actividades RAYEN.", { spacing: { before: 200, after: 140 } }),
];

const doc = new Document({
  styles: { default: { document: { run: { font: SANS } } } },
  sections: [{ properties: { page: { margin: { top: 850, bottom: 850, left: 1000, right: 1000 } } }, children: [...hoja, ...solicitud] }],
});
Packer.toBuffer(doc).then(buf => fs.writeFileSync(process.argv[2], buf));

import streamlit as st
import os
import json
from fpdf import FPDF
import datetime

# ==========================================
# LÓGICA DE RECOMENDACIÓN DE PRODUCTOS CISCO
# ==========================================
def generar_recomendaciones(q1, q2, q3, q4, q7, q8, q10_sec, q11, q_ha_b, q_ha_c, q_ha_d):
    recomendaciones = []
    
    if "modulares" in q1.lower() or "modulares" in q2.lower():
        recomendaciones.append("- Cisco UCS X-Series: Al buscar sistemas modulares y escalables, UCS X-Series con Intersight ofrece la flexibilidad para combinar nodos de cómputo y aceleradores PCIe (GPUs) adaptándose a las demandas de IA sin perder densidad.")
        
    if "reto" in q3.lower() or "adaptaremos" in q3.lower():
        recomendaciones.append("- Cisco Intersight Workload Optimizer (IWO) & Diseño Térmico UCS: Para abordar los retos de energía y enfriamiento, IWO permite optimizar la ubicación de cargas de trabajo para eficiencia energética, apoyado por el diseño térmico avanzado de los chasis UCS.")

    if "nube" in q4.lower():
        recomendaciones.append("- Cisco Intersight: Para una gestión centralizada, Intersight proporciona administración del ciclo de vida de la infraestructura, visibilidad y automatización desde una plataforma SaaS robusta.")
        
    if "importante" in q7.lower() or "certificadas" in q8.lower():
        recomendaciones.append("- Cisco Validated Designs (CVDs) - FlexPod / FlashStack: Para reducir el riesgo de integración, los CVDs ofrecen arquitecturas de red, cómputo y almacenamiento pre-probadas en conjunto con partners tecnológicos y certificadas para IA empresarial.")
        
    if "zero-trust" in q10_sec.lower() or "microsegmentación" in q11.lower() or "kernel" in q11.lower():
        recomendaciones.append("- Cisco Secure Workload (Tetration) & Cisco ACI: Para lograr protección a nivel de host, microsegmentación y seguridad Zero-Trust a nivel de carga de trabajo, estas soluciones protegen los entornos dinámicos de contenedores y clústeres de IA.")
        
    if "misión crítica" in q_ha_b.lower() or "misión crítica" in q_ha_c.lower() or "misión crítica" in q_ha_d.lower():
        recomendaciones.append("- Cisco Nexus 9000 Series (Lossless Network): Al ser un entorno de misión crítica, los switches Nexus garantizan un tejido de red sin pérdidas (RoCEv2), fundamental para que los clústeres de GPU no sufran interrupciones.")

    if not recomendaciones:
        recomendaciones.append("- Cisco UCS C-Series e Intersight: Con base en las respuestas, se sugiere una sesión consultiva uno a uno para afinar la arquitectura base y comenzar el camino de modernización.")

    return recomendaciones

# ==========================================
# FUNCIÓN AUXILIAR DE TEXTO PARA EL PDF
# ==========================================
def clean_txt(texto):
    """Limpieza extrema: elimina caracteres raros, saltos de línea y tabuladores que rompen FPDF."""
    if not texto:
        return "No especificado"
    texto_limpio = str(texto).replace('\n', ' ').replace('\r', '').replace('\t', ' ').strip()
    return texto_limpio.encode('latin-1', 'replace').decode('latin-1')

# ==========================================
# GENERACIÓN DE PDF ESTILO CORPORATIVO
# ==========================================
class PDF(FPDF):
    def header(self):
        try:
            self.image('logo_typhoon.jpg', 15, 10, 25)
            self.image('logo_cisco.jpg', 170, 10, 25)
        except Exception:
            pass 
        self.set_y(45)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def crear_pdf(datos_proyecto, datos_cuestionario, recomendaciones):
    pdf = PDF()
    
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- LA SOLUCIÓN UNIVERSAL PARA LA NUBE ---
    # Calculamos el ancho de forma matemática para que no falle en Streamlit Cloud
    epw = pdf.w - pdf.l_margin - pdf.r_margin 
    # ------------------------------------------
    
    # --- Título Principal ---
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(epw, 6, clean_txt('Acta de Evaluación - Data Center Compute (AI-Ready)'), ln=1, align='C')
    pdf.set_font('helvetica', '', 11)
    pdf.cell(epw, 6, clean_txt('Elaborado por: Best - Typhoon Technology'), ln=1, align='C')
    pdf.ln(8)
    
    # --- 1. Información General del Proyecto ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(epw, 8, clean_txt(' 1. Información General del Cliente'), ln=1, fill=True)
    pdf.ln(4)
    
    # Fila 1: Empresa y Contacto
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Empresa:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(75, 6, clean_txt(datos_proyecto.get('Nombre de la empresa')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Contacto:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('Contacto principal')), ln=1)
    
    # Fila 2: Correo y Puesto
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Correo:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(75, 6, clean_txt(datos_proyecto.get('Correo electrónico')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Puesto:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('Puesto')), ln=1)

    # Fila 3: Vertical y AM Cisco
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Vertical:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(75, 6, clean_txt(datos_proyecto.get('Vertical de negocio')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'AM Cisco:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('AM de Cisco')), ln=1)
    
    # Fila 4: Fecha y Responsable
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Fecha:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(75, 6, clean_txt(datos_proyecto.get('Fecha de evaluación')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 6, 'Responsable Best:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('Responsable de Best')), ln=1)
    pdf.ln(8)
    
    # --- 2. Record de Respuestas del Cliente ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(epw, 8, clean_txt(' 2. Cuestionario de Evaluación y Respuestas'), ln=1, fill=True)
    pdf.ln(4)
    
    for idx, item in enumerate(datos_cuestionario, start=1):
        pdf.set_x(15)
        pdf.set_font('helvetica', 'B', 10)
        pdf.multi_cell(0, 5, txt=clean_txt(item['pregunta']), align='L')
        
        pdf.set_x(15)
        pdf.set_font('helvetica', '', 10)
        texto_respuesta = f"Respuesta: {item['respuesta']}" if item['respuesta'] else "Respuesta: (Sin respuesta)"
        pdf.multi_cell(0, 5, txt=clean_txt(texto_respuesta), align='L')
        
        if item.get('nota') and str(item['nota']).strip() != "":
            pdf.set_x(15)
            pdf.set_font('helvetica', 'I', 9)
            texto_nota = f"Notas adicionales: {item['nota'].strip()}"
            pdf.multi_cell(0, 5, txt=clean_txt(texto_nota), align='L')
            
        pdf.ln(5)
        
    # --- 3. Soluciones Cisco Sugeridas ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(epw, 8, clean_txt(' 3. Soluciones Cisco Recomendadas'), ln=1, fill=True)
    pdf.ln(6)
    
    pdf.set_font('helvetica', '', 10)
    for rec in recomendaciones:
        pdf.set_x(15)
        pdf.multi_cell(0, 6, txt=clean_txt(rec), align='L')
        pdf.ln(4)
        
    pdf.ln(6)
    pdf.set_font('helvetica', 'U', 10)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(epw, 6, 'Link de referencia del portafolio Cisco Data Center', link="https://www.cisco.com/c/es_mx/solutions/data-center-virtualization/index.html", ln=1, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)
    
    pdf.set_font('helvetica', 'I', 9)
    disclaimer = "Nota importante: Esta información es una sugerencia preliminar generada a partir de los datos proporcionados. Queda estrictamente sujeta a los comentarios, validación técnica y diseño formal por parte de un profesional preventa o arquitecto de soluciones certificado de Typhoon Technology."
    pdf.set_x(15)
    pdf.multi_cell(0, 4, txt=clean_txt(disclaimer), align='C')
        
    return bytes(pdf.output())
# ==========================================
# INTERFAZ DE STREAMLIT
# ==========================================
st.set_page_config(page_title="Evaluación AI-Ready - Typhoon", page_icon="⚙️", layout="wide")

st.title("Formulario de Evaluación de Cómputo para Data Center (AI-Ready)")
st.markdown("**Partner de Cisco: Typhoon Technology**")
st.info("Complete este cuestionario simplificado para descubrir la arquitectura de Data Center recomendada para sus proyectos.")

# --- Sección: Información General ---
st.header("Información General del Proyecto")
col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input("Nombre de la empresa*")
    contacto = st.text_input("Contacto principal")
    correo = st.text_input("Correo electrónico")
    
    opciones_verticales = [
        "Seleccione una opción...", "Tecnología y Telecomunicaciones", "Finanzas y Banca", 
        "Salud y Farmacéutica", "Educación", "Retail y Comercio", 
        "Manufactura y Logística", "Gobierno y Sector Público", "Otro"
    ]
    vertical = st.selectbox("Vertical de negocio", opciones_verticales)

with col2:
    puesto = st.text_input("Puesto")
    am_cisco = st.text_input("AM de Cisco")
    responsable = st.text_input("Responsable de Best", value="Ana")
    fecha = st.date_input("Fecha de evaluación", datetime.date.today())

st.divider()

# --- SECCIÓN A ---
st.header("Sección A: Preparación de la Infraestructura")

t_q1 = "1. ¿Cómo planea implementar los servidores con GPU necesarios para sus proyectos de Inteligencia Artificial (IA)?"
q1 = st.radio(t_q1, [
    "Servidores dedicados y de altísima densidad (buscamos el máximo rendimiento).",
    "Sistemas modulares que permitan agregar GPUs poco a poco según se necesite.",
    "Instancias de GPU rentadas en la nube pública.",
    "Aún no tenemos una estrategia definida para escalar el uso de GPUs."
])
q1_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q1", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 1...")

st.write("---")
t_q2 = "2. Para las tareas de soporte (como preparación de datos) que requieren más CPU y memoria tradicional, ¿qué infraestructura utilizará?"
q2 = st.radio(t_q2, [
    "Plataformas modulares que se adapten ágilmente a los cambios de CPU/Memoria.",
    "Servidores tradicionales dedicados de propósito general.",
    "Principalmente recursos basados en la nube.",
    "Aún estamos evaluando la mejor arquitectura para estas tareas."
])
q2_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q2", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 2...")

st.write("---")
t_q3 = "3. ¿Qué nivel de preparación tiene su centro de datos en cuanto a energía y enfriamiento para soportar los nuevos equipos de IA?"
q3 = st.radio(t_q3, [
    "Total: Estamos diseñando proactivamente para alta densidad y enfriamiento avanzado.",
    "Parcial: Adaptaremos la infraestructura actual, asumiendo algunas actualizaciones.",
    "Bajo: Anticipamos que la energía y el enfriamiento serán un reto muy grande.",
    "Nulo: Aún no hemos evaluado el impacto físico en nuestro centro de datos."
])
q3_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q3", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 3...")

# --- SECCIÓN B ---
st.header("Sección B: Gestión y Eficiencia")

t_q4 = "4. ¿Cómo planea administrar y automatizar toda su infraestructura de IA?"
q4 = st.radio(t_q4, [
    "Mediante una plataforma única gestionada desde la nube para todo el ciclo de vida.",
    "Con herramientas de automatización locales (On-Premise).",
    "Principalmente con procesos manuales y scripts propios.",
    "Gestión reactiva: resolveremos las tareas conforme vayan apareciendo."
])
q4_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q4", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 4...")

st.write("---")
t_q5 = "5. ¿Cómo optimizarán el uso y rendimiento de las GPUs en sus diferentes tareas de IA?"
q5 = st.radio(t_q5, [
    "Orquestación avanzada (ej. Kubernetes o Slurm) para la asignación dinámica.",
    "Programación y asignación básica o manual de los recursos.",
    "Optimización dependiente de cada aplicación individual.",
    "Actualmente no tenemos una estrategia de optimización definida."
])
q5_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q5", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 5...")

st.write("---")
t_q6 = "6. En términos de gestión diaria, ¿qué tan crítica es la alta disponibilidad para sus procesos de IA?"
q_ha_b = st.radio(t_q6, [
    "De misión crítica: Cualquier caída impacta directamente al negocio.",
    "Importante: Se toleran caídas menores si existen planes de recuperación.",
    "Deseable: Es útil, pero no es nuestra prioridad de diseño principal.",
    "No es prioridad: Nuestras iniciativas actuales no requieren alta disponibilidad."
])
q6_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q6", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 6...")

# --- SECCIÓN C ---
st.header("Sección C: Integración y Ecosistema")

t_q7 = "7. ¿Qué valor le dan a adquirir una solución prevalidada (cómputo, red y almacenamiento ya integrados) para reducir riesgos?"
q7 = st.radio(t_q7, [
    "Extremadamente importante: Buscamos simplicidad y garantía de compatibilidad.",
    "Moderadamente importante: Vemos beneficios, pero podríamos integrarlo nosotros mismos.",
    "Poco importante: Preferimos armar la solución pieza por pieza para mayor control.",
    "No es un factor a considerar en nuestra estrategia actual."
])
q7_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q7", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 7...")

st.write("---")
t_q8 = "8. ¿Cómo garantizarán la compatibilidad entre el hardware nuevo y el software de IA (ej. NVIDIA AI Enterprise)?"
q8 = st.radio(t_q8, [
    "Priorizando soluciones de hardware y software que ya vengan certificadas juntas.",
    "Confiando en nuestros equipos internos para hacer la integración a la medida.",
    "Apoyándonos fuertemente en el soporte y consultoría del fabricante.",
    "Resolviendo la integración sobre la marcha según se necesite."
])
q8_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q8", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 8...")

st.write("---")
t_q9 = "9. A nivel de integración de red, ¿qué tan crítica es la alta disponibilidad para sus clústeres de IA?"
q_ha_c = st.radio(t_q9, [
    "De misión crítica: Cualquier caída impacta directamente al negocio.",
    "Importante: Se toleran caídas menores si existen planes de recuperación.",
    "Deseable: Es útil, pero no es nuestra prioridad de diseño principal.",
    "No es prioridad: Nuestras iniciativas actuales no requieren alta disponibilidad."
])
q9_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q9", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 9...")

# --- SECCIÓN D ---
st.header("Sección D: Seguridad y Protección de Datos")

t_q10 = "10. ¿Cómo protegerán los servidores de IA, los datos almacenados y el acceso a sus modelos confidenciales?"
q10_sec = st.radio(t_q10, [
    "Arquitectura Zero-Trust integral: seguridad en host, acceso granular y encriptación.",
    "Políticas estándar: parches de servidores y control de acceso básico.",
    "Seguridad a nivel de aplicación (ej. la que ofrezca la plataforma nativa).",
    "Aún estamos definiendo nuestra estrategia de seguridad para IA."
])
q10_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q10", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 10...")

st.write("---")
t_q11 = "11. Para cargas de trabajo dinámicas (contenedores/Kubernetes), ¿cómo implementarán la seguridad en la red?"
q11 = st.radio(t_q11, [
    "Seguridad avanzada a nivel de kernel para proteger procesos específicos.",
    "Microsegmentación de red para aislar cargas de trabajo.",
    "Agentes de seguridad tradicionales instalados en cada host.",
    "Firewalls tradicionales y listas de control de acceso (ACLs) perimetrales."
])
q11_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q11", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 11...")

st.write("---")
t_q12 = "12. En cuanto a ciberseguridad, ¿qué tan vital es mantener sus operaciones de IA siempre disponibles ante amenazas?"
q_ha_d = st.radio(t_q12, [
    "De misión crítica: Cualquier caída impacta directamente al negocio.",
    "Importante: Se toleran caídas menores si existen planes de recuperación.",
    "Deseable: Es útil, pero no es nuestra prioridad de diseño principal.",
    "No es prioridad: Nuestras iniciativas actuales no requieren alta disponibilidad."
])
q12_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q12", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 12...")

# --- SECCIÓN E & F ---
st.header("Secciones E & F: Preguntas Abiertas y Cómputo Confidencial")

t_q13 = "13. ¿Cuál es el mayor reto que prevé al comprar, instalar y operar su nueva infraestructura de IA?"
q13 = st.text_area(t_q13)

t_q14 = "14. ¿Cómo se imagina que crecerá su centro de datos en los próximos 3 a 5 años para soportar el avance de la IA?"
q14 = st.text_area(t_q14)

st.markdown("*Nota: El Cómputo Confidencial encripta los datos mientras se están procesando en memoria (Requiere procesadores modernos Intel/AMD o GPUs NVIDIA de última generación).*")
t_q15 = "15. ¿Qué porcentaje de su entorno actual soporta Cómputo Confidencial?"
q15 = st.selectbox(t_q15, [
    "75%-100%", "50%-74%", "25%-49%", "0%-24%"
])
q15_nota = st.text_area("Anotaciones adicionales (Opcional):", key="nota_q15", height=68, label_visibility="collapsed", placeholder="Anotaciones adicionales para la pregunta 15...")

st.divider()

# --- Bloque de Botón y Guardado en Sesión ---
if st.button("Generar Evaluación y Recomendaciones", type="primary"):
    if not empresa:
        st.warning("Por favor, ingresa al menos el 'Nombre de la empresa' para generar el documento.")
    else:
        vertical_final = vertical if vertical != "Seleccione una opción..." else ""
        
        datos_proyecto = {
            "Nombre de la empresa": empresa,
            "Contacto principal": contacto,
            "Correo electrónico": correo,
            "Puesto": puesto,
            "AM de Cisco": am_cisco,
            "Responsable de Best": responsable,
            "Fecha de evaluación": fecha.strftime("%d/%m/%Y"),
            "Vertical de negocio": vertical_final
        }
        
        datos_cuestionario = [
            {"pregunta": t_q1, "respuesta": q1, "nota": q1_nota},
            {"pregunta": t_q2, "respuesta": q2, "nota": q2_nota},
            {"pregunta": t_q3, "respuesta": q3, "nota": q3_nota},
            {"pregunta": t_q4, "respuesta": q4, "nota": q4_nota},
            {"pregunta": t_q5, "respuesta": q5, "nota": q5_nota},
            {"pregunta": t_q6, "respuesta": q_ha_b, "nota": q6_nota},
            {"pregunta": t_q7, "respuesta": q7, "nota": q7_nota},
            {"pregunta": t_q8, "respuesta": q8, "nota": q8_nota},
            {"pregunta": t_q9, "respuesta": q_ha_c, "nota": q9_nota},
            {"pregunta": t_q10, "respuesta": q10_sec, "nota": q10_nota},
            {"pregunta": t_q11, "respuesta": q11, "nota": q11_nota},
            {"pregunta": t_q12, "respuesta": q_ha_d, "nota": q12_nota},
            {"pregunta": t_q13, "respuesta": q13, "nota": ""},
            {"pregunta": t_q14, "respuesta": q14, "nota": ""},
            {"pregunta": t_q15, "respuesta": q15, "nota": q15_nota}
        ]
        
        recomendaciones = generar_recomendaciones(q1, q2, q3, q4, q7, q8, q10_sec, q11, q_ha_b, q_ha_c, q_ha_d)
        
        # Generamos el PDF con los datos validados
        pdf_bytes = crear_pdf(datos_proyecto, datos_cuestionario, recomendaciones)
        nombre_archivo = f"DC_Assessment_Compute_{empresa.replace(' ', '_')}.pdf"
        
        # Guardamos en la memoria del navegador
        st.session_state['pdf_bytes'] = pdf_bytes
        st.session_state['nombre_archivo'] = nombre_archivo
        st.session_state['empresa'] = empresa
        st.session_state['recomendaciones'] = recomendaciones
        
        # Guardado en archivo JSON local de respaldo
        registro = {
            "fecha_registro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": datos_proyecto,
            "respuestas": datos_cuestionario,
            "recomendaciones": recomendaciones
        }
        archivo_json = "evaluaciones_dc.json"
        datos_guardados = []
        if os.path.exists(archivo_json):
            try:
                with open(archivo_json, "r", encoding="utf-8") as f:
                    datos_guardados = json.load(f)
            except json.JSONDecodeError:
                datos_guardados = []
        
        datos_guardados.append(registro)
        with open(archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos_guardados, f, indent=4, ensure_ascii=False)

# --- Mostrar Resultados y Botón de Descarga Nativo ---
if 'pdf_bytes' in st.session_state:
    st.success(f"¡El documento para {st.session_state['empresa']} se ha generado y está listo para descargar!")
    
    st.subheader("Arquitectura Cisco Sugerida")
    for rec in st.session_state['recomendaciones']:
        st.write(rec)
        
    st.write("---")
    # Botón nativo estándar de Streamlit
    st.download_button(
        label="📄 Descargar Documento en PDF",
        data=st.session_state['pdf_bytes'],
        file_name=st.session_state['nombre_archivo'],
        mime="application/pdf"
    )
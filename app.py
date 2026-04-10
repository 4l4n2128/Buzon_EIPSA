import streamlit as st
from supabase import create_client

# --- 1. CONFIGURACIÓN (PON TUS LLAVES AQUÍ) ---
URL_SUPABASE = "https://mpcatrdfwzrjmkqqystj.supabase.co"
KEY_SUPABASE = "sb_publishable_mJaq6bbofO2QE7Ms9yIWxg_NzbkFNi_"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# --- 2. DISEÑO PROFESIONAL EIPSA ---
st.set_page_config(page_title="Buzón RH EIPSA", page_icon="📩")

# Estilo CSS para colores corporativos
st.markdown("""
    <style>
    .stButton>button { background-color: #003366; color: white; border-radius: 5px; }
    h1 { color: #b30000; }
    </style>
    """, unsafe_allow_html=True)

st.image("logo_eipsa.png", width=200) 
st.title("📩 Buzón de Atención al Empleado")
st.subheader("Especialistas en Instrumentación y Procesos S.A.")
st.markdown("---")

# --- 3. SISTEMA DE SEGURIDAD (CANDADO) ---
id_empleado = st.text_input("1. Ingresa tu ID de Empleado:")

if id_empleado:
    # Buscamos al trabajador en la base de datos
    consulta = supabase.table("Personal_EIPSA").select("*").eq("ID_Empleado", id_empleado).execute()
    
    if consulta.data:
        empleado = consulta.data[0] # Tomamos los datos del trabajador encontrado
        
        # SEGUNDO PASO: Pedir RFC (Se verá con puntitos ••••)
        rfc_usuario = st.text_input("2. Ingresa tu RFC para confirmar identidad:", type="password")
        
        if rfc_usuario:
            # Validamos que el RFC coincida (ignorando mayúsculas/minúsculas)
            if rfc_usuario.upper() == str(empleado['RFC']).upper():
                st.success(f"✅ Identidad confirmada: {empleado['Título']}")
                st.markdown("---")
                
                # --- INICIO DEL MENÚ BASADO EN TU DIAGRAMA ---
                whatsapp = st.text_input("Número de WhatsApp para que RH te contacte:")
                
                if whatsapp:
                    st.write("### Selecciona el trámite que deseas realizar")
                    tema = st.selectbox("Categoría principal:", 
                                        ["Selecciona...", "1.- Rotaciones", "2.- Nóminas", "3.- Permisos", "4.- Ambiente laboral"])

                    # --- 1. ROTACIONES ---
                    if tema == "1.- Rotaciones":
                        op1 = st.radio("Opciones de Rotación:", ["1.1.- Solicitud de rotación", "1.1.2.- Viáticos no pagados", "1.2.- Solicitud bono por no rotación"])
                        if "1.1.2" in op1:
                            st.warning("Especifique montos y conceptos no pagados.")
                            st.text_area("Detalles de viáticos:")
                            st.file_uploader("Sube evidencias (Fotos/PDF):", type=["png", "jpg", "pdf"])
                        else:
                            st.text_area("Información adicional (trayecto, fechas):")

                    # --- 2. NÓMINAS ---
                    elif tema == "2.- Nóminas":
                        op2 = st.selectbox("Opciones de Nómina:", ["2.1.- Descuentos", "2.2.- Faltas", "2.3.- INFONAVIT", "2.4.- Préstamo"])
                        if "2.2" in op2:
                            sub_f = st.radio("Tipo de reporte:", ["2.2.1.- Solicitud de faltas", "2.2.2.- Tengo una falta pero sí vine"])
                            if "2.2.2" in sub_f:
                                st.date_input("Fecha de la asistencia no reconocida:")
                                st.file_uploader("Sube evidencia (Listas de raya, ART):", type=["png", "jpg", "pdf"])

                    # --- 3. PERMISOS ---
                    elif tema == "3.- Permisos":
                        st.radio("Tipo de permiso:", ["3.1.- Con goce de sueldo", "3.2.- Sin goce de sueldo"])
                        st.text_area("Explica brevemente el motivo:")
                        st.info("Nota: Deberás entregar el formato físico en las oficinas de RH.")

                    # --- 4. AMBIENTE LABORAL ---
                    elif tema == "4.- Ambiente laboral":
                        op4 = st.selectbox("Opciones:", ["4.1.- Mobbing (Acoso)", "4.2.- Capacitaciones"])
                        if "4.1" in op4:
                            st.error("Reporte confidencial de Acoso Laboral")
                            st.text_area("Describe la situación detalladamente:")
                        else:
                            st.text_input("¿Qué capacitación te gustaría recibir?")

                    # BOTÓN FINAL
                    if st.button("Enviar Reporte a RH"):
                        # Aquí mañana programaremos que se guarde en una tabla de "Reportes"
                        st.balloons()
                        st.success(f"¡Gracias {empleado['Título']}! Tu reporte ha sido recibido. RH te contactará al {whatsapp}.")
            else:
                st.error("❌ El RFC no coincide. Verifica tu información.")
    else:
        st.error("❌ ID de empleado no encontrado.")
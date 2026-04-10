import streamlit as st
from supabase import create_client

# --- 1. CONFIGURACIÓN (PON TUS LLAVES AQUÍ) ---
URL_SUPABASE = "https://mpcatrdfwzrjmkqqystj.supabase.co"
KEY_SUPABASE = "sb_publishable_mJaq6bbofO2QE7Ms9yIWxg_NzbkFNi_"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# --- 2. DISEÑO PROFESIONAL EIPSA ---
st.set_page_config(page_title="Buzón RH EIPSA", page_icon="📩")

st.markdown("""
    <style>
    .stButton>button { background-color: #003366; color: white; border-radius: 5px; width: 100%; }
    h1 { color: #b30000; }
    </style>
    """, unsafe_allow_html=True)

st.image("logo_eipsa.png", width=200) 
st.title("📩 Buzón de Atención al trabajador EIPSO")
st.subheader("ELECTRICIDAD INDUSTRIAL DE POTENCIA")
st.markdown("---")

# --- 3. SISTEMA DE SEGURIDAD (CANDADO) ---
id_empleado = st.text_input("1. Ingresa tu número de casco:")

if id_empleado:
    consulta = supabase.table("Personal_EIPSA").select("*").eq("ID_Empleado", id_empleado).execute()
    
    if consulta.data:
        empleado = consulta.data[0] # Tomamos el primer registro
        
        rfc_usuario = st.text_input("2. Ingresa tu RFC para confirmar identidad:", type="password")
        
        if rfc_usuario:
            if rfc_usuario.upper() == str(empleado['RFC']).upper():
                st.success(f"✅ Identidad confirmada: {empleado['Título']}")
                st.markdown("---")
                
                # --- INICIO DEL FORMULARIO ---
                whatsapp = st.text_input("Número de WhatsApp para contacto:")
                
                if whatsapp:
                    tema = st.selectbox("¿Qué tema deseas consultar?", 
                                        ["Selecciona...", "1.- Rotaciones", "2.- Nóminas", "3.- Permisos", "4.- Ambiente laboral"])

                    opcion_final = "" # Variable para guardar la sub-opción

                    if tema == "1.- Rotaciones":
                        opcion_final = st.radio("Opciones:", ["1.1.- Solicitud de rotación", "1.1.2.- Viáticos no pagados", "1.2.- Solicitud bono no rotación"])
                    
                    elif tema == "2.- Nóminas":
                        opcion_final = st.selectbox("Opciones:", ["2.1.- Descuentos", "2.2.- Faltas", "2.3.- INFONAVIT", "2.4.- Préstamo"])
                    
                    elif tema == "3.- Permisos":
                        opcion_final = st.radio("Tipo:", ["3.1.- Con goce", "3.2.- Sin goce"])
                    
                    elif tema == "4.- Ambiente laboral":
                        opcion_final = st.selectbox("Opciones:", ["4.1.- Mobbing (Acoso)", "4.2.- Capacitaciones"])

                    if tema != "Selecciona...":
                        detalles = st.text_area("Explica detalladamente tu situación:")
                        archivo_evidencia = st.file_uploader("Sube una evidencia (foto o PDF) - Opcional:", type=["png", "jpg", "jpeg", "pdf"])

                        # --- BOTÓN DE ENVÍO FINAL ---
                        if st.button("🚀 ENVIAR REPORTE A RH"):
                            with st.spinner("Procesando tu reporte..."):
                                url_archivo = ""
                                
                                # A. Subida de archivo si existe
                                if archivo_evidencia:
                                    try:
                                        nombre_archivo = f"{id_empleado}_{archivo_evidencia.name}"
                                        supabase.storage.from_("evidencias_rh").upload(
                                            path=nombre_archivo,
                                            file=archivo_evidencia.getvalue(),
                                            file_options={"content-type": archivo_evidencia.type}
                                        )
                                        url_archivo = supabase.storage.from_("evidencias_rh").get_public_url(nombre_archivo)
                                    except Exception as e:
                                        st.error(f"Error al subir archivo: {e}")

                                # B. Guardado en la tabla Reportes_EIPSA
                                datos_reporte = {
                                    "id_empleado": id_empleado,
                                    "nombre_empleado": empleado['Título'],
                                    "whatsapp": whatsapp,
                                    "tema": tema,
                                    "opcion_seleccionada": opcion_final,
                                    "detalles": detalles,
                                    "url_archivo": url_archivo
                                }

                                res_insert = supabase.table("Reportes_EIPSA").insert(datos_reporte).execute()

                                if res_insert.data:
                                    st.balloons()
                                    st.success(f"✅ ¡Enviado! Gracias {empleado['Título']}, RH te contactará pronto.")
                                else:
                                    st.error("❌ Error al guardar el reporte.")
            else:
                st.error("❌ El RFC no coincide.")
    else:
        st.error("❌ ID no encontrado.")
import streamlit as st
from supabase import create_client

# --- 1. CONFIGURACIÓN Y LLAVES (PON LAS TUYAS AQUÍ) ---
URL_SUPABASE = "https://mpcatrdfwzrjmkqqystj.supabase.co"
KEY_SUPABASE = "sb_publishable_mJaq6bbofO2QE7Ms9yIWxg_NzbkFNi_"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# --- 2. DISEÑO EIPSA ---
st.set_page_config(page_title="Buzón RH EIPSA", page_icon="📩")
st.image("logo_eipsa.png", width=200) # Asegúrate de que el archivo se llame así
st.title("📩 Buzón de Atención al Empleado")
st.markdown("---")

# --- 3. IDENTIFICACIÓN ---
id_empleado = st.text_input("Por favor ingresa tu ID:")

if id_empleado:
    consulta = supabase.table("Personal_EIPSA").select("Título").eq("ID_Empleado", id_empleado).execute()
    
    if consulta.data:
        nombre = consulta.data[0]['Título']
        st.success(f"✅ Identificado: {nombre}")
        
        # Dato adicional solicitado en tu árbol
        whatsapp = st.text_input("Ingresa tu número de WhatsApp:")
        
        if whatsapp:
            st.write("### Menú Principal de Trámites")
            tema = st.selectbox("¿Qué tema deseas consultar?", 
                                ["Selecciona...", "1.- Rotaciones", "2.- Nóminas", "3.- Permisos", "4.- Ambiente laboral"])

            # --- SECCIÓN 1: ROTACIONES ---
            if tema == "1.- Rotaciones":
                opcion_1 = st.radio("Selecciona una opción:", ["1.1.- Solicitud de rotación", "1.1.2.- Viáticos no pagados", "1.2.- Solicitud bono por no rotación"])
                
                if "1.1.- Solicitud" in opcion_1:
                    st.info("Indica trayecto (punto A a punto B), medio, fecha salida y regreso.")
                    detalles = st.text_area("Detalles del traslado:")
                    st.download_button("Descargar Solicitud de Rotación", "Archivo de prueba", file_name="solicitud_rotacion.pdf")
                
                elif "1.1.2" in opcion_1:
                    st.warning("Especifica montos y conceptos no pagados.")
                    st.text_area("Descripción de montos:")
                    st.file_uploader("Sube evidencias de viáticos:", type=["jpg", "png", "pdf"])

            # --- SECCIÓN 2: NÓMINAS ---
            elif tema == "2.- Nóminas":
                opcion_2 = st.selectbox("Selecciona:", ["2.1.- Descuentos", "2.2.- Faltas", "2.3.- INFONAVIT", "2.4.- Préstamo"])
                
                if "2.1" in opcion_2:
                    st.text_input("Indica la quincena del descuento:")
                
                elif "2.2" in opcion_2:
                    sub_falta = st.radio("Tipo de reporte:", ["2.2.1.- Solicitud de faltas", "2.2.2.- Tengo una falta pero sí vine"])
                    if "2.2.2" in sub_falta:
                        st.date_input("Fecha de la falta:")
                        st.file_uploader("Sube evidencia (Listas, ART):", type=["jpg", "png", "pdf"])

            # --- SECCIÓN 3: PERMISOS ---
            elif tema == "3.- Permisos":
                opcion_3 = st.radio("Tipo de permiso:", ["3.1.- Con goce de sueldo", "3.2.- Sin goce de sueldo"])
                st.text_area("Explica el motivo de tu permiso:")
                st.info("Recuerda descargar y entregar el formato en RH.")

            # --- SECCIÓN 4: AMBIENTE LABORAL ---
            elif tema == "4.- Ambiente laboral":
                opcion_4 = st.selectbox("Selecciona:", ["4.1.- Mobbing (Acoso)", "4.2.- Capacitaciones"])
                if "4.1" in opcion_4:
                    st.error("Reporte de Acoso Laboral")
                    st.text_area("Explica la situación detalladamente:")
                elif "4.2" in opcion_4:
                    st.text_input("Capacitación que deseas recibir:")

            # BOTÓN FINAL DE ENVÍO
            if st.button("Enviar Reporte a RH"):
                st.balloons()
                st.success("¡Enviado! Nos pondremos en contacto contigo vía WA.")

    else:
        st.error("ID no encontrado.")
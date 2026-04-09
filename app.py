import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Buzón RH EIPSA", page_icon="📩", layout="centered")

# --- ESTILO TIPO EIPSA (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #003366; /* Azul EIPSA */
        color: white;
        border-radius: 5px;
    }
    h1 {
        color: #b30000; /* Rojo EIPSA */
        font-family: 'Helvetica', sans-serif;
    }
    </style>
    """,unsafe_allow_html=True)

# --- ENCABEZADO CON LOGO ---
# Si tienes el logo en la carpeta, descomenta la línea de abajo: 
st.image("logo_eipsa.png", width=200)

st.title("📩 Buzón de Atención al Empleado")
st.subheader("Especialistas en Instrumentación y Procesos S.A.")
st.markdown("---")

# --- TU CONEXIÓN SUPABASE (Mantén tus llaves aquí) ---
URL_SUPABASE = "https://mpcatrdfwzrjmkqqystj.supabase.co"
KEY_SUPABASE = "sb_publishable_mJaq6bbofO2QE7Ms9yIWxg_NzbkFNi_"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# --- LÓGICA DE IDENTIFICACIÓN ---
id_empleado = st.text_input("Ingresa tu número de Casco:")

if id_empleado:
    consulta = supabase.table("Personal_EIPSA").select("Título").eq("ID_Empleado", id_empleado).execute()
    
    if consulta.data:
        nombre = consulta.data[0]['Título']
        st.success(f"✅ Bienvenido, **{nombre}**")
        
        # MENÚ DE OPCIONES ESTILIZADO
        st.write("### ¿En qué podemos apoyarte?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💰 Mi Nómina"):
                st.session_state.opcion = "Nomina"
        with col2:
            if st.button("🏖️ Mis Vacaciones"):
                st.session_state.opcion = "Vacaciones"
    else:
        st.error("❌ ID no encontrado. Por favor, verifica con tu supervisor.")
import streamlit as st
from supabase import create_client

# 1. CONEXIÓN (Pega aquí tus datos de Supabase)
URL_SUPABASE = "https://mpcatrdfwzrjmkqqystj.supabase.co"
KEY_SUPABASE = "sb_publishable_mJaq6bbofO2QE7Ms9yIWxg_NzbkFNi_"

supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# 2. INTERFAZ
st.title("📩 Buzón de Atención EIPSA")
st.write("Ingresa tu ID para identificarte")

# 3. IDENTIFICACIÓN
id_empleado = st.text_input("Número de ID:")

if id_empleado:
    # Busca en la tabla SQL de Supabase el ID que escribas
    consulta = supabase.table("Personal_EIPSA").select("Título").eq("ID_Empleado", id_empleado).execute()
    
    if consulta.data:
        # Si lo encuentra, extrae el nombre (Título)
        nombre = consulta.data[0]['Título']
        st.success(f"✅ Hola {nombre}, te hemos identificado.")
        st.info("Próximamente: Menú de opciones de RH")
    else:
        st.error("❌ ID no encontrado. Verifica con RH.")
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from datetime import date
import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
# import snscrape.modules.twitter as sntwitter
import re  # para expresiones regulares
import matplotlib.pyplot as plt
# from pysentimiento import create_analyzer  # Para el analisis de sentimiento
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')
# stop_words = set(stopwords.words('spanish'))
import plotly.graph_objects as go


st.set_page_config(page_title="Tesis", layout="wide")
st.markdown("<style>" + open("./style.css").read() + "</style>", unsafe_allow_html=True)
st.title(
    "DISEÑO DE UN DASHBOARD PARA EMPRESAS DE TELECOMUNICACIONES UTILIZANDO COMO TÉCNICA LA MINERÍA DE OPINIONES"
)

# TODO: Menu horizontal
selected = option_menu(
    None,
    ["Inicio", "Extraccion", "Dashboard"],
    icons=["activity", "file-earmark-arrow-down", "file-bar-graph"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#3178c6"},
        "nav-link": {"font-size": "1rem", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fb796a"},
    },
)


if selected == "Inicio":
    st.title("Inicio")

elif selected == "Extraccion":
    st.title("Extraccion")
    
# ---------------------------------------------------------------------------------------------------------

# TODO: PESTA;A DASHBOARD
elif selected == "Dashboard":
    uploaded_file = st.file_uploader("Sube un archivo csv")
    if uploaded_file is not None:

        # El archivo se lo guarda en la variable df
        df = pd.read_csv(uploaded_file)

        # Eliminar col que se creo demas
        df = df.drop(["Unnamed: 0"], axis=1)
        
        # Poner al inicio para la fecha
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df['Dias'] = df['Datetime'].dt.day_name()
        df['Mes'] = df['Datetime'].dt.month_name()
        df['Hora'] = df['Datetime'].dt.hour.astype('str')

        # Mostrar los followers-following-tweets de la empresa de telecomunicaciones
        followers = df[["Username", "Followers", "Following", "Tweets", "ProfileImg"]]

        # Convierte el value_counts() dentro de una variable
        etiquetas = followers["Username"].value_counts().keys().tolist()

        # Elige el primer valor: Esta en formato lista ['empresa'] para hacerlo string es empresa[0]
        empresa = etiquetas[:1]

        # Seleccionar las demas cols haciendo una condicion: Esta en formato lista
        pri = followers[followers["Username"] == empresa[0]].iloc[0].keys().tolist()
        res = followers[followers["Username"] == empresa[0]].iloc[0].tolist()

        # Para poner en el centro el titulo
        em1, em2, em3 = st.columns(3)
        with em1:
            st.title("")

        with em2:
            st.markdown(
                f"<div class='test'><h3>Empresa {res[0]}</h3> <img src='{res[4]}'> </div>",
                unsafe_allow_html=True,
            )

        with em3:
            st.title("")

        # Muestra los datos de la empresa
        fol1, fol2, fol3 = st.columns(3)
        with fol1:
            st.markdown(
                f"<div class='test1'> <img class='logo' src='https://cdn-icons-png.flaticon.com/512/1165/1165674.png'> <div class='col'><h2 class='num'>{res[1]}</h2><p class='par'>{pri[1]}</p> </div> </div> ",
                unsafe_allow_html=True,
            )
            st.title("")
            

        with fol2:
            st.markdown(
                f"<div class='test1'> <img class='logo' src='https://cdn-icons-png.flaticon.com/512/2504/2504112.png'> <div class='col'><h2 class='num'>{res[2]}</h2><p class='par'>{pri[2]}</p> </div> </div> ",
                unsafe_allow_html=True,
            )
            st.title("")
            

        with fol3:
            st.markdown(
                f"<div class='test1'> <img class='logo' src='https://cdn-icons-png.flaticon.com/512/2580/2580225.png'> <div class='col'><h2 class='num'>{res[3]}</h2><p class='par'>{pri[3]}</p> </div> </div> ",
                unsafe_allow_html=True,
            )
            st.title("")
            
        
        # Crear una variable para saber cuantas opciones hay para los graficos
        pola = df["Sentimiento"].value_counts().keys().tolist()

        # Crear un expander y dentro el pie chart
        with st.expander("Polaridad", expanded=True):
            gnew1, gnew2, gnew3 = st.columns(3)
            with gnew2:
                sentiment_counts = df['Sentimiento'].value_counts()
                fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts, rotation=90, pull=[0.05, 0.05, 0.05])])
                fig.update_traces(hoverinfo='label+value+percent', textinfo='percent', textfont_size=20, marker=dict(colors=['crimson','gray','#2ca02c'], line=dict (color='black', width=2)))
                fig.update_layout(
                    # Texto
                    title_text='Polaridad', title_x=0.5, title_y=0.99, title_xanchor='center', title_font_size=30, title_font_family="Source Sans Pro",
                    # paper_bgcolor="skyblue",
                    # legend_title_font_color="green",
                    # Size
                    width=600, height=400, margin=dict(l=0,r=0,b=0,t=40,pad=0),
                    # box
                    legend=dict( orientation="v", x=0.95, y=0.5, traceorder="reversed", title_text='Sentimiento', title_font_family="Source Sans Pro",
                    font=dict( family="Source Sans Pro", size=18, 
                    # color="black"
                    ),
                    # bgcolor="LightSteelBlue",
                    bordercolor="gray", borderwidth=2
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
        
        
        # TODO: CHARTS DE UBICACION
        # Dic de provincias
        mymap = {
          "Ambato": "Tungurahua",
          "ambato": "Tungurahua",
          "Ambato Ecuador": "Tungurahua",
          "Ambato, Ecuador": "Tungurahua",
          "Ambato - Ecuador": "Tungurahua",
          "Ambato -Ecuador": "Tungurahua",
          "Ambato - Quito - Ecuador 🇪🇨": "Tungurahua",
          "Ambato - Tierrita Linda 🇪🇨": "Tungurahua",
          "Antonio Ante, Ecuador":"Imbabura",
          "Arenillas, Ecuador": "El Oro",
          "Atacames, Ecuador":"Esmeraldas",
          "Azogues Ecuador":"Cañar",
          "Azogues, Ecuador":"Cañar",
          "Azuay": "Azuay",
          "Azuay, Ecuador": "Azuay",
          "Baba, Ecuador": "Los Ríos",
          "Babahoyo": "Los Ríos",
          "Babahoyo - Ecuador": "Los Ríos",
          "Babahoyo, Ecuador": "Los Ríos",
          "Babahoyo_Guayaquil": "Los Ríos",
          "Balzar": "Guayas",
          "Balzar, Ecuador": "Guayas",
          "Baños De Agua Santa, Ecuador": "Tungurahua",
          "Bolivar, Ecuador": "Bolivar",
          "Buena Fe, Ecuador": "Los Ríos",
          "Buena fe - Los Rios - Ecuador": "Los Ríos",
          "Cantón Bolívar, Manabí Ecuador": "Manabí",
          "Cayambe":"Pichincha",
          "Cayambe, Ecuador":"Pichincha",
          "Cayambe, Quito, Ecuador.":"Pichincha",
          "Chone": "Manabí",
          "Chone y Guayaquil ": "Manabí",
          "Chone_ Ecuador": "Manabí",
          "Chone-Ecuador": "Manabí",
          "Chone, Ecuador": "Manabí",
          "Chone-Manabi": "Manabí",
          "cuenca": "Azuay",
          "#Cuenca": "Azuay",
          "Cuenca": "Azuay",
          "Cuenca Ecuador": "Azuay",
          "CUENCA ECUADOR": "Azuay",
          "cuenca Ecuador": "Azuay",
          "Cuenca - Azuay": "Azuay",
          "Cuenca, Azuay, Ecuador.": "Azuay",
          "Cuenca - Quito - Ecuador": "Azuay",
          "Cuenca - Ecuador": "Azuay",
          "Cuenca- Ecuador": "Azuay",
          "CUENCA-ECUADOR": "Azuay",
          "Cuenca-Ecuador": "Azuay",
          "Cuenca_Ecuador": "Azuay",
          "Cuenca, Ecuador": "Azuay",
          "Cuenca, Ecuador.": "Azuay",
          "Cuenca, Ecuador 🇪🇨": "Azuay",
          "Cumbaya":"Pichincha",
          "Cumbaya,Ecuador":"Pichincha",
          "Cumbayá - Quito":"Pichincha",
          "Chuyuipe, Sta Elena, Ecuador": "Santa Elena",
          "Daule": "Guayas",
          "Daule, Ecuador": "Guayas",
          "Duran": "Guayas",
          "Duran, Ecuador": "Guayas",
          "Durán, Ecuador": "Guayas",
          "Durán - Ecuador": "Guayas",
          "Durán - Guayas - Ecuador": "Guayas",
          "Ecuador-Guayaquil": "Guayas",
          "Ecuador - Guayaquil": "Guayas",
          "Ecuador-guayaquil": "Guayas",
          "ecuador - guayaquil": "Guayas",
          "ecuador-guayaquil": "Guayas",
          "Ecuador, Guayaquil": "Guayas",
          "Ecuador,Guayaquil": "Guayas",
          "Ecuador Guayaquil": "Guayas",
          "Ecuador _ Portoviejo": "Manabí",
          "Ecuador - Ambato": "Tungurahua",
          "Ecuador - El Oro": "El Oro",
          "Ecuador - Quito":"Pichincha",
          "Ecuador- Quito":"Pichincha",
          "Ecuador, Quito":"Pichincha",
          "Ecuador- Duran": "Guayas",
          "Eloy Alfaro, Ecuador": "Guayas",
          "EL EMPALME - GUAYAS": "Guayas",
          "Empalme, Ecuador": "Guayas",
          "El Oro / Guayas": "El Oro",
          "El Oro, Ecuador": "El Oro",
          "El Triunfo, Ecuador": "Guayas",
          "Esmeraldas":"Esmeraldas",
          "Esmeraldas - Ecuador":"Esmeraldas",
          "Esmeraldas-Ecuador":"Esmeraldas",
          "Esmeraldas, Ecuador":"Esmeraldas",
          "Galápagos": "Galápagos",
          "Galápagos - Ecuador": "Galápagos",
          "Galápagos-Ecuador": "Galápagos",
          "Galápagos, Ecuador": "Galápagos",
          "Guaranda": "Bolivar",
          "Guaranda - Quito - Ecuador": "Bolivar",
          "Guaranda, Ecuador": "Bolivar",
          "Guayas": "Guayas",
          "guayas": "Guayas",
          "Guayas-Ecuador": "Guayas",
          "Guayas, Ecuador": "Guayas",
          "Guayas, Guayaqui, Ecuador": "Guayas",
          "Guayakil": "Guayas",
          "Guayakill": "Guayas",
          "guayakill": "Guayas",
          "guayaquil": "Guayas",
          "guayaquil, Ecuador": "Guayas",
          "Guayaquil": "Guayas",
          "#Guayaquil": "Guayas",
          "GUAYAQUIL": "Guayas",
          "GUAYAQUIL ECUADOR": "Guayas",
          "GUAYAQUIL- ECUADOR": "Guayas",
          "GUAYAQUIL_ECUADOR": "Guayas",
          "guayaquil ecuador": "Guayas",
          "guayaquil,ecuador": "Guayas",
          "Guayaquil Ecuador": "Guayas",
          "Guayaquil-Ecuador": "Guayas",
          "Guayaquil_Ecuador": "Guayas",
          "Guayaqui-Ecuador": "Guayas",
          "Guayaquil- Ecuador": "Guayas",
          "Guayauil - Ecuador": "Guayas",
          "Guayaquil - Ecuador": "Guayas",
          "Guayaquil ~ Ecuador": "Guayas",
          "Guayaquil - Ecuador.": "Guayas",
          "Guayaquil,Ecuador": "Guayas",
          "Guayaquil, Ecuador 🇪🇨": "Guayas",
          "Guayaquil, Ecuador 📍": "Guayas",
          "Guayaquil, Ecuador": "Guayas",
          "Guayaquil, Quito": "Guayas",
          "Guayaquil-Quito (bilocalidad)": "Guayas",
          "Guayaqui . Ecuador": "Guayas",
          "Guayaqui * Ecuador": "Guayas",
          "Guayaqui / Ecuador": "Guayas",
          "Guayaquil / Ecuador": "Guayas",
          "Guayaquil/Ecuador": "Guayas",
          "Guayaqui /ecuador": "Guayas",
          "guayaqui / ecuador": "Guayas",
          "guayaqui /ecuador": "Guayas",
          "guayaqui-ecuador": "Guayas",
          "guayaquil-ecuador": "Guayas",
          "Guayaquil, ecuador": "Guayas",
          "Guayaquil, Ecuador.": "Guayas",
          "Guayaquil, Ecuador🇪🇨": "Guayas",
          "Guayaquil, Guayas Ecuador": "Guayas",
          "Guayaquil, Guayas, Ecuador": "Guayas",
          "Guayaquil,Guayas,Ecuador": "Guayas",
          "Guayaquil; Ecuador": "Guayas",
          "Guayaquil, La Troncal": "Guayas",
          "Guayaquil, Norte de la Ciudad": "Guayas",
          "Guayaquil City": "Guayas",
          "Guayaquil/Vinces": "Guayas",
          "Guayaquileño": "Guayas",
          "Guayaquil 🇪🇨": "Guayas",
          "Guayaquil, Daule": "Guayas",
          "Guayaquil, Ec": "Guayas",
          "Guayaquil, EC": "Guayas",
          "Guayaquil de mis calores.": "Guayas",
          "Gye": "Guayas",
          "GYE": "Guayas",
          "Gye - Ec": "Guayas",
          "GYE - Ec": "Guayas",
          "gye": "Guayas",
          "gye-ecu": "Guayas",
          "gye-ecuador": "Guayas",
          "Gye-ecuador": "Guayas",
          "Gye-Ecuador": "Guayas",
          "Gye, Ecuador": "Guayas",
          "GYE,Ecuador": "Guayas",
          "GYE-ECUADOR": "Guayas",
          "Gye - Ecuador": "Guayas",
          "GYE - Ecuador": "Guayas",
          "Ibarra":"Imbabura",
          "Ibarra Ecuador":"Imbabura",
          "Ibarra, Ecuador":"Imbabura",
          "Ibarra- Ecuador":"Imbabura",
          "Ibarra - Ecuador":"Imbabura",
          "Ibarra-Imbabura-Ecuador":"Imbabura",
          "IMBABURA":"Imbabura",
          "Imbabura, Ecuador":"Imbabura",
          "Jipijapa - Manabi -": "Manabí",
          "Jipijapa-Manabi-Ecuador": "Manabí",
          "Jipijapa, Ecuador": "Manabí",
          "La Aurora, Daule": "Guayas",
          "La Carita de Dios": "Pichincha",
          "La carita de Dios": "Pichincha",
          "La Libertad": "Santa Elena",
          "La Mana, Ecuador": "Cotopaxi",
          "La Perla del Pacifico": "Guayas",
          "La perla del Pacifico": "Guayas",
          "La Troncal, Ecuador":"Cañar",
          "Lago Agrio":"Sucumbíos",
          "Lago Agrio - Ecuador":"Sucumbíos",
          "Lago Agrio, Ecuador":"Sucumbíos",
          "Latacunga, Ecuador": "Cotopaxi",
          "loja": "Loja",
          "LOJA": "Loja",
          "Loja": "Loja",
          "loja ecuador": "Loja",
          "Loja - Ecuador": "Loja",
          "Loja-Ecuador": "Loja",
          "Loja, Ecuador": "Loja",
          "LOJA- Quito": "Loja",
          "Lomas De Sargentillo, Ecuador": "Guayas",
          "Los Ríos-Ecuador": "Los Ríos",
          "Machala": "El Oro",
          "Machala Ecuador": "El Oro",
          "Machala, Ecuador": "El Oro",
          "Machala - Ecuador": "El Oro",
          "Machala-Ecuador": "El Oro",
          "machala-ecuador": "El Oro",
          "Machala/Ecuador": "El Oro",
          "Machala / Ecuador": "El Oro",
          "MACHALA/ECUADOR": "El Oro",
          "Machala- El Oro": "El Oro",
          "Manabí": "Manabí",
          "Manabí - Ecuador": "Manabí",
          "Manabí- Ecuador": "Manabí",
          "Manabi- Ecuador": "Manabí",
          "Manabi, Ecuador": "Manabí",
          "manta": "Manabí",
          "Manta": "Manabí",
          "MANTA": "Manabí",
          "Manta - Ecuador": "Manabí",
          "Manta - Manabí - Ecuador": "Manabí",
          "Manta / Guayaquil": "Manabí",
          "Manta Ecuador": "Manabí",
          "Manta- Ecuador": "Manabí",
          "Manta-Ecuador": "Manabí",
          "Manta, Ecuador": "Manabí",
          "Manta, Manabí, Ecuador.": "Manabí",
          "Manta, Manabi. Ecuador": "Manabí",
          "Manta/Manabi": "Manabí",
          "Milagro": "Guayas",
          "Milagro, Ecuador": "Guayas",
          "Milagro-Ecuador": "Guayas",
          "Milagro - Ecuador": "Guayas",
          "Milagro Ecuador": "Guayas",
          "Mitad del Mundo":"Pichincha",
          "Mitad del Mundo 🇪🇨":"Pichincha",
          "MITAD DEL MUNDO!":"Pichincha",
          "Montalvo, Los Ríos, Ecuador": "Los Ríos",
          "Montecristi, Ecuador": "Manabí",
          "monumental bsc": "Guayas",
          "Monumental-Ecuador": "Guayas",
          "Morona Santiago, Ecuador": "Morona Santiago",
          "Morona, Ecuador": "Morona Santiago",
          "Mucho Lote 1 etapa 4ta": "Guayas",
          "Mulalillo, Cotopaxi, Ecuador": "Cotopaxi",
          "Naranjal-Ecuador": "Guayas",
          "Pajan, Ecuador": "Manabí",
          "Palanda, Ecuador": "Zamora Chinchipe",
          "Pasaje": "El Oro",
          "Pasaje - Ecuador": "El Oro",
          "Pasaje, Ecuador": "El Oro",
          "Perla del Pacifico": "Guayas",
          "Pichincha - Quito":"Pichincha",
          "Pichincha, Ecuador":"Pichincha",
          "Pimocha": "Los Ríos",
          "Piñas": "El Oro",
          "Piñas -El Oro": "El Oro",
          "Piñas el oro": "El Oro",
          "Piñas, Ecuador": "El Oro",
          "portoviejo": "Manabí",
          "Portoviejo": "Manabí",
          "Portovelo, Ecuador": "El Oro",
          "Portovelo - Ecuador": "El Oro",
          "Portoviejo Rock City": "Manabí",
          "Portoviejo, Manabí": "Manabí",
          "Portoviejo, Manabi, Ecuador": "Manabí",
          "Portoviejo, Ecuador": "Manabí",
          "Puebloviejo, Ecuador": "Los Ríos",
          "Puerto Cayo": "Manabí",
          "Puerto de Manta": "Manabí",
          "Puerto López-Ecuador": "Manabí",
          "Puerto Quito, Ecuador": "Pichincha",
          "Playas, Ecuador": "Guayas",
          "Punta Carnero, Ecuador 🇪🇨": "Santa Elena",
          "Quevedo": "Los Ríos",
          "Quevedo, Ecuador": "Los Ríos",
          "Quevedo-Ecuador": "Los Ríos",
          "Quininde, Ecuador":"Esmeraldas",
          "Quijos, Ecuador": "Napo",
          "quiteño, ecuatoriano": "Pichincha",
          "Quito, La Capital": "Pichincha",
          "Quito, Luz de América": "Pichincha",
          "Quito, Luz de América 🇪🇨": "Pichincha",
          "Quito, Mitad del Mundo.": "Pichincha",
          "Quito, UIO": "Pichincha",
          "Quito, Pichincha, Ecuador, Latinoamérica, Planeta Tierra, Vía Láctea, Universo 3A.": "Pichincha",
          "Quito Ecuador": "Pichincha",
          "Quito,Ecuador": "Pichincha",
          "Quito.Ecuador": "Pichincha",
          "Quito / Ecuador": "Pichincha",
          "Quito, Ecuador": "Pichincha",
          "Quito, Ecuador.": "Pichincha",
          "Quito-Ecuador": "Pichincha",
          "Quito- Ecuador": "Pichincha",
          "Quito_Ecuador": "Pichincha",
          "Quito - ECU": "Pichincha",
          "Quito,Ecu": "Pichincha",
          "quito - ecuador": "Pichincha",
          "QUITO - ECUADOR": "Pichincha",
          "QUITO ECUADOR": "Pichincha",
          "QUITO-ECUADOR": "Pichincha",
          "QUITO --ECUADOR": "Pichincha",
          "QUITO -ECUADOR": "Pichincha",
          "QUITO, ECUADOR": "Pichincha",
          "@QuitoEcuador": "Pichincha",
          "Quito - Ecuador": "Pichincha",
          "Quito - Ecuador.": "Pichincha",
          "Quito - EC": "Pichincha",
          "Quito, EC": "Pichincha",
          "Quito Ec.": "Pichincha",
          "quito": "Pichincha",
          "quito ecuador": "Pichincha",
          "quito, ecuador": "Pichincha",
          "quito-ecuador": "Pichincha",
          "Quito": "Pichincha",
          "@Quito": "Pichincha",
          "QUITO": "Pichincha",
          "riobamba":"Chimborazo",
          "Riobamba":"Chimborazo",
          "Riobamba ecuador":"Chimborazo",
          "Riobamba - Ecuador":"Chimborazo",
          "Riobamba-Ecuador":"Chimborazo",
          "Riobamba Ecuador":"Chimborazo",
          "Riobamba, Ecuador":"Chimborazo",
          "Rock City": "Manabí",
          "Rockcity, Manabi, Ecuador": "Manabí",
          "rumiñahui": "Pichincha",
          "Rumiñahui": "Pichincha",
          "Rumiñahui, Ecuador": "Pichincha",
          "salinas": "Santa Elena",
          "Salinas": "Santa Elena",
          "Salinas - Ecuador": "Santa Elena",
          "Salinas- Ecuador": "Santa Elena",
          "Salinas, Ecuador": "Santa Elena",
          "Salinas - Guayaquil": "Santa Elena",
          "Salitre, Ecuador": "Guayas",
          "Samborondón": "Guayas",
          "Samborondón.": "Guayas",
          "Samborondon - Ecuador": "Guayas",
          "Samborondon, Ecuador": "Guayas",
          "Samborondon, Guayas": "Guayas",
          "San Clemente, Ecuador": "Manabí",
          "San Cristóbal-Galápagos.": "Galápagos",
          "San Cristóbal, Venezuela": "Galápagos",
          "San Isidro Manabi": "Manabí",
          "San Jacinto De Yaguachi": "Guayas",
          "San Lorenzo, Ecuador":"Esmeraldas",
          "San Lorenzo, Esmeraldas- Ecuad":"Esmeraldas",
          "San Miguel De Los Bancos, Ecua": "Pichincha",
          "San Miguel, Ecuador 🇪🇨": "Pichincha",
          "San Rafael, cantón Rumiñahui": "Pichincha",
          "San Rafael, Ecuador": "Pichincha",
          "Sangolquí":"Pichincha",
          "Sangolqui":"Pichincha",
          "sangolqui - ecuador":"Pichincha",
          "sangolqui, ecuador":"Pichincha",
          "Santa Cruz, Galápagos": "Galápagos",
          "Santa Ana, Manabí, Ecuador": "Manabí",
          "Santa Elena, Ecuador": "Santa Elena",
          "Santa Lucía, Guayas, Ecuador": "Guayas",
          "Santo Domingo De Los Tsachilas, Ecuador":"Santo Domingo de los Tsáchilas",
          "Santo Domingo, Ecuador":"Santo Domingo de los Tsáchilas",
          "Santo Domingo - Ecuador":"Santo Domingo de los Tsáchilas",
          "santo domingo- ecuador":"Santo Domingo de los Tsáchilas",
          "Santo Domingo de los Tsachilas":"Santo Domingo de los Tsáchilas",
          "Santo Domingo":"Santo Domingo de los Tsáchilas",
          "santo domingo":"Santo Domingo de los Tsáchilas",
          "Santa Rosa - El Oro - Ecuador": "El Oro",
          "Santiago de Guayaquil / EC": "Guayas",
          "Santiago de Guayaquil, Ecuador": "Guayas",
          "Santiago de Guayaquil/La Perla": "Guayas",
          "Santiago de Gye - Ecuador": "Guayas",
          "Santiago de Guayaquil;Ecuador": "Guayas",
          "Tarqui Manta Ecuador": "Manabí",
          "Tena, Ecuador": "Napo",
          "Tulcan Ecuador": "Carchi",
          "Tungurahua": "Tungurahua",
          "Tungurahua, Ecuador": "Tungurahua",
          "uio": "Pichincha",
          "Uio": "Pichincha",
          "UIO": "Pichincha",
          "UIO - ECU": "Pichincha",
          "UIO - ECUADOR": "Pichincha",
          "Uio, ec": "Pichincha",
          "UIO, EC": "Pichincha",
          "Urdesa": "Guayas",
          "Urdesa,  Guayaquil, Ecuador": "Guayas",
          "valle de los chillos": "Pichincha",
          "Valle de los Chillos": "Pichincha",
          "Vinces": "Los Ríos",
          "vinces": "Los Ríos",
          "Vinces, Ecuador": "Los Ríos",
          "Vinces - Ecuador": "Los Ríos",
          "Zamora - Ecuador": "Zamora Chinchipe",
          "Zamora -Ecuador": "Zamora Chinchipe",
          "Zaruma - El Oro - Ecuador": "El Oro",
          "Zaruma-Guayaquil": "El Oro",
          "Zaruma, Ecuador": "El Oro",
          "Orellana, Ecuador" : "Orellana",
          "Orellana- Ecuador" : "Orellana",
          "Orellana - Ecuador" : "Orellana",
          "Orellana-Ecuador" : "Orellana",
          "Puyo" : "Pastaza",
          "Puyo- Ecuador" : "Pastaza",
          "Puyo-Ecuador" : "Pastaza",
          "Puyo - Ecuador" : "Pastaza",
          "Puyo, Ecuador" : "Pastaza",
        }
        
        # Dic de regiones
        mymapReg = {
            "Azuay" : "Región Sierra",
            "Bolívar" : "Región Sierra",
            "Cañar" : "Región Sierra",
            "Carchi" : "Región Sierra",
            "Chimborazo" : "Región Sierra",
            "Cotopaxi" : "Región Sierra",
            "El Oro" : "Región Costa", 
            "Esmeraldas" : "Región Costa", 
            "Galápagos" : "Región Sierra", 
            "Guayas" : "Región Costa", 
            "Imbabura" : "Región Sierra", 
            "Loja" : "Región Sierra", 
            "Los Ríos" : "Región Costa", 
            "Manabí" : "Región Costa", 
            "Morona Santiago" : "Región Amazónica", 
            "Napo" : "Región Amazónica",
            "Orellana" : "Región Amazónica",
            "Pastaza" : "Región Amazónica",
            "Pichincha" : "Región Sierra",
            "Santa Elena" : "Región Costa",
            "Santo Domingo de los Tsáchilas" : "Región Costa",
            "Sucumbíos" : "Región Amazónica",
            "Tungurahua" : "Región Sierra",
            "Zamora Chinchipe" : "Región Amazónica",
        }
        
        # Aplicar los dic
        df['Location']=df['Location'].map(mymap)
        df['Region']=df['Location'].map(mymapReg)
        
        # TODO: DF PARA REALIZAR LOS CHARTS DE PROVINCIAS Y REGIONES
        ubic = df[["Location", "Sentimiento"]]
        ubicReg = df[["Region", "Sentimiento"]]
        
        with st.expander("Ubicacion", expanded=True):
            # NaN values de usuarios sin ubicacion
            nanVal = df["Location"].isnull().sum()
            st.warning(f" Existen {nanVal} personas que no cuentan con una ubicación en Twitter", icon='⚠️')
            gpol1, gpol2, gpol3  = st.columns([3, 1, 1])
            
            with gpol1:
                prueba = st.multiselect('Principales tres provincias:', [3], default=3, disabled=True)

                # Crea una lista con los nombres de la provincia
                mainProv = ubic["Location"].value_counts().keys().tolist()

                # Select the locations you want to show the chart for
                tprov = mainProv[:prueba[0]] if len(mainProv) == 3 else mainProv[:prueba[0]]
                prov_locations = tprov

                # Calculate the value counts for each sentiment
                prov_sentiments = ubic.groupby(['Location', 'Sentimiento']).size().reset_index(name='counts')

                # Pivot the DataFrame to have each sentiment as a column
                prov_sentiments = prov_sentiments.pivot(index='Location', columns='Sentimiento', values='counts')

                # Plot the pie chart for each selected location
                fig, axs = plt.subplots(nrows=1, ncols=len(prov_locations), figsize=(5*len(prov_locations), 30), dpi=100)
                for i, ax in enumerate(axs.flatten()):
                    prov_sentiments.loc[prov_locations[i]].plot.pie(autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '', 
                                                            ax=ax, 
                                                            startangle = 90,
                                                            textprops=dict(color="w", size=11, weight='black'),
                                                            colors=['crimson','gray','#2ca02c'],
                                                            pctdistance=0.85, labeldistance=0,)
                    ax.set_title(prov_locations[i],size=30, weight='black')
                    # Center circle
                    my_circle = plt.Circle( (0,0), 0.7, color='white')
                    ax.add_artist(my_circle)
                    ax.legend(title="Sentimiento", loc='center', fontsize=14, bbox_to_anchor=(1, 0, -1, 1), fancybox=True, framealpha=0.5)
                    ax.set_ylabel('')
                    # ax.get_yaxis().set_visible(False)
                    fig.tight_layout()
                st.pyplot(fig)
                # st.plotly_chart(fig, use_container_width=True)

            with gpol2:
                maxProv = ubic["Location"].value_counts().keys().tolist()
                numProv = st.multiselect('Elige la provincia:', maxProv, default=maxProv[3])

                for location in numProv:
                    lugar = location
                    location_sentiments = ubic.groupby(['Location', 'Sentimiento']).size().reset_index(name='counts')
                    location_sentiments = location_sentiments.pivot(index='Location', columns='Sentimiento', values='counts')
                    location_sentiments = location_sentiments.loc[location]
                    location_sentiments = location_sentiments.dropna()
                    labels = location_sentiments.index
                    sizes = location_sentiments.values
                    fig = px.pie(names=labels, values=sizes, title=location, hole=0.7)
                    fig.update_traces(hoverinfo='label', textposition='inside', textinfo='percent', textfont_size=20, 
                                    marker=dict(colors=['crimson','gray','#2ca02c'], line=dict (color='black', width=0)))
                    fig.update_layout(
                        # Texto
                        title_text=location, title_x=0.5, title_y=0.99, title_xanchor='center', title_font_size=30, title_font_family="Source Sans Pro",
                        # Size height=400,
                        width=600, height=370, margin=dict(l=0,r=0,b=10,t=40,pad=0), paper_bgcolor="skyblue",
                        # box
                        legend=dict( orientation="v", x=0.5, xanchor='center', y=0.5, yanchor='middle', traceorder="reversed", title_text='Sentimiento', title_font_family="Source Sans Pro",
                        font=dict( family="Source Sans Pro", size=20, 
                        ),
                        bordercolor="gray", borderwidth=2
                    )
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
            with gpol3:
                maxReg = ubicReg["Region"].value_counts().keys().tolist()
                numReg = st.multiselect('Elige la region:', maxReg, default=maxReg[0])

                for region in numReg:
                    lugar2 = region
                    region_sentiments = ubicReg.groupby(['Region', 'Sentimiento']).size().reset_index(name='counts')
                    region_sentiments = region_sentiments.pivot(index='Region', columns='Sentimiento', values='counts')
                    region_sentiments = region_sentiments.loc[region]
                    labels = region_sentiments.index
                    sizes = region_sentiments.values
                    fig = px.pie(names=labels, values=sizes, title=region, hole=0.7)
                    fig.update_traces(hoverinfo='label', textposition='inside', textinfo='percent', textfont_size=20, 
                                    marker=dict(colors=['crimson','gray','#2ca02c'], line=dict (color='black', width=0)))
                    fig.update_layout(
                        # Texto
                        title_text=region, title_x=0.5, title_y=0.99, title_xanchor='center', title_font_size=30, title_font_family="Source Sans Pro",
                        # Size height=400,
                        width=600, height=370, margin=dict(l=0,r=0,b=10,t=40,pad=0), paper_bgcolor="skyblue",
                        # box
                        legend=dict( orientation="v", x=0.5, xanchor='center', y=0.5, yanchor='middle', traceorder="reversed", title_text='Sentimiento', title_font_family="Source Sans Pro",
                        font=dict( family="Source Sans Pro", size=20, 
                        ),
                        bordercolor="gray", borderwidth=2
                    )
                    )
                    st.plotly_chart(fig, use_container_width=True)


        #TODO: GRAFICOS DE DATETIME
        
        # Dic para cambiar al esp los dias
        dayss = {
            'Monday' : 'Lunes', 
            'Tuesday' : 'Martes',
            'Wednesday' : 'Miércoles',
            'Thursday' : 'Jueves',
            'Friday' : 'Viernes',
            'Saturday' : 'Sábado' ,
            'Sunday' : 'Domingo'
        }
        
        # Aplicar el dic
        df['Dias'] = df['Dias'].map(dayss)
        
        # DF con el que se trabaja
        date = df[['Sentimiento','Dias']]
        
        with st.expander("See explanation",expanded=True):
            
            # with st.form("Formulario dinamico"):
                
            #     col1, col2 = st.columns(2)
            #     with col1:
            #         dias1 = st.checkbox("Dias (1row-1col)")
            #     with col2:
            #         dias2 = st.checkbox("Dias (1row-3col)")

            #     # Boton que sirve para elegir cuales graficos mostrar
            #     genGraph = st.form_submit_button("Generar Graficos")
            #     if genGraph:
            #         c1, c2 = st.columns(2)
            #         if dias1:
            #             with c1:
            #                 date = df[['Sentimiento','Dias']]

            #                 day_of_week_sentiments = date.groupby(['Dias', 'Sentimiento']).size().reset_index(name='counts')
            #                 day_of_week_sentiments = day_of_week_sentiments.pivot(index='Dias', columns='Sentimiento', values='counts')

            #                 day_of_week_sentiments = day_of_week_sentiments.reindex(['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])

            #                 day_of_week_sentiments = day_of_week_sentiments.divide((day_of_week_sentiments.sum(axis=1)/100), axis=0)

            #                 fig, ax = plt.subplots(figsize=(10,10))
            #                 day_of_week_sentiments.plot(kind='line', ax=ax, color=['red','gray','green'], fontsize=14)

            #                 max_pos = day_of_week_sentiments['Positivo'].max()
            #                 max_neg = day_of_week_sentiments['Negativo'].max()
            #                 max_neu = day_of_week_sentiments['Neutral'].max()
            #                 min_pos = day_of_week_sentiments['Positivo'].min()
            #                 min_neg = day_of_week_sentiments['Negativo'].min()
            #                 min_neu = day_of_week_sentiments['Neutral'].min()

            #                 max_pos_day = day_of_week_sentiments[day_of_week_sentiments['Positivo'] == max_pos].index[0]
            #                 max_neg_day = day_of_week_sentiments[day_of_week_sentiments['Negativo'] == max_neg].index[0]
            #                 max_neu_day = day_of_week_sentiments[day_of_week_sentiments['Neutral'] == max_neu].index[0]
            #                 min_pos_day = day_of_week_sentiments[day_of_week_sentiments['Positivo'] == min_pos].index[0]
            #                 min_neg_day = day_of_week_sentiments[day_of_week_sentiments['Negativo'] == min_neg].index[0]
            #                 min_neu_day = day_of_week_sentiments[day_of_week_sentiments['Neutral'] == min_neu].index[0]

            #                 ax.axhline(max_pos, color='green', linestyle='--')
            #                 ax.axhline(max_neg, color='red', linestyle='--')
            #                 ax.axhline(max_neu, color='gray', linestyle='--')
            #                 ax.axhline(min_pos, color='green', linestyle='--')
            #                 ax.axhline(min_neg, color='red', linestyle='--')
            #                 ax.axhline(min_neu, color='gray', linestyle='--')
            #                 ax.annotate(f'            {round(max_pos,1)}% ↑', xy=(day_of_week_sentiments.index.get_loc(max_pos_day), max_pos), 
            #                                                                 xycoords='data', size=10, ha='left', va='bottom', color='green', 
            #                                                                 weight='bold',arrowprops=dict(arrowstyle="->", color='black'))
            #                 ax.annotate(f'            {round(max_neg,1)}% ↑', xy=(day_of_week_sentiments.index.get_loc(max_neg_day), max_neg), 
            #                                                                 xycoords='data', size=10, ha='left', va='bottom', color='red', 
            #                                                                 weight='bold', arrowprops=dict(arrowstyle="->", color='black'))
            #                 ax.annotate(f'            {round(max_neu,1)}% ↑', xy=(day_of_week_sentiments.index.get_loc(max_neu_day), max_neu), 
            #                                                                 xycoords='data', size=10, ha='left', va='bottom', color='gray', 
            #                                                                 weight='bold', arrowprops=dict(arrowstyle="->", color='black'))

            #                 ax.annotate(f'            {round(min_pos,1)}% ↓', xy=(day_of_week_sentiments.index.get_loc(min_pos_day), min_pos), 
            #                                                                 xycoords='data', size=10, ha='left', va='top', color='green', 
            #                                                                 weight='bold',arrowprops=dict(arrowstyle="->", color='black'))
            #                 ax.annotate(f'            {round(min_neg,1)}% ↓', xy=(day_of_week_sentiments.index.get_loc(min_neg_day), min_neg), 
            #                                                                 xycoords='data', size=10, ha='left', va='top', color='red', 
            #                                                                 weight='bold', arrowprops=dict(arrowstyle="->", color='black'))
            #                 ax.annotate(f'            {round(min_neu,1)}% ↓', xy=(day_of_week_sentiments.index.get_loc(min_neu_day), min_neu), 
            #                                                                 xycoords='data', size=10, ha='left', va='top', color='gray', 
            #                                                                 weight='bold', arrowprops=dict(arrowstyle="->", color='black'))

            #                 ax.set_xlabel('')
            #                 ax.set_ylabel('Porcentaje %', size=14, weight='bold')
            #                 ax.tick_params(axis='x', rotation=0)
            #                 fig.tight_layout()
            #                 st.pyplot(fig)
                        
            #         if dias2:
            #             with c2:
            
            
            day_of_week_sentiments = date.groupby(['Dias', 'Sentimiento']).size().reset_index(name='counts')
            day_of_week_sentiments = day_of_week_sentiments.pivot(index='Dias', columns='Sentimiento', values='counts')
            day_of_week_sentiments = day_of_week_sentiments.reindex(['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])
            day_of_week_sentiments = day_of_week_sentiments.divide((day_of_week_sentiments.sum(axis=1)/100), axis=0)

            days = day_of_week_sentiments.index.tolist()

            pos_data = go.Scatter(x=days, y=day_of_week_sentiments['Positivo'], name='Positivo', line=dict(color='green'))
            neg_data = go.Scatter(x=days, y=day_of_week_sentiments['Negativo'], name='Negativo', line=dict(color='red'))
            neu_data = go.Scatter(x=days, y=day_of_week_sentiments['Neutral'], name='Neutral', line=dict(color='gray'))
            
            fig = go.Figure(data=[pos_data, neg_data, neu_data])
            # fig = px.line(day_of_week_sentiments)

            max_pos = day_of_week_sentiments['Positivo'].max()
            max_neg = day_of_week_sentiments['Negativo'].max()
            max_neu = day_of_week_sentiments['Neutral'].max()
            # min_pos = day_of_week_sentiments['Positivo'].min()
            # min_neg = day_of_week_sentiments['Negativo'].min()
            # min_neu = day_of_week_sentiments['Neutral'].min()

            max_pos_day = day_of_week_sentiments[day_of_week_sentiments['Positivo'] == max_pos].index[0]
            max_neg_day = day_of_week_sentiments[day_of_week_sentiments['Negativo'] == max_neg].index[0]
            max_neu_day = day_of_week_sentiments[day_of_week_sentiments['Neutral'] == max_neu].index[0]
            # min_pos_day = day_of_week_sentiments[day_of_week_sentiments['Positivo'] == min_pos].index[0]
            # min_neg_day = day_of_week_sentiments[day_of_week_sentiments['Negativo'] == min_neg].index[0]
            # min_neu_day = day_of_week_sentiments[day_of_week_sentiments['Neutral'] == min_neu].index[0]
            # fig.add_shape(type='line', x0=0, x1=1, xref='paper', y0=max_pos, y1=max_pos, yref='y', line=dict(color='green',dash='dash'))
            # fig.add_shape(type='line', x0=0, x1=1, xref='paper', y0=max_neg, y1=max_neg, yref='y', line=dict(color='red', dash='dash'))
            # fig.add_shape(type='line', x0=0, x1=1, xref='paper', y0=max_neu, y1=max_neu, yref='y', line=dict(color='gray', dash='dash'))
            
            fig.add_annotation(
                text=f"{round(max_pos,1)}% ↑",
                x=day_of_week_sentiments.index.get_loc(max_pos_day),
                y=max_pos,
                xref="x",
                yref="y",
                xanchor="left",
                yanchor="bottom",
                font=dict(size=16, color='green'),
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor='green',
                ax=20,
                ay=-10
            )
            
            fig.add_annotation(
                text=f"{round(max_neg,1)}% ↑",
                x=day_of_week_sentiments.index.get_loc(max_neg_day),
                y=max_neg,
                xref="x",
                yref="y",
                xanchor="left",
                yanchor="bottom",
                font=dict(size=16, color='red'),
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor='red',
                ax=20,
                ay=-10
            )
            
            fig.add_annotation(
                text=f"{round(max_neu,1)}% ↑",
                x=day_of_week_sentiments.index.get_loc(max_neu_day),
                y=max_neu,
                xref="x",
                yref="y",
                xanchor="left",
                yanchor="bottom",
                font=dict(size=16, color='gray'),
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor='gray',
                ax=20,
                ay=-10
            )
            
            fig.update_layout(xaxis_title='Día de la semana', yaxis_title='Porcentaje %', width=500,height=500,paper_bgcolor="skyblue",
                            margin=dict(l=0,r=0,b=0,t=40,pad=0),)
            
            st.plotly_chart(fig, use_container_width=True)

            # st.dataframe(df)

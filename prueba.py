import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from datetime import date
import numpy as np
import pandas as pd # grafico
import matplotlib.pyplot as plt # grafico
import plotly.express as px # grafico
import plotly.graph_objects as go # grafico  
import snscrape.modules.twitter as sntwitter # modulo tw
import re  # para expresiones regulares
import matplotlib.pyplot as plt
from pysentimiento import create_analyzer  # Para el analisis de sentimiento
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('spanish'))

st.set_page_config(page_title="Tesis", layout="wide")
st.markdown("<style>" + open("./style.css").read() + "</style>", unsafe_allow_html=True)
st.title(
    "DASHBOARD PARA EMPRESAS DE TELECOMUNICACIONES"
)

# TODO: Menu horizontal
selected = option_menu(
    None,
    ["Extraccion", "Dashboard"],
    icons=["file-earmark-arrow-down", "file-bar-graph"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#3178c6"},
        "nav-link": {"font-size": "1rem", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#fb796a"},
    },
)

if selected == "Extraccion":

    # Sirve para generar la fecha actual en el boton de submit para que no vuelva a iterarse
    today = date.today()

    # Para hacer un form y utilizar el boton submit y de esa forma evitar que se genere la tabla de forma automatica
    with st.form("my_form"):
        # Extraccion max de tweets
        maxTweets = 100000
        st.subheader(
            "Ingrese los métodos requeridos para el proceso de extracción de datos"
        )
        # Variable para tratar de hacerlo dinamico
        rango = st.selectbox(
            "Empresa",
            (
                "@NetlifeEcuador",
                "@ClaroEcua",
                "@CNT_EC",
                "@MovistarEC",
                "@TuentiEC",
                "@PuntonetEcuador",
            ),
        )
        # Para elegir un rango de fecha
        since = st.date_input("Desde:")
        until = st.date_input("Hasta:")

        # boton, funciona con un if y por lo regular esta en falso
        # Concatenacion de texto
        result = st.form_submit_button("Generar reporte de sentimiento")
        if result:
            unirRango = f"{rango} since:{since} until:{until}"
        else:
            # unirRango = f"{rango} since:{since} until:{until}"
            unirRango = f"{today.day} since:{today.month} until:{today.year}"

        
        # import time
        # start = time.time()
        # Your code here
        # Tiempo de ejecucion
        # x = [i**2 for i in range(1000000)]
        # end = time.time()
        # st.info(f"Tiempo de ejecutar el analisis: {end - start} segundos")
        
        # Creating list to append tweet data to
        tweets_list = []

        # Using TwitterSearchScraper to scrape data and append tweets to list
        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(unirRango).get_items()
        ):
            if i > maxTweets:
                break
            tweets_list.append(
                [
                    tweet.date,
                    tweet.user.username,
                    tweet.user.followersCount,
                    tweet.user.friendsCount,
                    tweet.user.statusesCount,
                    tweet.user.location,
                    tweet.sourceLabel,
                    tweet.user.profileImageUrl,
                    tweet.rawContent,
                ]
            )

        # Crear el df con las cols necesarias
        tweets_df = pd.DataFrame(
            tweets_list,
            columns=[
                "Datetime",
                "Username",
                "Followers",
                "Following",
                "Tweets",
                "Location",
                "Device",
                "ProfileImg",
                "Text",
            ],
        )

        # Limpia el texto
        def limpiarTweets(text):    
            # convierte el texto a minuscula
            text = text.lower()
            # remueve enlaces
            text = re.sub(r"https\S+|www\S+https\S+", '',text, flags=re.MULTILINE)
            # remueve el usuario con @
            text = re.sub(r'@[A-Za-z09-_-_0-_9]+', '', text)
            # remueve los #   
            text = re.sub(r'#[A-Za-z09]+', '', text)
            # remueve los numeros
            text = re.sub(r'[0-9]\S+', r'', text)
            # remueve emojis y signos de puntuacion
            text = re.sub(r'[^\w\s]','',text)
            text = re.sub(r'RT[\s]+', '', text)
            
            return text
        
        tweets_df['Text_limpio'] = tweets_df['Text'].apply(limpiarTweets)
        
        # Para el analisis de sentimiento
        @st.cache_resource  
        def analisisEsp():
            return create_analyzer(task="sentiment", lang="es")
        analyzer = analisisEsp()
        
        def wordSentiment(text):
            text = str(analyzer.predict(text))
            text = text[22:25]
            return text
        
        ## Aplicar la funcion wordSentiment
        tweets_df['Sentimiento'] = tweets_df['Text_limpio'].apply(wordSentiment)
        
        # Crear un dic para poner los resultados en esp
        palabra_com = {
            'POS' : 'Positivo',
            'NEG' : 'Negativo',
            'NEU' : 'Neutral'
        }
        
        tweets_df['Sentimiento'] = tweets_df['Sentimiento'].map(palabra_com)
        
        # Crear un nuevo df para mostrar las cols principales
        mainCols = tweets_df[
            [
                "Datetime",
                "Username",
                "Location",
                "Device",
                "Text",
                'Sentimiento'
            ]
        ]

        # Muestra el df
        st.dataframe(mainCols, use_container_width=True)
        
        # Genera un mensaje diciendo la cantidad de tws extraidos 
        if len(tweets_df) > 0:
            st.success(f'Se extrajeron {len(tweets_df)} tweets', icon='✅') 
        

    # Agrega automaticamente el nombre del archivo dependiendo las variables ingresadas en el form
    filename = st.text_input(
        "Nombre del archivo:", value=f"{rango} {since} {until}", disabled=True
    )

    if filename == "":
        st.error("Ingrese un nombre!", icon="🚨")
    else:
        # Boton para descargar el archivo csv
        @st.cache_data
        def convert_df(df):
            return df.to_csv().encode("utf-8")

        csv = convert_df(tweets_df)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{filename}.csv",
            mime="text/csv",
        )

    
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
            
        
        # Eliminar los tweets de la empresa
        df = df[df['Username'] != empresa[0]]
        
        # Crear una variable para saber cuantas opciones hay para los graficos
        pola = df["Sentimiento"].value_counts().keys().tolist()

        # Crear un expander y dentro el pie chart
        with st.expander("Polaridad", expanded=True):
            # Cantidad de tweets extraidos
            cantidad = len(df)
            t1,t2 = st.columns(2)
            with t1:
                st.info('Categorización de los sentimientos en base a los tweets de los usuarios', icon="✅")
            with t2:
                st.success(f'Cantidad de tweets analizados: {cantidad}', icon="🤖",)
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
            porc = round((100-(nanVal*100)/cantidad), 2)
            st.warning(f"De {cantidad} tweets,  existen {nanVal} usuarios que no cuentan con una ubicación en Twitter, lo que quiere decir que solo el {porc}% de tweets están siendo procesados para realizar las gráficas", icon='⚠️')
            gpol1, gpol2, gpol3  = st.columns([1,3,1])
            
            with gpol2:
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

            with gpol3:
                maxProv = ubic["Location"].value_counts().keys().tolist()
                numProv = st.multiselect('Elige la provincia:', maxProv, default=maxProv[0])

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
                        width=600, height=370, margin=dict(l=0,r=0,b=10,t=40,pad=0), 
                        # paper_bgcolor="skyblue",
                        # box
                        legend=dict( orientation="v", x=0.5, xanchor='center', y=0.5, yanchor='middle', traceorder="reversed", title_text='Sentimiento', title_font_family="Source Sans Pro",
                        font=dict( family="Source Sans Pro", size=20, 
                        ),
                        bordercolor="gray", borderwidth=2
                    )
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
            with gpol1:
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
                        width=600, height=370, margin=dict(l=0,r=0,b=10,t=40,pad=0), 
                        # paper_bgcolor="skyblue",
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
        
        meses = {
            'January' : 'Enero', 
            'February' : 'Febrero',
            'March' : 'Marzo',
            'April' : 'Abril',
            'May' : 'Mayo',
            'June' : 'Junio',
            'July' : 'Julio',
            'August' : 'Agosto',
            'September' : 'Septiembre',
            'October' : 'Octubre',
            'November' : 'Noviembre' ,
            'December' : 'Diciembre'
        }
        
        horaPal = {
            '0':'Noche',
            '1':'Noche',
            '2':'Noche',
            '3':'Noche',
            '4':'Noche',
            '5':'Madrugada',
            '6':'Madrugada',
            '7':'Madrugada',
            '8':'Madrugada',
            '9':'Madrugada',
            '10':'Madrugada',
            '11':'Mañana',
            '12':'Mañana',
            '13':'Mañana',
            '14':'Mañana',
            '15':'Mañana',
            '16':'Mañana',
            '17':'Tarde',
            '13':'Tarde',
            '19':'Tarde',
            '20':'Tarde',
            '21':'Tarde',
            '22':'Tarde',
            '23':'Noche',
        }
        
        # Aplicar el dic
        df['Dias'] = df['Dias'].map(dayss)
        df['Mes'] = df['Mes'].map(meses)
        df['Hora'] = df['Hora'].map(horaPal)
        
        # DF con el que se trabaja
        date = df[['Sentimiento','Dias']]
        mes = df[['Mes','Sentimiento']]
        hr = df[['Hora','Sentimiento']]
        
        with st.expander("Fecha",expanded=True):
            day1, day2  = st.columns([3, 1])
            
            with day1:
                
                # 1er grafico 
                st.info('Muestra los gráficos de manera completa', icon='🚨')
                day_of_week_sentiments = date.groupby(['Dias', 'Sentimiento']).size().reset_index(name='counts')
                day_of_week_sentiments = day_of_week_sentiments.pivot(index='Dias', columns='Sentimiento', values='counts')
                day_of_week_sentiments = day_of_week_sentiments.reindex(['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])
                day_of_week_sentiments = day_of_week_sentiments.divide((day_of_week_sentiments.sum(axis=1)/100), axis=0)

                days = day_of_week_sentiments.index.tolist()

                pos_data = go.Scatter(x=days, y=day_of_week_sentiments['Positivo'], name='Positivo', line=dict(color='#2ca02c'))
                neg_data = go.Scatter(x=days, y=day_of_week_sentiments['Negativo'], name='Negativo', line=dict(color='crimson'))
                neu_data = go.Scatter(x=days, y=day_of_week_sentiments['Neutral'], name='Neutral', line=dict(color='gray'))
                
                fig = go.Figure(data=[pos_data, neg_data, neu_data])
                # fig = px.line(day_of_week_sentiments)

                max_pos = day_of_week_sentiments['Positivo'].max()
                max_neg = day_of_week_sentiments['Negativo'].max()
                max_neu = day_of_week_sentiments['Neutral'].max()
                
                max_pos_day = day_of_week_sentiments[day_of_week_sentiments['Positivo'] == max_pos].index[0]
                max_neg_day = day_of_week_sentiments[day_of_week_sentiments['Negativo'] == max_neg].index[0]
                max_neu_day = day_of_week_sentiments[day_of_week_sentiments['Neutral'] == max_neu].index[0]
                
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
                
                fig.update_layout(title='Días de la semana', yaxis_title='Porcentaje %', yaxis_title_font_size=20, 
                                width=500,height=500,
                                paper_bgcolor="skyblue", 
                                margin=dict(l=0,r=0,b=20,t=30,pad=0),)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 2do grafico area
                
                hrValues = hr.groupby(['Hora', 'Sentimiento']).size().reset_index(name='counts')
                hrValues = hrValues.pivot(index='Hora', columns='Sentimiento', values='counts')

                # Para hacer el grafico en %
                # hrValues = hrValues.divide((hrValues.sum(axis=1)/100), axis=0)
                hrValues = hrValues.reindex(['Mañana','Tarde','Noche','Madrugada'])

                # Plot the line chart for the sentiments
                fig, ax = plt.subplots(figsize=(10,3.94))
                hrValues.plot(kind='area',ax=ax, stacked=False, color=['crimson','gray','#2ca02c'])

                # Obtiene el maximo valor de los sentimientos
                hr_pos = hrValues['Positivo'].max()
                hr_neg = hrValues['Negativo'].max()
                hr_neu = hrValues['Neutral'].max()

                # Obtiene la posicion del max valor de los sentimientos
                max_pos_hr = hrValues[hrValues['Positivo'] == hr_pos].index[0]
                max_neg_hr = hrValues[hrValues['Negativo'] == hr_neg].index[0]
                max_neu_hr = hrValues[hrValues['Neutral'] == hr_neu].index[0]

                # Agrega una line que recorre todo el chart
                ax.axhline(hr_pos, color='green', linestyle='--')
                ax.axhline(hr_neg, color='red', linestyle='--')
                ax.axhline(hr_neu, color='gray', linestyle='--')

                ax.annotate(f'                      Max Positivo', xy=(hrValues.index.get_loc(max_pos_hr), hr_pos), 
                                                                xycoords='data', size=10, ha='left', va='bottom', color='green', 
                                                                weight='bold',arrowprops=dict(arrowstyle="->", color='black'))
                ax.annotate(f'                      Max Negativo', xy=(hrValues.index.get_loc(max_neg_hr), hr_neg), 
                                                                xycoords='data', size=10, ha='left', va='bottom', color='red', 
                                                                weight='bold', arrowprops=dict(arrowstyle="->", color='black'))
                ax.annotate(f'                      Max Neutral', xy=(hrValues.index.get_loc(max_neu_hr), hr_neu), 
                                                                xycoords='data', size=10, ha='left', va='bottom', color='gray', 
                                                                weight='bold', arrowprops=dict(arrowstyle="->", color='black'))

                ax.set_xlabel('')
                ax.set_title('Tiempo del día', size=14, weight='bold')
                # ax.set_ylabel('Total Tweets', size=14, weight='bold')
                ax.tick_params(axis='x', rotation=0)
                fig.tight_layout()
                st.pyplot(fig)
                
                # 3er grafico barh
                mesValues = mes.groupby(['Mes', 'Sentimiento']).size().reset_index(name='counts')
                mesValues = mesValues.pivot(index='Mes', columns='Sentimiento', values='counts')
                mesValues = mesValues.divide((mesValues.sum(axis=1)/100), axis=0)
                
                fig = px.bar(mesValues,orientation='h' ,barmode='group',color_discrete_map={'Negativo': 'crimson', 'Neutral': 'gray', 'Positivo': '#2ca02c'},
                            text_auto=True, 
                            )
                fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=1, texttemplate='%{value:.1f}%')
                fig.update_layout(
                    title='Meses del año',
                    xaxis=dict(title="", tickangle=0, tickfont=dict(size=18)),
                    yaxis=dict(title=""),
                    height=507,
                    paper_bgcolor="skyblue",
                    margin=dict(l=0,r=0,b=0,t=30,pad=0)
                )
                st.plotly_chart(fig,use_container_width=True)
                
            
            with day2:
                
                st.info('Muestra los gráficos de manera individual', icon='🚨')
                # 1er bar Dias
                maxDia = date["Dias"].value_counts().keys().tolist()
                indDia = st.select_slider('Selecciona un día:', maxDia)
                def tolist(string):
                    li = list(string.split(" "))
                    return li
                li = tolist(indDia)
                sel_day = date[date['Dias'].isin(li)]
                day_of_week_sentiments = sel_day.groupby(['Dias', 'Sentimiento']).size().reset_index(name='counts')
                day_of_week_sentiments = day_of_week_sentiments.pivot(index='Dias', columns='Sentimiento', values='counts')
                
                fig = px.bar(day_of_week_sentiments, barmode='group',color_discrete_map={'Negativo': 'crimson', 'Neutral': 'gray', 'Positivo': '#2ca02c'},
                            text_auto=True, 
                            # pattern_shape_sequence=["|", "x", "+"]['', '/', '\\', 'x', '-', '|', '+', '.']
                            )
                fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=1)
                fig.update_layout(
                    legend=dict(title="", font=dict(size=10), orientation="h", x=0.5, xanchor='center', y=-0.11, yanchor='middle',),
                    xaxis=dict(title="", tickangle=0, tickfont=dict(size=18)),
                    yaxis=dict(title="", tickfont=dict(size=12)),
                    margin=dict(l=0, r=0, t=0, b=0 ,pad=0),
                    height=397,
                    paper_bgcolor="skyblue",
                )

                st.plotly_chart(fig,use_container_width=True)
                
                # 2er bar tiempo del dia
                maxHr = hr["Hora"].value_counts().keys().tolist()
                indHR = st.select_slider('Selecciona un tiempo del día:', maxHr)
                def tolist(string):
                    li = list(string.split(" "))
                    return li
                liHr = tolist(indHR)
                sel_hr = hr[hr['Hora'].isin(liHr)]
                hr_sentiments = sel_hr.groupby(['Hora', 'Sentimiento']).size().reset_index(name='counts')
                hr_sentiments = hr_sentiments.pivot(index='Hora', columns='Sentimiento', values='counts')
                
                fig = px.bar(hr_sentiments, barmode='group',color_discrete_map={'Negativo': 'crimson', 'Neutral': 'gray', 'Positivo': '#2ca02c'},
                            text_auto=True, 
                            # pattern_shape_sequence=["|", "x", "+"]['', '/', '\\', 'x', '-', '|', '+', '.']
                            )
                fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=1)
                fig.update_layout(
                    legend=dict(title="", font=dict(size=10), orientation="h", x=0.5, xanchor='center', y=-0.11, yanchor='middle',),
                    xaxis=dict(title="", tickangle=0, tickfont=dict(size=18)),
                    yaxis=dict(title="", tickfont=dict(size=12)),
                    margin=dict(l=0, r=0, t=0, b=0 ,pad=0),
                    height=397,
                    paper_bgcolor="skyblue",
                )

                st.plotly_chart(fig,use_container_width=True)
                
                # 3er bar meses
                maxMes = mes["Mes"].value_counts().keys().tolist()
                indMes = st.select_slider('Selecciona un mes:', 
                                        #   maxMes,
                                        options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])
                def tolist(string):
                    li = list(string.split(" "))
                    return li
                liHr = tolist(indMes)
                sel_mes = mes[mes['Mes'].isin(liHr)]
                mesValues =sel_mes.groupby(['Mes', 'Sentimiento']).size().reset_index(name='counts')
                mesValues = mesValues.pivot(index='Mes', columns='Sentimiento', values='counts')
                
                fig = px.bar(mesValues, barmode='group',color_discrete_map={'Negativo': 'crimson', 'Neutral': 'gray', 'Positivo': '#2ca02c'},
                            text_auto=True, 
                            # pattern_shape_sequence=["|", "x", "+"]['', '/', '\\', 'x', '-', '|', '+', '.']
                            )
                fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=1)
                fig.update_layout(
                    legend=dict(title="", font=dict(size=10), orientation="h", x=0.5, xanchor='center', y=-0.11, yanchor='middle',),
                    xaxis=dict(title="", tickangle=0, tickfont=dict(size=18)),
                    yaxis=dict(title="", tickfont=dict(size=12)),
                    margin=dict(l=0, r=0, t=0, b=0 ,pad=0),
                    height=397,
                    paper_bgcolor="skyblue",
                )

                st.plotly_chart(fig,use_container_width=True)

        with st.expander("Dispositivos",expanded=True):
        
            disp = df[["Device", "Sentimiento"]]
            disp1, disp2 = st.columns([3,1])
            with disp1:
                mainDisp = disp["Device"].value_counts().keys().tolist()

                # Select the locations you want to show the chart for
                tdisp = mainDisp[0:3] if len(mainDisp) == 3 else mainDisp[0:3]
                disp_ind = tdisp
                device_sentiments = disp.groupby(['Device', 'Sentimiento']).size().reset_index(name='counts')
                device_sentiments = device_sentiments.pivot(index='Device', columns='Sentimiento', values='counts')
                device_sentiments = device_sentiments.divide((device_sentiments.sum(axis=1)/100), axis=0)
                fig = px.bar(device_sentiments.loc[disp_ind], color_discrete_map={'Negativo': 'crimson', 'Neutral': 'gray', 'Positivo': '#2ca02c'}, orientation='h',text_auto=True,)
                
                fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=1, texttemplate='%{value:.1f}%')
                fig.update_layout(barmode='stack', xaxis_title='Porcentaje %', yaxis_title='', title='Dispositivos', legend_title='Sentimiento',
                    paper_bgcolor="skyblue",
                    height=500,)

                st.plotly_chart(fig,use_container_width=True)    

            with disp2:
                # 2do chart
                mainDisp2 = disp["Device"].value_counts().keys().tolist()
                indDisp = st.select_slider('Selecciona un dispositivo:', mainDisp2)
                def tolist(string):
                    lid = list(string.split(","))
                    return lid
                lid = tolist(indDisp)
                sel_disp = disp[disp['Device'].isin(lid)]
                device_sentiments = sel_disp.groupby(['Device', 'Sentimiento']).size().reset_index(name='counts')
                device_sentiments = device_sentiments.pivot(index='Device', columns='Sentimiento', values='counts')
                
                fig = px.bar(device_sentiments, barmode='group',color_discrete_map={'Negativo': 'crimson', 'Neutral': 'gray', 'Positivo': '#2ca02c'}, text_auto=True,)
                fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=1)
                fig.update_layout(
                    legend=dict(title="", font=dict(size=10), orientation="h", x=0.5, xanchor='center', y=-0.12, yanchor='middle',),
                    xaxis=dict(title="", tickangle=0, tickfont=dict(size=18)),
                    yaxis=dict(title="", tickfont=dict(size=12)),
                    margin=dict(l=0, r=0, t=0, b=0 ,pad=0),
                    height=397,
                    paper_bgcolor="skyblue",
                )

                st.plotly_chart(fig,use_container_width=True)
            
        with st.expander("Frecuencia de Palabras",expanded=True):
            # Add palabras al stopwords
            elimiar_es = [
                'q','gran','ing','dientes','carlos','parte','usuarios','pepin','siga','septiembre','carbensemix','oracle','trae','mayo','sectores','labor', 'alianza','gerente','nacional','compañeros','junto','juntos','migración','pensamosenti','suárez','año','si','cada','vez','d','x','hoy', 'provincia','punta','muchas','ahora','abril','enero','febrero','junio','julio','agosto','marzo','octubre','noviembre','diciembre','así','mas', 'galápagos','siempre','clientes','presente','país','puerta','todossomoscnt','cntep','adelante','2','3','4','5','6','7','8','9','0','solo', 'días','día','van','dan','hace','ustedes','señores'
            ]

            stop_words = nltk.corpus.stopwords.words('spanish')
            stop_words.extend(elimiar_es)
            
            # Funcion para eliminar stopwords
            def wordImg(text):
                text = text.lower()
                text = re.sub(r"https\S+|www\S+https\S+", '',text, flags=re.MULTILINE)
                text = re.sub(r'@[A-Za-z09-_-_0-_9]+', '', text)
                text = re.sub(r'#[A-Za-z09-á-é-í-ó-ú]+', '', text)
                text = re.sub(r'[0-9]\S+', r'', text)
                text = re.sub(r'[^\w\s]','',text)
                text = re.sub(r'RT[\s]+', '', text)
                text_tokens = word_tokenize(text)
                filtered_text = [w for w in text_tokens if not w in stop_words]
                return " ".join(filtered_text)
            
            # Crear una cal y aplicar la def
            df['Fre_Words'] = df['Text'].apply(wordImg)
            
            # Nuevo DF
            words = df[['Fre_Words','Sentimiento']]
            
            pos_tweets = df[df['Sentimiento'] == 'Positivo']
            neg_tweets = df[df['Sentimiento'] == 'Negativo']
            
            positive_words = pos_tweets['Fre_Words'].str.split(expand=True).stack().value_counts()
            negative_words = neg_tweets['Fre_Words'].str.split(expand=True).stack().value_counts()
            
            # wordGr = positive_words.keys().tolist()
            # st.write(wordGr[0])
            wordGr = st.slider('¿Cuántas palabras?', 0, 30, 5)
                
            fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))
            # pos
            positive_words.head(wordGr).plot(kind='pie', ax=ax1, textprops=dict(color="green", size=11, weight='black'), 
                                        startangle = 90, wedgeprops = {"linewidth": 2, "edgecolor": "#383838"},)
            ax1.set_title("Frecuencia - Palabras Positivas", size=14, weight='bold')
            ax1.set_ylabel('')

            #neg
            negative_words.head(wordGr).plot(kind='pie', ax=ax2, textprops=dict(color="red", size=11, weight='black'), 
                                        startangle = 90, wedgeprops = {"linewidth": 2, "edgecolor": "#383838"},)
            ax2.set_title("Frecuencia - Palabras Negativas", size=14, weight='bold')
            ax2.set_ylabel('')

            ax1.legend(title="Positivas", loc='center', fontsize=12, bbox_to_anchor=(1, 0, 0.65, 1), fancybox=True, framealpha=0.5)
            ax2.legend(title="Negativas", loc='center', fontsize=12, bbox_to_anchor=(1, 0, 0.65, 1), fancybox=True, framealpha=0.5)
            
            st.pyplot(fig)

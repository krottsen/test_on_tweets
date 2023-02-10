# import streamlit as st
# import snscrape.modules.twitter as sntwitter
# import pandas as pd
# import numpy as np

# # st. es el nombre acortado dado a streamlit

# # Para hacer un form y utilizar el boton submit y de esa forma evitar que se genere la tabla de forma automatica
# with st.form("my_form"):
#     # Extraccion max de tweets
#     maxTweets = 50000

#     # Variable para tratar de hacerlo dinamico
#     st.text("Ingrese los metodos requeridos para el proceso de extraccion de datos")
#     rango = st.text_input("Empresa", "@NetlifeEcuador", disabled=False)
#     # Para elegir un rango de fecha
#     since = st.date_input("Desde:")
#     until = st.date_input("Hasta:")

#     # boton, funciona con un if y por lo regular esta en falso
#     # Concatenacion de texto
#     result = st.form_submit_button("Generar reporte de sentimiento")
#     if result:
#         unirRango = f"{rango} since:{since} until:{until}"
#     else:
#         unirRango = f"{rango} since:{since} until:{until}"

#     # Creating list to append tweet data to
#     tweets_list2 = []

#     # Using TwitterSearchScraper to scrape data and append tweets to list
#     for i, tweet in enumerate(sntwitter.TwitterSearchScraper(unirRango).get_items()):
#         if i > maxTweets:
#             break
#         tweets_list2.append(
#             [tweet.date, tweet.user.username, tweet.content, tweet.sourceLabel]
#         )

#     # Creating a dataframe from the tweets list above
#     tweets_df2 = pd.DataFrame(
#         tweets_list2, columns=["Datetime", "Username", "Content", "Device"]
#     )

#     # Display first 5 entries from dataframe
#     # tweets_df2.head()
#     st.table(tweets_df2)

# Test PDF
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


def save_multi_image(filename):
    pp = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        pp.savefig(fig)
    pp.close()


uploaded_file = st.file_uploader("Elige un archivo csv")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)

    # Eliminar cols
    # df = df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1)

    # Un dic para filtar las provincias
    mymap = {
        "Ambato": "Tungurahua",
        "ambato": "Tungurahua",
        "Ambato Ecuador": "Tungurahua",
        "Ambato, Ecuador": "Tungurahua",
        "Ambato - Ecuador": "Tungurahua",
        "Ambato -Ecuador": "Tungurahua",
        "Ambato - Quito - Ecuador 🇪🇨": "Tungurahua",
        "Ambato - Tierrita Linda 🇪🇨": "Tungurahua",
        "Antonio Ante, Ecuador": "Imbabura",
        "Arenillas, Ecuador": "El Oro",
        "Atacames, Ecuador": "Esmeraldas",
        "Azogues Ecuador": "Cañar",
        "Azogues, Ecuador": "Cañar",
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
        "Cayambe": "Pichincha",
        "Cayambe, Ecuador": "Pichincha",
        "Cayambe, Quito, Ecuador.": "Pichincha",
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
        "Cumbaya": "Pichincha",
        "Cumbaya,Ecuador": "Pichincha",
        "Cumbayá - Quito": "Pichincha",
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
        "Ecuador - Quito": "Pichincha",
        "Ecuador- Quito": "Pichincha",
        "Ecuador, Quito": "Pichincha",
        "Ecuador- Duran": "Guayas",
        "Eloy Alfaro, Ecuador": "Guayas",
        "EL EMPALME - GUAYAS": "Guayas",
        "Empalme, Ecuador": "Guayas",
        "El Oro / Guayas": "El Oro",
        "El Oro, Ecuador": "El Oro",
        "El Triunfo, Ecuador": "Guayas",
        "Esmeraldas": "Esmeraldas",
        "Esmeraldas - Ecuador": "Esmeraldas",
        "Esmeraldas-Ecuador": "Esmeraldas",
        "Esmeraldas, Ecuador": "Esmeraldas",
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
        "Ibarra": "Imbabura",
        "Ibarra Ecuador": "Imbabura",
        "Ibarra, Ecuador": "Imbabura",
        "Ibarra- Ecuador": "Imbabura",
        "Ibarra - Ecuador": "Imbabura",
        "Ibarra-Imbabura-Ecuador": "Imbabura",
        "IMBABURA": "Imbabura",
        "Imbabura, Ecuador": "Imbabura",
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
        "La Troncal, Ecuador": "Cañar",
        "Lago Agrio": "Sucumbíos",
        "Lago Agrio - Ecuador": "Sucumbíos",
        "Lago Agrio, Ecuador": "Sucumbíos",
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
        "Mitad del Mundo": "Pichincha",
        "Mitad del Mundo 🇪🇨": "Pichincha",
        "MITAD DEL MUNDO!": "Pichincha",
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
        "Pichincha - Quito": "Pichincha",
        "Pichincha, Ecuador": "Pichincha",
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
        "Quininde, Ecuador": "Esmeraldas",
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
        "riobamba": "Chimborazo",
        "Riobamba": "Chimborazo",
        "Riobamba ecuador": "Chimborazo",
        "Riobamba - Ecuador": "Chimborazo",
        "Riobamba-Ecuador": "Chimborazo",
        "Riobamba Ecuador": "Chimborazo",
        "Riobamba, Ecuador": "Chimborazo",
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
        "San Lorenzo, Ecuador": "Esmeraldas",
        "San Lorenzo, Esmeraldas- Ecuad": "Esmeraldas",
        "San Miguel De Los Bancos, Ecua": "Pichincha",
        "San Miguel, Ecuador 🇪🇨": "Pichincha",
        "San Rafael, cantón Rumiñahui": "Pichincha",
        "San Rafael, Ecuador": "Pichincha",
        "Sangolquí": "Pichincha",
        "Sangolqui": "Pichincha",
        "sangolqui - ecuador": "Pichincha",
        "sangolqui, ecuador": "Pichincha",
        "Santa Cruz, Galápagos": "Galápagos",
        "Santa Ana, Manabí, Ecuador": "Manabí",
        "Santa Elena, Ecuador": "Santa Elena",
        "Santa Lucía, Guayas, Ecuador": "Guayas",
        "Santo Domingo De Los Tsachilas, Ecuador": "Santo Domingo de los Tsáchilas",
        "Santo Domingo, Ecuador": "Santo Domingo de los Tsáchilas",
        "Santo Domingo - Ecuador": "Santo Domingo de los Tsáchilas",
        "santo domingo- ecuador": "Santo Domingo de los Tsáchilas",
        "Santo Domingo de los Tsachilas": "Santo Domingo de los Tsáchilas",
        "Santo Domingo": "Santo Domingo de los Tsáchilas",
        "santo domingo": "Santo Domingo de los Tsáchilas",
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
    }
    # TODO:Sirve para eliminar el warning, x ahora lo usare, pero tratare de encontrar una forma diferente
    st.set_option("deprecation.showPyplotGlobalUse", False)

    # Funcion map para que filtre con el dic recien creado
    df["Location"] = df["Location"].map(mymap)

    # Los valores NaN para no perder datos, tendran como valor la palabra Ecuador
    # df["Location"] = df["Location"].fillna("Ecuador")

    # Muestra una tabla con los valores en la col Location
    # st.table(df["Location"].value_counts())

    # Variables
    location = df["Location"].value_counts()
    device = df["Device"].value_counts()

    st.title("Dashboard")
    with st.container():
        # TODO:Cuando trabaje con en csv normal debo crear un nuevo df dropeando la traduccion en ing
        st.write("Informacion del dataframe")
        # st.dataframe(df, use_container_width=True, height=245)

    col1, col2 = st.columns(2)

    with col1:
        st.text("Grafico de ubicacion")
        # st.text(f" Hay {nanVal} personas que no cuentan con una ubicacion en Twitter")
        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        # tab1.write("comida")
        values = tab1.slider("Rango de provincias", 3, 24)
        colors = ("#cc5a49", "#4586ac", "white", "green", "red")
        wp = {"linewidth": 0.2, "edgecolor": "#383838"}
        # Solo muestra los primero 5 valores
        tags = location.nlargest(values)
        tags.plot(
            kind="pie",
            autopct="%1.1f%%",
            # colors=colors,
            # startangle=90,
            wedgeprops=wp,
            legend=("reverse", 1),
            figsize=(10, 8),
            fontsize=6,
        )
        # plt.title("Polaridad")
        # st.pyplot()

        tab1.pyplot()

        # tab1.line_chart(location, height=388)
        tab2.dataframe(location, use_container_width=True, height=388)
        # Expandir

    with col2:
        st.text("Grafico de dispositivo")
        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        # tab1.subheader("A tab with a chart")
        # plt.figure(figsize=(10, 5))
        sns.countplot(data=df, y="Device")
        # st.pyplot()
        tab1.pyplot()
        # tab2.subheader("A tab with the data")
        tab2.dataframe(device, use_container_width=True, height=388)

        # IMAGEN EN PDF
        # df["Location"].value_counts()
        # plt.figure(figsize=(20, 10))
        plt.title("Provincias")
        # plt.xlabel('')
        # plt.xlabel('Ciudad/Provincia/Pais')
        df["Location"].value_counts().nlargest(5).plot(kind="pie")
        # plt.show()
        fig, ax = plt.subplots()
        ax.hist([1, 2, 3, 4])
        ax.set(
            xlabel="Combined Fuel Economy (MPG)",
            ylabel="Number of cars",
            title="Combined Fuel Economy (2000-2020)",
        )

    fig, ax = plt.subplots()

    fruits = ["apple", "blueberry", "cherry", "orange"]
    counts = [40, 100, 30, 55]
    bar_labels = ["red", "blue", "_red", "orange"]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel("fruit supply")
    ax.set_title("Fruit supply by kind and color")
    ax.legend(title="Fruit color")
    st.pyplot(fig)
    # fig.show()

    if st.button("Download PDF"):
        with open(filename, 'rb') as f:
            b = f.read()
            st.write("Here is your file: ", st.file_downloader("Download PDF", b, "t3.pdf"))

    # FUNCION PARA HACER EL PDF

    # if st.button("Say hello"):
    #     st.write("Why hello there")

    #     def save_multi_image(filename):
    #         pp = PdfPages(filename)
    #         fig_nums = plt.get_fignums()
    #         figs = [plt.figure(n) for n in fig_nums]
    #         for fig in figs:
    #             fig.savefig(pp, format="pdf")
    #         pp.close()

    #     filename = "t3.pdf"
    #     save_multi_image(filename)
    # else:
    #     st.write("Goodbye")
    # ---------------------------------------------------------------------------------------------------------------------------------

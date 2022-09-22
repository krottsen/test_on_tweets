import streamlit as st
!pip3 install snscrape
import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np

# st. es el nombre acortado dado a streamlit

# Para hacer un form y utilizar el boton submit y de esa forma evitar que se genere la tabla de forma automatica
with st.form("my_form"):
    # Extraccion max de tweets
    maxTweets = 50000

    # Variable para tratar de hacerlo dinamico
    st.text("Ingrese los metodos requeridos para el proceso de extraccion de datos")
    rango = st.text_input("Empresa", "@NetlifeEcuador", disabled=True)
    # Para elegir un rango de fecha
    since = st.date_input("Desde:")
    until = st.date_input("Hasta:")

    # boton, funciona con un if y por lo regular esta en falso
    # Concatenacion de texto
    result = st.form_submit_button("Generar reporte de sentimiento")
    if result:
        unirRango = f"{rango} since:{since} until:{until}"
    else:
        unirRango = f"{rango} since:{since} until:{until}"

    # Creating list to append tweet data to
    tweets_list2 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(unirRango).get_items()):
        if i > maxTweets:
            break
        tweets_list2.append(
            [tweet.date, tweet.user.username, tweet.content, tweet.sourceLabel]
        )

    # Creating a dataframe from the tweets list above
    tweets_df2 = pd.DataFrame(
        tweets_list2, columns=["Datetime", "Username", "Content", "Device"]
    )

    # Display first 5 entries from dataframe
    # tweets_df2.head()
    st.table(tweets_df2)

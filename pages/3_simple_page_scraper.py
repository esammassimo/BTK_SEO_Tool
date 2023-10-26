import os
import streamlit as st
st.write(st.session_state["shared"])

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

st.title("Scrape Page")
st.write("Estrae da una pagina HTML il title, la description e l'h1.")

url = st.text_input("Inserisci URL:")
if url:
    st.write("URL: ", url)
    
    l = []
    r = requests.get(url).text
    soup = BeautifulSoup(r, "html.parser")

    d={}
    d["title"] = soup.find("title").text
    d["description"] = soup.find("meta", {"name":"description"}).get('content')
    d["H1"] = soup.find("h1").text
    l.append(d)

    df = pd.DataFrame(l)
    st.write(df)
    
else:
    st.write("Nessuna URL inserita")
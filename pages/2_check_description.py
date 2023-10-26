import os
import streamlit as st
st.write(st.session_state["shared"])

from bs4 import BeautifulSoup
import requests
import pandas as pd

st.title("Check Description")
st.write("Il file deve contenere nella prima colonna le URL, nella seconda la Meta Description SEO ottimizzata.")
st.write("Lo script controlla che la Meta Description SEO ottimizzata sia stato correttamente implementata in pagina.")

try:
    file_name = st.file_uploader("Carica il File")
except:
    st.write("Errore in fase di lettura del file. Verificare di aver inserito correttamente nome ed estensione.")

try:
    df = pd.read_excel(file_name)
except:
    st.write("Errore in fase di lettura del file. Verificare di aver inserito correttamente nome ed estensione.")

df["Description online"] = ""
df["Check"] = ""
for index, row in df.iterrows():
    try:
        pagina = requests.get(row[0])
        contenutoPagina = pagina.content
        contenutoParsato = BeautifulSoup(contenutoPagina,"html.parser")
        try:
            descr = contenutoParsato.find("meta", {"name":"description"}).get("content")
            descr = descr.lstrip()
            descr = descr.strip('\n')
            descr = descr.strip('\t')
            descr = descr.strip('\r')
            row["Description online"] = descr
            if row[1] == row["Description online"]:
                row["Check"] = "Ottimizzata"
            else:
                row["Check"] = "Non ottimizzata"
        except:
            row["Description online"] = "Errore in lettura della Meta Description"
            row["Check"] = ""
    except:
        row["Description online"] = "Errore generale"
        row["Check"] = ""

try:
    df.to_excel("check-description.xlsx", index=False)
    st.write("File salvato correttamente.")
except:
    st.write("Errore nel salvataggio.")
df
import os
import streamlit as st
st.write(st.session_state["shared"])

from bs4 import BeautifulSoup
import requests
import pandas as pd

st.title("Check Title")
st.write("Il file deve contenere nella prima colonna le URL, nella seconda il Title SEO ottimizzato.")
st.write("Lo script controlla che il Title SEO ottimizzato sia stato correttamente implementato in pagina.")

file_name = st.file_uploader("Carica il File")

if file_name:
    df = pd.read_excel(file_name)
    
    df["Title online"] = ""
    df["Check"] = ""
    for index, row in df.iterrows():
        try:
            pagina = requests.get(row[0])
            contenutoPagina = pagina.content
            contenutoParsato = BeautifulSoup(contenutoPagina,"html.parser")
            try:
                title = contenutoParsato.find("title").text
                title = title.lstrip()
                title = title.strip('\n')
                title = title.strip('\t')
                title = title.strip('\r')
                row["Title online"] = title
                if row[1] == row["Title online"]:
                    row["Check"] = "Ottimizzato"
                else:
                    row["Check"] = "Non ottimizzato"
            except:
                row["Title online"] = "Errore in lettura del Title"
                row["Check"] = ""
        except:
            row["Title online"] = "Errore generale"
            row["Check"] = ""
    
    xls_file = df.to_excel("check-title.xlsx", index=False)
    
    st.write("File salvato correttamente.")
    st.dataframe(df)
    
    st.download_button(
        label="Download File",
        data=xls_file,
        file_name="check_title.csv",
        mime="text/csv",
    )
    
else:
    st.write("Nessun File Caricato")
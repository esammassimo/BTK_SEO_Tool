import os
from apikey import apikey
import streamlit as st

import openai
import people_also_ask

st.write(st.session_state["shared"])
openai.api_key = apikey

st.title("People Also Asked GPT Rewrite")
st.write("Data una query estrae le domande degli Utenti e le riscrive tramite Chat GPT")

kw = st.text_input("Inserisci keyword (in inglese): ")
if kw:
    st.write("Query: ", kw)
    
    questions = people_also_ask.get_related_questions(kw)
    
    for question in questions:
        def risposte(kw):
            
            response = openai.ChatCompletion.create(
                model = "gpt-4",
                temperature = 0.9,
                max_tokens = 2500,
                messages = [
                    {"role":"system", "content":"You are an Italian SEO Professional"},
                    {"role":"user", "content":f"Write me and translate in italian a quick answer for the {question}, write in italian language with minimum 400-word lenght"},
                    {"role":"user", "content":f"Titolo: {question}\nKeyword:{kw}"}
                ]
            )
            
            generated_text = response["choices"][0]["message"]["content"]
            return generated_text
    
    answers = risposte(kw)
    st.write(f"Domanda:{question}\nRisposta:\n{answers}")
else:
    st.write("Nessuna Keyword Inserita")
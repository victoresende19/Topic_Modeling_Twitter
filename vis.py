from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_icon='🦜', page_title='Tópicos Twitter', layout='centered')
st.markdown("<h1 style='text-align: center; color: black;'> 🏎️ Twitter - Formula 1 🏎️ </h1>", unsafe_allow_html=True)
st.write("<p align='justify'> <strong>Esse venceu o hackathon IBM Esteira Cognitiva.</strong> Visava utilizar a API do X (antigo Twitter) em Python para, à escolha de um tema a gosto do autor, identificar os tópicos mais abordados nos tweets do respectivo tema, do qual escolheu-se por: <strong> Formúla 1 </strong> <p align='justify'>", unsafe_allow_html=True)
st.write("<p align='justify'> Por Victor Augusto Souza Resende  <p align='justify'>", unsafe_allow_html=True)
suspense_bar = st.selectbox('Selecione tipo de visualização:', ['bigram', 'trigram'], key="1")

db = create_engine(f'sqlite:///twitter_{str(suspense_bar)}.sqlite', echo=False)
conn = db.raw_connection()
query = f'SELECT * FROM twitter_{str(suspense_bar)}'
df = pd.read_sql_query(query, conn)

fig = px.bar(df[0:11], x='termo', y='rank')
st.plotly_chart(fig)
st.write(f"<p align='justify'> Quantidade de dados: {len(df)} <p align='justify'>", unsafe_allow_html=True)

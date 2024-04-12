from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_icon='🦜', page_title='Tópicos Twitter', layout='centered')
st.markdown("<h3 style='text-align: center; color: black;'> 🏎️ Assuntos Twitter: Fórmula 1 🏎️ </h3>", unsafe_allow_html=True)
st.write("<p align='justify'> <strong>Esse projeto venceu o hackathon IBM Esteira Cognitiva 2023, utiliza o conceito de Topic Modeling.</strong> Visava utilizar a API do X (antigo Twitter) em Python para, à escolha de um tema escolhido pelo do autor, identificar os tópicos mais abordados nos tweets do respectivo tema, do qual escolheu-se por: <strong> Fórmula 1 </strong>. <p align='justify'>", unsafe_allow_html=True)
st.write("<p align='justify'> O projeto foi concebido após a arquitetura: ETL para extração e aplicação de técnicas de NLP (Normalização, tokenização e lematização) visando o tratamento dos textos nos tweets em Python. Aplicação da técnica TF-IDF para a configuração dos pesos nas palavras mais relevantes do corpus em Python. Armazenamento dos resultados em unigrama, bigrama, trigrama em um banco de dados SQLite via Python. Por fim, a disponibilização dos resultados utilizando a biblioteca Streamlit em Python. <p align='justify'>", unsafe_allow_html=True)
st.write("<p align='justify'> Por Victor Augusto Souza Resende  <p align='justify'>", unsafe_allow_html=True)
suspense_bar = st.selectbox('Selecione tipo de visualização:', ['bigram', 'trigram'], key="1")

db = create_engine(f'sqlite:///twitter_{str(suspense_bar)}.sqlite', echo=False)
conn = db.raw_connection()
query = f'SELECT * FROM twitter_{str(suspense_bar)}'
df = pd.read_sql_query(query, conn)

fig = px.bar(df[0:11], x='termo', y='rank')
st.plotly_chart(fig)
st.write(f"<p align='justify'> Quantidade de dados: {len(df)} <p align='justify'>", unsafe_allow_html=True)

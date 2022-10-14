from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import streamlit as st

st.title('Tópico Twiiter - Fórmula 1')
suspense_bar = st.selectbox('Selecione', ['bigram', 'trigram'], key="1")

db = create_engine(f'sqlite:///twitter_{str(suspense_bar)}.sqlite', echo=False)
conn = db.connect()
query = f'SELECT * FROM twitter_{str(suspense_bar)}'
df = pd.read_sql_query(query, conn)
st.plotly_chart(sns.barplot(data=df, x="termo", y="rank"))
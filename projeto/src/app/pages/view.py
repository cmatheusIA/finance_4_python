import sys
sys.path.append('/mnt/o/finance_4_python/projeto/src/ingestao')
import streamlit as st
from crawler.crawler import Crawler
import time

st.title("Finance with Python")



robot = Crawler()


paises = robot.get_countries()
opcoes = ['FIIS','ACOES']
with st.sidebar:
    opt = st.selectbox(
        'Escolha uma das opções abaixo',
        opcoes
    )
    if opt== opcoes[0]:
        st.write('FII')
        # option  = st.selectbox(
        #     'Escolha o pais dos ativos',
        #     paises
        # )
        df,symbols = robot.getFIIS()
        options_2 = st.multiselect(
        'Escolha seus ativos',
        symbols)
        # st.write('Pais selecionado:', option)
        st.write( options_2)
        print(options_2)
    if opt == opcoes[1]:
        st.write('ACOES')
        option  = st.selectbox(
            'Escolha o pais dos ativos',
            paises
        )
        df,symbols = robot.get_symbol_by_country(option)

        options_2 = st.multiselect(
        'Escolha seus ativos',
        symbols)
        st.write('Pais selecionado:', option)
        st.write( options_2)
        print(options_2)

    if st.button("Refresh Page"):
        time.sleep(2)
        st.rerun()
st.write("aqui")
st.table(df[df['symbol'].isin(options_2)].reset_index(drop=True))

#tickets = st.text_input("Digite os tickets das ações (separados por vírgula):")
start_date = st.text_input("Digite a data de início (YYYY-MM-DD):")
if st.button("Obter Dados"):
    data = robot.get_tickets_info(options_2, start_date)
    col1, col2 = st.columns(2)
    with col1:
        st.header("Dados das Ações")
        st.dataframe(data)

    with col2:
        st.header("Estatísticas Descritivas")
        st.dataframe(data.describe())
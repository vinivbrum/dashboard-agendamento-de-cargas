import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

#start a streamlit app and create a imput widget
st.write('Cargas agendadas')
upload = "Pedidos Semanal.xlsx"
wb = pd.read_excel(upload, sheet_name='COMPRAS',skiprows=2,header=0)
_today= np.datetime64(datetime.today().strftime('%Y-%m-%d'))

def transform(df):
    df.drop(columns=['shelflife','Estoque'],inplace=True)
    df = df[df['Status'] == 'Pedido']
    df.drop(columns='Status',inplace=True)
    colums_list = df.columns.to_list()
    dias = colums_list[3:14]
    df = df.melt(id_vars=['Responsável','BASE ID','Item'],value_vars=dias,var_name='Pedido',value_name='Valor',ignore_index=True )
    df = df.dropna(subset=['Valor'])
    def separar_dia(dia):
        dia = dia.split(' ')
        dia = dia[0]
        return dia
    df['Dia'] = df['Pedido'].apply(separar_dia)
    def separar_data(data):
        data = data.split(' ')
        data = data[1]
        data = data + '/2024'
        return data
    df['Data'] = df['Pedido'].apply(separar_data)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df = df.sort_values(by=['Data','Responsável','Item'],ascending=True)
    df = df[df['Data'] >= _today]
    return df


df = transform(wb)

# Filtro para Responsável
responsavel_filtro = st.sidebar.multiselect('Filtrar por Responsável', df['Responsável'].unique(),default = df['Responsável'].unique())
data_filtro = st.sidebar.multiselect('Data', df['Data'].unique(),default = _today +1 , format_func=lambda x: x.strftime('%d/%m/%Y'))



# Aplicar filtro de datas
filtered_df = df[df['Responsável'].isin(responsavel_filtro) & df['Data'].isin(data_filtro)]

st.dataframe(
    filtered_df,
    width  = 1000,
    height  = 1000,
    column_config={
        "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YY"),
        "Valor": st.column_config.NumberColumn("Valor", format = '%d', step = 1),
        "Pedido" : None,
        "Item" : st.column_config.Column(width = 'medium')
        
    },
    hide_index=True,
)


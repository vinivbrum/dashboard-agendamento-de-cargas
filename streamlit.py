import streamlit as st
import pandas as pd

#start a streamlit app and create a imput widget
st.write('Cargas agendadas')
upload = st.file_uploader("Escolha um arquivo Excel", type="xlsx")
wb = None
if upload == None:
    pass
else: 
    wb = pd.read_excel(upload, sheet_name='COMPRAS',skiprows=2,header=0)


def transform(df):
    df.drop(columns=['shelflife','Estoque'],inplace=True)
    df = df[df['Status'] == 'Pedido']
    df.drop(columns='Status',inplace=True)
    colums_list = df.columns.to_list()
    dias = colums_list[3:14]
    df = df.melt(id_vars=['Responsável','Item','BASE ID'],value_vars=dias,var_name='Pedido',value_name='Valor',ignore_index=True )
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
    df = df.sort_values(by=['Responsável','Data','Item'],ascending=True)
    return df


    
#create filters for this dataframe in streamlit



# write dataframe to streamlit


#create filters for this dataframe in streamlit

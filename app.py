import streamlit as st
import pandas as pd

# Carregar os dados
@st.cache
def load_data():
    data = pd.read_csv('houses_to_rent_v2.csv')
    return data

data = load_data()

# Título do dashboard
st.title('Aluguéis de Imóveis')

# Filtros
city_filter = st.sidebar.selectbox('Selecione a cidade:', data['city'].unique())
rooms_filter = st.sidebar.slider('Número de quartos', int(data['rooms'].min()), int(data['rooms'].max()), (1, 3))

# Aplicar filtros
filtered_data = data[(data['city'] == city_filter) & (data['rooms'] >= rooms_filter)]

# Exibir tabela filtrada
st.write(f"Imóveis disponíveis em {city_filter} com pelo menos {rooms_filter} quartos:")
st.dataframe(filtered_data)

# Visualizações
st.subheader('Distribuição de Aluguéis')
st.bar_chart(filtered_data['rent amount (R$)'])

st.subheader('Distribuição por Número de Quartos')
st.bar_chart(filtered_data['rooms'].value_counts())

st.subheader('Relação entre Área e Valor Total')
st.scatter_chart(filtered_data[['area', 'total (R$)']].set_index('area'))

# Rodapé
st.write('Fonte dos dados: houses_to_rent_v2.csv')

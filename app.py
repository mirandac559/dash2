import streamlit as st
import pandas as pd

# Função para carregar os dados
@st.cache
def load_data():
    data = pd.read_csv('houses_to_rent_v2.csv')
    
    # Garantir que a coluna 'rooms' seja numérica e tratar valores inválidos
    data['rooms'] = pd.to_numeric(data['rooms'], errors='coerce')  # Converte valores inválidos para NaN
    data = data.dropna(subset=['rooms'])  # Remove linhas onde 'rooms' é NaN
    data['rooms'] = data['rooms'].astype(int)  # Converte 'rooms' para inteiro após remoção dos NaNs
    
    # Verificar se as colunas necessárias têm valores numéricos válidos
    data = data.dropna(subset=['rent amount (R$)', 'total (R$)', 'area'])  # Remover linhas com valores NaN nas colunas relevantes
    return data

data = load_data()

# Título do dashboard
st.title('Dashboard de Aluguéis de Imóveis')

# Filtros
city_filter = st.sidebar.selectbox('Selecione a cidade:', data['city'].unique())
rooms_filter = st.sidebar.slider('Número de quartos', int(data['rooms'].min()), int(data['rooms'].max()), (1, 3))

# Aplicar filtros e garantir que a filtragem seja feita apenas em valores válidos
filtered_data = data[(data['city'] == city_filter) & (data['rooms'] >= rooms_filter)]

# Exibir tabela filtrada
st.write(f"Imóveis disponíveis em {city_filter} com pelo menos {rooms_filter} quartos:")
st.dataframe(filtered_data)

# Verificar se o dataframe filtrado contém dados antes de gerar os gráficos
if not filtered_data.empty:
    # Visualizações
    st.subheader('Distribuição de Aluguéis')
    st.bar_chart(filtered_data['rent amount (R$)'])

    st.subheader('Distribuição por Número de Quartos')
    st.bar_chart(filtered_data['rooms'].value_counts())

    st.subheader('Relação entre Área e Valor Total')
    st.scatter_chart(filtered_data[['area', 'total (R$)']].set_index('area'))
else:
    st.write("Nenhum imóvel encontrado com os critérios selecionados.")

# Rodapé
st.write('Fonte dos dados: houses_to_rent_v2.csv')

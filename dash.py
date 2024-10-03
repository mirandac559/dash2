import streamlit as st
import pandas as pd

# Função para carregar e limpar os dados
@st.cache
def load_data():
    data = pd.read_csv('houses_to_rent_v2.csv')

    # Converter 'rooms' para numérico e remover valores inválidos
    data['rooms'] = pd.to_numeric(data['rooms'], errors='coerce')  # Converte valores inválidos para NaN
    data = data.dropna(subset=['rooms'])  # Remove linhas com NaN em 'rooms'
    data['rooms'] = data['rooms'].astype(int)  # Converter 'rooms' para inteiro

    # Remover linhas com valores NaN em outras colunas importantes
    data = data.dropna(subset=['city', 'rent amount (R$)', 'total (R$)', 'area'])

    return data

# Carregar os dados
data = load_data()

# Título do dashboard
st.title('Aluguéis de Imóveis')

# Filtros
city_filter = st.sidebar.selectbox('Selecione a cidade:', data['city'].unique())

# Obter o valor mínimo e máximo de quartos, garantindo que sejam inteiros válidos
min_rooms = int(data['rooms'].min())
max_rooms = int(data['rooms'].max())

# Alteração no filtro para capturar intervalo de quartos corretamente
rooms_filter = st.sidebar.slider('Número de quartos', min_rooms, max_rooms, (min_rooms, max_rooms))

# Aplicar filtros de forma segura
try:
    # Aplicar filtro de intervalo de quartos corretamente
    filtered_data = data[(data['city'] == city_filter) & (data['rooms'] >= rooms_filter[0]) & (data['rooms'] <= rooms_filter[1])]

    # Exibir a tabela filtrada
    st.write(f"Imóveis disponíveis em {city_filter} com quartos entre {rooms_filter[0]} e {rooms_filter[1]}:")
    st.dataframe(filtered_data)

    # Se houver dados após a filtragem, exibir os gráficos
    if not filtered_data.empty:
        st.subheader('Distribuição de Aluguéis')
        st.bar_chart(filtered_data['rent amount (R$)'])

        st.subheader('Distribuição por Número de Quartos')
        st.bar_chart(filtered_data['rooms'].value_counts())

        st.subheader('Relação entre Área e Valor Total')
        st.scatter_chart(filtered_data[['area', 'total (R$)']].set_index('area'))
    else:
        st.write("Nenhum imóvel encontrado com os critérios selecionados.")
except Exception as e:
    st.error(f"Erro ao aplicar os filtros: {e}")

# Rodapé
st.write('Fonte dos dados: houses_to_rent_v2.csv')

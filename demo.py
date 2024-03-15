import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.title('U B U N T U')

# data = pd.read_csv('demo.csv', dtype={'column_name': str})
# print(data.head())

# @st.cache_data
def load_data():
    # Cargar datos y especificar tipo de datos para la columna problemática
    data = pd.read_csv('demo.csv', dtype={'column_name': str})
    rel_platos = pd.read_csv('rel_platos.csv', dtype={'column_name': str})
    platos = pd.read_csv('platos.csv', dtype={'column_name': str})
    data['createdAt'] = pd.to_datetime(data['createdAt'])
    data = pd.merge(data, rel_platos, on='id_pedido', how='outer')
    data = pd.merge(data, platos, on='id_plato', how='outer')
    # data['nombre_plato'] = data['nombre_plato'].replace({'1/2 Pollo': 'medio_pollo', '2342sdfsdf': 'xx'})
    return data

data_load_state = st.text('Cargando data...')
data = load_data()
data_load_state.text('Cargando data... Hecho!')

st.subheader('Raw data')
st.write(data)

# hist_values = np.histogram(data['createdAt_x'].dt.month, bins=13, range=(1,13))[0]

st.slider('mes', 1, 12, 3)

venta_total = data['pagoxconsumo_pedido'].sum()
cantidad_pedidos = data['codigo_pedido'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric(label='Venta Total', value=venta_total, delta='1.2 %')
col2.metric(label='Cantidad pedidos', value=cantidad_pedidos, delta='-8%')
col3.metric('TBD', '??', '??')

# st.subheader('Histograma')
# st.bar_chart(hist_values)

# bar_values = data.pivot_table(index='nombre_plato', values='pagototal_pedido', aggfunc='sum')
# bar_values_sorted = bar_values['pagototal_pedido'].sort_values(ascending=False)

# st.subheader('x')
# bar_values_df = bar_values_sorted.to_frame()
# st.bar_chart(bar_values_df)

# print(bar_values_sorted)

# bar_values_sorted = bar_values_sorted.reset_index()  # Reiniciar el índice para evitar problemas
# bar_values_sorted.columns = ['nombre_plato', 'pagototal_pedido']  # Cambiar el nombre de las columnas
# bar_values_df = bar_values_sorted.sort_values(by='pagototal_pedido', ascending=False)  # Ordenar el DataFrame

# st.bar_chart(bar_values_df.set_index('nombre_plato'))  # Representar el gráfico de barras


# bar_values_2 = data.groupby(data['nombre_plato'])['pagototal_pedido'].sum().sort_values(ascending=True)
# bar_values_sorted_2 = bar_values_2.sort_values(ascending=False)
# print(bar_values_sorted_2)

# st.line_chart(bar_values_2)

# print(data.info())


# st.write(bar_values_sorted_2)
# st.write(alt.Chart(bar_values_sorted_2).mark_bar().encode(
#     x=alt.X('nombre_plato', sort=None),
#     y='pagototal_pedido',
# ))


# st.title('Ventas totales')

# # Convertir la columna 'nombre_plato' a tipo de datos categoría
# data['nombre_plato'] = data['nombre_plato'].astype('category')

# # Agrupar y sumar los valores
# bar_values_3 = data.groupby('nombre_plato')['pagototal_pedido'].sum().sort_values(ascending=False)

# # Crear el gráfico con Altair
# bar_chart = alt.Chart(bar_values_3.reset_index()).mark_bar().encode(
#     x='nombre_plato',
#     y='pagototal_pedido'
# )

# # Mostrar el gráfico en Streamlit
# st.altair_chart(bar_chart, use_container_width=True)

# bar_chart_2 = alt.Chart(bar_values_3).mark_bar().encode(
#     x='sum(yield):Q',
#     y=alt.Y('site:N').sort('-x')
# )

# st.altair_chart(bar_chart_2, use_container_width=True)


# bar_chart_2 = alt.Chart(bar_values_3).mark_bar().encode(
#     x='sum(yield):Q',
#     y=alt.Y('site:N', sort=alt.EncodingSortField(field='sum(yield)', order='descending'))
# )

# st.altair_chart(bar_chart_2, use_container_width=True)


# Calcular la suma de 'pagototal_pedido' por 'nombre_plato'
sum_plato = data.groupby('nombre_plato')['pagototal_pedido'].sum().reset_index()

# Crear el gráfico de barras con Altair
bar_chart_2 = alt.Chart(sum_plato).mark_bar().encode(
    x=alt.X('sum(pagototal_pedido):Q', title='Suma del monto del pedido'), 
    y=alt.Y('nombre_plato:N', sort='-x'), 
)

# Mostrar el gráfico en Streamlit
st.altair_chart(bar_chart_2, use_container_width=True)

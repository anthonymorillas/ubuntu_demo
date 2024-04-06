import streamlit as st
import pandas as pd
import requests
#from streamlit_dynamic_filters import DynamicFilters
import altair as alt
#import schedule
import time
import subprocess
import threading


# Poner en columnas
# st.page_link('streamlit_app.py', label='Home', icon='🏠')
# st.page_link('pages/streamlit_app_2.py', label='Página 1', icon='1️⃣')

# Poner en columnas
col7, col8, col9 = st.columns(3)

# Crear los enlaces como objetos HTML para que se abran en la misma ventana
home_link = f'<a href="streamlit_app" target="_self" style="text-decoration: none; color: inherit;"><span style="font-size:1.25em">🏠</span> Home</a>'
page1_link = f'<a href="streamlit_app_2" target="_self" style="text-decoration: none; color: inherit;"><span style="font-size:1.25em">1️⃣</span> Página 1</a>'

# Agregar los enlaces a las columnas correspondientes
col7.write(home_link, unsafe_allow_html=True)
col8.write(page1_link, unsafe_allow_html=True)


# st.title('U B U N T U')

# @st.cache_data
@st.cache_data(ttl=1800)

def load_data():
    try:
        response = requests.get('https://teamubuntu.cl:2500/api/pedidos/report/get_pedidos')

        if response.status_code == 200:
            # Convertir los datos JSON en un DataFrame de Pandas
            data = response.json()
            # data['fechareg_categoriapla'] = pd.to_datetime(data['fechareg_categoriapla'])
            return data
        else:
            st.error(f"Error al cargar los datos: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None
    
# def git_push():
#     try:
#         subprocess.run(["git", "push"])
#         #print("Push exitoso.")
#     except Exception as e:
#         print("Error al realizar el push:", e)

def git_push():
    try:
        process = subprocess.Popen(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    except Exception as e:
        print("Error al realizar el push:", e)

# Función para ejecutar git_push() en un hilo separado
def push_thread():
    while True:
        git_push()
        time.sleep(1800)  # Esperar 30 minutos

# Iniciar el hilo para ejecutar git_push()
push_thread = threading.Thread(target=push_thread, daemon=True)
push_thread.start()


# Cargar los datos y mostrar un mensaje de estado
data_load_state = st.text('Cargando datos...')
data = load_data()
if data is not None:
    data_load_state.text('Carga de datos exitosa.')
    df = pd.DataFrame(data['body'])
    df = df.drop(columns=['text_plapedido', 'descripcion_plato', 'commets_pedido'])
    df['amountpeople_pedido'] = df['amountpeople_pedido'].replace(0, 1)
    df['nombre_plato'] = df['nombre_plato'].replace('1/2 Pollo', 'Medio Pollo')
    df['nombre_plato'] = df['nombre_plato'].replace('Sour Sabores (Frutilla/Chirimoya)', 'Sour Sabores (Frutilla-Chirimoya)')
    df['nombre_plato'] = df['nombre_plato'].replace('Queneles de Risotto (Pesto, Oliva y Atomatado)', 'Queneles de Risotto (Pesto Oliva y Atomatado)')
    df['comment_motive'] = df['comment_motive'].replace('cristian :)', 'cristian')
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    df['fechareg_pedido'] = pd.to_datetime(df['fechareg_pedido'])
    df['año'] = df['fechareg_pedido'].dt.year
    df = df[df['año'] == 2024]
    df['mes'] = df['fechareg_pedido'].dt.month
    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
         7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    df['nombre_mes'] = df['mes'].map(meses)
    df['semana'] = df['fechareg_pedido'].dt.isocalendar().week
    df['dia'] = df['fechareg_pedido'].dt.day
    df['venta_neta'] = round(df['precio_plato'] / 1.19)
    df['ticket_promedio'] = round((df['pagoxconsumo_pedido'] / 1.19) / df['amountpeople_pedido'])
    df['ticket_promedio'].fillna(1, inplace=True)
    df['share_venta'] = round(((df['venta_neta'] / df['venta_neta'].sum()) * 100), 4)
    df['precio_plato_neto'] = round(df['precio_plato'] / 1.19)
    

    # Filtrar los datos según la opción seleccionada en el sidebar
    with st.sidebar:
        add_radio = st.radio('Empresa', ('Todos', 'Dejando Huella RCS', 'Doña Anita', 'Verde Mostaza'))
        add_selectbox_year = st.selectbox("Año", ('Todo', '2024'))
        add_selectbox_month = st.selectbox("Mes", ('Todo', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        add_selectbox_week = st.selectbox("Semana", ('Todo', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'))
        add_selectbox_day = st.selectbox("Día", ('Todo', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'))

    # Aplicar los filtros de empresa, año y mes
    if add_radio != 'Todos':
        df = df[df['nom_emp'] == add_radio]
    if add_selectbox_year != 'Todo':
        df = df[df['año'] == int(add_selectbox_year)]
    if add_selectbox_month != 'Todo':
        df = df[df['mes'] == int(add_selectbox_month)]
    if add_selectbox_week != 'Todo':
        df = df[df['semana'] == int(add_selectbox_week)]
    if add_selectbox_day != 'Todo':
        df = df[df['dia'] == int(add_selectbox_day)]

    # Mostrar la tabla si se selecciona
    if st.checkbox('Mostrar tabla'):
        st.write(df)
        
    # if add_radio != 'Todos':
    #     df_filtered = df_filtered[df_filtered['nom_emp'] == add_radio]
    # if add_selectbox_year != 'Todo':
    #     df_filtered = df_filtered[df_filtered['año'] == int(add_selectbox_year)]
    # if add_selectbox_month != 'Todo':
    #     df_filtered = df_filtered[df_filtered['mes'] == int(add_selectbox_month)]
    # if add_selectbox_week != 'Todo':
    #     df_filtered = df_filtered[df_filtered['semana'] == int(add_selectbox_week)]
    # if add_selectbox_day != 'Todo':
    #     df_filtered = df_filtered[df_filtered['dia'] == int(add_selectbox_day)]

    # # Mostrar la tabla si se selecciona
    # if st.checkbox('Mostrar tabla'):
    #     st.write(df_filtered)
    

    # Calcular la venta total y la cantidad de pedidos
    venta_total = df['precio_plato'].sum()
    venta_neta_total = round(df['venta_neta'].sum())
    propina_total = df['pagopropina_pedido'].sum()
    
    cantidad_pedidos = df['codigo_pedido'].nunique()
    max_amountpeople = df['amountpeople_pedido'].max()
    total_cantidad_pedidos = cantidad_pedidos * max_amountpeople

    # ticket_promedio = round(venta_neta_total/total_cantidad_pedidos)
    ticket_promedio = round(df['ticket_promedio'].mean())

    # Mostrar las métricas
    col1, col2, col3 = st.columns(3)
    col1.metric(label='Venta Bruta Total', value='{:,}'.format(venta_total))#, delta='1.2 %')
    col2.metric(label='Venta Neta Total', value='{:,}'.format(venta_neta_total))#, delta='-8%')
    col3.metric(label='Cantidad pedidos', value='{:,}'.format(cantidad_pedidos))#, delta='-8%')
    
    col4, col5, col6 = st.columns(3)
    col4.metric(label='Propina Total', value='{:,}'.format(propina_total))#, delta='-8%')
    col5.metric(label='Ticket Promedio', value='{:,}'.format(ticket_promedio))

    meses_ordenados = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    df['nombre_mes'] = df['mes'].map(meses_ordenados)

    st.markdown('<h1 style="color: #e0004d;">Venta Mensual</h1>', unsafe_allow_html=True)
    # Crear el gráfico de barras con Altair
    bar_chart = alt.Chart(df).mark_bar(color='#33058d').encode(
        x = alt.X('nombre_mes:N', title='Mes', sort=list(meses_ordenados.values())),
        y = alt.Y('sum(venta_neta):Q', title='Venta Neta', axis=alt.Axis(format=',d')),
        tooltip=[alt.Tooltip('sum(venta_neta)', title='Venta Neta', format=',')]
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(bar_chart, use_container_width=True)


    st.header('Categorías - Top 10')

    # Calcular la suma del monto del pedido por nombre de plato
    sum_cat = df.groupby('nombre_categoriapla')['venta_neta'].sum().reset_index()

    # Ordenar por la suma del monto del pedido en orden descendente y luego tomar los primeros 20 registros
    sum_cat_2 = sum_cat.sort_values(by='venta_neta', ascending=False).head(10)

    # Crear el gráfico de barras con Altair
    bar_chart_3 = alt.Chart(sum_cat_2).mark_bar().encode(
        x=alt.X('sum(venta_neta):Q', title='Venta Neta'), 
        y=alt.Y('nombre_categoriapla:N', sort='-x', title='Categorías'), 
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(bar_chart_3, use_container_width=True)


    st.header('Platos - Top 20')

    # Calcular la suma del monto del pedido por nombre de plato
    sum_plato = df.groupby('nombre_plato')['venta_neta'].sum().reset_index()

    # Ordenar por la suma del monto del pedido en orden descendente y luego tomar los primeros 20 registros
    sum_plato_top_20 = sum_plato.sort_values(by='venta_neta', ascending=False).head(20)

    # Crear el gráfico de barras con Altair
    bar_chart_2 = alt.Chart(sum_plato_top_20).mark_bar().encode(
        x=alt.X('sum(venta_neta):Q', title='Venta Neta'), 
        y=alt.Y('nombre_plato:N', sort='-x', title='Platos'), 
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(bar_chart_2, use_container_width=True)

    # xx
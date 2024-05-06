import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Se realiza la lectura de los datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Título del dashboard
st.write("# 13MBID - Visualización de datos")
st.write("## Panel de visualización generado sobre los datos de créditos y tarjetas emitidas a clientes de la entidad")
st.write("#### Persona/s: Paula Domski")
st.write("----")

# Gráficos
st.write("### Caracterización de los créditos otorgados")

# Se tienen que agregar las definiciones de gráficos desde la libreta
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Se realiza la "impresión" del gráfico en el dashboard
st.plotly_chart(creditos_x_objetivo)

# Histograma de los importes de créditos otorgados

histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

st.plotly_chart(histograma_importes)


# Gráfico obtenido desde Dtale

if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

s = df[~pd.isnull(df['limite_credito_tc'])]['limite_credito_tc']
chart = pd.value_counts(s).to_frame(name='data')
chart['percent'] = (chart['data'] / chart['data'].sum()) * 100
chart.index.name = 'labels'
chart = chart.reset_index().sort_values(['data', 'labels'], ascending=[False, True])
chart = chart[:100]
charts = [go.Bar(x=chart['labels'].values, y=chart['data'].values, name='Frequency')]
figure1 = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h'},
    'title': {'text': 'limite_credito_tc Value Counts'},
    'xaxis': {'title': {'text': 'limite_credito_tc'}},
    'yaxis': {'title': {'text': 'Frequency'}}
}))


st.plotly_chart(figure1)



# Filtros

option = st.selectbox(
    'Qué tipo de crédito desea filtrar?',
     df['objetivo_credito'].unique())

df_filtrado = df[df['objetivo_credito'] == option]

st.write(f"Tipo de crédito seleccionado: {option}")

if st.checkbox('Mostrar créditos finalizados?', value=True):

    # Conteo de ocurrencias por estado
    estado_credito_counts = df_filtrado['estado_credito_N'].value_counts()

    # Gráfico de torta de estos valores
    fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
    fig.update_layout(title_text='Distribución de créditos por estado registrado')
else:
    df_filtrado = df_filtrado[df_filtrado['estado_credito_N'] == 'P']
    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    # Create a Pie chart
    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora')

st.write(f"Cantidad de créditos con estas condiciones: {df_filtrado.shape[0]}")
st.plotly_chart(fig)


#pct_inrgeso vs importe_solicitado

if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

s = df[~pd.isnull(df['pct_ingreso'])]['pct_ingreso']
chart = pd.value_counts(s).to_frame(name='data')
chart['percent'] = (chart['data'] / chart['data'].sum()) * 100
ordinal_data = df.groupby('pct_ingreso')[['importe_solicitado']].sum()
chart['ordinal'] = ordinal_data
chart.index.name = 'labels'
chart = chart.reset_index().sort_values('ordinal')
chart = chart[:100]
charts = [go.Bar(x=chart['labels'].values, y=chart['data'].values, name='Frequency')]
charts.append(go.Scatter(
	x=chart['labels'].values, y=chart['ordinal'].values, yaxis='y2',
	name='importe_solicitado (sum)', line={'shape': 'spline', 'smoothing': 0.3}, mode='lines'
))
figure2 = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h'},
    'title': {'text': 'pct_ingreso Value Counts'},
    'xaxis': {'title': {'text': 'pct_ingreso'}},
    'yaxis': {'title': {'text': 'Frequency'}},
    'yaxis2': {'overlaying': 'y', 'side': 'right', 'title': {'text': 'importe_solicitado (sum)'}}
}))

st.plotly_chart(figure2)

# Situación de vivienda


if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

s = df[~pd.isnull(df['situacion_vivienda'])]['situacion_vivienda']
chart = pd.value_counts(s).to_frame(name='data')
chart['percent'] = (chart['data'] / chart['data'].sum()) * 100
chart.index.name = 'labels'
chart = chart.reset_index().sort_values(['data', 'labels'], ascending=[False, True])
chart = chart[:100]
charts = [go.Bar(x=chart['labels'].values, y=chart['data'].values, name='Frequency')]
figure3 = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h'},
    'title': {'text': 'situacion_vivienda Value Counts'},
    'xaxis': {'title': {'text': 'situacion_vivienda'}},
    'yaxis': {'title': {'text': 'Frequency'}}
}))


st.plotly_chart(figure3)


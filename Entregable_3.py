from dash import html, dcc, Dash
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

# Cargar el dataset
dataset = pd.read_excel('datasetcrimeneslimpio.xlsx')

# Convertir la columna 'FECHA HECHO' a formato de fecha
dataset['FECHA HECHO'] = pd.to_datetime(dataset['FECHA HECHO'], errors='coerce')

# Agrupar los datos por fecha para contar la cantidad de crímenes por fecha
time_series_data = dataset.groupby('FECHA HECHO').size().reset_index(name='CANTIDAD')

app = Dash(__name__)
paleta_azul_personalizada = ['#13294B', '#264D89', '#1A6DB2', '#1985C4', '#35A7FF']
# Agrupar datos para el gráfico de barras
aggregated_data = dataset.groupby('ARMA MEDIO')['CANTIDAD'].sum().reset_index()
frecuencia_departamentos = dataset['DEPARTAMENTO'].value_counts()

# Diseño del tablero
app.layout = html.Div(style={'backgroundColor': 'black', 'padding': '20px'}, children=[
    html.H1("DASHBOARD CRÍMENES EN COLOMBIA", style={'textAlign': 'center', 'color': 'white', 'fontSize': '40px', 'fontFamily': 'Courier New TUR'}),
    
    # Primera fila de gráficas
    html.Div([
        # Gráfico de líneas
        html.Div([
            dcc.Graph(
                id='line-graph',
                figure=px.line(time_series_data, x='FECHA HECHO', y='CANTIDAD', title='Serie Temporal de Crímenes')
                .update_layout(
                    width=700, 
                    height=400, 
                    plot_bgcolor='#1A6DB2', 
                    paper_bgcolor='black', 
                    font=dict(color='white')
                )
                .update_traces(line=dict(color='#13294B'))
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}), 
        
        # Gráfico de dispersión
        html.Div([
            dcc.Graph(
                id='scatter-plot',
                figure=px.scatter(dataset, x='GENERO', y='CANTIDAD', title='Gráfico de Dispersión de Crímenes por Género')
                .update_layout(
                    width=700, 
                    height=400, 
                    plot_bgcolor='#1A6DB2', 
                    paper_bgcolor='black', 
                    font=dict(color='white'), 
                    xaxis=dict(showgrid=False), 
                    yaxis=dict(showgrid=False)
                )
                .update_traces(marker=dict(color='#13294B'))
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),  

    # Segunda fila de gráficas
    html.Div([
        # Gráfico de barras
        html.Div([
            dcc.Graph(
                id='bar-chart',
                figure=px.bar(
                    aggregated_data,  
                    x='CANTIDAD',
                    y='ARMA MEDIO',
                    title='Gráfico de Barras Horizontal de Crímenes por Arma/Medio',
                    color_discrete_sequence=['#13294B'],
                    orientation='h'
                ).update_layout(
                    width=700, 
                    height=400, 
                    plot_bgcolor='#1A6DB2', 
                    paper_bgcolor='black', 
                    font=dict(color='white')
                )
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        # Gráfico de pastel
        html.Div([
            dcc.Graph(
                id='pie-chart',
                figure=px.pie(
                    dataset, 
                    names='DEPARTAMENTO', 
                    values='CANTIDAD', 
                    title='Crímenes por Departamento',
                    color_discrete_sequence= paleta_azul_personalizada
                ).update_traces(textposition='inside', textinfo='percent+label')
                .update_layout(paper_bgcolor='black', font=dict(color='white'))
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),  
])
if __name__ == '__main__':
    app.run_server(debug=True)

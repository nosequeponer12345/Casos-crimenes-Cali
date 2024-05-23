from dash import html, dcc, Dash, callback, Input, Output
import matplotlib as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go  



#DATASET 


#dataset= pd.read_excel('G:/Mi unidad/UAO/INGENIERÍA DE DATOS E I.A/SEMESTRE 2/PROGRAMACIÓN/PROYECTO FINAL/casos_crimenes_2023.xlsx') 


dataset= pd.read_excel('G:/Mi unidad/UAO/INGENIERÍA DE DATOS E I.A/SEMESTRE 2/PROGRAMACIÓN/datasetadidas2.xlsx')

print(dataset)  # muestra el dataset y columnas y filas

print(dataset.shape)  # muestra columnas y filas

dataset.head()  #muestra los 5 primeros registros


#datos incompletos: eliminar los datos faltantes

dataset.dropna(inplace=True) # elimina la fila completa con los datos faltantes y el inplace lo reescribe
dataset.info() # verificar la misma cantidad de filas


#columnas irrelevantes: eliminarlas 

del dataset['Retailer ID']
dataset.info()


#cambiar nombre de columnas

dataset=dataset.rename(columns= {'Retailer':'Minorista', 'Invoice Date':'Fecha de facturación', 'Region':'Región', 'State': 'Estado', 'City':'Ciudad', 'Product':'Producto', 'Price per Unit':'Precio por Unidad', 'Units Sold':'Unidades Vendidas', 'Total Sales':'Ventas Totales', 'Operating Profit':'Beneficio operativo', 'Operating Margin':'Margen operativo', 'Sales Method':'Método de venta'})
print(dataset)





#paleta colores

paleta_azul_personalizada = ['#13294B', '#264D89', '#1A6DB2', '#1985C4', '#35A7FF']



# inicializar la app

app = Dash(__name__)


# Layouts 



# Agrupar por producto y sumar las ventas totales
aggregated_data = dataset.groupby('Producto')['Ventas Totales'].sum().reset_index()
frecuencia_estados = dataset['Estado'].value_counts()



# Diseño del tablero
app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.H1("DASHBOARD VENTAS ADIDAS USA 2020-2022", style={'textAlign': 'center', 'color': 'white', 'fontSize': '40px', 'fontFamily': 'Courier New TUR'}),
    
    # Primera fila de gráficas
    html.Div([
        html.Div([
            dcc.Graph(
                id='histogram-graph',
                figure=px.histogram(dataset, x='Fecha de facturación', title='Histograma').update_layout(width=800,height=400,  # Ancho y Altura de la gráfica
                plot_bgcolor='#1A6DB2',paper_bgcolor='black',font=dict(color='white')).update_traces(marker=dict(color='#13294B'))  
                
            )
        ], style={'width': '50%', 'display': 'inline-block'}),  #ubicación de la grafica
        
        html.Div([
            dcc.Graph(
                id='scatter-plot',
                figure=px.scatter(dataset, x='Precio por Unidad', y='Unidades Vendidas', title='Gráfico de Dispersión').update_layout(width=800,height=400,
                plot_bgcolor='#1A6DB2',paper_bgcolor='black',font=dict(color='white'),xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
                .update_traces(marker=dict(color='#13294B')) 
                 
                # Fondo  del área del gráfico   # Fondo  del papel
            )
        ], style={'width': '33%', 'display': 'inline-block'}), # Se utilizarán 6 columnas para esta gráfica
    ]),  # Fin de la primera fila



    # Segunda fila de gráficas
    html.Div([
        html.Div([
            dcc.Graph(
                id='bar-chart',
                figure=px.bar(
                    aggregated_data,  # Usar los datos agrupados y sumados
                    x='Producto',
                    y='Ventas Totales',
                    title='Gráfico de Barras',
                    color_discrete_sequence=['#13294B']  # Color de las barras
                ).update_layout(width=650,height=400,plot_bgcolor='#1A6DB2',paper_bgcolor='black',font=dict(color='white'))
            )
        ], style={'width': '36%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='3dplot', figure=px.scatter_3d(dataset,x='Margen operativo',y='Beneficio operativo',z='Ventas Totales').update_layout(width=650,height=450,
                    paper_bgcolor='black',font=dict(color='white')).update_traces(marker=dict(color='#13294B'))
                    .update_layout(scene=dict(xaxis=dict(gridcolor='#1A6DB2'), yaxis=dict(gridcolor='#1A6DB2'), zaxis=dict(gridcolor='#1A6DB2')))
            )
        ], style={'width': '31%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(
                id='pie-chart',
                figure=px.pie(
                    dataset, 
                    names='Región', 
                    values='Ventas Totales', 
                    title='Ventas Totales por Región',color_discrete_sequence= paleta_azul_personalizada
                ).update_traces(textposition='inside', textinfo='percent+label').update_layout(paper_bgcolor='black',font=dict(color='white'))
                # Muestra porcentajes y etiquetas dentro del gráfico
            )
        ], style={'width': '33%', 'display': 'inline-block'})
    ]),  # Fin de la segunda fila
    
    # Tercera fila de gráficas
    html.Div([
        dcc.Graph(
            id='map-chart',
            figure=go.Figure(data=go.Choropleth(
                locations= ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],  # Ubicaciones geográficas
                z= frecuencia_estados,  # Valores a representar
                locationmode='USA-states',  # Modo de ubicación (por estados de EE.UU.)
                colorscale='Blues',  # Escala de colores
                marker_line_color='white',# Color de las líneas del contorno del mapa
                
            )).update_layout(
                title='Mapa de Estados Unidos',
                geo=dict(bgcolor='black', showframe=False, showcoastlines=False),  # Configuración del mapa
                paper_bgcolor='black',
                font=dict(color='white')
            ).update_layout(width=1000, height=900)
    )
    
    ], style={'width': '100%', 'margin': '0 auto'})  # Fin de la tercera fila

])





# Ejecución de la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)



import pandas as pd
from dash  import html, dcc, dash_table
import plotly.express as px


from procesos.comerciales import *



def listar_comerciales(lista):
    data = [{'Columna':elemento} for elemento in lista]
    tabla = dash_table.DataTable(
        id='tabla',
        columns=[{'name': 'Columna', 'id': 'Columna'}],
        data=data,
        style_table={'width': '100%'},
        style_data={'whiteSpace': 'normal'},
    )
    return tabla


#def graficas_comerciales(comerciales_lt, comercial_df, importes_df ) -> html.Div:
def graficas_comerciales(ventas) -> html.Div:
    comerciales_df = pd.DataFrame(comerciales_estado(ventas))
    importes_df = pd.DataFrame(comerciales_ventas(ventas))
    tiposervicio_df = pd.DataFrame(tipo_servicio_contrato_general(ventas))


    # Empezamos con los gráficos
    # Comerciales
    fig_comerciales = px.bar(comerciales_df, x='Comercial'
                             , y=['Cerrada y ganada','Cerrada y no presentada','Cerrada y perdida']
                             , barmode='stack'
                             , title="Servicios Presentados: Número de servicios por estado"
                             , height=600)
    fig_comerciales.update_layout(xaxis_tickangle=45)
    
    # ventas
    fig_ventas = px.bar(importes_df, x='Comercial'
                        , y=['Importeprevisto']
                        , title="Servicios Ganados: Importe de ventas por comercial"
                        , height=600)
    fig_ventas.update_layout(xaxis_tickangle=45)
    
    # tipo de servicio
    fig_tipodeservicio = px.bar(tiposervicio_df
                                , x= 'Comercial'
                                , y =['Bolsa de Horas','Formación','Gestionado','Precio Cerrado','Selección Directa','Time and Material','Venta Software']
                                , barmode='stack'
                                , title='Servicios Ganados: Número de tipos de servicios por comercial'
                                , height=600)
    fig_tipodeservicio.update_layout(xaxis_tickangle=45)
    div = html.Div([
        html.Div([
            html.Div([dcc.Graph(id='display-selected-values', figure=fig_comerciales),],),
            html.Div([dcc.Graph(id='display-selected-values2', figure=fig_ventas),]),
            html.Div([dcc.Graph(id='display-selected-values3', figure=fig_tipodeservicio),]),
        ])
    ])
    return div

def graficas_comercial(ventas,  nombre) -> html.Div:
    
    comercial_df = comercial_ventas(ventas, nombre)
    fig_comercial = px.treemap(comercial_df, path=['Cliente'], values='Importeprevisto')
    fig_comercial.update_layout(height=900)

    fechas_df = comercial_fechas(ventas, nombre)
    #fig_scatter = px.scatter(fechas_df, x='Anualidad', y='Importeprevisto', color='Cliente')
    fig_scatter = px.bar(fechas_df, x='Anualidad', y='Importeprevisto', color='Cliente')
    fig_scatter.update_layout(height=900)


    datos = tipo_servicio_contrato(ventas, nombre)
    fig_bar = px.bar(datos, x="Anualidad", y="Importeprevisto", color="Tiposdeservicio", title="Ventas por tipos de servicio", text="Tiposdeservicio")
    fig_bar.update_layout(height = 900)


    #fig_pie = px.pie(tipo_servicio, values='Tipodeservicio')

    div = html.Div([
            html.H1(nombre),
            html.Div([dcc.Graph(id='display-selected-values', figure=fig_comercial),],),
            html.Div(
                children=[
                    html.Div([dcc.Graph(id='display-selected-values2', figure=fig_scatter),],className='col-sm-6'),
                    html.Div([dcc.Graph(id='display-selected-values3', figure=fig_bar),],className='col-sm-6'),
                ],
                className='row'
            ),
    ])
    return div


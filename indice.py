import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from urllib.parse import parse_qs

from procesos.comerciales import *
from procesos.ficheros import leer_comerciales
from procesos.comerciales_representacion import *
from procesos.tablas import *

ventas = None
comerciales_df = None
importes_df = None
comercial_df = None
comerciales_lt = None

ventas = leer_comerciales("c:\datos\[OPORT021]_Oportunidades_con_multiples_filtros_RAW.xls", ventas)
print('Primera lectura')
ventas = preprocesar(ventas)
comerciales_lt = lista_comerciales(ventas)


app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.css.append_css({
    'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
})

layout_inicio = html.Div([
    html.H1('Estadísticas generales'),
    graficas_comerciales(ventas),
    generar_tabla(comerciales_lt),
])

layout_comerciales = html.Div([
    html.Div(id='comercial-content'),
    html.Div(
        children=[
            html.A('Volver al Inicio', href='/', className='btn btn-primary'),
        ],
    ),
        
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(
    Output('page-content', 'children'), 
    [Input('url', 'pathname')], 
    )


def display_page(pathname):
    if pathname == '/':
        return layout_inicio
    elif pathname == '/comerciales':
        return layout_comerciales
    else:
        return 'Página no encontrada'


@app.callback(Output('comercial-content', 'children'), [Input('url', 'search')])
def display_comercial(search):
    params = parse_qs(search[1:])
    nombre_comercial = params.get('nombre', [''])[0]
    return graficas_comercial(ventas, nombre_comercial)



if __name__ == '__main__':
    app.run_server(debug=True)

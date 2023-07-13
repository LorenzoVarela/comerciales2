from dash  import html, dcc, dash_table
from urllib.parse import quote

# Tabla

def codificar_nombre(nombre):
    return quote(nombre)

# Crear los enlaces a los comerciales
def crear_enlace(nombre_comercial):
    nombre_codificado = codificar_nombre(nombre_comercial)
    enlace = f"/comerciales?nombre={nombre_codificado}"
    return html.A(nombre_comercial, href=enlace)

# Crear la tabla con los enlaces a los comerciales
def generar_tabla(comerciales):
    comerciales_lt = sorted(comerciales) 
    filas = []
    for i in range(0, len(comerciales_lt), 3):
        fila = [
            html.Td(crear_enlace(comerciales_lt[i])),
            html.Td(crear_enlace(comerciales_lt[i + 1])) if i + 1 < len(comerciales_lt) else html.Td(),
            html.Td(crear_enlace(comerciales_lt[i + 2])) if i + 2 < len(comerciales_lt) else html.Td()
        ]
        filas.append(html.Tr(fila))

    tabla = html.Table([
        html.Thead([
            html.Tr([
                html.Th("Comercial"),
                html.Th("Comercial"),
                html.Th("Comercial")
            ])
        ]),
        html.Tbody(filas)
    ])

    return tabla

#Tabla


import pandas as pd
# from dash  import html, dash_table


def preprocesar(ventas):
    ventas['Importeprevisto'] = ventas['Importeprevisto'].replace('', '0')
    ventas['Importeprevisto'] = ventas['Importeprevisto'].replace(' ', '0')
    ventas['Importeprevisto']=ventas['Importeprevisto'].astype(float)
    ventas['Fechacreación'] = pd.to_datetime(ventas['Fechacreación'])
    ventas['Fecha'] = ventas['Fechacreación'].dt.strftime('%Y%m')
    ventas['Anualidad'] = ventas['Fechacreación'].dt.strftime('%Y').astype('int')

    print('procesamos DF')
    return ventas


def comerciales_estado(ventas):
    # Para todos los comerciales sacamos las estadísitcas de las ofertas que están en Cerrada y ganada, Cerrada y Perdia y
    # Cerrada y no presentada
    ventas_cerradas = ventas[ventas['Estado'].isin(["Cerrada y ganada","Cerrada y perdida","Cerrada y no presentada"])]
    
    # Agrupar por "Comercial" y "Estado" y realizar las agregaciones
    nuevo_df_t = ventas_cerradas.groupby(['Comercial', 'Estado']).agg(Cantidad=('Estado', 'count')).reset_index()
    nuevo_df = nuevo_df_t.pivot_table(index='Comercial', columns='Estado',values='Cantidad')
    nuevo_df.reset_index(inplace=True)
    nuevo_df.columns.name = None
    nuevo_df = nuevo_df.fillna(0)
    return nuevo_df

def comerciales_ventas(ventas):
    # Para todos los comerciales sumamos las cantidades Importeprevisto de las ofertas ganadas
    # sacamos las ventas
    nuevo_df = pd.DataFrame(ventas[ventas['Estado'] == 'Cerrada y ganada'].groupby('Comercial')['Importeprevisto'].sum())
    nuevo_df.reset_index(inplace=True)
    return nuevo_df


def comercial_ventas(ventas, nombre):
    # PAra un comercial, las ventas por cliente
    nuevo_df = pd.DataFrame(ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')].groupby('Cliente')['Importeprevisto'].sum())
    nuevo_df.reset_index(inplace=True)
    return nuevo_df

def lista_comerciales(ventas):
    # Sacamos la lista de todos los comerciales
    # Extraemos la lista de los comerciales
    df_sp = ventas['Comercial']
    df_sp = df_sp.drop_duplicates()
    df_sp.head()
    comerciales=df_sp.tolist()
    return comerciales

#def presentar_comerciales():
#    return True

def comercial_fechas(ventas, nombre):
    # Agrupamos los datos de un comercial por fecha
    nuevo_df = pd.DataFrame(ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')])
    nuevo_df.reset_index(inplace=True)
    nuevo_df.columns.name = None
    nuevo_df = nuevo_df.fillna(0)    
    nuevo_df = nuevo_df.sort_values('Anualidad')
    return nuevo_df


def tipo_servicio_contrato(ventas, nombre):
    # agrupamos, para un comercial los tipos de servicio
    ventas_cerradas = ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')]
    nuevo_df = ventas_cerradas.groupby(['Tiposdeservicio', 'Anualidad']).agg(Cantidad=('Tiposdeservicio', 'count')).reset_index()
    
    nuevo_df = nuevo_df.sort_values('Anualidad')
    return nuevo_df



def tipo_servicio_contrato_general(ventas):
    # agrupamos, para un comercial los tipos de servicio
    ventas_cerradas = ventas[(ventas['Estado'] == 'Cerrada y ganada')]
    nuevo_df = ventas_cerradas.groupby(['Comercial','Tiposdeservicio']).agg(Cantidad=('Tiposdeservicio', 'count')).reset_index()
    nuevo_df = nuevo_df.pivot_table(index='Comercial', columns='Tiposdeservicio',values='Cantidad')
    nuevo_df.reset_index(inplace=True)
    nuevo_df.columns.name = None
    nuevo_df = nuevo_df.fillna(0)
    return nuevo_df


def tipo_servicio_contrato(ventas, nombre):
    # agrupamos, para un comercial los tipos de servicio
    # ventas_cerradas = pd.DataFrame(ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')])
    ventas_cerradas = ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')]
    nuevo_df = ventas_cerradas.groupby(['Tiposdeservicio', 'Anualidad'])['Importeprevisto'].sum().reset_index()
    

    #nuevo_df.reset_index(inplace=True)
    #nuevo_df.columns.name = None
    #nuevo_df = nuevo_df.fillna(0)    
    
    nuevo_df = nuevo_df.sort_values('Anualidad')
    return nuevo_df


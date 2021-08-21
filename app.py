import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


from dash.dependencies import Input, Output
from s3_utils import s3Utils


app = dash.Dash(__name__)
server = app.server

# Read s3Utils
cnel_bucket = s3Utils()
df_cnel= cnel_bucket.read_df_cnel_latlong()

df_cnel['cluster_2d'] = df_cnel['cluster_2d'].astype("string")
df_cnel['cluster'] = df_cnel['cluster'].astype("string")


cluster_2dim_data = []
for cluster2 in sorted(df_cnel['cluster_2d'].unique()):
  count = df_cnel.loc[(df_cnel["cluster_2d"] == cluster2)].shape[0]
  data = (cluster2, count)
  cluster_2dim_data.append(data)

cluster_24dim_data = []
for cluster24 in sorted(df_cnel['cluster'].unique()):
  count = df_cnel.loc[(df_cnel["cluster"] == cluster24)].shape[0]
  data = (cluster24, count)
  cluster_24dim_data.append(data)

# Plot the different figures
def plot_fig():
    fig = px.scatter_mapbox((df_cnel.loc[(df_cnel['top_25'] == 1) | (df_cnel['top_25'] == -1)]), 
                            lat="lat", lon="long", hover_name="cuenta_contrato", 
                            color="cluster", zoom=10, height=560, hover_data = ["promedio","std","centroide", "distancia"] )
    #fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def plot_fig2d():
    fig_2d = px.scatter_mapbox((df_cnel.loc[(df_cnel['top_25_2d'] == 1) | (df_cnel['top_25_2d'] == -1)]), 
                            lat="lat", lon="long", hover_name="cuenta_contrato",
                            color="cluster_2d", zoom=10, height=560, hover_data = ["promedio","std", "distancia_2d","centroide_2d"] )
    fig_2d.update_layout(mapbox_style="carto-positron")
    fig_2d.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    #fig_2d.update_layout(mapbox_style="open-street-map")
    fig_2d.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #fig.show()
    return fig_2d

def plot_individual(cuentacontrato,promedio):
    df_test = df_cnel.loc[df_cnel['cuenta_contrato'] == cuentacontrato]
    index_name = df_test.index[0]
    df_test = df_test.iloc[:,5:29]
    df_test = df_test.transpose()
    df_test.reset_index(level=0, inplace=True)
    df_test.rename(columns = {index_name: 'Consumo','index':'Mes'}, inplace = True)
    df_test['promedio'] = promedio
    fig = px.line(df_test, x='Mes', y='Consumo', title='Consumo Eléctrico de: ' + str(cuentacontrato) )
    fig.update_yaxes(title="Consumo [kwh]")
    fig.update_traces(mode='markers+lines')
    fig.add_scatter(x=df_test['Mes'], y=df_test['promedio'], mode='lines', name="Promedio [kwh]")
    return fig


app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'CNEL Consumo Eléctrico',
                        ),
                        html.H4(
                            'Evaluación de Clustering',
                        )
                    ],

                    className='eight columns'
                ),
                html.Img(
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    className='two columns',
                ),
                html.A(
                    html.Button(
                        "Learn More",
                        id="learnMore"

                    ),
                    href="https://plot.ly/dash/pricing/",
                    className="two columns"
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Métodos de Clustering:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='well_status_selector',
                            options=[
                                {'label': 'Kmeans', 'value': 'kmeans'},
                                {'label': 'DBSCAN', 'value': 'dbscan'},
                                {'label': 'Kmediods', 'value': 'kmediods'}
                            ],
                            value='active',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                        html.P(
                            'Estratificaciones Disponibles:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id = 'kmeans_dim_selector',
                            options=[
                                {'label': 'Usando 24 Meses', 'value': '24'},
                                {'label': 'Usando Promedio y Desviación Estándar', 'value': '2'},
                                {'label': 'Usando Estratificación Actual', 'value': '3'}
                            ],
                            value='24',
                            labelStyle={'display': 'block'},
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [   
                        html.Div(
                            [
                                html.P(
                                    'Registros de CNEL - Consumo 2019 a 2020',
                                ),
                            ],
                            className="info_text"
                        ),
                        # Row para CNEL original
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("No. de Registros"),
                                        html.H6(
                                            "458860",
                                            id="total_reg",
                                            className="info_text"
                                        )
                                    ],
                                    id="wells",
                                    className="pretty_container"
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P("No. Reg. < 10 KWH"),
                                                html.H6(
                                                    "27345",
                                                    id="less10Text",
                                                    className="info_text"
                                                )
                                            ],
                                            id="less10",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("No. Reg. > 1000 KWH"),
                                                html.H6(
                                                    "23353",
                                                    id="grather10Text",
                                                    className="info_text"
                                                )
                                            ],
                                            id="grather10",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("Registros Usados"),
                                                html.H6(
                                                    "408162",
                                                    id="regUseText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="reguse",
                                            className="pretty_container"
                                        ),
                                    ],
                                    id="tripleContainer",
                                )

                            ],
                            id="infoContainer",
                            className="row"
                        ),
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(
                            type="circle",
                            children=dcc.Graph(
                                id='main_graph',
                                figure=plot_fig()
                            )
                        )
                    ],
                    className='pretty_container eight columns',
                ),
                html.Div(
                    [
                        dcc.Loading(
                            type="circle",
                            children=dcc.Graph(
                                id='individual_graph'
                            )
                        )
                    ],
                    className='pretty_container four columns',
                ),

            ],
            className='row'
        )
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)

# Callback to use map
@app.callback(
    Output("main_graph", "figure"),
    [Input("kmeans_dim_selector", "value")])
def update_figure(kmeans_dim_selector):
  if kmeans_dim_selector == '2':
    list_cluster = cluster_2dim_data
    return plot_fig2d()
  elif kmeans_dim_selector == '24':
    list_cluster = cluster_24dim_data
    return plot_fig()

# Callback to use line plot
@app.callback(
    Output("individual_graph", "figure"),
    [Input("main_graph", "hoverData")])
def update_line_plot(hoverData):
  chosen = [point['hovertext'] for point in hoverData['points']]
  promedio = hoverData['points'][0]['customdata'][0]
  cuentacontrato = chosen[0]
  return plot_individual(cuentacontrato,promedio)


# Main
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, dev_tools_ui=True)
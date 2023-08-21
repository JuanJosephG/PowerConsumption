import dash
import dash_auth
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px


from dash.dependencies import Input, Output
from utils.s3_connection import S3Connection
from utils.figures import Figures
from utils.constants import DESCRIPTION_kmeans_24dim, DESCRIPTION_kmeans_2dim, DESCRIPTION_dbscan_2dim, DESCRIPTION_estratificacion

# Read s3Utils
cnel_bucket = S3Connection()
df_cnel= cnel_bucket.read_df_cnel_latlong()

#df_cnel_gye.drop('Unnamed: 0', axis=1, inplace=True)
credentials = cnel_bucket.read_credentials()
crd = credentials.split(',')


VALID_USERNAME_PASSWORD_PAIRS = {
    crd[0]: crd[1]
}

app = dash.Dash(__name__,title="Unidad Eléctrica", meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server



figures = Figures(df_cnel)

description_clustering = DESCRIPTION_kmeans_24dim

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

cluster_2dim_dbscan_data = []
for cluster_2d_dbscan in sorted(df_cnel['cluster_dbscan_2d'].unique(),key=int):
  if(cluster_2d_dbscan != '-1'):
    count = df_cnel.loc[(df_cnel["cluster_dbscan_2d"] == cluster_2d_dbscan)].shape[0]
    data = (cluster_2d_dbscan, count)
    cluster_2dim_dbscan_data.append(data)

estratos_data = []
for estrato in sorted(df_cnel['estrato'].unique()):
  if (estrato != '5' and estrato != "X"):
    count = df_cnel.loc[(df_cnel["estrato"] == estrato)].shape[0]
    data = (estrato, count)
    estratos_data.append(data)

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Unidad Eléctrica Consumo Energía',
                        ),
                        html.H4(
                            'Evaluación de Clustering',
                        )
                    ],

                    className='eight columns'
                ),
                html.Img(
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    #src="https://drive.google.com/uc?export=view&id=1eWQPRdZT2lALPve976TDB3PqiIYT4p22",
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
                            'Métodos de Clustering y Estratificación:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='clustering_selector',
                            options=[
                                {'label': 'Kmeans', 'value': 'kmeans'},
                                {'label': 'DBSCAN', 'value': 'dbscan'},
                                {'label': 'Estratificación Actual', 'value': 'actual'},
                            ],
                            value='kmeans',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                        html.P(
                            'Estratificaciones Disponibles:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id = 'dim_selector',
                            labelStyle={'display': 'block'},
                            className="dcc_control"
                        ),
                        html.P(
                            'Descripción Método de Clustering y Estratificación (?)',
                            id="description_clustering",
                            title=description_clustering,
                            style={"textDecoration": "underline", "color":"#0060ae"}
                        )
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [   
                        html.Div(
                            [
                                html.P(
                                    'Registros de Unidad Eléctrica - Consumo 2019 a 2020',
                                ),
                            ],
                            className="info_text"
                        ),
                        # Row para Unidad Eléctrica original
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("No. Registros Originales"),
                                        html.H6(
                                            "697747",
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
                                                    "227045",
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
                                                    "35041",
                                                    id="grather10Text",
                                                    className="info_text"
                                                )
                                            ],
                                            id="grather10",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("No. Reg. Coord."),
                                                html.H6(
                                                    "643285",
                                                    id="regCoordText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="regcoord",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("No. Reg. Usados"),
                                                html.H6(
                                                    "112510",
                                                    id="regUsedText",
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
                            id="infoContainer container-display",
                            className="row"
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Loading(
                                            children=dcc.Graph(
                                                id='cluster_graph',
                                                figure=figures.cluster_kmeans24dim()
                                            )
                                        )
                                    ],
                                    className='pretty_container',
                                )
                            ],
                            className='row'
                        )
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
                            children=dcc.Graph(
                                id='main_graph',
                                figure=figures.plot_fig()
                            )
                        )
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Loading(
                            children=dcc.Graph(
                                id='individual_graph',
                                figure = figures.plot_graph_empty()
                            )
                        )
                    ],
                    className='pretty_container six columns',
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
    Output("dim_selector", "options"),
    Output("dim_selector", "value"),
    [Input("clustering_selector", "value")]
)
def update_dimselector(clustering_selector):
    if clustering_selector == 'kmeans':
        options=[
                    {'label': 'Usando 24 Meses', 'value': '24'},
                    {'label': 'Usando Promedio y Desviación Estándar', 'value': '2'},
                ]
        return options, '24'

    if clustering_selector == 'dbscan':
        options=[
                {'label': 'Usando Promedio y Desviación Estándar', 'value': '3'},
            ]
        return options, '3'

    if clustering_selector == 'actual':
        options=[
                {'label': 'Usando Promedio 24 Meses', 'value': '4'},
            ]
        return options, '4'

@app.callback(
    Output("main_graph", "figure"),
    Output("description_clustering", "title"),
    Output("cluster_graph", "figure"),
    [Input("clustering_selector", "value")],
    [Input("dim_selector", "value")])
def update_figure(clustering_selector, dim_selector):
    if clustering_selector == 'kmeans':
        if dim_selector == '2':
            list_cluster = cluster_2dim_data
            return figures.plot_fig2d(), DESCRIPTION_kmeans_2dim, figures.cluster_kmeans2dim()
        elif dim_selector == '24':
            list_cluster = cluster_24dim_data
            return figures.plot_fig(), DESCRIPTION_kmeans_24dim, figures.cluster_kmeans24dim()

    if clustering_selector == 'dbscan':
        list_cluster = cluster_2dim_dbscan_data
        return figures.plot_fig2d_dbscan(), DESCRIPTION_dbscan_2dim, figures.cluster_dbscan2dim()

    if clustering_selector == 'actual':
        list_cluster = estratos_data
        return figures.plot_estratos(), DESCRIPTION_estratificacion, figures.cluster_estratos()

# Callback to use line plot
@app.callback(
    Output("individual_graph", "figure"),
    [Input("main_graph", "hoverData")])
def update_line_plot(hoverData):
    chosen = [point['hovertext'] for point in hoverData['points']]
    promedio = hoverData['points'][0]['customdata'][0]
    cuentacontrato = chosen[0]
    return figures.plot_individual(cuentacontrato, promedio)



# Main
if __name__ == '__main__':
    #app.run_server(debug=True, threaded=True, dev_tools_ui=True) #dev-debug
    app.run_server(debug=False, threaded=True, dev_tools_ui=True) #dev-debug-false
    #app.run_server(debug=False, threaded=True, dev_tools_ui=True, port=80, host='0.0.0.0') #prod

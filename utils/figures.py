import plotly.express as px

from utils.constans import MES, MES_TICKS

# Plot the different figures
class Figures(object):
    def __init__(self, df_cnel):
        super().__init__()
        self.df_cnel = df_cnel
    
    def plot_fig(self):
        """Plot map using top_25 of df_cnel

        returns:
            - on success this method returns the GYE map using the top 25 of
            Power Consumption
        """
        fig = px.scatter_mapbox((self.df_cnel.loc[(self.df_cnel['top_25'] == 1) | (self.df_cnel['top_25'] == -1)]), 
                                lat="lat", lon="long", hover_name="cuenta_contrato", 
                                color="cluster", zoom=10, hover_data = ["promedio","std","centroide", "distancia"] )
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

    def plot_fig2d(self):
        """Plot map using top_25 with VAR and MEDIAN

        returns:
            - on success this method returns the GYE map using the top 25
            in two dimensions, it means VAR and MEDIAN
        """
        fig_2d = px.scatter_mapbox((self.df_cnel.loc[(self.df_cnel['top_25_2d'] == 1) | (self.df_cnel['top_25_2d'] == -1)]), 
                                lat="lat", lon="long", hover_name="cuenta_contrato",
                                color="cluster_2d", zoom=10, hover_data = ["promedio","std", "distancia_2d","centroide_2d"] )
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

    def plot_individual(self, cuentacontrato, promedio):
        """Plot individual graph of each user

        returns:
            - on success this method returns a linear plot of each user,
            that represent the historic of power consumption of the user
        """
        df_test = self.df_cnel.loc[self.df_cnel['cuenta_contrato'] == int(cuentacontrato)]
        index_name = df_test.index[0]
        df_test = df_test.iloc[:,5:29]
        df_test = df_test.transpose()
        df_test.reset_index(level=0, inplace=True)
        df_test.rename(columns = {index_name: 'Consumo','index':'Mes'}, inplace = True)
        df_test['promedio'] = promedio
        fig = px.line(df_test, x=MES, y='Consumo', title='Consumo Eléctrico de: ' + str(cuentacontrato) )
        fig.update_yaxes(title="Consumo [kwh]")
        fig.update_xaxes(title="Año-Mes")
        fig.update_traces(mode='markers+lines')
        fig.add_scatter(x=MES, y=df_test['promedio'], mode='lines', name="Promedio [kwh]")
        fig.update_xaxes(tickangle=45)
        fig.update_xaxes(tickformat='%Y-%m')
        fig.update_xaxes(tickvals = MES_TICKS)
        return fig
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

    def plot_estratos(self):
        fig_estratos = px.scatter_mapbox((self.df_cnel.loc[(self.df_cnel['top_25_estrato'] == 1) | (self.df_cnel['top_25_estrato'] == -1)]), 
                                lat="lat", lon="long", hover_name="cuenta_contrato",
                                color="estrato", zoom=10, height=450, hover_data = ["promedio","std"] )
        fig_estratos.update_layout(mapbox_style="carto-positron")
        fig_estratos.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))
        #fig_2d.update_layout(mapbox_style="open-street-map")
        fig_estratos.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        #fig.show()
        return fig_estratos
    
    def plot_fig2d_dbscan(self):
        fig_2d_dbscan = px.scatter_mapbox((self.df_cnel.loc[(self.df_cnel['cluster_dbscan_2d'] != '-1')]), 
                                lat="lat", lon="long", hover_name="cuenta_contrato",
                                color="cluster_dbscan_2d", zoom=10, height=450, hover_data = ["promedio","std"] )
        fig_2d_dbscan.update_layout(mapbox_style="carto-positron")
        fig_2d_dbscan.update_layout(
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig_2d_dbscan.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig_2d_dbscan

    def cluster_kmeans24dim(self):
        cluster_24dim_data = []
        for cluster in sorted(self.df_cnel['cluster'].unique()):
            count = self.df_cnel.loc[(self.df_cnel["cluster"] == cluster)].shape[0]
            data = (cluster, count)
            cluster_24dim_data.append(data)

        kmeans24dim_labels = [data[0] for data in cluster_24dim_data]
        kmeans24dim_count = [data[1] for data in cluster_24dim_data]

        promedio_kmeans24dim = []
        for cluster in kmeans24dim_labels:
            promedio = round((self.df_cnel[(self.df_cnel['cluster'] == cluster)]['promedio']).mean(),4)
            promedio_kmeans24dim.append(promedio)

        min_kmeans24dim = []
        for cluster in kmeans24dim_labels:
            min = round((self.df_cnel[(self.df_cnel['cluster'] == cluster)]['promedio']).min(),4)
            min_kmeans24dim.append(min)

        max_kmeans24dim = []
        for cluster in kmeans24dim_labels:
            max = round((self.df_cnel[(self.df_cnel['cluster'] == cluster)]['promedio']).max(),4)
            max_kmeans24dim.append(max)

        fig_clusters_estratos = px.bar( x = kmeans24dim_labels, y = kmeans24dim_count, text=kmeans24dim_count,
                                        title='K-means 24 Dim Cluster Data', 
                                        hover_data=[promedio_kmeans24dim, min_kmeans24dim, max_kmeans24dim],
                                        width=760, height=270)
        fig_clusters_estratos.update_yaxes(title="Usuarios")
        fig_clusters_estratos.update_xaxes(title="Clusters")
        fig_clusters_estratos.update_xaxes(tickvals = kmeans24dim_labels)
        fig_clusters_estratos.update_traces(hovertemplate='<b>Cluster: </b>: %{x}<br>' + 
                                        '<br><b>No. Usuarios: </b>: %{y}<br>' + 
                                        '<br><b>Promedio [kwh]: </b>: %{customdata[0]}<br>'+ 
                                        '<br><b>Mínimo [kwh]: </b>: %{customdata[1]}<br>'+
                                        '<br><b>Máximo [kwh]: </b>: %{customdata[2]}<br>'
                                        )

        return fig_clusters_estratos

    def cluster_kmeans2dim(self):
        cluster_2dim_data = []
        for cluster2 in sorted(self.df_cnel['cluster_2d'].unique()):
            count = self.df_cnel.loc[(self.df_cnel["cluster_2d"] == cluster2)].shape[0]
            data = (cluster2, count)
            cluster_2dim_data.append(data)

        kmeans2dim_labels = [data[0] for data in cluster_2dim_data]
        kmeans2dim_count = [data[1] for data in cluster_2dim_data]

        promedio_kmeans2dim = []
        for cluster in kmeans2dim_labels:
            promedio = round((self.df_cnel[(self.df_cnel['cluster'] == cluster)]['promedio']).mean(),4)
            promedio_kmeans2dim.append(promedio)

        min_kmeans2dim = []
        for cluster in kmeans2dim_labels:
            min = round((self.df_cnel[(self.df_cnel['cluster'] == cluster)]['promedio']).min(),4)
            min_kmeans2dim.append(min)
        
        max_kmeans2dim = []
        for cluster in kmeans2dim_labels:
            max = round((self.df_cnel[(self.df_cnel['cluster'] == cluster)]['promedio']).max(),4)
            max_kmeans2dim.append(max)

        fig_clusters_estratos = px.bar( x = kmeans2dim_labels, y = kmeans2dim_count, text= kmeans2dim_count,
                                        title='K-means 2 Dim Cluster Data', 
                                        hover_data=[promedio_kmeans2dim, min_kmeans2dim, max_kmeans2dim])
        fig_clusters_estratos.update_yaxes(title="Usuarios")
        fig_clusters_estratos.update_xaxes(title="Clusters")
        fig_clusters_estratos.update_xaxes(tickvals = kmeans2dim_labels)
        fig_clusters_estratos.update_traces(hovertemplate='<b>Cluster: </b>: %{x}<br>' + 
                                        '<br><b>No. Usuarios: </b>: %{y}<br>' + 
                                        '<br><b>Promedio [kwh]: </b>: %{customdata[0]}<br>'+ 
                                        '<br><b>Mínimo [kwh]: </b>: %{customdata[1]}<br>'+
                                        '<br><b>Máximo [kwh]: </b>: %{customdata[2]}<br>'
                                        )
        return fig_clusters_estratos

    def cluster_dbscan2dim(self):
        cluster_2dim_dbscan_data = []
        for cluster_2d_dbscan in sorted(self.df_cnel['cluster_dbscan_2d'].unique(),key=int):
            if(cluster_2d_dbscan != '-1'):
                count = self.df_cnel.loc[(self.df_cnel["cluster_dbscan_2d"] == cluster_2d_dbscan)].shape[0]
                data = (cluster_2d_dbscan, count)
                cluster_2dim_dbscan_data.append(data)
    
        dbscan_clusters_labels = [data[0] for data in cluster_2dim_dbscan_data]
        dbscan_clusters_count = [data[1] for data in cluster_2dim_dbscan_data]

        promedio_dbscan = []
        for cluster in dbscan_clusters_labels:
            promedio = round((self.df_cnel[(self.df_cnel['cluster_dbscan_2d'] == cluster)]['promedio']).mean(),4)
            promedio_dbscan.append(promedio)

        min_dbscan = []
        for cluster in dbscan_clusters_labels:
            min = round((self.df_cnel[(self.df_cnel['cluster_dbscan_2d'] == cluster)]['promedio']).min(),4)
            min_dbscan.append(min)

        max_dbscan = []
        for cluster in dbscan_clusters_labels:
            max = round((self.df_cnel[(self.df_cnel['cluster_dbscan_2d'] == cluster)]['promedio']).max(),4)
            max_dbscan.append(max)

        fig_clusters_dbscan = px.bar( x = dbscan_clusters_labels, y = dbscan_clusters_count, text= dbscan_clusters_count,
                                    title='Dbscan Cluster Data', 
                                    hover_data=[promedio_dbscan, min_dbscan, max_dbscan])
        fig_clusters_dbscan.update_yaxes(title="Usuarios")
        fig_clusters_dbscan.update_xaxes(title="Clusters")
        fig_clusters_dbscan.update_xaxes(tickvals = dbscan_clusters_labels)
        fig_clusters_dbscan.update_traces(hovertemplate='<b>Cluster: </b>: %{x}<br>' + 
                                        '<br><b>No. Usuarios: </b>: %{y}<br>' + 
                                        '<br><b>Promedio [kwh]: </b>: %{customdata[0]}<br>'+ 
                                        '<br><b>Mínimo [kwh]: </b>: %{customdata[1]}<br>'+
                                        '<br><b>Máximo [kwh]: </b>: %{customdata[2]}<br>'
                                        )

        return fig_clusters_dbscan

    def cluster_estratos(self):
        estratos_data = []
        for estrato in sorted(self.df_cnel['estrato'].unique()):
            if (estrato != '5' and estrato != "X"):
                count = self.df_cnel.loc[(self.df_cnel["estrato"] == estrato)].shape[0]
                data = (estrato, count)
                estratos_data.append(data)
    
        estratos_labels = [data[0] for data in estratos_data]
        estratos_count = [data[1] for data in estratos_data]

        promedio_estratos = []
        for cluster in estratos_labels:
            promedio = round((self.df_cnel[(self.df_cnel['estrato'] == cluster)]['promedio']).mean(),4)
            promedio_estratos.append(promedio)

        min_estratos = []
        for cluster in estratos_labels:
            min = round((self.df_cnel[(self.df_cnel['estrato'] == cluster)]['promedio']).min(),4)
            min_estratos.append(min)

        max_estratos = []
        for cluster in estratos_labels:
            max = round((self.df_cnel[(self.df_cnel['estrato'] == cluster)]['promedio']).max(),4)
            max_estratos.append(max)

        fig_clusters_estratos = px.bar( x = estratos_labels, y = estratos_count, text= estratos_count,
                                        title='Estratos Data', 
                                        hover_data=[promedio_estratos, min_estratos, max_estratos])
        fig_clusters_estratos.update_yaxes(title="Usuarios")
        fig_clusters_estratos.update_xaxes(title="Clusters")
        fig_clusters_estratos.update_xaxes(tickvals = estratos_labels)
        fig_clusters_estratos.update_traces(hovertemplate='<b>Estrato: </b>: %{x}<br>' + 
                                        '<br><b>No. Usuarios: </b>: %{y}<br>' + 
                                        '<br><b>Promedio [kwh]: </b>: %{customdata[0]}<br>'+ 
                                        '<br><b>Mínimo [kwh]: </b>: %{customdata[1]}<br>'+
                                        '<br><b>Máximo [kwh]: </b>: %{customdata[2]}<br>'
                                        )

        return fig_clusters_estratos

    def plot_graph_empty(self):
        return {}
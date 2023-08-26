MES = [
    "2019-1",
    "2019-2",
    "2019-3",
    "2019-4",
    "2019-5",
    "2019-6",
    "2019-7",
    "2019-8",
    "2019-9",
    "2019-10",
    "2019-11",
    "2019-12",
    "2020-1",
    "2020-2",
    "2020-3",
    "2020-4",
    "2020-5",
    "2020-6",
    "2020-7",
    "2020-8",
    "2020-9",
    "2020-10",
    "2020-11",
    "2020-12",
    ]

MES_TICKS = [
    "2019-1",
    "2019-4",
    "2019-7",        
    "2019-10",
    "2019-12",
    "2020-3",
    "2020-5",
    "2020-8",
    "2020-10",
    "2020-12",
    ]

DESCRIPTION_kmeans_24dim = """KMEANS es un algoritmo de clasificación no   supervisada
(clusterización) que agrupa objetos en k grupos basándose
en sus características. En este caso se está tomando   en
consideración el consumo eléctrico [kwh] mensual en los años 
2019 y 2020"""

DESCRIPTION_kmeans_2dim = """KMEANS es un algoritmo de clasificación no   supervisada
(clusterización) que agrupa objetos en k grupos basándose
en sus características. En este caso se está tomando   en
consideración el consumo eléctrico promedio  [kwh]  y  la 
desviación estándar de los 24 meses correspondiente a los 
2019 y 2020"""

DESCRIPTION_dbscan_2dim = """Descripción DBSCAN"""

DESCRIPTION_estratificacion = """Estratificación actual usada por la Unidad de Negocios
divide el promedio de los consumos anuales por rangos:
estrato 1: promedio >= 10  y promedio < 150
estrato 2: promedio >= 150 y promedio < 250
estrato 3: promedio >= 250 y promedio < 500
estrato 4: promedio >= 500 y promedio < 1000
estrato 5: promedio >= 1000"""
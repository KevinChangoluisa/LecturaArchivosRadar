# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:37:27 2022

@author: Kevin Changoluisa
"""

from pathlib import Path
import pandas as pd


fileDir = r'C:\\Users\\kchan\\Desktop\\RADAR'
fileExt = r"**\*.p00"

#Cargamos las estaciones
estaciones = pd.read_excel('estaciones.xlsx')

#Cargamos todos los archivos P00
nameFiles=[str(_) for _ in Path(fileDir).glob(fileExt)]


informacion={}



def obtenerX_Y(codigo,este,norte):
    
    puntos=[]                   #Almacenaremos los 4 puntos proximos a la estacion
    coordenadas=[]              #Almacenaremos las coordenadas en i,j de cada punto
    vPixel=500                  #valor de cada pixel en metros
    origenRadarE=780811         #Punto de origen del radar en UTM
    origenRadarN=9974061.5      #Punto de origen del radar en UTM
    vradioMetros=60000          #Valor del radio de la onda del radar
    limite=10000000             #Limite zona sur 0-limite norte 

    PxOrigen=origenRadarE-(vradioMetros+vPixel)   #Este
    PyOrigen=origenRadarN+(vradioMetros+vPixel)-limite   #Norte
    
    for i in range(1,241):
        PxNewOrigen=PxOrigen
        if PyOrigen>0:
            PyOrigen=PyOrigen-vPixel
        elif PyOrigen<=0:
            PyOrigen=limite
        for j in range(1,241):
            if(PxNewOrigen>=este-vPixel and PxNewOrigen<este+vPixel and PyOrigen>=norte-vPixel and PyOrigen<norte+vPixel):
                
                distEste=abs(int(este-PxNewOrigen)) #Medimos la distancia entre la estacion meteorologica y el punto cercano en X
                distNort=abs(int(norte-PyOrigen))   #Medimos la distancia entre la estacion meteorologica y el punto cercano en Y
                
                puntos.append([distEste,distNort])  #Agregamos los puntos en una lista ejm puntos[[1,2],[1,3],[4,2],[3,2]]
                coordenadas.append([i,j])           #Agregamos los puntos i,j en una lista
                
               
            PxNewOrigen=PxNewOrigen+vPixel
    
    PntsDistMin=min(puntos) #Obtenemos el punto con la distancia mas cerca al origen(estacion pluviometro)
    indexPntDstMin=puntos.index(PntsDistMin)
    coord_i_j=coordenadas[indexPntDstMin] #Obtenemos las coordenas en i,j del punto minimo
    return coord_i_j
        



def obtenerPrecipitacion(x_y,codigo):
    
    for i in nameFiles:
        
        data = Path(i).read_bytes()     #Leemos el archivo P00
        dateFile=(data[17:29].decode("utf-8")).strip() #Obtenemos la Fecha y Hora de escaneo
        dateFile=''+dateFile[6:8]+'/'+dateFile[4:6]+'/'+dateFile[0:4]+' '+dateFile[8:10]+':'+dateFile[10:14] #Asinamos un formato de fecha aaaa/mm/dd hh:mm
        #nombreRadar=data[31:50].decode("utf-8").strip()
        precipitacion=data[(x_y[0]*x_y[1])+98] #Obtenemos el valor de precipitacion
        informacion[codigo][dateFile]=precipitacion #Agregamos el valor de precipitacion segun el codigo y la fecha
    
    



for k in range(len(estaciones.index)):
    codigo=estaciones.iloc[k]['Codigo']
    informacion[codigo]={}
    estacionEste=estaciones.iloc[k]['este']
    estacionNorte=estaciones.iloc[k]['norte']
    x_y=obtenerX_Y(codigo,estacionEste,estacionNorte)
    obtenerPrecipitacion(x_y,codigo)

    
df = pd.DataFrame(data=informacion)

df.to_excel('informacionRadarEstaciones.xlsx')


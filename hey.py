# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:48:01 2019


@author: andrea.a.blanco
"""

from __future__ import print_function
from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from os import scandir
import easygui as eg
import os

#EXTRAER METADATOS DE UNA FOTO
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()
#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


#EXTRAER METADATOS CON NOMBRE DE ETIQUETA DE UNA FOTO
def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled
#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


#EXTRAE METADATOS GEOGRÁFICOS DE UNA FOTO
def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging
#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


#DEVUELVE EN DECIMAL
def get_decimal_from_dms(dms, ref):
    
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5) 
#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


#EXTRAER COORDENADAS DE UNA FOTO EN FORMATO DECIMAL
def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon) 
#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
    

#CONVIERTE IMAGEN EN ICONO
def make_thumbnail(filename):
    img = Image.open(directorio + "/" + filename)

    (width, height) = img.size
    if width > height:
        ratio = 50.0 / width
    else:
        ratio = 50.0 / height

    img.thumbnail((round(width * ratio), round(height * ratio)), Image.LANCZOS)
    img.save(directorioIconos + "/" + filename)
#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


#EXTRAER EL ATRIBUTO FECHAYHORA DE LOS METADATOS DE UNA FOTO
def sacarfechayhora(r):
    exif=get_exif(r)
    labeled = get_labeled_exif(exif) 
    return labeled["DateTimeDigitized"]


#CREA UNA LISTA CON LOS NOMBRES DE TODAS LAS FOTOS DADAS
def arrayDeDirectorio(path): 
    return [obj.name for obj in scandir(path) if obj.is_file()]


#ORDENA LA LISTA DE FOTOS POR FECHA Y HORA
def ArraySortedByFecha(dir):
    
    A=arrayDeDirectorio(dir) #array A con todas las fotos que hay en el directorio
    #print(A);
    
    FH=[]
    i=0
    for a in A:
        FH.append(sacarfechayhora(dir + "/" + a))
        i=i+1
        
    FH.sort()  #array con las fechas de las fotos ordenadas
    #print(FH)
    
    FotosOrdenadas=[] 
    k=0
    j=0
    while k<len(FH):   
             if (sacarfechayhora(dir + "/" + A[j])) == FH[k]:
                    FotosOrdenadas.append(A[j])
                    k=k+1
                    j=0
             else:
                    j=j+1
    return FotosOrdenadas


#PIDE AL USUARIO EL DIRECTORIO INICIAL CON LAS FOTOS A ANALIZAR
def selectDirectorio():
     dir = eg.diropenbox(msg="Abrir directorio:",
                            title="Control: diropenbox")
     return(dir)
     
    
#CREA UNA CARPETA PARA GUARDAR LOS ICONOS DE CADA FOTO EN LA RUTA PROPORCIONADA POR EL USUARIO
def dirIconos():
    try:
        os.stat(directorio + "/iconos")
    except:
        os.mkdir(directorio + "/iconos")
    return directorio + "/iconos"


#VARIABLES: DIRECTORIO CON FOTOS DATO
dir=selectDirectorio()   
directorio=dir.replace("\\","/" )     


directorioIconos = dirIconos()
print(directorioIconos)

arrayFotos = ArraySortedByFecha(directorio)


f = open('GeoTrace.html','w')


mens1 = """<!DOCTYPE html>
<html>
 <head>
    <meta charset="utf-8" />
        <style>
          html, body{
            height:80%;
            width:100%
            margin-top: 700px;
          }
        </style>
	<script type='text/javascript'>
     var directionsManager;
     function GetMap() {
         var map = new Microsoft.Maps.Map('#myMap', {
            credentials: 'AusAvA14VCSfLYOZmrvHRfdg_B_fcPT4V3wV-ovSNhvI7WbVPOGhbEMfKH2ZdTVe',
            center: new Microsoft.Maps.Location(40.433367, -3.700833),
            mapTypeId: Microsoft.Maps.MapTypeId.calles,
            zoom: 10
      });

      var center = map.getCenter();"""

for a in arrayFotos:
          nombreFoto = directorio + "/" + a
          exif = get_exif(nombreFoto)  #todos los metadatos de una foto
          geotags = get_geotagging(exif)
          coordenada=get_coordinates(geotags)  #coordenadas decimales de: nombreFoto           
          make_thumbnail(a)  #pasa foto a tamaño icono          
          auxiliar1 = """ 
                    //Create custom Pushpin
                    var pin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location("""+str(coordenada[0])+""" , """+str(coordenada[1])+"""), {
                            icon: '"""+directorioIconos+"""/"""+a+"""',
                            anchor: new Microsoft.Maps.Point(12, 39)
                            });
                     //Add the pushpin to the map
                     map.entities.push(pin);
                              """
          mens1=mens1+auxiliar1;

mens2="""Microsoft.Maps.loadModule('Microsoft.Maps.Directions', function () {
                                                
            //Ask for routing mode(default = driving) via html-select
            var user = document.getElementById("routingModing");
            var routeSelected = user.options[user.selectedIndex].text;
            
           //Set routing mode as user wants 
           var routeModeSelected=Microsoft.Maps.Directions.RouteMode.driving
           if(routeSelected == "walking"){
            routeModeSelected=Microsoft.Maps.Directions.RouteMode.walking
           }else if(routeSelected == "transit"){
            routeModeSelected=Microsoft.Maps.Directions.RouteMode.transit
           }
                                               
            //Create an instance of the directions manager.
            directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
            //Calculate a date time that is 1 hour from now.
            var departureTime  = new Date();
            departureTime.setMinutes(departureTime.getHours() + 1);
            //Set Route Mode
            directionsManager.setRequestOptions({
                routeMode: routeModeSelected,
                time: departureTime,
                timeType: Microsoft.Maps.Directions.TimeTypes.departure
            });""" 
         
for a in arrayFotos:
          nombreFoto = directorio + "/" + a
          exif = get_exif(nombreFoto)  #todos los metadatos de una foto
          geotags = get_geotagging(exif)
          coordenada=get_coordinates(geotags)  #coordenadas decimales de: nombreFoto           
          make_thumbnail(a)  #pasa foto a tamaño icono  
          auxiliar2=""" var workWaypoint = new Microsoft.Maps.Directions.Waypoint({ address: '"""+a[:-4]+"""', location: new Microsoft.Maps.Location("""+str(coordenada[0])+""" ,"""+str(coordenada[1])+""") });
                        directionsManager.addWaypoint(workWaypoint); """
          mens2=mens2+auxiliar2

mens3="""
            //Specify the element in which the itinerary will be rendered.
             directionsManager.setRenderOptions({ itineraryContainer: document.getElementById('directionsItinerary') });
            //Calculate directions.
            directionsManager.calculateDirections();
                });
            }
                                            
            function refreshMap(){
                    GetMap();
            }
   </script>
            
   <script type='text/javascript' src='http://www.bing.com/api/maps/mapcontrol?callback=GetMap&key=[AusAvA14VCSfLYOZmrvHRfdg_B_fcPT4V3wV-ovSNhvI7WbVPOGhbEMfKH2ZdTVe]' async defer></script>
 </head>
<body>
      <div>
          <p style="font-family:fantasy;color:darkcyan;font-size:40px;margin-bottom:5px;text-align: center;">Geotrace</p>
          <p style="font-family: auto;color:darkcyan;font-size:20px;margin-bottom: 50px;text-align: center;">Una aplicaci&oacute;n para el seguimiento geogr&aacute;fico de im&aacute;genes</p>
      </div>
  
      <div style="color: darkcyan;font-family: auto;font-size: 18px;">Please select your favorite option:
        <select id="routingModing" onchange="refreshMap()" style="font-size: 20px;color: darkcyan;font-family: auto;border: none;cursor: pointer;font-style: italic;font-weight: 900">
        <option value="1" selected="selected" style="color: red;">driving</option>
        <option value="2" style="color: orange;">transit</option> 
        <option value="3" style="color: greenyellow;">walking</option>
        </select>
      </div>                      
                  
      <div id="myMap" style="margin-top:5px"></div>
      <div id='directionsItinerary'></div>
</body>
</html>
"""
#https://docs.microsoft.com/en-us/bingmaps/v8-web-control/



mensaje =mens1+mens2+mens3
f.write(mensaje)
f.close()

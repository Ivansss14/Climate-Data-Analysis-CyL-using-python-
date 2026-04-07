import pandas as pd
import requests
import json
import time
import os

#get the directory where the script is located
base_dir=os.path.dirname(os.path.abspath(__file__))

#read our API key from the txt file
rutaapi=os.path.join(base_dir, "api.txt")
with open(rutaapi, "r") as archivo:
    API=archivo.read().strip()

estaciones=["2331","9051"] #Burgos. Here we can use some stations for one province or combine with others
inicio=1980
final=2025 #years of study
key={'api_key': API}

#path where I save the data (relative to the script folder)
ruta =os.path.join(base_dir, "Datos", "BURGOS", "rescates")

#I analyze in a period of 6 months (aemet api criteria)
mitad = [("-01-01T00:00:00UTC", "-06-30T23:59:59UTC"), ("-07-01T00:00:00UTC", "-12-31T23:59:59UTC")]

#we read the climate stations
for est in estaciones:
    print(f"Downloading data for station {est} (Burgos)")
    archivo_csv=os.path.join(ruta, f"data_{est}_2019.csv")
    
    if not os.path.exists(archivo_csv):
        #create folder if it doesn't exist
        os.makedirs(ruta, exist_ok=True)
        with open(archivo_csv, "w", encoding="utf-8") as f:
            f.write("fecha,precipitacion,tmed,tmin,tmax\n")
        
    for year in range(inicio, final):
        for mesini, mesfin in mitad:
            ini = f"{year}{mesini}"
            fin = f"{year}{mesfin}"
            web=f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{ini}/fechafin/{fin}/estacion/{est}"
            respuesta=requests.get(web, headers=key)
            
            #check for empty response in the Aemet data
            if respuesta.text.strip() == "":
                print(f"Year and month {ini[:10]} with empty response")
            else:
                datos = respuesta.json()
                if datos.get('estado') == 200:
                    linkreal =datos['datos']
                    resultado =requests.get(linkreal)
                    prectemp =resultado.json() #json response
                    
                    #we save the data. Here we format numbers to numeric and replace commas with dots
                    with open(archivo_csv, "a", encoding="utf-8") as f:
                        for dia in prectemp:
                            fecha =dia.get('fecha', '')
                            prec =dia.get('prec', '0,0').replace(',', '.')
                            tmed =dia.get('tmed', '').replace(',', '.')
                            tmin =dia.get('tmin', '').replace(',', '.')
                            tmax =dia.get('tmax', '').replace(',', '.')
                            f.write(f"{fecha},{prec},{tmed},{tmin},{tmax}\n")
                    print(f"Downloaded and written: {ini[:10]} to {fin[:10]} ({len(prectemp)} days)")
                else:
                    mensaje =datos.get('descripcion', 'unknown error')
                    print(f"Error in {year}: {mensaje}")
            
            print("Waiting 1 minute (AEMET criteria)")
            time.sleep(70) #wait for at least 60s (its better more than 60) to prevent api ban

print("Download Finished :)")
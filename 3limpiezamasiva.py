import pandas as pd
import glob
import os

#get the directory where the script is located to use relative paths
base_dir= os.path.dirname(os.path.abspath(__file__))

#data location
ruta=os.path.join(base_dir, "Datos")
provincias=["VALLADOLID","BURGOS","SALAMANCA","AVILA","SEGOVIA","ZAMORA","SORIA","PALENCIA","LEON"]

print("Starting massive data cleaning")

#provinces loop (we analyze all of them)
for provincia in provincias:
    print(f"\n ---processing province: {provincia.upper()}---")
    #province save path
    rutaprovincia= os.path.join(ruta, provincia)
    rescate= os.path.join(rutaprovincia, "rescates")
    #we select the data to analyze (not the clean ones)
    busco= os.path.join(rescate, "*.csv")
    archivos= glob.glob(busco)
    
    #analyze files inside each province
    for data in archivos:
        if "_limpio" in data:
            continue #skip already cleaned files
            
        estacion = os.path.basename(data)
        print(f"cleaning station: {estacion}")
        df= pd.read_csv(data)
        df['fecha']= pd.to_datetime(df['fecha'])
        
        #replace Ip (inappreciable precipitation) with 0.0
        df['precipitacion']= df['precipitacion'].astype(str).str.replace('Ip','0.0')
        
        #convert columns to numeric
        df['precipitacion']= pd.to_numeric(df['precipitacion'], errors='coerce')
        df['tmed']= pd.to_numeric(df['tmed'], errors='coerce')
        df['tmin']= pd.to_numeric(df['tmin'], errors='coerce')
        df['tmax']= pd.to_numeric(df['tmax'], errors='coerce')
        
        #save the clean file and dataframe (pandas)
        limpio = data.replace(".csv", "_limpio.csv")
        df.to_csv(limpio, index=False)

print("CLEANING COMPLETE! :)")
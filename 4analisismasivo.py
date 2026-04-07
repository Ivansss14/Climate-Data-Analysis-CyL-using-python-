import pandas as pd
import glob
import os

#get the directory
base_dir= os.path.dirname(os.path.abspath(__file__))

#access the provinces folder
ruta= os.path.join(base_dir, "Datos")
provincias= ["VALLADOLID","SORIA","SALAMANCA","ZAMORA","LEON","SEGOVIA","PALENCIA","AVILA","BURGOS"]
final= pd.to_datetime('2025-12-31')

print("--Analyzing CYL--")
for provincia in provincias:
    print(f"---Scanning: {provincia.upper()}")
    rutaprov = os.path.join(ruta, provincia)
    
    #search only for clean files
    busco= os.path.join(rutaprov, "*_limpio.csv")
    limpios= glob.glob(busco)
    
    for archivo in limpios:
        estacion = os.path.basename(archivo).replace("_limpio.csv","")
        print(f"\n Analyzing station: {estacion}")
        
        #read and create the analysis calendar
        df = pd.read_csv(archivo)
        df['fecha']= pd.to_datetime(df['fecha'])
        
        #remove duplicate values from some stations
        df= df.drop_duplicates(subset=['fecha'], keep='first')
        
        inicio= df['fecha'].min()
        calendario= pd.date_range(start=inicio, end=final, freq='D')
        
        #index the dates
        df.set_index('fecha', inplace=True)
        df_completo= df.reindex(calendario)
        
        #the data failures
        totalhuecos = df_completo['precipitacion'].isna().sum()
        if totalhuecos == 0:
            print("Perfect station")
        else:
            print(f" Data starts at: {inicio.date()} Total gaps: {totalhuecos} days")
            
            #check for api failures
            huecosyear = df_completo['precipitacion'].isna().groupby(df_completo.index.year).sum()
            badyears = huecosyear[huecosyear > 100] # Semester-long failures
            if not badyears.empty:
                print("Missing semesters in the following years:")
                for year, dias in badyears.items():
                    print(f"Year: {year}, missing {dias} days")
import pandas as pd
import glob
import os
base_dir = os.path.dirname(os.path.abspath(__file__))

#data location
ruta = os.path.join(base_dir, "Datos")
provincias = ["VALLADOLID","BURGOS","SALAMANCA","AVILA","SEGOVIA","ZAMORA","SORIA","PALENCIA","LEON"]

print("data fusion")

for provincia in provincias:
    print(f"\n ---PROVINCE: {provincia}")
    rutaprovincia= os.path.join(ruta, provincia)
    rescate= os.path.join(rutaprovincia, "rescates")
    
    #we take only the clean files
    limpio= os.path.join(rutaprovincia, "*_limpio.csv")
    base= glob.glob(limpio)
    
    for archivo in base:
        nombre = os.path.basename(archivo)
        
        #extract the station code:
        try:
            estacion= nombre.split('_')[1]
        except IndexError:
            continue #in case there are files with other naming formats
        
        print(f"Analyzing station: {estacion} from {provincia}")
        
        #use asterisks to catch any year for the selected station
        rutarescate = os.path.join(rescate, f"*{estacion}*_limpio.csv")
        parche = glob.glob(rutarescate)
        
        #open the base file without the "rescates":
        df_base = pd.read_csv(archivo)
        df_base['fecha'] = pd.to_datetime(df_base['fecha'])
        
        if not parche:
            print(f"No rescue files found, saving directly as definitive")
            df_fusion= df_base
        else:
            print(f"Fusion started. Found rescue files: {len(parche)}")
            union= [df_base]
            for falta in parche: #add missing data files
                df_parche= pd.read_csv(falta)
                df_parche['fecha'] = pd.to_datetime(df_parche['fecha'])
                union.append(df_parche) #merge them with the base
                
            #concatenate all files into a single table
            df_fusion= pd.concat(union, ignore_index=True)
            #sort by date
            df_fusion= df_fusion.sort_values(by='fecha')
            #remove duplicates, keeping the patch data just in case
            df_fusion= df_fusion.drop_duplicates(subset=['fecha'], keep='last')
            
        #final save as definitive
        definitivo= archivo.replace("_limpio.csv", "_definitivo.csv")
        df_fusion.to_csv(definitivo, index=False)
        
        print(f"Saving: {os.path.basename(definitivo)}")

print("FUSION COMPLETE")
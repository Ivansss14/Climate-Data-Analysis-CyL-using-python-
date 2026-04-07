import pandas as pd
import os
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))

#read downloaded files from Inforiego, clean and adjust them to AEMET format
ruta = os.path.join(base_dir, "Datos", "ZAMORA", "Inforiego", "Toro")
guardado = os.path.join(base_dir, "Datos", "ZAMORA", "Inforiego", "datos_Toro_Inforiego_definitivo.csv")
#that directory is from my final analysis from the station (from inforiego) of Toro, Zamora. You should edit your program to analyze your data carefully :)

print("---Building the File---")
archivos = glob.glob(os.path.join(ruta, "*.csv")) #get all files
limpio= []

#cleaning each file
for archivo in archivos:
    print(f"Processing: {os.path.basename(archivo)}")
    
    #read skipping info headers and selecting only necessary columns
    df= pd.read_csv(archivo, sep=';', skiprows=19, usecols=[0, 1, 2, 4, 17], index_col=False, encoding='latin1')
    df= df.drop(0)
    
    #rename columns to match AEMET format
    df.columns= ['fecha', 'tmed', 'tmax', 'tmin', 'precipitacion']
    
    #convert dates and remove the bottom summary table
    df['fecha']= pd.to_datetime(df['fecha'], format='%d/%m/%Y', errors='coerce')
    df= df.dropna(subset=['fecha']) #delete extra info rows
    
    #convert data to numeric format
    for col in ['tmed', 'tmax', 'tmin', 'precipitacion']:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    #append to our list
    limpio.append(df)

#merge all files into one
df_final= pd.concat(limpio, ignore_index=True)
#remove duplicates just in case
df_final= df_final.sort_values('fecha').drop_duplicates(subset=['fecha'], keep='last')
#create the calendar and check for missing days
print("Creating the calendar, counting missing days")
df_final.set_index('fecha', inplace=True)
calendario= pd.date_range(start=df_final.index.min(), end=df_final.index.max())
df_final= df_final.reindex(calendario)
df_final= df_final.rename_axis('fecha').reset_index()
#reorder columns to match aemet files
df_final = df_final[['fecha', 'precipitacion', 'tmed', 'tmin', 'tmax']]
df_final['fecha'] = df_final['fecha'].dt.strftime('%Y-%m-%d')

#save result
df_final.to_csv(guardado, index=False)
print("DONE")
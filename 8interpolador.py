import pandas as pd
import glob
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

#file paths (Zamora was my last...)
inicio= os.path.join(base_dir, "Datos", "ZAMORA", "DATOS A INTERPOLAR")
guardado= os.path.join(base_dir, "Datos", "ZAMORA", "DATOS DEFINITIVOS")

#create output folder if it doesnt exist
os.makedirs(guardado, exist_ok=True)

print("Starting data interpolation")
archivos= glob.glob(os.path.join(inicio, "*.csv"))

for archivo in archivos:
    nombre= os.path.basename(archivo)
    print(f"Interpolating: {nombre}")
    
    df= pd.read_csv(archivo)
    #convert date to datetime just in case
    df['fecha']= pd.to_datetime(df['fecha'])
    interpolacion= ['precipitacion', 'tmed', 'tmin', 'tmax'] #WHERE WE WANT TO APPLY THE INTERPOLATION
    #LIMIT OF 3 DAYS, MY PRECISE RIGOR (ESPECIALLY FOR PRECIPITATION)
    df[interpolacion]= df[interpolacion].interpolate(method='linear', limit=3) 
    #just in case precipitation goes below 0, we restrict it
    df.loc[df['precipitacion'] < 0, 'precipitacion'] = 0 #limit of 0 or greater for precipitation
    #round decimals and save and its doneeeee
    df[interpolacion]= df[interpolacion].round(2)
    rguardado = os.path.join(guardado, nombre)
    df.to_csv(rguardado, index=False)
    
print("DONE")
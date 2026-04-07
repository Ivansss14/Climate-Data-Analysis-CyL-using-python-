import pandas as pd
import matplotlib.pyplot as mt
import os
base_dir= os.path.dirname(os.path.abspath(__file__))
#direction (Leon was my last in the study this time :)
ruta= os.path.join(base_dir, "Datos", "LEON", "DATOS DEFINITIVOS", "datos2661_Leon.csv")
nombre_archivo = os.path.basename(ruta)
print(f"Analyzing data from: {nombre_archivo}")
df= pd.read_csv(ruta)
df['fecha']= pd.to_datetime(df['fecha'])

#analyze by year to group data
df['year'] = df['fecha'].dt.year
#calculate and group annually grouping by year: sum of precipitation, mean for temperatures
df_anual = df.groupby('year').agg({'precipitacion': 'sum', 'tmed': 'mean', 'tmin': 'mean', 'tmax': 'mean'}).reset_index()

#two stacked plots (temp n prec)
graf, (ax1, ax2) = mt.subplots(2, 1, figsize=(12, 10))
#top plot: temp
ax1.plot(df_anual['year'], df_anual['tmed'], color='darkgreen', marker='o', linewidth=2.5, label='Mean Temp')
ax1.plot(df_anual['year'], df_anual['tmin'], color='blue', linestyle='--', alpha=0.6, label='Min Temp')
ax1.plot(df_anual['year'], df_anual['tmax'], color='red', linestyle='--', alpha=0.6, label='Max Temp')

ax1.set_title("Annual Temperature Evolution - Leon Capital (1980-2025)", fontsize=14, fontweight='bold')
ax1.set_ylabel('Temperature (ºC)', fontsize=12)
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend()

#bottom plot: prec
ax2.bar(df_anual['year'], df_anual['precipitacion'], color='teal', alpha=0.7)

#historical mean prec line
mediaprec = df_anual['precipitacion'].mean()
ax2.axhline(mediaprec, color='darkred', linestyle='--', linewidth=2, label='Historic Mean Precipitation (mm)')

ax2.set_title("Annual Precipitation - Leon Capital (1980-2025)", fontsize=14, fontweight='bold')
ax2.set_ylabel('Accumulated Precipitation (mm)', fontsize=12)
ax2.set_xlabel('Year', fontsize=12)
ax2.grid(True, linestyle=':', alpha=0.7, axis='y')
ax2.legend()

mt.tight_layout()
mt.show()
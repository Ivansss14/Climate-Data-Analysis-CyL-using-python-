import pandas as pd
import os

#the directory
base_dir=os.path.dirname(os.path.abspath(__file__))

#this program is a proof to see if it works, then i made the big one.
archivo=os.path.join(base_dir, "Datos", "VALLADOLID", "datosValladolid_2422_limpio.csv")

print(f"Analyzing {archivo}")
df= pd.read_csv(archivo)
df['fecha']= pd.to_datetime(df['fecha']) #manage dataframes to put the datetime as columns

#the start and end for our calendar
inicio= df['fecha'].min() #the minimum of our date data is the initial date
final= pd.to_datetime('2025-12-31')

print(f"First day of data in this station: {inicio}")
print(f"Final date: {final}")

#create the calendar. With pd.date_range we create a list of days (freq='D' day frequency)
calendario= pd.date_range(start=inicio, end=final, freq='D')

#overlay the data (index the days)
df.set_index('fecha', inplace=True)

#days without data in our file will appear as NaN in the calendar
df_todo=df.reindex(calendario)

#count the missing data
huecosprec= df_todo['precipitacion'].isna().sum()
huecostmed= df_todo['tmed'].isna().sum()
huecostmax= df_todo['tmax'].isna().sum()
huecostmin= df_todo['tmin'].isna().sum()

print(f"Days without precipitation data: {huecosprec}")
print(f"Days without tmed data: {huecostmed}")
print(f"Days without tmax data: {huecostmax}")
print(f"Days without tmin data: {huecostmin}")

#we check for missing full years or 6-month gaps (api failure)
print("Missing data by years")
huecosyear = df_todo['precipitacion'].isna().groupby(df_todo.index.year).sum()
badyears = huecosyear[huecosyear > 0]
print(badyears)
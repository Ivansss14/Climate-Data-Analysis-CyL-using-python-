import pandas as pd
import os

base_dir= os.path.dirname(os.path.abspath(__file__))

#paths (Soria was the last I analyzed. You should change the csv directory in case you wanna join other files)
aemet = os.path.join(base_dir, "Datos", "SORIA", "datosSoria_2092_definitivo.csv")
inforiego = os.path.join(base_dir, "Datos", "SORIA", "Inforiego", "datos_SanEsteban_Inforiego_definitivo.csv")
final = os.path.join(base_dir, "Datos", "SORIA", "DATOS A INTERPOLAR", "datos2092_BOsma.csv")
print("Starting AEMET and Inforiego union")
#read data
df_aemet= pd.read_csv(aemet)
df_info= pd.read_csv(inforiego)

#align the calendars
df_aemet.set_index('fecha', inplace=True)
df_info.set_index('fecha', inplace=True)

# our original aemet file is the important one, we fill missing data or gaps with Inforiego
df_union= df_aemet.combine_first(df_info)
df_union= df_union.rename_axis('fecha').reset_index()
df_union= df_union.sort_values('fecha')
df_union= df_union[['fecha', 'precipitacion', 'tmed', 'tmin', 'tmax']]
#save it
df_union.to_csv(final, index=False)
print("DONE")
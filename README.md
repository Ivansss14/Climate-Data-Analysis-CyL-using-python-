# Climate-Data-Analysis-CyL-using-python-
This will be a diary of my Final Year Project (TFG) in Physics. I will upload my working method and my python scripts that I use in the data analysis from AEMET and Inforiego to see if climate change is notable in this region of Spain.

---

## ❓About the Project

The goal of this project is to collect, clean and analyze historical meteorological data to see if climate change is appreciable in Castilla y Leon, Spain. The principal purpose is to understand whether precipitacion has varied over the years in this region. 

---

## 📕Work Diary

Until now I made this work:
1. **Geographical analysis:** I selected 3 or 4 meteorological stations well separated to fully analyze each province of Castilla y Leon as best as possible.
   
2. **Download data (API):** I downloaded the data from different meteorological stations using AEMET API in a scale of 30-45 years (from 1980 to 2025).
   
3. **Data cleaning and analysis:** I developed a script to identify the missing data (days or years) for each station and then another script to make a massive clean for all the data. Removing corrupted data, making a full daily calendar using dataframes. Libraries used: **os, glob and pandas.**
   
4. **Download lost data (API):** I downloaded the lost data (API failures, connection drops). And I merged those CSVs with the original datasets.
   
5. **Data enrichment by using Inforiego:** I got new data for the stations(or near them up to a maximum of 25 km to have precise accuracy). I cleaned this new data, transformed the CSVs to match the AEMET format and merged it all in the calendar by using dataframes.
   
6. **Interpolation:** I made a linear interpolation to fill small gaps by the strict 3-day limit. (THIS COULD CHANGE BECAUSE INTERPOLATING PRECIPITATION IS NOT STANDARD SCIENTIFIC PRACTICE).
   
7. **Visualization:** Generating graphs by using **matplotlib.pyplot** to see the results of temperature and precipitation.

## 🌧️Structure (Scripts)
Here is a summary of how the python scripts I made work:

*1descargaAPI.py:* This program accesses to the AEMET API and downloads the data for the station or stations we want. It downloads the data in a time period we indicate. Also it prepares the data into float format and changes commas into dots.

*2pruebanalisis.py:* This script makes a calendar for our data and tells us the days in which data is missing. Using **os and pandas.**

*3limpiezamasiva.py:* Cleans all the data for the different provinces using **pandas, glob and os**. (corrupt data and other cases).

*4analisismasivo.py:* It takes the cleaned data and tells us ALL the gaps and the failures by analyzing each year. 

*5fusion.py:* It takes the saved years ("rescates") and the original datasets and merges them into one unique file for each station (CSV).

*6inforiego.py:* As the name says, this program analyzes the CSVs downloaded from inforiego and converts them into AEMET format. It also cleans this data.

*7union.py:* It makes the union of AEMET files and Inforiego ones into one unique CSV for each station.

*8interpolador.py:* Here, we do the linear interpolation with the limit I detailed before.

*9grafica.py:* This script generates two graphs for each CSV to analyze precipitation and temperature correctly.

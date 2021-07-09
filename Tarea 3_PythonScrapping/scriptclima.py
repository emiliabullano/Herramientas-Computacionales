# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 10:23:02 2021

@author: Gaston
"""
import os
os.chdir("C:/Users/Gaston/Desktop/Herramientas computacionales/Clase 3 - Scrapping/Tarea/WorldWeatherOnline-master")
from wwo_hist import retrieve_hist_data

frequency=24
start_date = '01-JAN-2015'
end_date = '31-DEC-2015'
api_key = 'd6e69e37ff3d46178b5175203210507'
location_list = ["20625", "20650", "20688", "20749", "20871", "21040", "21041", "21157", "21212", "21220", "21405", "21501", "21606", "21638", "21639", "21643", "21651", "21704", "21741", "21801", "21811", "21853", "21914"]

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)
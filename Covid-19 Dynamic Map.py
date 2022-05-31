# -*- coding: utf-8 -*-
"""
Created on Mon May 30 09:41:43 2022

@author: gahat
"""
#importing Data
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import PIL
import io

data=pd.read_csv('time_series_covid19_confirmed_global.csv')

#sorting Data
data=data.groupby('Country/Region').sum()

#dropping unncessary data
data=data.drop(columns={'Lat','Long'})

#Transposing Data
data_transposed=data.T 
#data_transposed.plot(y=['US','Brazil','India'],use_index=True,figsize=(8,7))

#Loading world map
world_map=gpd.read_file('Coronavirus Cases March 2020\World_Map.shp')
#replacing unnecesary datas
data_transposed=data_transposed.drop(columns={'Antarctica','Kosovo','South Sudan','Diamond Princess','Holy See','MS Zaandam','Micronesia','Summer Olympics 2020','Winter Olympics 2022'})
covid_data=data_transposed.T
#replacing name of country
world_map.replace('Viet Nam', 'Vietnam', inplace = True)
world_map.replace('Brunei Darussalam', 'Brunei', inplace = True)
world_map.replace('Cape Verde', 'Cabo Verde', inplace = True)
world_map.replace('Democratic Republic of the Congo', 'Congo (Kinshasa)', inplace = True)
world_map.replace('Congo', 'Congo (Brazzaville)', inplace = True)
world_map.replace('Czech Republic', 'Czechia', inplace = True)
world_map.replace('Swaziland', 'Eswatini', inplace = True)
world_map.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
world_map.replace('Korea, Republic of', 'Korea, South', inplace = True)
world_map.replace("Lao People's Democratic Republic", 'Laos', inplace = True)
world_map.replace('Libyan Arab Jamahiriya', 'Libya', inplace = True)
world_map.replace('Republic of Moldova', 'Moldova', inplace = True)
world_map.replace('The former Yugoslav Republic of Macedonia', 'North Macedonia', inplace = True)
world_map.replace('Syrian Arab Republic', 'Syria', inplace = True)
world_map.replace('Taiwan', 'Taiwan*', inplace = True)
world_map.replace('United Republic of Tanzania', 'Tanzania', inplace = True)
world_map.replace('United States', 'US', inplace = True)
world_map.replace('Palestine', 'West Bank and Gaza', inplace = True)
world_map.replace("Korea, Democratic People's Republic of", 'Korea, North', inplace = True)
world_map.replace('Republic of Kosovo', 'Kosovo', inplace = True)
world_map.replace('Republic of South Sudan', 'South Sudan', inplace = True)

#Checking Worldmap and data

for index,row in covid_data.iterrows():
    if index not in world_map['NAME'].to_list():
        print(index+' not in the list')
    else:
        pass

#Merging Data

combined_data=world_map.join(covid_data,on='NAME',how='right') 
image_frames=[]
#plotting
for dates in combined_data.columns.to_list()[2:862]:
    plot=combined_data.plot(column=dates,
                            cmap = 'OrRd',
                            legend=True,
                            scheme = 'user_defined', 
                            classification_kwds = {'bins':[1000,10000,100000,1000000,10000000,50000000]},
                            figsize=(12,12))
    #Add Title to the map
    plot.set_title('Total Confirmed Coronavirus Cases: '+dates, fontdict = 
                     {'fontsize':20}, pad = 12.5)
    # Move the legend 
    plot.get_legend().set_bbox_to_anchor((0.28, 0.45))
    
    img=plot.get_figure()
    f = io.BytesIO()
    img.savefig(f, format = 'png', bbox_inches = 'tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))

# Create a GIF animation 
image_frames[0].save('Dynamic COVID-19 Map.gif', format = 'GIF',
            append_images = image_frames[1:], 
            save_all = True, duration = 3000, 
            loop = 3)
f.close()
   


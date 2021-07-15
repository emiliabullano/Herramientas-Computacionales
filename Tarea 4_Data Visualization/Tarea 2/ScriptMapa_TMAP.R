rm(list=ls())

setwd("E:/Desktop/Emilia/Maestria UdeSA/Herramientas Computacionales/Data visualization/videos 2 y 3/videos 2 y 3")

# Leemos base espacial
library(sf)
lnd <- st_read("data/london_sport.shp")
names(lnd)

# Chequeo clase de las variables
sapply(lnd, class)

summary(lnd$geometry)

## Base de Crimen
crime_data <- read.csv("data/mps-recordedcrime-borough.csv")

head(crime_data$CrimeType) # information about crime type

# Extract "Theft & Handling" crimes and save
crime_theft <- crime_data[crime_data$CrimeType == "Theft & Handling", ]
table(crime_theft$Borough)

# Calculate the sum of the crime count for each district, save result
crime_ag <- aggregate(CrimeCount ~ Borough, FUN = sum, data = crime_theft)

# Compare the name column in lnd to Borough column in crime_ag to see which rows match.
lnd$name %in% crime_ag$Borough
# Return rows which do not match
lnd$name[!lnd$name %in% crime_ag$Borough]

## Unimos a la base espacial
library(dplyr)
names(crime_ag)
names(lnd)
lnd <- left_join(lnd, crime_ag, by = c('name' = 'Borough'))

# Creamos Variable de Interes
lnd$robos_1000 = lnd$CrimeCount/lnd$Pop_2001*1000

# Creamos Etiqueta para los mapas
lnd$etiq =round(lnd$robos_1000,0) 


############ MAPAS ############

# Mapa de base
library(ggmap)
polygon <- c(left =-0.6505177, bottom = 51.18589, right = 0.4645123, top = 51.76324)
basemap = get_stamenmap(polygon, zoom = 10, 
                        maptype = "terrain")
ggmap(basemap)

devtools::install_github("poissonconsulting/poisspatial") #instalar una unica vez
library(poisspatial)
raster = ps_ggmap_to_raster(basemap) #lo pasamos a raster para poder usar en tmap
class(raster)

# Pasamos a 4326 (sist de coord google)
lnd_4326 = st_transform(lnd, crs = 4326)

# Colores
library(RColorBrewer)
col = brewer.pal(n=7, "Reds")

## TMAP ##
library(tmap)
library(tmaptools)

tmap_mode('plot')
map_tmap <- tm_shape(raster$layer.1) +
  tm_raster("layer.1", legend.show = F, alpha = 0.3, saturation = 1,
            palette = c("black","grey","white")) +
  tm_shape(lnd_4326)+
  tm_fill("robos_1000", title = "Robos c/ 1000 hab.", style = "quantile", 
          n=5, palette = "Reds")+
  tm_text("etiq", size = 0.7)+
  tm_borders("black",lwd = 0.5, alpha = 0.4)+
  tm_layout(legend.outside = F, legend.outside.position = "left",
            legend.position = c("left", "bottom"),
            inner.margins = 0,
            legend.title.size = 0.8,
            legend.frame = F,
            main.title = "Robos cada 1000 habitantes según distrito en Londres",
            main.title.position = c("center", "top"),
            main.title.size = 1.1)+
  tm_scale_bar(position= c("right", "bottom"), breaks = c(0,5,10),text.size = 0.6)

map_tmap


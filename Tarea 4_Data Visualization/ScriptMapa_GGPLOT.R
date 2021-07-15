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

# London of City FALTA
faltante = subset(lnd, is.na(lnd$robos_1000) ==T)
faltante$`No Disponible` = "N/D"


############ MAPA ############
## GGPLOT2 ##
library(ggplot2)

# Mapa de base
library(ggmap)
polygon <- c(left =-0.6505177, bottom = 51.18589, right = 0.4645123, top = 51.76324)
basemap = get_stamenmap(polygon, zoom = 10, 
                        maptype = "terrain")
ggmap(basemap) 

# Pasamos a 4326 (sist de coord q use google)
lnd_4326 = st_transform(lnd, crs = 4326)

devtools::install_github("yutannihilation/ggsflabel") #instalar una unica vez
library(ggsflabel) #para poner geom_sf_text() 
library(ggsn) # para poner la scalebar()


map_ggplot = ggmap(basemap, alpha=0.5) +
  geom_sf(data = lnd_4326, aes(fill=robos_1000), inherit.aes = FALSE) +
  geom_sf_text(data = lnd_4326, aes(label = etiq), size=3, 
               inherit.aes = FALSE, ) +
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.title = element_blank(),
        axis.ticks = element_blank(),
        rect = element_blank(),
        legend.position=c(.87,.23),
        legend.background = element_rect(fill = alpha("white", 0.7)),
        plot.title = element_text(hjust = 0.5)) +
  xlab("") + ylab("") + 
  labs(fill = "Robos c/ 1000 hab.", 
       title = "Robos cada 1000 habitantes según districtos de Londres") +
  scalebar(lnd_4326, location = "bottomleft", dist=5, dist_unit = "km", model = "WGS84",
           transform = T, st.bottom = T) +
  scale_fill_gradientn(colours = c("#FFFFFF", "#FC9272", "#FB6A4A", "#EF3B2C", "#e34a33", "red"),
                      guide = "legend",
                      labels = c(paste0(0," - ",37) ,paste0(37," - ",57) ,paste0(57," - ",66),  
                                 paste0(66," - ",85),paste0(85," - ",112),paste0(112," - ",430)),
                      breaks = c(37.35668 , 56.96215  ,66.10526,  85.26955, 112.20953, 429.30981),
                      na.value = "grey50")+
  geom_sf(data = faltante, aes(color=`No Disponible`), inherit.aes = FALSE)
   
map_ggplot


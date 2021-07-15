#################### Tarea 4 - Parte 1. Bullano y García Zavaleta ##############

# En este trabajo se corrigen una serie de gr??aficos realizados en clase
# y en practicos anteriores a partir de las sugerencias encontradas en Schwabish (2014).

#Cargamos las librerías.
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")

# Agregamos la librería que contiene la fuente que vamos a usar en nuestro theme.
library("extrafont")
loadfonts(device = "win")

#Seteamos el directorio de trabajo.
setwd("C:/Users/Gaston/Desktop/Herramientas computacionales/Clase 4 - Data Visualization")
#Check working directory
getwd()

# Cargamos las base de datos.
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")


# 1. Cantidad de clientes según monto de préstamo por categoría.
# En esta primera sección se corrige la Figura 1.

# Código para Figura 1 (hecho en clase).

df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))


pb1<-ggplot(df3s,aes(x=loan_amnt))
pb1
pb2<-pb1+geom_histogram(bins=10,fill="cadetblue4")
pb2
#Facet_wrap
pb3<-pb2+facet_wrap(~grade) 
pb3
#Free y coordinate for the subplots
pb4<-pb3+facet_wrap(~grade, scale="free_y")
pb4

# Código para Figura 2.

pb4corr2 = ggplot(df3s, aes(x=loan_amnt, fill = grade)) +
  geom_bar(position = "stack") +
  stat_bin(bins = 10, colour = "white") + 
  scale_fill_brewer(palette="YlOrRd") +
  xlab("Monto del préstamo") + 
  ylab("Cantidad de clientes") +
  labs(fill="Categoría") +
  theme(
    text = element_text(family = "Times New Roman", size=12),
    # Hide panel borders and remove grid lines
    panel.border = element_rect(colour = "grey", fill = NA),
    panel.grid.major = element_line(colour = "#E5E7E9", size=0.0001, linetype = "dashed"),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill="white"),
    # Change axis line
    axis.line = element_line(colour = "grey"),
    axis.ticks = element_line(colour = "grey"),
    axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
    axis.title.x = element_text(margin = margin(t =10, r = 0, b = 0, l = 0))
  )
pb4corr2 

# Código para figura 3.

pb4corr3 = ggplot(df3s, aes(x=loan_amnt, fill = grade)) +
  geom_density(position = "fill") +
  scale_fill_brewer(palette="YlOrRd") +
  xlab("Monto del préstamo") + 
  ylab("Densidad") +
  labs(fill="Categoría") +
  theme(
    text = element_text(family = "Times New Roman", size=12),
    # Hide panel borders and remove grid lines
    panel.border = element_rect(colour = "grey", fill = NA),
    panel.grid.major = element_line(colour = "#E5E7E9", size=0.0001, linetype = "dashed"),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill="white"),
    # Change axis line
    axis.line = element_line(colour = "grey"),
    axis.ticks = element_line(colour = "grey"),
    axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
    axis.title.x = element_text(margin = margin(t =10, r = 0, b = 0, l = 0))
  )
pb4corr3


# 2. Relación entre producto y consumo de electricidad per cápita.
# En esta sección se corrige la Figura 4.


# Código para Figura 4 (hecho en clase).

dfs <- subset(df,Country %in% c("Germany","India","China","United States", "Japan", "United Kingdom"))
var1<-"Electricity_consumption_per_capita"
var2<-"gdp_per_capita"
name1<- "Electricity"
name2<- "GDP"
# Change color and shape of points
p1<- ggplot(dfs,aes_string(x=var1,y=var2))+
  geom_point(color=2,shape=2)+xlim(0,10000)+xlab(name1)+ylab(name2)
p1
#Grouping points by a variable mapped to colour and shape
p2 <- ggplot(dfs,aes_string(x=var1,y=var2))+
  geom_point(aes(color=Country,shape=Country), show.legend = FALSE)+xlim(0,10000)+xlab(name1)+ylab(name2)
grid.arrange(p1, p2, nrow = 2)
p2


# Código para Figura 5.

# Corregimos la Figura 4 siguiendo los consejos vistos en clase. 
# En el gráfico original las leyendas se situaban al costado derecho del gráfico,
# nosotros preferimos incluirlas dentro del mismo.

p2corr = p2 +
  geom_text(x=8000, y=45000, label="Alemania", colour="olivedrab", size = 3.5) + 
  geom_text(x=9000, y=22500, label="Estados Unidos", colour="magenta1", size = 3.5) + 
  geom_text(x=3800, y=9900, label="China", colour="indianred2", size = 3.5) + 
  geom_text(x=800, y=7000, label="India", colour="green4", size = 3.5) + 
  geom_text(x=4500, y=36000, label="Reino Unido", colour="steelblue3", size = 3.5) +
  geom_text(x=9100, y=35200, label="Japón", colour="turquoise3", size = 3.5) +
  theme_minimal() +
  theme(
    panel.grid.major = element_blank(),
    panel.border = element_blank(),
    panel.grid.minor = element_blank(),
    # Change axis line
    axis.line = element_line(colour = "grey")
  ) +
  scale_y_continuous(breaks = seq(0,50000, 10000)) +
  theme(
    text = element_text(family = "Times New Roman", size=12),
    # Hide panel borders and remove grid lines
    panel.border = element_rect(colour = "grey", fill = NA),
    panel.grid.major = element_line(colour = "#E5E7E9", size=0.0001, linetype = "dashed"),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill="white"),
    # Change axis line
    axis.line = element_line(colour = "grey"),
    axis.ticks = element_line(colour = "grey"),
    axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
    axis.title.x = element_text(margin = margin(t =10, r = 0, b = 0, l = 0))
  )

p2corr


# 3. Relación entre cantidad de asaltos y precipitaciones.
# En esta sección se corrige la Figura 6.

# Código para Figura 6 (realizado para Tarea 3).

# Abrimos base espacial 
library(sf)
base = st_read("basefinal_geo.shp")
names(base)
summary(base)

graf_anter = ggplot(base, aes(x=prec_mn, y=Asslt_p, color=Condado)) +
  geom_point() + geom_smooth(method=lm, se=FALSE, fullrange=FALSE) + 
  xlab("Precipitaciones Promedio Mensual") + ylab("Asaltos PC Promedio Mensual")
graf_anter

# Código para Figura 7.

# Creamos la base nueva con la variable correlacion por condado entre asalto pc y precipitaciones mensuales
base2 = st_drop_geometry(base) %>% 
  group_by(county) %>% 
  summarise(
    coef_corr = cor(prec_mn, Asslt_p)
  )
names(base2)

# Pegamos la nueva variable a la base original
base = left_join(base, base2, by ="county")
summary(base$coef_corr)

# Eliminamos NA
base3 = subset(base, is.na(coef_corr)==F)
# Creamos etiquetas
base3$'Condado (Coef Corr)' = paste0(base3$county, " (",round(base3$coef_corr,2), ")")
table(base3$`Condado (Coef Corr)`)

# Figura 7.
graf_desp = ggplot(base3, aes(x=prec_mn, y=Asslt_p, color=`Condado (Coef Corr)`, shape =`Condado (Coef Corr)` )) +
  geom_point() +  
  geom_smooth(method=lm, se=FALSE, fullrange=FALSE) + 
  xlab("Precipitaciones Promedio Mensual") + ylab("Asaltos PC Promedio Mensual") +
  scale_shape_manual(values=rep(c(0,1,2,5), 5))
graf_desp

# Código para Figura 8

# Variable cada 1000 habitantes
base3$asalto_1000 = base3$Asslt_p*1000

graf_desp2 = ggplot(base3, aes(x=prec_mn, y=asalto_1000, color=`Condado (Coef Corr)`)) +
  geom_point(shape=16,show.legend = F) +  
  geom_smooth(method=lm, se=FALSE, fullrange=FALSE, show.legend = F) + 
  xlab("Precipitaciones Promedio Mensual") + ylab("Asaltos Promedio Mensual (c/1.000 hab)") +
  facet_wrap(`Condado (Coef Corr)` ~ .) + 
  theme(
    text = element_text(family = "Times New Roman", size=12),
    # Hide panel borders and remove grid lines
    panel.border = element_rect(colour = "grey", fill = NA),
    panel.grid.major = element_line(colour = "#E5E7E9", size=0.0001, linetype = "dashed"),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill="white"),
    # Change axis line
    axis.line = element_line(colour = "grey"),
    axis.ticks = element_line(colour = "grey"),
    axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
    axis.title.x = element_text(margin = margin(t = 10, r = 0, b = 0, l = 0))
  )
graf_desp2

# Código para Figura 9

## Creamos la base nueva
base2 = st_drop_geometry(base) %>% 
  group_by(county) %>% 
  summarise(
    coef_corr = as.numeric(cor(prec_mn, Asslt_p))
  )

## Creamos el gráfico. 

graf_nuevo = ggplot(base2, aes(x=coef_corr)) +
  geom_area(stat = "density", alpha = 0, colour = "black", fill="gray1", size = 1.2) + 
  xlab("Coeficiente de correlación") + ylab("Cantidad") + 
  geom_segment(data=base2, aes(x = mean(base2$coef_corr, na.rm = TRUE) , y = 0, xend = mean(base2$coef_corr, na.rm = TRUE), yend=1.55), linetype="dashed", size = 2, colour = "red4") +
  geom_text(x=-0.15, y=1.65, label="Media = -0.03", colour="red4", size = 5, family = "Times New Roman", size=12) +
  theme(
    text = element_text(family = "Times New Roman", size=12),
    # Hide panel borders and remove grid lines
    panel.border = element_rect(colour = "grey", fill = NA),
    panel.grid.major = element_line(colour = "#E5E7E9", size=0.0001, linetype = "dashed"),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill="white"),
    # Change axis line
    axis.line = element_line(colour = "grey"),
    axis.ticks = element_line(colour = "grey"),
    axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
    axis.title.x = element_text(margin = margin(t =10, r = 0, b = 0, l = 0))
  )

graf_nuevo
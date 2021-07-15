/************************************************************************************

Tarea 4 - Bullano y García Zavaleta - Mapa de crímenes cada mil habitantes.
************************************************************************************/

* Seteamos el directorio de trabajo.
	
global DATA = "C:\Users\Gaston\Desktop\Herramientas computacionales\Clase 4 - Data Visualization\Scripts mapas\videos 2 y 3\data" 
cd "$DATA"

* Instalamos los paquetes necesarios.

*ssc install spmap
*ssc install shp2dta
*net install spwmatrix, from(http://fmwww.bc.edu/RePEc/bocode/s)



* Importamos el archivo shape.

shp2dta using london_sport.shp, database(ls) coord(coord_ls) genc(c) genid(id) replace

use ls, clear
describe

use coord_ls, clear
describe

* Importamos y transformamos los datos de Excel a formato Stata
import delimited "$DATA/mps-recordedcrime-borough.csv", clear 

* De todos los crímenes nos quedamos solo con robos y hurtos para hacer el mismo mapa que hicimos en R.

keep if crimetype == "Theft & Handling"

* En Stata necesitamos que la variable tenga el mismo nombre en ambas bases para hacer el merge
rename borough name
* preserve
collapse (sum) crimecount, by(name)
save "crime.dta", replace

describe

* Unimos las bases

use ls, clear
merge 1:1 name using crime.dta
*merge 1:1 name using crime.dta, keep(3) nogen
*keep if _m==3
drop _m

save london_crime_shp.dta, replace

************************************************************************************

use london_crime_shp.dta, clear

* Generamos la cantidad de crímenes cada mil habitantes.

gen crimenescadamil = crimecount/Pop_2001 * 1000


* Mapa de crímenes cada 1000 habitantes.
graph set window fontface "Times New Roman"

* Cambiamos el formato de la variable para que en el mapa las etiquetas no contengas decimales.
format (crimenescadamil) %12.0f

* Hacemos el mapa.
spmap crimenescadamil using coord_ls, id(id) line(data(coord_ls) size(0.1) color(white)) label(label(crimenescadamil) xcoord(x_c) ycoord(y_c) size(vsmall)) clmethod(q) cln(6) title("Robos cada mil habitantes según distrito en Londres") legend(size(small) position(5) xoffset(15.05)) fcolor(Heat) plotregion(margin(b+15)) ndfcolor(white) name(g2,replace)  


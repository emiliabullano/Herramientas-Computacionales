#########################################################################################
####################                    Modelo 4B                    ####################
#########################################################################################

"""
Model exported as python.
Name : modelo4b
Group : 
With QGIS : 31415
"""


#########################################################################################
###                   Importamos las funciones que vamos a necesitar                  ###
#########################################################################################
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing
#########################################################################################

class Modelo4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_distance_joined', 'centroids_nearest_coast_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_with_coordinates', 'centroids_with_coordinates', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}

        

#########################################################################################
###                      Computamos el centroide de cada polígono                     ###
#########################################################################################
# Lo hacemos sobre la capa countries (después de haber arreglado su geometría).
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': 'Geometrías_corregidas_a59af566_3211_4476_b187_cae895e03ab0',
            'OUTPUT': parameters['Country_centroids']
        }
        outputs['CentroidesCountry'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['CentroidesCountry']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
#########################################################################################


        
#########################################################################################
###                   Corregimos la variable cat de la capa 'nearout'                 ###
#########################################################################################
# Creamos una nueva variable cuyo valor es igual al original - 1. 
# Esto será útil para posteriormente realizar un merge con la capa 'distout'.
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'attribute($currentfeature, \'cat\')-1',
            'INPUT': 'from_output_32e5acd3_185e_4fa8_a6b8_48c2b93abebc',
            'NEW_FIELD': False,
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['CalculadoraDeCamposCatAdjust'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['CalculadoraDeCamposCatAdjust']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                                   Quitamos campos                                 ###
#########################################################################################
# Borramos los campos que no vamos a necesitar de la capa 'added_field_coast_lon'.
# Exportamos la base resultante en formato como 'dist_coast.csv'.
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculado_10c3704b_2ea3_408f_8f49_c38ac859ed4b',
            'OUTPUT': 'E:/Desktop/Emilia/Maestria UdeSA/Herramientas Computacionales/Python y QGIS/dist_coast.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                                   Quitamos campos                                 ###
#########################################################################################
# Quitamos los campos ycoord y xcoord de la base nearest_cat_adjust'.

        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculado_519ee7a1_13e5_4748_8035_33157fe23239',
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['QuitarCamposNearest_cat_adjust'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['QuitarCamposNearest_cat_adjust']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###               Creamos un campo igual a 'Xcoord' llamado 'coast_lon'               ###
#########################################################################################
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'xcoord\')',
            'INPUT': 'Calculado_368e3989_f49f_43ff_b799_164932707462',
            'NEW_FIELD': True,
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['CalculadoraDeCamposCoast_lon'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['CalculadoraDeCamposCoast_lon']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                             Corregimos las geometrías                             ###
#########################################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.
# En este bloque se corrigen las geometrías de la capa 'ne_10m_admin_0_countries.shp'.
        alg_params = {
            'INPUT': 'E:/Desktop/Emilia/Maestria UdeSA/Herramientas Computacionales/Python y QGIS/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['CorregirGeometrasCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['CorregirGeometrasCountries']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                                 Extraemos vértices                                ###
#########################################################################################
        alg_params = {
            'INPUT': 'Capa_unida_79075691_4a1f_4f07_bf65_9aa27245e9b6',
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtraerVrtices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtraerVrtices']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                                   Quitamos campos                                 ###
#########################################################################################
# Quitamos campos de la capa 'added_field_cent_lon'.

        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': 'Calculado_10c3704b_2ea3_408f_8f49_c38ac859ed4b',
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['QuitarCamposCent_lon'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['QuitarCamposCent_lon']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                Creamos un campo igual a 'ycoord' llamado coast_lat                ###
#########################################################################################
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'ycoord\')',
            'INPUT': 'Información_de_geometría_añadida_0294edb2_4e6a_4620_a64e_7145ce159e91',
            'NEW_FIELD': True,
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['CalculadoraDeCamposCoastLat'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['CalculadoraDeCamposCoastLat']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
#########################################################################################

        

#########################################################################################
###                            Extraemos campos por atributo                          ###
#########################################################################################
# De la capa 'extract_vertices' extraemos aquellas observaciones para las cuales la distancia es >0.
        alg_params = {
            'FIELD': 'distance',
            'INPUT': 'Vértices_8aa2d582_002d_4d89_9a90_3a16214ceaf4',
            'OPERATOR': 2,
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtraerPorAtributo'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtraerPorAtributo']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}
#########################################################################################        
        

    
#########################################################################################
###                                   Quitamos campos                                 ###
#########################################################################################
# Quitamos campos que no vamos a necesitar de la base 'Centroids_nearest_coast_joined'.
        alg_params = {
            'COLUMN': ['ADMIN_2','ISO_A3_2'],
            'INPUT': 'Capa_unida_0c2c3aef_80e6_44d8_a7c3_478fcd86a3c6',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['QuitarCamposCentroid_coast_joined'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['QuitarCamposCentroid_coast_joined']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}
#########################################################################################


        
#########################################################################################
###                  Unimos las capas 'centroidsout' y 'nearest_cat_adjust'           ###
#########################################################################################
# Usamos la variable 'ISO_A3' para la unión.
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': 'Campos_restantes_e492d4b3_703d_4d8a_8291_0116695de997',
            'INPUT_2': 'Campos_restantes_621d7b2b_5412_4332_a2a0_a2fe5086d67a',
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['UnirAtributosPorValorDeCampoCentroidsYCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['UnirAtributosPorValorDeCampoCentroidsYCoast']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
#########################################################################################

        
        
#########################################################################################
###                   Computamos las coordenadas de los centroides                    ###
#########################################################################################
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': 'Centroides_53b940af_f546_4b23_bacf_9eefdddec7bc',
            'OUTPUT': parameters['Centroids_with_coordinates']
        }
        outputs['AgregarAtributosDeGeometra'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_with_coordinates'] = outputs['AgregarAtributosDeGeometra']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                             Corregimos las geometrías                             ###
#########################################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.
# En este bloque se corrigen las geometrías de la capa 'coastline.shp'.
        alg_params = {
            'INPUT': 'E:/Desktop/Emilia/Maestria UdeSA/Herramientas Computacionales/Python y QGIS/ne_10m_coastline/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['CorregirGeometrasCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['CorregirGeometrasCoast']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                Creamos un campo igual a 'xcoord' llamado cent_lon                 ###
#########################################################################################
# Renombramos la longitud del centroide.
# Después tenemos que eliminar la variable original.
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'xcoord\')',
            'INPUT': 'Calculado_916641b4_01c7_488e_9563_5948d476e58a',
            'NEW_FIELD': True,
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['CalculadoraDeCamposLonDelCentroide'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['CalculadoraDeCamposLonDelCentroide']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}
#########################################################################################
        

#########################################################################################
###                   Unimos campos según valor de la variable 'cat'                  ###
#########################################################################################
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': 'output_61481424_8cfe_4d1c_bb67_2e92bf6e23bb',
            'INPUT_2': 'Campos_restantes_ecee40de_f1dc_4964_bae4_7c01e1876391',
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_distance_joined']
        }
        outputs['UnirAtributosPorValorDeCampoByCat'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_joined'] = outputs['UnirAtributosPorValorDeCampoByCat']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###        Calculamos la distancia desde cada centroide a la costa más cercana        ###
#########################################################################################
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': 'Campos_restantes_e492d4b3_703d_4d8a_8291_0116695de997',
            'from_type': [0,1,3],
            'to': 'Campos_restantes_0fb3e549_c179_493b_a462_d4be8ec4ff3d',
            'to_column': '',
            'to_type': [0,1,3],
            'upload': [0],
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                Creamos un campo igual a 'ycoord' llamado cent_lat                 ###
#########################################################################################
# Renombramos la longitud del centroide.
# Después tenemos que eliminar la variable 'ycoord'.
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cen_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'ycoord\')',
            'INPUT': 'Extraído__atributo__bc255aa3_f8b6_4d2e_952f_09fde1b041dc',
            'NEW_FIELD': True,
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['CalculadoraDeCamposlatDelCentroide'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['CalculadoraDeCamposlatDelCentroide']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                          Agregamos atributos de geometría                         ###
#########################################################################################
# Calculamos las coordenadas del punto de la costa más cercano a cada centroide.
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': 'Campos_restantes_0e3ec8cc_e927_44c1_8b5d_8b0da749c917',
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AgregarAtributosDeGeometra'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AgregarAtributosDeGeometra']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}
#########################################################################################
        
    
    
#########################################################################################
###                                   Quitamos campos                                 ###
#########################################################################################
# Quitamos algunos campos de la base 'fix_geo_coast' que no vamos a necesitar.

        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': 'Geometrías_corregidas_292f80e0_2a25_47f5_92a4_f4236bc6af25',
            'OUTPUT': parameters['Coastout']
        }
        outputs['QuitarCamposCoast'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['QuitarCamposCoast']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                                   Quitamos campos                                 ###
#########################################################################################
# Quitamos campos de la capa 'centroids_w_coord' y nos quedamos solo con los que necesitamos.

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': 'Información_de_geometría_añadida_a7150d8f_443a_4b7b_b8d5_b5594f8de677',
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['QuitarCamposCentroid_w_c'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['QuitarCamposCentroid_w_c']['OUTPUT']
        return results
#########################################################################################


    def name(self):
        return 'modelo4b'

    def displayName(self):
        return 'modelo4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4b()

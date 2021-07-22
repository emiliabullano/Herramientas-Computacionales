#########################################################################################
####################                    Modelo 4C                    ####################
#########################################################################################


"""
Model exported as python.
Name : modelo4c
Group : 
With QGIS : 31608
"""



#########################################################################################
###                   Importamos las funciones que vamos a necesitar                  ###
#########################################################################################
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing
#########################################################################################

class Modelo4c(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Areas_out', 'areas_out', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_fixgeo', 'countries_fixgeo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_reprojected', 'countries_reprojected', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_drop_fields', 'countries_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        
#########################################################################################
###                    Quitamos las variables que no vamos a usar                     ###                        
#########################################################################################
# Se eliminan las variables en 'COLUMN' de la capa en 'INPUT'. Capa resultado en 'OUTPUT'
        
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9','ADMIN_2','ISO_A3_2'],
            'INPUT': 'ne_10m_admin_0_countries_b187319e_0c2e_47d8_befc_5386205d0a18',
            'OUTPUT': parameters['Countries_drop_fields']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_drop_fields'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
#########################################################################################
        
        
#########################################################################################
###                   Guardamos la base creada en formato .csv                      #####
#########################################################################################
# Se guarda el archivo remanente ('INPUT') en formato .csv (pueden ser otros)              
# Se asigna la ruta y el nombre en 'OUTPUT
        
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Calculado_ae193de0_7e8c_4d83_98c9_651bf78431ad',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/Gaston/Desktop/Herramientas computacionales/Clase 5 - PyQGIS/csvfinal/modelo4c/areas.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
        
#########################################################################################
        
        
        
#########################################################################################
###               Calculamos el area de cada poligono ('km2_area')                  #####
#########################################################################################
# nombre de la nueva variable en 'FIELD_NAME'
# Capa sobre la cual realizar la variable en 'INPUT'
# Capa resultado en 'OUTPUT'

        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'km2area',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'area($geometry)/1000000',
            'INPUT': 'Geometrías_corregidas_d34ed773_ab88_44c8_96e9_da203ea34dba',
            'OUTPUT': parameters['Areas_out']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Areas_out'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
#########################################################################################
        
        
        
#########################################################################################
###                             Corregimos las geometrías                             ###
#########################################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.
        
        alg_params = {
            'INPUT': 'Reproyectada_37e62b09_6b71_4457_a133_d4d68de8d39c',
            'OUTPUT': parameters['Countries_fixgeo']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_fixgeo'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
#########################################################################################

        
    
#########################################################################################
###                             Reproyectar capa                                      ###
#########################################################################################
# Sistema de coordenadas ESRI:54034- ('SOURCE_CRS')

        alg_params = {
            'INPUT': 'Campos_restantes_7ea0d45c_10b0_47ac_8cf1_79ecfc819704',
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'),
            'OUTPUT': parameters['Countries_reprojected']
        }
        outputs['ReproyectarCapa'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_reprojected'] = outputs['ReproyectarCapa']['OUTPUT']
        return results
#########################################################################################
    
    def name(self):
        return 'modelo4c'

    def displayName(self):
        return 'modelo4c'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4c()

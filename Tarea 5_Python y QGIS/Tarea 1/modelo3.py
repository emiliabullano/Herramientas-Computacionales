"""
Model exported as python.
Name : modelo3
Group : 
With QGIS : 31608
"""
############################################################################
############################ MODELO 3 ######################################
############################################################################


############################################################################
###        SE IMPORTAN LOS PAQUETES PARA TRABAJAR QGIS                   ###
############################################################################
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo3(QgsProcessingAlgorithm):
############################################################################
###         SE ABREN LAS BASES DE DATOS QUE VAMOS A UTILIZAR             ###
############################################################################
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonalstatistics', 'zonalstatistics', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}
############################################################################


############################################################################
###     Calculamos la media de la variable "Pop_2000" por polígono       ###
############################################################################
        alg_params = {
            'COLUMN_PREFIX': 'pop2000',
            'INPUT': 'Estadistica_zonal_ff4bfe49_f056_4b0e_9976_a611b5cdb857',
            'INPUT_RASTER': 'popc_2000AD_d2728e7c_0d54_40e6_8183_876141273935',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Zonalstatistics']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonalstatistics'] = outputs['EstadsticasDeZona']['OUTPUT']
############################################################################


        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}


############################################################################
###                      Corregimos las geometrías                       ###
############################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.
         
        alg_params = {
            'INPUT': 'ne_10m_admin_0_countries_34521fae_600f_4aef_9554_c58dc6a7e5e8',
            'OUTPUT': parameters['Fixgeo_3']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_3'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
############################################################################.



############################################################################
###                            Quitamos campos                           ###
############################################################################
# Quitamos las variables que se encuentran en la lista "COLUMN".

        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': 'Geometrías_corregidas_ec648295_2044_4162_8291_219861eb6d30',
            'OUTPUT': parameters['Drop_fields_3']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
############################################################################



############################################################################
###                Guardamos la base creada en formato csv               ###
############################################################################
# Se guarda el archivo remanente ('INPUT') en formato .csv (pueden ser otros)              
# Se asigna la ruta y el nombre en 'OUTPUT
        
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Estadistica_zonal_66b5342a_02c6_4265_a0a0_89fd8c6f5eb1',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/Gaston/Desktop/Herramientas computacionales/Clase 5 - PyQGIS/csvfinal/modelo3/raster_stats.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
############################################################################



############################################################################
###    Calculamos la media de la variable "Landquality" por polígono     ###
############################################################################
        
        alg_params = {
            'COLUMN_PREFIX': 'landq',
            'INPUT': 'Campos_restantes_73f813be_a40d_49ae_8fa8_5c5f5b9bb19e',
            'INPUT_RASTER': 'landquality_051403b4_0391_4eda_91fc_9bbe39001c6b',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Landq']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
        
############################################################################
###     Calculamos la media de la variable "Pop_1800" por polígono       ###
############################################################################

        alg_params = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': 'Estadistica_zonal_c8e53903_5dc2_46f3_9559_589dd94adebd',
            'INPUT_RASTER': 'popc_1800AD_c7002d74_ce64_4e0f_9bfa_8df05283638c',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop1800']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
        
############################################################################
###     Calculamos la media de la variable "Pop_1900" por polígono       ###
############################################################################

        alg_params = {
            'COLUMN_PREFIX': 'pop1900',
            'INPUT': 'Estadistica_zonal_d0aae37f_2f32_4937_87d2_f50779dc982b',
            'INPUT_RASTER': 'popc_1900AD_ebdafec7_7bc7_4acc_97ae_e042667168ef',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop1900']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['EstadsticasDeZona']['OUTPUT']
        return results
############################################################################


    def name(self):
        return 'modelo3'

    def displayName(self):
        return 'modelo3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo3()

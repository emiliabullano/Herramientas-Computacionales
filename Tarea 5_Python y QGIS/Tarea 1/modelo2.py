##########################################################################################
################################          MODELO 2         ###############################
##########################################################################################

"""
Model exported as python.
Name : modelo2
Group : 
With QGIS : 31608
"""


#########################################################################################
###                   Importamos las funciones que vamos a necesitar                  ###
#########################################################################################
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing
#########################################################################################


# ABRIMOS EL RASTER 
class Modelo2(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}
        

#########################################################################################
###                    Usamos la función combar(reproyectar) capa                     ###
#########################################################################################
# Reproyectamos a WGS84 - Sistema de coordenadas EPSG_4326- ('SOURCE_CRS')
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': 'suit_85bf5e89_2390_4ddc_9e10_fc448aae89f7',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_CRS': None,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        outputs['CombarReproyectar'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['CombarReproyectar']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
#########################################################################################


#########################################################################################
###                              Extraemos la proyección                              ###
#########################################################################################
        alg_params = {
            'INPUT': outputs['CombarReproyectar']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        outputs['ExtraerProyeccin'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results
#########################################################################################


    def name(self):
        return 'modelo2'

    def displayName(self):
        return 'modelo2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo2()

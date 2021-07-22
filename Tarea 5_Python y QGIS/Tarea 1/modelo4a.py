##########################################################################################
##################                      MODELO 4A                       ##################
##########################################################################################


"""
Model exported as python.
Name : modelo4a
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
import processing
#########################################################################################


class Modelo4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        
#########################################################################################
###                             Corregimos las geometrías                             ###
#########################################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.
# En este bloque se corrigen las geometrías de la base clean.shp, creada en el modelo 1.
        alg_params = {
            'INPUT': 'clean_1e98a9a0_d52b_4791_a02d_53e356ed3b6b',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['CorregirGeometrasWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['CorregirGeometrasWlds']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###              Calculamos la media de la variable "ADMIN" por polígono              ###
#########################################################################################
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersección_c8ba2631_67f6_48a3_ad27_90c4bb803bcb',
            'OUTPUT': 'C:/Users/Gaston/Desktop/Herramientas computacionales/Clase 5 - PyQGIS/csvfinal/modelo4a/languagesbycountry.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EstadsticasPorCategoras'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                             Corregimos las geometrías                             ###
#########################################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.
# En este bloque se corrigen las geometrías de la base ne.10m.admin.0.countries.shp
        alg_params = {
            'INPUT': 'ne_10m_admin_0_countries_ed83962c_4da8_4d95_bf84_dd5271df5d0f',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['CorregirGeometrasCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['CorregirGeometrasCountries']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        
#########################################################################################
###                      Hacemos la intersección entre dos capas                      ###
#########################################################################################
# Después de haber corregido las geometrías, intersectamos las capas ne.10m.admin.0.countries.shp
# y clean.shp y nos quedamos las variables GID y ADMIN.
        
        alg_params = {
            'INPUT': outputs['CorregirGeometrasWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['CorregirGeometrasCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Interseccin'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Interseccin']['OUTPUT']
        return results
#########################################################################################


    def name(self):
        return 'modelo4a'

    def displayName(self):
        return 'modelo4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4a()

#########################################################################################
####################                    Modelo 1                     ####################
#########################################################################################

"""
Model exported as python.
Name : modelo1
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

class Modelo1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Geometrias_corr_inc', 'geometrias_corr_inc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Geometras_corr', 'geometrías_corr', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}

#########################################################################################
###                    Quitamos las variables que no vamos a usar                     ###                        
#########################################################################################
# Se eliminan las variables en 'COLUMN' de la capa en 'INPUT'. Capa resultado en 'OUTPUT'

        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculado_b253be02_a6d5_446c_83f2_33ece48b0318',
            'OUTPUT': parameters['Wldsout']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                             Corregimos las geometrías                             ###
#########################################################################################
# Es importante realizar este paso para evitar problemas como polígonos que se superponen
# o polígonos que no están cerrados.

        alg_params = {
            'INPUT': 'langa_4c55e7a9_ca84_4b17_b41c_8dd16e06f57b',
            'OUTPUT': parameters['Geometras_corr']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Geometras_corr'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###                         Guardamos la base creada como shp                         ###
#########################################################################################
# La ruta donde se guarda en 'OUTPUT' y la capa a guardar es 'INPUT'
# Se pueden configurar con otras extensiones (csv, shp, gpkg, entre otras)

alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Campos_restantes_13ab7cca_e998_4e86_a240_0f32f7c50773',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/Gaston/Desktop/Herramientas computacionales/Clase 5 - PyQGIS/shapesfinales/clean.shp',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###   Nos quedamos con las observaciones cuyo nombre tiene menos de 11 caracteres     ###
#########################################################################################
        alg_params = {
            'INPUT': 'Calculado_145a32e9_d777_42e2_93f6_a9094f26ed8f',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FiltroDeEntidad'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FiltroDeEntidad']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###   Calculamos la cantidad de caracteres de la variable "NAME_PROP" para cada obs   ###
###   A la variable que contiene el resultado de este cálculo la llamamos "length"    ###
#########################################################################################
# nombre de la nueva variable 'FIELD_NAME'
# Capa sobre la cual realizar la variable 'INPUT'
# Capa resultado ''OUTPUT
    
    alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incrementado_a856cd77_188b_4509_9ed2_62354efaa16a',
            'OUTPUT': parameters['Length']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###           Clonamos la variable "OUTPUT_menor_a_11" y la llamamos "lmn"            ###
#########################################################################################
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lmn',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': 'NAME_PROP',
            'INPUT': 'menor_a_11_c5aae02a_5a20_4a5b_b510_74ac4c4278d9',
            'OUTPUT': parameters['Field_calc']
        }
        outputs['FieldCalculatorClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['FieldCalculatorClone']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
#########################################################################################



#########################################################################################
###     Creamos un campo de nombre "GID" que se autoincrementa (para numerar obs)     ###
#########################################################################################
# Valor sobre el cual empieza a autoincrementarse 'START'

    alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': 'Geometrías_corregidas_3d10f768_e0d9_422f_8a5f_249e111de595',
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Geometrias_corr_inc']
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Geometrias_corr_inc'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']
        return results
#########################################################################################


    def name(self):
        return 'modelo1'

    def displayName(self):
        return 'modelo1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo1()

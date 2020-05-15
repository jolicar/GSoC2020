# encoding: utf-8

from gvsig import *

from gvsig.commonsdialog import *

from gvsig.libs.toolbox import *

from areaUtils import copyDataFilterByArea, createLayerFilterByArea


class skillGSoC2020(ToolboxProcess):
  
  def defineCharacteristics(self):
    """
En esta operacion debemos definir los parametros de netrada y salida que va a precisar nuetro proceso.
    """
    # Fijamos el nombre con el que se va a mostrar nuestro proceso
    self.setName("Ejercicio skill GSoC 2020")
    
    # Indicamos el grupo en el que aparecera
    self.setGroup("Vectorial")
        
    params = self.getParameters()
    # Indicamos que precisamos un parametro LAYER, del tipo punto y que es obligatorio
    params.addInputVectorLayer("LAYER","Capa de entrada", SHAPE_TYPE_POLYGON,True)
    # Indicamos que precisamos un valor numericos, area umbral 
    params.addNumericalValue("area", "Area_umbral",0, NUMERICAL_VALUE_DOUBLE)
    
    # Y por ultimo indicamos que precisaremos una capa de salida de puntos.
    self.addOutputVectorLayer("RESULT_POLYGON", "New_Layer_Polygon", SHAPE_TYPE_POLYGON)

  def processAlgorithm(self):
    """
Esta operacion es la encargada de realizar nuetro proceso.
    """
    try:
      """
      Recogemos los parametros y creamos el conjunto de entidades asociadas a la capa
      de entrada.
      """
      params = self.getParameters()
      sourceLayer = params.getParameterValueAsVectorLayer("LAYER")
      minArea = params.getParameterValueAsDouble("area")

      targetStore = self.buildOutPutStore(
        sourceLayer.getDefaultFeatureType(), 
        SHAPE_TYPE_POLYGON,
        "New_Layer_Polygon",
        "RESULT_POLYGON"
      )
      
      sourceStore = sourceLayer.getFeatureStore()
      #copyDataFilterByArea(minArea,sourceStore,targetStore)

      """
      Nos recorremos todas las entidades de entrada, y las evaluamos con respecto al area umbral
      """
      
      features=sourceStore.getFeatures()
      self.setRangeOfValues(0,features.getSize())
      targetStore.edit()
      
      for feature in features.iterator():
        if self.isCanceled():
          # Si el usuario indico que quiere cancelar el proceso abortamos.
          print "Proceso cancelado"
          break
        
        # Incrementamos el progreso de nuestro proceso.
        self.next()
        if (feature.geometry().area()>minArea):
            newFeature=targetStore.createNewFeature(feature)
            targetStore.insert(newFeature)
      targetStore.finishEditing()

    finally:
      print "Proceso terminado %s" % self.getCommandLineName() 
      return True
    

def main(*args):
    # Creamos nuesto geoproceso
    process = skillGSoC2020()
    # Lo registramos entre los procesos disponibles en el grupo de "Scripting"
    process.selfregister("Scripting")
    # Actualizamos el interface de usuario de la Toolbox
    process.updateToolbox()
    msgbox("Incorporado el script '%s/%s/%s' a la paleta de geoprocesos." % (
        "Scripting",
        process.getGroup(),
        process.getName()
      )
    )

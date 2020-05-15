# encoding: utf-8

import gvsig
from gvsig import geom

def areaTotal(layer):
    features=layer.features()
    at=0
    for i in features:
        at+= i.geometry().area()
    return at

def copyLayerFilterByArea(minArea,sourceLayer):

    targetLayer=createLayerFilterByArea(sourceLayer)
    targetStore=targetLayer.getFeatureStore()
    sourceStore=sourceLayer.getFeatureStore()

    copyDataFilterByArea(minArea,sourceStore,targetStore)
    return targetLayer

def createLayerFilterByArea(sourceLayer):
    sourceSchema=sourceLayer.getSchema()
    targetSchema=gvsig.createFeatureType(sourceSchema)
    targetLayer=gvsig.createShape(targetSchema, prefixname="new_layer")

    return targetLayer

def copyDataFilterByArea(minArea,sourceStore,targetStore):
    targetStore.edit()
    features=sourceStore.getFeatures()
    for feature in features:
        if (feature.geometry().area()>minArea):
            newFeature=targetStore.createNewFeature(feature)
            targetStore.insert(newFeature)
    targetStore.finishEditing()

def main(*args):
    layer=gvsig.currentLayer()
    p=500000000
    print areaTotal(layer)
    gvsig.currentView().addLayer(copyLayerFilterByArea(p,layer))
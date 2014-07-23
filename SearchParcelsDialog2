# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SearchParcels2Dialog
                                 A QGIS plugin
 This plugin searches parcels in cadastral map


                             -------------------
        begin                : 2014-05-30
        copyright            : (C) 2014 by Nicola Pezzotta and Paola Marinelli
        email                : nico.pezzotta@gmail.com


 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui_searchparcels2 import Ui_SearchParcels2
# create the dialog for zoom to point

class SearchParcels2Dialog(QtGui.QDialog, Ui_SearchParcels2):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        QObject.connect(self.uptadeButton, SIGNAL("clicked()"), self.chooseLayer)
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(QString)"), self.chooseField)
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(QString)"), self.chooseField2)
        QObject.connect(self.selectBox, SIGNAL("stateChanged(int)"), self.OnSelectBoxClicked)
        QObject.connect(self.cancelButton, SIGNAL("clicked()"), self.cancelSearch)
        QObject.connect(self.goButton, SIGNAL("clicked()"), self.search) 
        
        self.chooseLayer()

    # in first comboBox show the list of layers (list of names)
    def chooseLayer(self): 
        layerList = []     # crea una lista vuota
        self.comboBox.clear()     # svuota la lista del combo box
        layerList = self.getLayerNames()     # a layerList assegna il risultato della procedura getLayerNames()
        self.comboBox.addItems(layerList)
        self.FoglioLine.clear()
        self.ParticelLine.clear()
        self.OnSelectBoxClicked()
        return

    # Get the list of layers (list of names) in QgsMapLayerRegistry
    def getLayerNames(self):
        layermap = QgsMapLayerRegistry.instance().mapLayers()   # assegna a layermap l'insieme dei layers caricati
        layerLst = []
        for i, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:    # considera solo i layers vettoriali
                layerLst.append( unicode( layer.name() ) )   # prende il nome di ogni layer a lo aggiunge alla lista layerLst
        return layerLst

    # in second comboBox show the list fields (list of names)
    def chooseField(self):
        fieldList = []
        self.campo1.clear()
        fieldList = self.getFieldNames()
        self.campo1.addItems( fieldList )
        return

    # Get the list fields (list of names) for the selected layer
    def getFieldNames(self):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        fieldLst = []
        for i, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == self.comboBox.currentText():
                if layer.isValid():
                    fields = layer.dataProvider().fields()
                    for i in range(fields.count()):
                        field = fields[i]
                        fieldLst.append(field.name())
        return fieldLst

    # in third comboBox show the list fields (list of names)
    def chooseField2(self):
        fieldList = []
        self.campo2.clear()
        fieldList = self.getFieldNames()
        self.campo2.addItems( fieldList )
        return

    def OnSelectBoxClicked(self):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for i, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == self.comboBox.currentText():
                if layer.isValid():
                    if not self.selectBox.isChecked():
                        self.panBox.setEnabled(False)
                        self.scaleBox.setEnabled(False)
                    else:
                        self.panBox.setEnabled(layer.hasGeometryType())
                        self.scaleBox.setEnabled(layer.hasGeometryType())
        return

    def cancelSearch(self):
        self.close()
        return

    def search(self):
        i = self.comboBox.currentIndex()
        if i < 0:
            return None
        layerId = self.comboBox.itemData(i)
        layer = QgsMapLayerRegistry.instance().mapLayer(layerId)
#        layer = self.getLayer()
        if layer is None:
            return
        toFind = self.FoglioLine.text()
        toFind2 = self.ParticelLine.text()
        f = QgsFeature()
        results = []
        fieldIndex = self.campo1.currentIndex()
        fieldName = self.campo1.itemData(fieldIndex)
        fieldIndex2 = self.campo2.currentIndex()
        fieldName2 = self.campo2.itemData(fieldIndex2)
        if fieldName == "" or fieldName2 == "":
            QMessageBox
            msgBox.setText("Search Parcels 2: Seleziona un campo.")
            msgBox.exec_()
            return
        try:
            float(toFind)
        except ValueError:
            QMessageBox
            msgBox.setText("Search Parcels 2: Inserisci un valore numerico.")
            msgBox.exec_()
            return
        try:
            float(toFind2)
        except ValueError:
            QMessageBox
            msgBox.setText("Search Parcels 2: Inserisci un valore numerico.")
            msgBox.exec_()
            return
        # show progress bar
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(layer.featureCount())
        self.progressBar.setValue(0)
        self.widget_2.show()
        # disable rest of UI
        self.layerWidgetGroup.setEnabled(False)
        self.SearchWidgetGroup.setEnabled(False)
        self.CheckWidgetGroup.setEnabled(False)
        # create feature request
        featReq = QgsFeatureRequest()
        featReq.setFlags(QgsFeatureRequest.NoGeometry)
        Req = featReq.setSubsetOfAttributes([fieldIndex])
        Re2 = featReq.setSubsetOfAttributes([fieldIndex2])
        iter = layer.getFeatures(featReq)
        # process
        k = 0
        n = 0
#        self.continueSearch = True
        while iter.nextFeature(f): #and self.continueSearch:
            k += 1
            if self.evaluate(f[fieldName], toFind):
                results.append(f.id())
        f2 = QgisFeature(f.id())
        while iter.nextFeature(f2): #and self.continueSearch:
            n += 1
            if self.evaluate(f[fieldName2], toFind2):
                results2.append(f2.id())
            self.progressBar.setValue(n)
            QCoreApplication.processEvents()
        # reset UI
        self.widget_2.hide()
        self.layerWidgetGroup.setEnabled(True)
        self.SearchWidgetGroup.setEnabled(True)
        self.CheckWidgetGroup.setEnabled(True)
        # process results
        if self.continueSearch:
            QMessageBox
            msgBox.setText("Search Parcels 2: %u particelle trovate.")
            msgBox.exec_()
            self.processResults(results2)
        return

#    def getLayer(self):
#        i = self.comboBox.currentIndex()
#        if i < 0:
#            return None
#        layerId = self.comboBox.itemData(i)
#        return QgsMapLayerRegistry.instance().mapLayer(layerId)

    def evaluate(self, v1, v2):
        return float(v1) == float(v2)

    def processResults(self, results2):
        if layer is None:
            return
        if self.selectBox.isChecked():
            layer.setSelectedFeatures(results2)
            if len(results2) == 0:
                return

            if self.panBox.isEnabled() and self.panBox.isChecked():
                canvas = self.iface.mapCanvas()
                rect = canvas.mapRenderer().layerExtentToOutputExtent(layer, layer.boundingBoxOfSelected())
                if rect is not None:
                    if self.scaleBox.isEnabled() and self.scaleBox.isChecked():
                        rect.scale(1.5)
                        canvas.setExtent(rect)
                    else:
                        canvas.setExtent(QgsRectangle(rect.center(), rect.center()))
                canvas.refresh()
        if self.formBox.isChecked():
            f = QgsFeature()
            for id in results2:
                if layer.getFeatures(QgsFeatureRequest().setFilterFid(id)).nextFeature(f):
                    self.IdentifyResult(layer, f)
        return


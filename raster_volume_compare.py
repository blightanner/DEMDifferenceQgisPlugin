# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterVolumeCompare
                                 A QGIS plugin
 Calculates the difference in volume between two raster layers
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-01-16
        git sha              : $Format:%H$
        copyright            : (C) 2023 by L Yang/Bligh Tanner
        email                : lauren.yang@blightanner.com.au
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, Qgis, QgsRasterLayer, QgsMessageLog, QgsTaskManager, QgsProcessingAlgRunnerTask, QgsProcessingContext, QgsProcessingFeedback, QgsApplication,QgsField, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils, QgsTask, QgsVectorLayer
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt5.QtWidgets import QFileDialog
from qgis.utils import iface
from qgis import processing

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .raster_volume_compare_dialog import RasterVolumeCompareDialog
import os.path
import logging
import os
from datetime import datetime
from functools import partial


class RasterVolumeCompare:
    context = QgsProcessingContext()
    feedback = QgsProcessingFeedback()
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RasterVolumeCompare_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Raster Volume Comparison')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        
        self.context = QgsProcessingContext()
        self.feedback = QgsProcessingFeedback()
        self.task_manager = QgsApplication.taskManager()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RasterVolumeCompare', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/raster_volume_compare/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Volume Difference'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Raster Volume Comparison'),
                action)
            self.iface.removeToolBarIcon(action)

    def select_output_file(self):  
        
        todayDateString = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        niceFileName = 'DifferenceRaster' + todayDateString
        filename, _filter = QFileDialog.getSaveFileName(  
            self.dlg, "Select output filename and destination",niceFileName, 'GeoTIFF(*.tif)')  
        self.dlg.lineEdit.setText(filename)  
        
    def select_style_file(self):  
        filename, _filter = QFileDialog.getSaveFileName(  
            self.dlg, "Select output filename and destination","layer_info", 'QML(*.qml)')  
        self.dlg.lineEdit_2.setText(filename) 
    
    def OnZonalStatsComplete(self, context, successful, results):
        if not successful:
            QgsMessageLog.logMessage('Zonal Stats task finished unsucessfully with description ',
                                     'my-plugin', Qgis.Warning)
        
        
        else:        
            todayDateString = datetime.today().strftime('%Y-%m-%d')
            
            
            # update the attributes table
            self.testTask = EditGpkgTask(results["OUTPUT_TABLE"], self.iface, todayDateString)
            QgsApplication.taskManager().addTask(self.testTask)
            
            taskStatus = self.testTask.status()
            QgsMessageLog.logMessage('Task status is ' + str(taskStatus), 'my-plugin', Qgis.Info)
            
            # version blocking ui
            '''
            layerHandle.startEditing()
            pv = layerHandle.dataProvider()
            pv.addAttributes([QgsField('Volume', QVariant.Double)])
            layerHandle.updateFields()
            
            calculatorExpression = QgsExpression('"zone" * "m2"')
            
            calculatorContext = QgsExpressionContext()
            calculatorContext.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layerHandle))
            
            for f in layerHandle.getFeatures():
                calculatorContext.setFeature(f)
                f['Volume'] = calculatorExpression.evaluate(calculatorContext)
                layerHandle.updateFeature(f)
            
            layerHandle.commitChanges()
            #end blocking ui
            '''

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = RasterVolumeCompareDialog()
            self.dlg.toolButton.clicked.connect(self.select_output_file)  
            self.dlg.toolButton_2.clicked.connect(self.select_style_file)  

         # Fetch the currently loaded layers  
        layers = QgsProject.instance().mapLayers()
        
        layers_names = []
        for layer in QgsProject.instance().mapLayers().values():
            layers_names.append(layer.name())

        # Clear the contents of the comboBox from previous runs  
        self.dlg.comboBox.clear()

        # Populate the comboBox with names of all the loaded layers  
        self.dlg.comboBox.addItems(layers_names)
        
        # Clear the contents of the comboBox from previous runs  
        self.dlg.comboBox_2.clear()

        # Populate the comboBox with names of all the loaded layers  
        self.dlg.comboBox_2.addItems(layers_names)
        
    
        # Show the dialog  
        self.dlg.show()

        # Run the dialog event loop  
        result = self.dlg.exec_()
        
        # See if OK was pressed
        if result:
            QgsMessageLog.logMessage('Started task ', 'my-plugin', Qgis.Info)
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            newFilename = self.dlg.lineEdit.text()
            
            # Get the first selected layer
            layer1Nametest = self.dlg.comboBox.currentText()
            QgsMessageLog.logMessage('Layer 1 name is ' + layer1Nametest, 'my-plugin', Qgis.Info)
            selectedLayer1 = QgsProject.instance().mapLayersByName(layer1Nametest)
                
            # Get the second selected layer
            selectedLayer2Name = self.dlg.comboBox_2.currentText()  
            selectedLayer2 = QgsProject.instance().mapLayersByName(selectedLayer2Name) 
            
            #set up layer references
            layer1Ref=QgsRasterCalculatorEntry()
            #should check here for empty or null list...
            layer1Ref.raster=selectedLayer1[0]
            layer1Ref.bandNumber = 1
            layer1Ref.ref = "selectedLayer1@1"
            layer2Ref=QgsRasterCalculatorEntry()
            layer2Ref.raster=selectedLayer2[0]
            layer2Ref.bandNumber = 1
            layer2Ref.ref = "selectedLayer2@1"
            
            entries = []
            entries.append(layer1Ref)
            entries.append(layer2Ref)
            calculationString = layer1Ref.ref + ' - ' +layer2Ref.ref
            differenceRaster = QgsRasterCalculator(calculationString, newFilename, "GTiff", selectedLayer2[0].extent(), selectedLayer2[0].width(), selectedLayer2[0].height(), entries)
            differenceRaster.processCalculation()
            
            todayDateString = datetime.today().strftime('%Y-%m-%d')
            rLayerDifference = iface.addRasterLayer(newFilename, "DifferenceRaster" + todayDateString)

            currentDir = os.getcwd()
            QgsMessageLog.logMessage('Current working directy is ' + currentDir, 'my-plugin', Qgis.Info)
            
            userSpecifiedStylePath = self.dlg.lineEdit_2.text()
            templateStylePath = currentDir + '\\3 Styles\\SandElevationChange.qml'
            stylePath = ""
            if userSpecifiedStylePath:
                stylePath = userSpecifiedStylePath
            elif os.path.isfile(templateStylePath):
                stylePath = templateStylePath
            else:
                stylePath = ""
            
            if stylePath:
                rLayerDifference.loadNamedStyle(stylePath)
                rLayerDifference.triggerRepaint()
            
            statsFolder = currentDir + '\\5 Working Files'
            
            # check for existence of designated working files folder
            if os.path.isdir(statsFolder):
                statsFilePath = currentDir + '\\5 Working Files\\zonalStats' + todayDateString + '.gpkg'
            else:
                statsFilePath = todayDateString + '.gpkg'
            
            # task stuff
            alg = QgsApplication.processingRegistry().algorithmById(
                                      'native:rasterlayerzonalstats')
            
            params = {'INPUT': rLayerDifference.source(), 'BAND': 1, 'ZONES_BAND': 1, 'ZONES': rLayerDifference.source(),'OUTPUT_TABLE': statsFilePath}
            task = QgsProcessingAlgRunnerTask(alg, params, self.context, self.feedback)
            task.executed.connect(partial(self.OnZonalStatsComplete, self.context))
            QgsApplication.taskManager().addTask(task)
            
class EditGpkgTask(QgsTask):

    importComplete = pyqtSignal()
    errorOccurred = pyqtSignal()

    def __init__(self, gpkgPath, iface, datestring):
        QgsTask.__init__(self, "Update attributes table")
        self.gpkg = gpkgPath
        self.iface = iface
        self.datestring = datestring

    def run(self):
        QgsMessageLog.logMessage('Starting test task')
        
        QgsMessageLog.logMessage('Working on updating volume', 'my-plugin', Qgis.Info)
        statsLayer = QgsVectorLayer(self.gpkg, 'zonalStats' + self.datestring, "ogr")
        
        if not statsLayer.isValid():
            QgsMessageLog.logMessage('Unable to load gpkg statistics file', 'my-plugin', Qgis.Info)
            return False
        
        statsLayer.startEditing()
        pv = statsLayer.dataProvider()
        pv.addAttributes([QgsField('Volume', QVariant.Double)])
        statsLayer.updateFields()
        
        calculatorExpression = QgsExpression('"zone" * "m2"')
        
        calculatorContext = QgsExpressionContext()
        calculatorContext.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(statsLayer))
        
        for f in statsLayer.getFeatures():
            calculatorContext.setFeature(f)
            f['Volume'] = calculatorExpression.evaluate(calculatorContext)
            statsLayer.updateFeature(f)
        
        statsLayer.commitChanges()

        return True

    def finished(self, result):
        QgsMessageLog.logMessage('In finished(), emit signal')
        if result:
            QgsMessageLog.logMessage('In with no error')
            self.iface.addVectorLayer(self.gpkg, 'zonalStats' + self.datestring, "ogr")
            self.iface.messageBar().createMessage("Info", "Finished calculating volume difference")
            self.importComplete.emit()
        else:
            QgsMessageLog.logMessage('Error excuting volume calculation task!')
            self.iface.messageBar().createMessage("Error", "Unable to calculate volume difference")
            self.errorOccurred.emit()        
            

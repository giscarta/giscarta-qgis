# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GisCartaQGISDialogLayers
                                 A QGIS plugin
 Manage your GisCarta data
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-09-07
        git sha              : $Format:%H$
        copyright            : (C) 2023 by GisCarta
        email                : info@giscarta.com
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

import os
from pathlib import Path

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from sys import platform


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
root_path = Path(__file__).parents[1]
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    root_path, 'ui', 'giscarta_dialog_edit_layer.ui'))


class GisCartaQGISDialogEditLayer(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GisCartaQGISDialogEditLayer, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        imgPath_logo_mini = os.path.join(
            root_path,
            'icons',
            'icon.png',
            )
        icon = QIcon()
        wtPixmap = QPixmap(imgPath_logo_mini)
        icon.addPixmap(wtPixmap)
        self.setWindowIcon(icon)
        if platform == "win32":
            self.setStyleSheet('QCheckBox{font-size:9pt; font-family:"Arial";} QCheckBox#checkBox_selected{font-size:7pt; font-family:"Arial";} QLabel{font-size:7pt; font-family:"Arial";}')
        else:
            self.setStyleSheet('QCheckBox{font-size:15pt; font-family:"Arial";} QCheckBox#checkBox_selected{font-size:13pt; font-family:"Arial";} QLabel{font-size:13pt; font-family:"Arial";}')
        #print(__file__)
        
        self.setupUi(self)
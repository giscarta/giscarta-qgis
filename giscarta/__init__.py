# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GisCartaQGIS
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
from qgis.PyQt.QtCore import QUrl, QSettings, QTranslator, QCoreApplication, Qt, QSize, QItemSelectionModel
from qgis.PyQt.QtGui import QIcon, QDesktopServices
from qgis.PyQt.QtWidgets import QAction, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
from ..constants import (
    PRIVACY_POLICY_URL,
    TOS_URL
)
from qgis.core import QgsRasterLayer


from .. import resources
# Import the code for the dialog
from ..dialogs.giscarta_dialog import GisCartaQGISDialog
from ..dialogs.giscarta_dialog_layers import GisCartaQGISDialogLayers
from ..dialogs.giscarta_dialog_add_layer import GisCartaQGISDialogAddLayer
from ..dialogs.giscarta_dialog_edit_layer import GisCartaQGISDialogEditLayer

import os
from ..api import ApiClient


class GisCartaQGIS:
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
            'GisCartaQGIS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GisCarta')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.token = None
        self.user_layers = None
        self.username = None
        self.domain = None
        self.selected_rows_indexes = []
        self.api = None

    from .login import _log_in, _sign_up, _logout_click
    from .add_layer import _add_layer, _add_click
    from .toc import _create_table, _select_table_row, _refresh_click
    from .remove_layer import _delete_layers, _del_click
    from .create_gpkg import _create_gpkg_from_layer, _clear_folder
    from .edit_layer import _edit_layer, _edit_click

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
        return QCoreApplication.translate('GisCartaQGIS', message)

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
            self.iface.addPluginToWebMenu(
                self.menu,
                action)
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/giscarta/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GisCarta'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&GisCarta'),
                action)
            self.iface.removePluginVectorMenu(
                self.tr(u'&GisCarta'),
                action)
            self.iface.removePluginRasterMenu(
                self.tr(u'&GisCarta'),
                action)
            self.iface.removeToolBarIcon(action)

    def connect_hyperlinks(self):
        try:
            self.dlg.footer_label.linkActivated.disconnect(self._link_activated)
        except TypeError:
            pass
        try:
            self.dlg_layers.footer_label.linkActivated.disconnect(self._link_activated)
        except TypeError:
            pass
        self.dlg.footer_label.linkActivated.connect(self._link_activated)
        self.dlg_layers.footer_label.linkActivated.connect(self._link_activated)

    # adding links to security policy and usage rules labels
    def _link_activated(self, link: str):
        """
        Called when a hyperlink is clicked in dialog labels
        """
        if link == 'privacy_policy':
            url = QUrl(PRIVACY_POLICY_URL)
        elif link == 'terms_of_use':
            url = QUrl(TOS_URL)
        else:
            return

        QDesktopServices.openUrl(url)

    # is raster lyr for add dialog
    def _is_raster_lyr(self):
        if self.dlg_add_layer.map_layers_cb.currentLayer():
            if isinstance(self.dlg_add_layer.map_layers_cb.currentLayer(), QgsRasterLayer):
                if self.dlg_add_layer.checkBox_selected.isChecked():
                    self.dlg_add_layer.checkBox_selected.setChecked(False)
                self.dlg_add_layer.checkBox_selected.setEnabled(False)
            else:
                self.dlg_add_layer.checkBox_selected.setEnabled(True)
        else:
            self.dlg_add_layer.checkBox_selected.setEnabled(False)

    # is raster lyr for edit dialog
    def _is_raster_lyr_edit(self):
        if self.dlg_edit_layer.map_layers_cb.currentLayer():
            if isinstance(self.dlg_edit_layer.map_layers_cb.currentLayer(), QgsRasterLayer):
                if self.dlg_edit_layer.checkBox_selected.isChecked():
                    self.dlg_edit_layer.checkBox_selected.setChecked(False)
                self.dlg_edit_layer.checkBox_selected.setEnabled(False)
            else:
                self.dlg_edit_layer.checkBox_selected.setEnabled(True)
        else:
            self.dlg_edit_layer.checkBox_selected.setEnabled(False)

    # update geometry checkbox
    def _edit_geom(self):
        if self.dlg_edit_layer.checkBox_update_geom.isChecked():
            self.dlg_edit_layer.layer_label.setEnabled(True)
            self.dlg_edit_layer.map_layers_cb.setEnabled(True)
            self.dlg_edit_layer.checkBox_selected.setEnabled(True)
            self.dlg_edit_layer.edit_layer_button.setEnabled(True)
        else:
            self.dlg_edit_layer.layer_label.setEnabled(False)
            self.dlg_edit_layer.map_layers_cb.setEnabled(False)
            self.dlg_edit_layer.checkBox_selected.setEnabled(False)
            if not self.dlg_edit_layer.checkBox_update_meta.isChecked():
                self.dlg_edit_layer.edit_layer_button.setEnabled(False)

    # update meta checkbox
    def _edit_meta(self):
        if self.dlg_edit_layer.checkBox_update_meta.isChecked():
            self.dlg_edit_layer.name_label.setEnabled(True)
            self.dlg_edit_layer.text_name.setEnabled(True)
            self.dlg_edit_layer.description_label.setEnabled(True)
            self.dlg_edit_layer.text_description.setEnabled(True)
            self.dlg_edit_layer.tags_label.setEnabled(True)
            self.dlg_edit_layer.text_tags.setEnabled(True)
            self.dlg_edit_layer.edit_layer_button.setEnabled(True)
        else:
            self.dlg_edit_layer.name_label.setEnabled(False)
            self.dlg_edit_layer.text_name.setEnabled(False)
            self.dlg_edit_layer.description_label.setEnabled(False)
            self.dlg_edit_layer.text_description.setEnabled(False)
            self.dlg_edit_layer.tags_label.setEnabled(False)
            self.dlg_edit_layer.text_tags.setEnabled(False)
            if not self.dlg_edit_layer.checkBox_update_geom.isChecked():
                self.dlg_edit_layer.edit_layer_button.setEnabled(False)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = GisCartaQGISDialog()
            self.dlg_layers = GisCartaQGISDialogLayers()
            self.dlg_add_layer = GisCartaQGISDialogAddLayer()
            self.dlg_edit_layer = GisCartaQGISDialogEditLayer()
        if self.dlg.isVisible():
            self.dlg.raise_()
            self.dlg.activateWindow()
        elif self.dlg_layers.isVisible():
            self.dlg_layers.raise_()
            self.dlg_layers.activateWindow()
        elif self.dlg_add_layer.isVisible():
            self.dlg_add_layer.raise_()
            self.dlg_add_layer.activateWindow()
        else:
            # show the dialog
            self.dlg.show()        

            # connect events when the plugin window opens
            self.connect_hyperlinks()
            self.dlg.sign_up_button.clicked.connect(self._sign_up)
            self.dlg.log_in_button.clicked.connect(self._log_in)

            # Run the dialog event loop
            result = self.dlg.exec_()

            # disconnect events when closing a window
            if result == 0:
                self.dlg.footer_label.linkActivated.disconnect(self._link_activated)
                self.dlg.sign_up_button.clicked.disconnect(self._sign_up)
                self.dlg.log_in_button.clicked.disconnect(self._log_in)
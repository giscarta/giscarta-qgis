from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox
from qgis.core import QgsProject, QgsVectorLayer, QgsFeature, QgsField, QgsGeometry, QgsPointXY
from qgis.gui import *
from qgis.PyQt.QtCore import QVariant
import requests

def _export_layer(self): 
    selectedIndex = self.selected_rows_indexes[0]
    user_layer = self.user_layers[selectedIndex]
    username = self.username
    password = self.password
    endpoint = '/auth/token/login' 
    data = {'username': username, 'password': password}
    response = self.api.post(endpoint, data = data)
    self.token = response.get('auth_token')    
    url = "https://map.giscarta.com/geoserver/user_data/ows" 

    headers = {
            "Referer": "https://map.giscarta.com/builder/",
            "Authorization": f"Token {self.token}"}

    if user_layer['type'] != 'raster':
        params = {
            "srsName": "EPSG:4326",
            "cql_filter": "1=1",
            "propertyNames": "",
            "format_options": "charset=UTF-8",
            "request": "GetFeature",
            "service": "WFS",
            "typeName": "user_data:" + user_layer['name'],
            "version": "2.0.0",
            "settings": "",
            "outputFormat": "application/json"
        }

        response = requests.get(url, params = params, headers = headers) 
        if response.status_code == 200:
            geojson_data = response.json()
            geom_type = user_layer['geometryType'].lstrip('org.locationtech.jts.geom.')
            lyr = QgsVectorLayer(f'{geom_type}?crs=epsg:4326', str(user_layer['title']), 'memory')
            field_names = list(geojson_data['features'][0]['properties'].keys())
            fields = []
            for field_name in field_names:
                fields.append(QgsField(field_name, QVariant.String))
            lyr.dataProvider().addAttributes(fields)
            lyr.updateFields()

            def create_geometry(geom_type, coordinates):
                if geom_type == 'Point':
                    return QgsGeometry.fromPointXY(QgsPointXY(coordinates[0], coordinates[1]))
                if geom_type == 'MultiPoint':
                    return QgsGeometry.fromPointXY(QgsPointXY(coordinates[0][0], coordinates[0][1]))
                elif geom_type == 'LineString':
                    return QgsGeometry.fromPolylineXY([QgsPointXY(coord[0], coord[1]) for coord in coordinates])
                elif geom_type == 'MultiLineString':
                    return QgsGeometry.fromPolylineXY([QgsPointXY(coord[0], coord[1]) for coord in coordinates[0]])
                elif geom_type == 'Polygon':
                    return QgsGeometry.fromPolygonXY([[QgsPointXY(coord[0], coord[1]) for coord in coordinates[0]]])
                elif geom_type == 'MultiPolygon':
                    return QgsGeometry.fromPolygonXY([[QgsPointXY(coord[0], coord[1]) for coord in coordinates[0][0]]])

            features = []
            for feature in geojson_data['features']:
                properties = feature['properties']
                geom_type = feature['geometry']['type']
                coordinates = feature['geometry']['coordinates']
                geom = create_geometry(geom_type, coordinates)
                new_feature = QgsFeature()
                new_feature.setGeometry(geom)
                new_feature.setAttributes(list(properties.values()))
                features.append(new_feature)
            lyr.dataProvider().addFeatures(features)
            QgsProject.instance().addMapLayer(lyr)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Layer was loaded successfully")
            msg.setWindowTitle("Status")
            msg.setStandardButtons(QMessageBox.Ok)
            returnValue = msg.exec()
            
        else:
            print("error", response.status_code, response.text)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(response.text)
            msg.setWindowTitle("Layer loading error")
            msg.setStandardButtons(QMessageBox.Ok)
            returnValue = msg.exec()
    
    else: # for raster 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Trying to load a raster layer")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            returnValue = msg.exec()


def _export_click(self):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText("Are you sure you want to download a layer from GISCARTA?")
    msg.setWindowTitle("Saving a layer")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    returnValue = msg.exec()
    if returnValue == QMessageBox.Ok:
        _export_layer(self)
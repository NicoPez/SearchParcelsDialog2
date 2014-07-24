# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SearchParcels2
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load SearchParcels2 class from file SearchParcels2
    from searchparcels2 import SearchParcels2
    return SearchParcels2(iface)

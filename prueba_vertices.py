from qgis.core import *
import qgis.utils
from qgis.gui import *
from PyQt5.QtCore import *
import math
from datetime import datetime
from pyproj import Proj, transform
from osgeo import ogr
import shapely.geometry
import shapely.wkt
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
from scipy.spatial import *
from shapely.ops import triangulate
import numpy as np
#import matplotlib.pyplot as plt

# vertex iteration includes all parts and rings
geometry = QgsGeometry.fromWkt( 'MultiPolygon((( 0 0, 0 10, 10 10, 10 0, 0 0 ),( 5 5, 5 6, 6 6, 6 5, 5 5)),((20 2, 22 2, 22 4, 20 4, 20 2)))' )
#verti = [v for v in geometry.vertices()]
puntos = [(v.x(), v.y()) for v in geometry.vertices()]
print(puntos)
pnt2 = shapely.geometry.MultiPoint(puntos)
print(pnt2)
# Crear una triangulación de Delaunay a partir de la capa de puntos
#delaunay = QgsGeometryUtils.convexHull(pnt2, 0)
#simplices = Delaunay(pnt2).simplices
simp = scipy.spatial.Delaunay(pnt2).simplices
#print (np.unique(simp)) 
#triangles = triangulate(pnt2)
#print (simplices.coplanar)
#print (triangles)
#delauna = ConvexHull(pnt2)
#hull_points = delauna.simplices

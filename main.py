# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 16:54:35 2020

@author: Oscar Riquelme Moya
"""
import numpy as np
import utils
from Delaunay import Delaunay



#puntos = np.asarray([(1,1.9),(3.6,1),(6.5,3), (4,5), (3,5),(1,4),(-1,3)])
puntos = np.asarray([(1,-6), (3.5,-6.1), (4.5,-3), (5,-1.1), (4.8,1), (3.4,4),\
                    (1.5,5.1), (-1,5.7),(-3,4.8), (-4.8,2.7), (-6,1.2),\
                    (-6,-0.7),(-5.8,-2), (-4,-4.5), (-1,-6)])
    
td = Delaunay(center=utils.Center(puntos), radius=utils.radiusFrame(puntos))
for punto in puntos:
    td.AddPoint(punto)
    
triangulos = td.exportarTriangulos()
circulos = []#td.exportarCirculos()

utils.PlotDT(puntos,triangulos,circulos, radius=utils.radiusFrame(puntos))
area = 0
for triangulo in triangulos:
    A = puntos[triangulo[0]]
    B = puntos[triangulo[1]]
    C = puntos[triangulo[2]]
    
    area += utils.areaTriangulo(A,B,C)
if(utils.isConvex(puntos)):  
    print("El area el poligono es",round(area,16))
    
else:
    print("Esta distribución de puntos no corresponde a un poligono convexo.\n \
          No es posible calcular el area del poligono.")

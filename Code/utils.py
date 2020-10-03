# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 12:03:13 2020

@author: Oscar Riquelme Moya


"""
import numpy as np
import matplotlib.pyplot as plt


def Center(puntos):
    x = y = 0
    for i in range(len(puntos)):
        x += puntos[i][0]
        y += puntos[i][1]
    return np.array([x/len(puntos),y/len(puntos)])

def perpendicular(p,q):
    """
    A partir de 2 puntos p,q calculamos el punto medio y 
    la pendiente de la recta que los une, con el fin de calcular la recta 
    perpendicular que pasa por el punto medio
    Parameters
    ----------
    p : 
        punto de inicio.
    q : 
        punto final.

    Returns
    -------
        Devuelve un array con los coeficientes de x,y 
        y otro con el termino independiente

    """
    p = np.asarray(p)
    q = np.asarray(q)
    #Puntpo medio
    PM = (p+q)*0.5
    
    
    if(q[0]-p[0] == 0):# Es una recta vertical su perpendicular será y = k
        return np.array([0,1]),np.array([PM[1]])
    elif(q[1]-p[1] ==0):# Es una recta horizontal su perpendicular será x = k
        return np.array([1,0]),np.array([PM[0]])
    else:
        #pendiente recta (p,q)
        m = (q[1]-p[1])/(q[0]-p[0])
        
        #Ecuación recta perpendicular:    y-PM[1] = (-1/m)(x-PM[0])
        # Si lo ponemos de la forma ax+by=c:   x/m + y = PM[0]/m + PM[1]
        # En array:
        return np.array([1/m,1]),np.array([PM[0]/m+PM[1]])
    


def ScatterPoints(points,**kwargs):
    """
    Dada una lista de puntos representa el grafico de dispersion

    Parameters
    ----------
    points : array (n,2)
        lista de puntos en R^2
    **kwargs : TYPE
        Argumentos de la clase Line2D
    """
    
    plt.plot(points[:,0],points[:,1], 'o', **kwargs)


def PlotDT(coords, triangulos, circulos=[],radius=99999):
    """
    Dibuja la triangulación de Delaunay
    
    
    coords: puntos a partir de los que triangulamos
    
    triangulos: lista de los indices de los vertices de cada triangulo
    
    circulos: listas tipo (centro,radio) de los circuncirculos de los triangulos
            por defecto lista vacia(no se dibujaran los circulos)

    """
    fig, ax = plt.subplots(dpi=300)
    
     #Dibujamos los triangulos
    for tri in triangulos:
        #Por cada vertice del triangulo obtenemos sus coordenadas 
        #para dibujar las tres rectas y comprobamos si son vertices
        #consecutivos para pintar el contorno de otro color.
        
        x1 = coords[tri[0]][0],coords[tri[1]][0]
        y1 = coords[tri[0]][1],coords[tri[1]][1]
        if abs(tri[0]-tri[1]) == 1 or abs(tri[0]-tri[1]) == len(coords)-1:
            color1 = "black"
        else:
            color1 = "red"
        
        x2 = coords[tri[1]][0],coords[tri[2]][0]
        y2 = coords[tri[1]][1],coords[tri[2]][1]
        if abs(tri[1]-tri[2]) == 1 or abs(tri[1]-tri[2]) == len(coords)-1:
            color2 = "black"
        else:
            color2 = "red"
            
        x3 = coords[tri[2]][0],coords[tri[0]][0]
        y3 = coords[tri[2]][1],coords[tri[0]][1]
        if abs(tri[2]-tri[0]) == 1 or abs(tri[2]-tri[0]) == len(coords)-1:
            color3 = "black"
        else:
            color3 = "red"
            
        plt.plot(x1, y1, color1,\
                 x2, y2, color2,\
                 x3, y3, color3)
    
    #Dibujamos los circulos
    for circulo in circulos:
        ax.add_artist(plt.Circle(circulo[0],circulo[1],color="green",fill=False))

    #Por último dibujamos los puntos
    ScatterPoints(coords, c='b')
    
    plt.axis([-1, radius+1, -1, radius+1])
    plt.axis('equal')
    plt.axis('off')
    plt.show()



def areaTriangulo(A,B,C):
    #Calculamos la longitud de los lados del triangulo
    AB = np.linalg.norm(B-A)
    AC = np.linalg.norm(C-A)
    BC = np.linalg.norm(C-B)
    
    #Calculamos el semiperímetro s
    s = (AB + AC + BC)*0.5
    
    #Ahora usando la formula de Herón calculamos el área:
    return (s*(s-AB)*(s-AC)*(s-BC))**0.5
    
    

def isConvex(puntos):
    puntos = np.asarray(puntos)
    for i in range(1,len(puntos)-1):
        u = puntos[i]-puntos[i-1]
        v = puntos[i+1]-puntos[i]
        angle = np.math.atan2(np.linalg.det([u,v]),np.dot(u,v))
        if(angle <0):
            return False
    return True
     

 
def radiusFrame(puntos):
    minX = puntos[0][0]
    minY = puntos[0][1]
    maxX = puntos[0][0]
    maxY = puntos[0][1]
    
    for i in range(1,len(puntos)):
        if puntos[i][0] < minX:
            minX = puntos[i][0]
        if puntos[i][1] < minY:
            minY = puntos[i][1]
            
        if puntos[i][0] > maxX:
            maxX = puntos[i][0]
        if puntos[i][1] > maxY:
            maxY = puntos[i][1]

    return max(maxX-minX,maxY-minY)
    
    
    
    
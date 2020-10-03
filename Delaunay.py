# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 11:45:43 2020
Algoritmo Delaunay basado en el de Jose M. Espadero ( http://github.com/jmespadero/pyDelaunay2D )
@author: Oscar Riquelme Moya
"""
import numpy as np
import utils


class Delaunay:

    def __init__(self, center=(0, 0), radius=9999):
        """ Creamos el cuadrado inicial para la triangulación
        center -- Opcional posición del centro del cuadrado. Default (0,0)
        radius -- Opcional distancia de las esquinas al centro.
        """
        center = np.asarray(center)
        # Creamos las coordenadas de las esquinas del cuadrado
        self.coords = [center+radius*np.array((-1, -1)),
                       center+radius*np.array((+1, -1)),
                       center+radius*np.array((+1, +1)),
                       center+radius*np.array((-1, +1))]

        # Creamos un discionario para los triangulos y otro para los circulos
        self.triangulos = {}
        self.circulos = {}

        # Creamos los dos triangulos CCW (sentido inverso a las agujas del reloj)
        #                                 (del ingles "counterclockwise")
        T1 = (0, 1, 3)
        T2 = (2, 3, 1)
        self.triangulos[T1] = [T2, None, None]
        self.triangulos[T2] = [T1, None, None]
        
        #Calculamos el centro y el radio del circulo para cada triangulo
        for t in self.triangulos:
            self.circulos[t] = self.circuncentro(t)
            
            
    def circuncentro(self, tri):
        """
        Cálculo del circuncentro de un triangulo

        """
        
        A,B,C = np.asarray([self.coords[v] for v in tri])
        #Calculamos las rectas perpendiculares de dos lados del triangulo
        #y las organizamos en matriz de coeficientes y matriz de resultados
        r = utils.perpendicular(A,B)
        s = utils.perpendicular(A,C)
        M = np.array([r[0],s[0]])
        N = np.array([r[1],s[1]])
        #resolvemos el sistema y obtenemos el punto de corte, el circuncentro
        centro = np.linalg.solve(M,N).reshape(2,)
        radio = np.linalg.norm(A - centro) #Calculamos la distancia euclidea

        return (centro, radio)
    
    def inCircle(self, tri, p):
        """
        Comporbamos si el punto está en el circuncirculo del triangulo.

        """
        
        centro, radio = self.circulos[tri]
        return np.linalg.norm(centro-p)<=radio


    def AddPoint(self, p):
        p = np.asarray(p)
        idx = len(self.coords)
        self.coords.append(p)
        
        #Buscamos los triangulos cuyo circuncirculo contenga a p
        bad_triangles = []
        for T in self.triangulos:
            if self.inCircle(T, p):
                bad_triangles.append(T)
                
        # Encontramos el perimetro CCW (poligono estrellado) del triangulo
        # expresado como una lista de pares de puntos y el triangulo opuesto a
        #cada lado
        perimetro = []
        # Elegimos un triangulo y lado aleatorio
        T = bad_triangles[0]
        lado = 0
        #Encontramos el triangulo opuesto a este lado:
        
        while True:
            # Comprobamos si el lado del triangulo T esta en el perimetro
            # si el triangulo opuesto al lado está fuera de la lista
            tri_op = self.triangulos[T][lado]
            if tri_op not in bad_triangles:
                # Añadimos el lado y el triangulo externo a la lista del perimetro
                perimetro.append((T[(lado+1) % 3], T[(lado-1) % 3], tri_op))
    
                # Nos movemos al siguiente lado del triangulo
                lado = (lado + 1) % 3
    
                # Comporbamos si el perimetro es un bucle cerrado
                if perimetro[0][0] == perimetro[-1][1]:
                    break
            else:
                # Nos movemos al siguiente lado del triangulo opuesto
                lado = (self.triangulos[tri_op].index(T) + 1) % 3
                T = tri_op
                
        
        
        # Quitamos los triangulos muy cerca del punto p de nuestra solución
        for T in bad_triangles:
            del self.triangulos[T]
            del self.circulos[T]
            
        
        # retriangulamos el hueco deado por bad_triangles
        new_triangles = []
        for (e0, e1, tri_op) in perimetro:
            # Creamos un nuevo triangulo usiando el punto p y el lado
            T = (idx, e0, e1)

            # guardamos el circuncentro y el circunradio del triangulo
            self.circulos[T] = self.circuncentro(T)

            # fijamos el triangulo opuesto al lado como vecino de T
            self.triangulos[T] = [tri_op, None, None]

            # Tratamops de fijar T como vecinodel triangul opuesto
            if tri_op:
                # buscamos el vecino de tri_op que use el lado (e1, e0)
                for i, vecino in enumerate(self.triangulos[tri_op]):
                    if vecino:
                        if e1 in vecino and e0 in vecino:
                            # cambiamos la relación para usar nuestro nuevo triangulo
                            self.triangulos[tri_op][i] = T

            #Añadimos el triangulo a una lista temporal
            new_triangles.append(T)
        # Relacionamos el nuevo triangulo con los otros
        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangulos[T][1] = new_triangles[(i+1) % N]   # siguiente
            self.triangulos[T][2] = new_triangles[(i-1) % N]   # anterior
    def exportarTriangulos(self):
        """Exportamos la lista de Triangulos de Delaunay
        """
        # Filtramos los triángulos con cualquier vértice en el cuadrado inicial
        return [(a-4, b-4, c-4)
                for (a, b, c) in self.triangulos if a > 3 and b > 3 and c > 3]
    
    def exportarCirculos(self):
        """Exportamos las circunferencias como una lista de (centro, radio)
        """
         # Filtramos los triángulos con cualquier vértice en el cuadrado inicial
        return [(self.circulos[(a, b, c)][0], self.circulos[(a, b, c)][1])
                for (a, b, c) in self.triangulos if a > 3 and b > 3 and c > 3]




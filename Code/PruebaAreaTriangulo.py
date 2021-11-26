# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 11:19:41 2020

@author: User
"""

import utils
import numpy as np
import time

#Nuestro objetivo es comprobar la eficiencia de dos funciones para ello
#calcularemos el tiempo que tarda en realizarse cada una de ellas n veces
#obteniendo un ratio, esto lo haremos 100 veces para obtener una medida más
#precisa de este ratio.
n = 300
ratio = []
for i in range(100):
    
    def pruebaHeron():
        A,B,C = (np.random.rand(6)*10-5).reshape(3,2)
        utils.areaTrianguloHeron(A, B, C)
        
    def pruebaDeterminantes():
        A,B,C = (np.random.rand(6)*10-5).reshape(3,2)
        utils.areaTrianguloDeterminante(A, B, C)
    
    
    timeA0 = time.time()
    for i in range(n):
        pruebaHeron()
        
    deltaTA = time.time()-timeA0
    
    
    timeB0 = time.time()
    for i in range(n):
        pruebaDeterminantes()
        
    deltaTB = time.time()-timeB0
    ratio.append(deltaTA/deltaTB)
    
np.mean(ratio)
min(ratio)

#Lo primero que notamos es que si se realiza pocas veces (n<50) el tiempo para
#ambas funciones es practicamente 0 con lo que si en el programa principal se
#utiliza pocas veces la diferencia es despreciable.

#No obstante, aumentando el número de repeticiones obtenemos un ratio medio
#de 3.5 con lo que calculaer el area por determinantes es unas 3 veces más rápido
# dado que el objetivo es que el prorama sea escalable a una cantidad muy
#grande de puntos, esta será la opción que eligiremos
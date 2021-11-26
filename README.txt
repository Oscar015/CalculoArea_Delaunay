Cálculo del area de un poligono convexo mediante la triangulación de Delaunay

https://es.wikipedia.org/wiki/Triangulaci%C3%B3n_de_Delaunay
La triangulación de Delaunay es una red de triángulos conexa y convexa que cumple la condición de Delaunay. esta condición establece que la circunferencia circunscrita del mismo no debe contener ningún otro vértice de la triangulación en su interior, aunque sí se admiten vértices situados sobre la circunferencia.
Esta triangulación maximiza el ángulo mínimo de cada triangulo por lo que tiende a formar triangulos equilateros (pues cualquier otro tipo de triangulo tiende a tener un ángulo muy agudo) y la frontera externa de triangulación forma la envolvente convexa del conjunto de puntos, es por esto que en polígonos cóncavos no podemos usarla para calcular el área.

Hay distintos algoritmos para calcular la triangulación de Delaunay, aquí en concreto usaré el algoritmo incremental de Bowyer-Watson. En este método crearemos un cuadrado inicial que contenga en su interior a todos los vertices del polígono y lo dividimos en 2 triangulos. Después iremos poco a poco añadiendo uno por uno los puntos y comprobando que se cumpla la condición de Delaunay.

A la hora de graficar los triangulos y trabajar con ellos es necesario que la lista de puntos que se recibe como imput esté ordenada en el sentido contrario a las agujas del reloj.

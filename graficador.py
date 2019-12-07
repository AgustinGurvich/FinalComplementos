import random
import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from time import sleep


class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False, temp=100, ctemp=0.95, ancho=100, alto=100, grav=0.1):
        '''
        Parametros de layout:
        iters: cantidad de iteraciones a realizar.
        refresh: Numero de iteraciones entre actualizaciones de pantalla. 0 -> se grafica solo al final.
        c1: constante usada para calcular la repulsion entre nodos.
        c2: constante usada para calcular la atraccion de aristas.        
	verbose: opcion para activar los detalles de la ejecucion.
	ctemp: constante usada para reducir la temperatura por cada iteracion.
        temp: valor para manejar la convergencia del grafo.
        ancho: ancho inicial del grafico.
        alto: alto inicial del grafico.
        grav: constante de gravedad.
        '''
        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        self.posiciones = {}
        self.fuerzas = {}
        self.c1 = c1
        self.c2 = c2
        self.ancho = ancho
        self.alto = alto
        self.grav = grav
        self.temp = temp
        self.ctemp = ctemp

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        self.refresh = refresh

    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''

        if(self.verbose):
            print("Los parametros elegidos son: ")
            print("Iteraciones: " + str(self.iters))
            print("Refrescos: " + str(self.refresh))
            print("Fuerza de gravedad: " + str(self.grav))
            print("Temperatura: " + str(self.temp))
            print("Multiplicador de la temperatura: " + str(self.ctemp))
            print("Constante de atraccion:" + str(self.c2))
            print("Constante de repulsion: " + str(self.c1))
            print("Alto inicial: " + str(self.alto))
            print("Ancho inicial: " + str(self.ancho))
            sleep(10)  # Permite leer las opciones

        ejes = plt.gca()
        # ejes.set_xlim([0, self.ancho])
        # ejes.set_ylim([0, self.alto])
        plt.ion()

        N, E = self.grafo
        self.posiciones = posiciones_aleatorias( #Calculo las posiciones iniciales
            self.grafo, self.alto, self.ancho)
        for k in range(self.iters):
            if self.verbose:
                print("Iteracion n°", k+1)
            # Acumuladores
            accum_x = {node: 0 for node in self.grafo[0]}
            accum_y = {node: 0 for node in self.grafo[0]}
            # Atraccion
            if(self.verbose):
                print("Calculando fuerza de atracción")
            for ni, nj in E:
                dist = distancia_euclidiana(self, (ni, nj))
                if dist < 10**-5:
                    f = random.random()
                    self.posiciones[ni][0] += f
                    self.posiciones[ni][1] += f
                    self.posiciones[nj][0] -= f
                    self.posiciones[nj][1] -= f
                    dist = distancia_euclidiana(self, (ni, nj))
                mod_fa = f_atracction(self, dist)
                fx = (mod_fa*(self.posiciones[nj]
                              [0]-self.posiciones[ni][0]))/dist
                fy = (mod_fa*(self.posiciones[nj]
                              [1]-self.posiciones[ni][1]))/dist
                accum_x[ni] += fx
                accum_y[ni] += fy
                accum_x[nj] -= fx
                accum_y[nj] -= fy
            # Repulsion
            if(self.verbose):
                print("Calculando fuerza de repulsión")
            for ni in N:
                for nj in N:
                    if ni != nj:
                        dist = distancia_euclidiana(self, (ni, nj))
                        if dist < 10**-5:
                            f = random.random()
                            self.posiciones[ni][0] += f
                            self.posiciones[ni][1] += f
                            self.posiciones[nj][0] -= f
                            self.posiciones[nj][1] -= f
                            dist = distancia_euclidiana(self, (ni, nj))

                        mod_fa = f_repulsion(self, dist)
                        fx = (mod_fa*(self.posiciones[nj]
                                      [0]-self.posiciones[ni][0]))/dist
                        fy = (mod_fa*(self.posiciones[nj]
                                      [1]-self.posiciones[ni][1]))/dist
                        accum_x[nj] += fx
                        accum_y[nj] += fy
                        accum_x[ni] -= fx
                        accum_y[ni] -= fy
            # Gravedad
            if(self.verbose):
                print("Calculando fuerza de gravedad")
            for ni in N:
                pos0 = self.posiciones[ni]
                dist = ((pos0[0]-self.ancho/2)**2 +
                        (pos0[1]-self.alto/2)**2)**(1/2)
                if dist < 10**-5:
                    f = random.random()
                    self.posiciones[ni][0] += f
                    self.posiciones[ni][1] += f
                    dist = ((pos0[0]-self.ancho/2)**2 +
                            (pos0[1]-self.alto/2)**2)**(1/2)
                mod_fa = self.grav
                fx = (mod_fa*(self.posiciones[ni]
                              [0]-self.ancho/2)/dist)
                fy = (mod_fa*(self.posiciones[ni]
                              [1]-self.alto/2)/dist)
                accum_x[ni] -= fx
                accum_y[ni] -= fy
            if(self.verbose):
                print(accum_x, accum_y)
            # Posiciones
            for nodo in N:
                f = [accum_x[nodo], accum_y[nodo]]
                mod_accum = sqrt(f[0]**2 + f[1]**2)
                if mod_accum > self.temp:
                    f[0] = f[0]/mod_accum * self.temp
                    f[1] = f[1]/mod_accum * self.temp
                    (accum_x[nodo], accum_y[nodo]) = f
                self.posiciones[nodo][0] = self.posiciones[nodo][0] + accum_x[nodo]
                self.posiciones[nodo][1] = self.posiciones[nodo][1] + accum_y[nodo]
            # Actualizar temperatura
            self.temp = self.ctemp*self.temp
            # Creo listas X,Y
            ejex = [self.posiciones[i][0] for i in N]
            ejey = [self.posiciones[i][1] for i in N]
            # Grafico
            if self.refresh != 0 and k % self.refresh == 0:
                plt.pause(0.00001)
                plt.clf()
                plt.scatter(ejex, ejey)
                for e in E:
                    i1 = N.index(e[0])
                    i2 = N.index(e[1])
                    plt.plot((ejex[i1], ejex[i2]), (ejey[i1], ejey[i2]))

        if self.refresh == 0:
            plt.clf()
            plt.scatter(ejex, ejey)
            for e in E:
                i1 = N.index(e[0])
                i2 = N.index(e[1])
                plt.plot((ejex[i1], ejex[i2]), (ejey[i1], ejey[i2]))
        plt.ioff()
        plt.show()


def lee_grafo_archivo(archivo):
    '''
    Lee un grafo desde un archivo y devuelve su representacion como lista.
    Ejemplo Entrada:
        3
        A
        B
        C
        A B
        B C
        C B
    Ejemplo retorno:
        (['A','B','C'],[('A','B'),('B','C'),('C','B')])
    '''
    vertices = list()
    aristas = list()
    with open(archivo, "r") as file:
        lines = file.readlines()
        i = int(lines[0])
        for x in range(1, i+1):
            vertices += [lines[x].rstrip()]
        for k in range(i+1, len(lines)):
            sep = lines[k].rstrip().split()
            aristas += [(sep[0], sep[1])]
    return (vertices, aristas)


def posiciones_aleatorias(G, alto, ancho):
    '''
    Recibe un grafo en forma de lista, el alto y el ancho del plot inicial
    Devuelve un diccionario donde las claves son los vertices y los valores son
    tuplas de posicion (x,y)
    '''
    posiciones = {}
    for v in G[0]:
        posiciones[v] = [random.random() * ancho, random.random() * alto]
    return posiciones


def distancia_euclidiana(G, arista):
    '''
    Recibe un elemento de la clase LayoutGraph y una arista de un grafo
    Devuelve el largo de la arista con respecto al grafo en G
    '''
    pos0 = G.posiciones[arista[0]]
    pos1 = G.posiciones[arista[1]]
    return ((pos0[0]-pos1[0])**2+(pos0[1]-pos1[1])**2)**(1/2)


def f_atracction(G, dist):
    '''
    Recibe un elemento de la clase LayoutGraph y la distancia entre dos vertices
    Devuelve la fuerza de atraccion entre ambos vertices
    '''
    k = G.c2*sqrt((G.alto*G.ancho)/len(G.grafo[0]))
    return (dist)**2/k


def f_repulsion(G, dist):
    '''
    Recibe un elemento de la clase LayoutGraph y la distancia entre dos vertices
    Devuelve la fuerza de repulsion entre ambos vertices
    '''
    k = G.c1*sqrt((G.alto*G.ancho)/len(G.grafo[0]))
    return k**2/dist


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )

    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '-i','--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=100
    )

    # Tasa de redibujado, opcional, 2 por defecto
    parser.add_argument(
        '-r','--refresh',
        type=int,
        help='Cada cuanto redibujamos el grafo. Si el argumento es 0, se dibuja al finalizar las iteraciones',
        default=2
    )
    # Temperatura inicial, 200 por defecto
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=200.0
    )

    # Constante para disminuir temp, 0.95 por defecto
    parser.add_argument(
        '--ctemp',
        type=float,
        help='Constante para multiplicar Temp',
        default=0.95
    )

    #Constante de fuerza de gravedad, 0.05 por defecto
    parser.add_argument(
        '--grav',
        type=float,
        help='Fuerza de gravedad',
        default=0.05
    )

    #Alto inicial del grafo, para reducir el esparcimiento de los vertices
    parser.add_argument(
        '--alto',
        type=int,
        help='Alto del espacio de grafico',
        default=1000
    )

    #Ancho inicial del grafo, para reducir el esparcimiento de los vertices
    parser.add_argument(
        '--ancho',
        type=int,
        help='Ancho del espacio de grafico',
        default=1000
    )

    #Constante de la fuerza de atraccion entre vertices, 0.1 por defecto
    parser.add_argument(
        '-c2','--atrac',
        type=float,
        help='Fuerza de atraccion entre vertices',
        default=0.1
    )

    #Constante de la fuerza de repulsion entre vertices, 5 por defecto
    parser.add_argument(
        '-c1','--rep',
        type=float,
        help='Fuerza de repulsion entre vertices',
        default=5
    )

    args = parser.parse_args()

    grafo = lee_grafo_archivo(args.file_name)

    classG = LayoutGraph(grafo,
                         iters=args.iters,
                         refresh=args.refresh,
                         c1=args.rep,
                         c2=args.atrac,
                         verbose=args.verbose,
                         temp=args.temp,
                         ctemp=args.ctemp,
                         ancho=args.ancho,
                         alto=args.alto)

    # Ejecutamos el layout
    classG.layout()
    return


if __name__ == '__main__':
    main()

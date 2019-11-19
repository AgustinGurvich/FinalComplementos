import random
import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

alto = ancho = 100
gravedad = 0.1


class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False, temp=100):
        '''
        Parametros de layout:
        iters: cantidad de iteraciones a realizar
        refresh: Numero de iteraciones entre actualizaciones de pantalla.
        0 -> se grafica solo al final.
        c1: constante usada para calcular la repulsion entre nodos
        c2: constante usada para calcular la atraccion de aristas
        '''

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        # Completar
        self.posiciones = {}
        self.fuerzas = {}

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        self.temp = 1000000

    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''
        pass


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


def posiciones_aleatorias(G):
    posiciones = {}
    for v in G.grafo[0]:
        posiciones[v] = [random.random() * ancho, random.random() * alto]
    return posiciones


def distancia_euclidiana(G, arista):
    pos0 = G.posiciones[arista[0]]
    pos1 = G.posiciones[arista[1]]
    return ((pos0[0]-pos1[0])**2+(pos0[1]-pos1[1])**2)**(1/2)


def f_atracction(G, dist):
    k = G.c2*sqrt((alto*ancho)/len(G.grafo[0]))
    return (dist)**2/k


def f_repulsion(G, dist):
    k = G.c1*sqrt((alto*ancho)/len(G.grafo[0]))
    return k**2/dist


# def algoritmo1(G):
#     accum = {}
#     G.posiciones = posiciones_aleatorias(G)
#     for i in range(0, G.iters):
#         reset_accum()
#     for e in G.grafo[1]:
#         f = distancia_euclidiana(G, e)
#         accum[e[0]] += f
#         accum[e[1]] -= f
#     for i in range(len(G.posiciones)):
#         for j in range(len(G.posiciones)):
#             if i != j:
#                 f = distancia_euclidiana(G, (i, j))
#                 accum[i] += f
#                 accum[j] -= f


def layout(G):
    N, E = G.grafo
    G.posiciones = posiciones_aleatorias(G)
    for k in range(1, G.iters+1):
        # print(G.posiciones)
        # Acumuladores
        accum_x = {node: 0 for node in G.grafo[0]}
        accum_y = {node: 0 for node in G.grafo[0]}
        # print(accum_x)
        # Atraccion
        for ni, nj in E:
            dist = distancia_euclidiana(G, (ni, nj))
            if dist < 1:
                print("MENOR 0")
                f = random.random()
                G.posiciones[ni][0] += f
                G.posiciones[ni][1] += f
                G.posiciones[nj][0] -= f
                G.posiciones[nj][1] -= f
                dist = distancia_euclidiana(G, (ni, nj))
            mod_fa = abs(f_atracction(G, dist))
            fx = (mod_fa*(G.posiciones[nj][0]-G.posiciones[ni][0]))/dist
            fy = (mod_fa*(G.posiciones[nj][1]-G.posiciones[ni][1]))/dist
            # print("Los valores de fx y fy son ", fx, " ", fy)
            accum_x[ni] += fx
            accum_y[ni] += fy
            accum_x[nj] -= fx
            accum_y[nj] -= fy
            # print(accum_x)
            # a = input()
        # Repulsion
        for ni in N:
            for nj in N:
                if ni != nj:
                    dist = distancia_euclidiana(G, (ni, nj))

                    if dist < 10**-5:
                        f = random.random()
                        G.posiciones[ni][0] += f
                        G.posiciones[ni][1] += f
                        G.posiciones[nj][0] -= f
                        G.posiciones[nj][1] -= f
                        dist = distancia_euclidiana(G, (ni, nj))

                    mod_fa = f_repulsion(G, dist)
                    fx = (mod_fa*(G.posiciones[nj]
                                  [0]-G.posiciones[ni][0]))/dist
                    fy = (mod_fa*(G.posiciones[nj]
                                  [1]-G.posiciones[ni][1]))/dist
                    accum_x[nj] += fx
                    accum_y[nj] += fy
                    accum_x[ni] -= fx
                    accum_y[ni] -= fy
        # Gravedad
        for ni in N:
            pos0 = G.posiciones[ni]
            dist = ((pos0[0]-ancho/2)**2+(pos0[1]-alto/2)**2)**(1/2)
            if dist < 10**-5:
                f = random.random()
                G.posiciones[ni][0] += f
                G.posiciones[ni][1] += f
                dist = ((pos0[0]-ancho/2)**2+(pos0[1]-alto/2)**2)**(1/2)
            mod_fa = gravedad
            fx = (mod_fa*(G.posiciones[ni]
                          [0]-ancho/2)/dist)
            fy = (mod_fa*(G.posiciones[ni]
                          [1]-alto/2)/dist)
            accum_x[ni] -= fx
            accum_y[ni] -= fy
        # Posiciones
        # Hacer los limites de la ventana dinamicos
        for nodo in N:
            f = (accum_x[nodo], accum_y[nodo])
            if sqrt(f[0]**2 + f[1]**2) > G.temp:
                f = f/sqrt(f[0]**2 + f[1]**2) * G.temp
                (accum_x[nodo], accum_y[nodo]) = f
            G.posiciones[nodo][0] = G.posiciones[nodo][0] + accum_x[nodo]
            G.posiciones[nodo][1] = G.posiciones[nodo][1] + accum_y[nodo]
        # Actualizar temperatura
        G.temp = 0.7*G.temp
    ejex = [G.posiciones[i][0] for i in N]
    ejey = [G.posiciones[i][1] for i in N]
    # print(ejex, ejey)
    plt.scatter(ejex, ejey)
    for e in E:
        i1 = N.index(e[0])
        i2 = N.index(e[1])
        plt.plot((ejex[i1], ejex[i2]), (ejey[i1], ejey[i2]))
    plt.show()


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=50
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    # print(args.verbose)
    # print(args.iters)
    # print(type(args.file_name))
    # print(args.file_name)
    # print(args.temp)
    # return

    # TODO: Borrar antes de la entrega
    # grafo1 = ([1, 2, 3, 4, 5, 6, 7],
    #           [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])

    # Creamos nuestro objeto LayoutGraph
    # layout_gr = LayoutGraph(
    #     grafo1,  # TODO: Cambiar para usar grafo leido de archivo
    #     iters=args.iters,
    #     refresh=1,
    #     c1=0.1,
    #     c2=5.0,
    #     verbose=args.verbose
    # )

    grafo = lee_grafo_archivo(args.file_name)
    # N, E = grafo

    layoutG = LayoutGraph(grafo,
                          iters=args.iters,
                          refresh=1,
                          c1=0.01,
                          c2=100,
                          verbose=args.verbose,
                          temp=100)

    # Ejecutamos el layout
    layout(layoutG)
    return


if __name__ == '__main__':
    main()

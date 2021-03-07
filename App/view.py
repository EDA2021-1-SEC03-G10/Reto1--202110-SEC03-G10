"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
import sys
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los videos con más vistas y que son tendencia en un país")
    print("3- Consultar video que ha sido tendencia para un país")
    print("4- Consultar video que más dias ha sido tendencia para una categoría")
    print("5- Consultar videos con más likes en un pais")
    print("0- Salir")

def initCatalog(tipo_representacion):
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog(tipo_representacion)

def printResults(ord_videos, sample=3): 
    size = lt.size(ord_videos) 
    if size > sample: 
        print("Los primeros ", sample, " videos ordenados son:") 
        i=0 
        while i <= sample: 
            video = lt.getElement(ord_videos,i) 
            print('Trending_date: ' + video['trending_date'] + ' Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + 'publish_time: ' + video['publish_time'] +
                    'views: '+ video['views'] + 'likes: '+ video['likes'] + 'dislikes: '+ video['dislikes']) 
            i+=1

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("1- ARRAY_LIST")
        print("2- LINKED_LIST")
        tipo_representacion = input ("Seleccione el tipo de representación deseado para la lista\n")
        print("Cargando información de los archivos ....")
        catalog = initCatalog(tipo_representacion)
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categories'])))

    elif int(inputs[0]) == 2: 
        size = int(input("Indique tamaño de la muestra: ")) 
        if size > lt.size(catalog['videos']):
            print ("el tamaño de muestra solicitado excede la cantidad de datos de videos cargados")
        else:
            print("1- Selection_sort")
            print("2- Insertion_sort")
            print("3- Shell_sort")
            print("4- Merge_sort")
            print("5- Quick_sort")
            tipo_ordenamiento = input ("Seleccione el tipo de algoritmo de ordenamiento que desea\n")
            result = controller.sortVideos(catalog, int(size), tipo_ordenamiento) 
            print("Para la muestra de", size, " elementos, el tiempo (mseg) es: ", str(result[0])) 
            printResults(result[1],size)

        pass

    else:
        sys.exit(0)
sys.exit(0)


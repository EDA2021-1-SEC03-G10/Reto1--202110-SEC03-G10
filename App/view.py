
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

def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()

def printResults(ord_videos): 
    size = lt.size(ord_videos) 
    #if size > sample: 
        #print("Los primeros ", sample, " videos ordenados son:") 
    i=1 
    while i <= size: 
        video = lt.getElement(ord_videos,i) 
        print('Trending_date: ' + video['trending_date'] + ' Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + 'publish_time: ' + video['publish_time'] +
                'views: '+ video['views'] + 'likes: '+ video['likes'] + 'dislikes: '+ video['dislikes']) 
        i+=1

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)

    video = lt.firstElement(catalog['videos'])
    print( 'Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + ' Trending_date: ' + video['trending_date'] + 
    ' country: ' + video['country'] + ' views: '+ video['views'] + ' likes: '+ video['likes'] + ' dislikes: '+ video['dislikes'])

    for category in lt.iterator(catalog['categories']):
        print  ( 'id: ' + str(category['id']) + ' name: ' + category['name'])

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categories'])))

    elif int(inputs[0]) == 2: 
        size = int(input("Indique el número de videos que quiere listar: ")) 
        pais = input ("Ingrese el país para el cual desea realizar la consulta: ")
        categoria = input ("Ingrese la categoría que quiere consultar: ")
        if size > lt.size(catalog['videos']):
            print ("el tamaño de muestra solicitado excede la cantidad de datos de videos cargados")
        else:
            result = controller.sortVideos(catalog, size, pais, categoria) 

        printResults(result)

    elif int(inputs[0]) == 3:
        country = input ("Ingrese el país para el cual desea realizar la consulta: ")
        [result, count] = controller.getTrendingVideoByCountry(catalog, country)

        video = result
        print( 'Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + ' Country: ' + video['country'] + ' Días: '+ str(count))

    else:
        sys.exit(0)
sys.exit(0)


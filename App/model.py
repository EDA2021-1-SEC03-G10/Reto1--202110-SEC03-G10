"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import selectionsort as ss
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Sorting import quicksort as qs


assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipo_representacion):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos. Adicionalmente crea una lista vacia para guardar el título, el canal, 
    fecha de tendencia, pais, vistas, me gusta, no me gusta. Retorna el catalogo inicializado.
    title, cannel_title, trending_date, country, views, likes, dislikes
    """
    catalog = {'videos': None,
               'channels': None,
               'categories':None,
               'countries':None,
               'tags': None}
    if tipo_representacion == 2:

        catalog['videos'] = lt.newList()

        catalog['channels'] = lt.newList('LINKED_LIST',
                                        cmpfunction = comparechannels)
        catalog['categories'] = lt.newList('LINKED_LIST',
                                    cmpfunction = comparecategories)
        catalog['countries'] = lt.newList('LINKED_LIST',
                                    cmpfunction = comparecountries)
        catalog['tags'] = lt.newList('LINKED_LIST',
                                    cmpfunction=comparetags)

    else:
        catalog['videos'] = lt.newList()

        catalog['channels'] = lt.newList('ARRAY_LIST',
                                        cmpfunction = comparechannels)
        catalog['categories'] = lt.newList('ARRAY_LIST',
                                    cmpfunction = comparecategories)
        catalog['countries'] = lt.newList('ARRAY_LIST',
                                    cmpfunction = comparecountries)
        catalog['tags'] = lt.newList('ARRAY_LIST',
                                    cmpfunction=comparetags)


    return catalog
    

# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    # Se obtienen los canales de cada video y se adicionan
    channel = video['channel_title']
    lt.addLast(catalog['channels'], channel)
    # Se obtienen los paises de cada video y se adicionan
    country = video['country']
    lt.addLast(catalog['countries'], country)
    #Se obtienen los tags de cada video
    tags = video['tags'].split("|")
    # Cada tag, se crea en la lista de videos del catalogo, y se
    # crea un video en la lista de dicho tag (apuntador al video)
    for tag in tags:
        lt.addLast(catalog['tags'], tag)

def addCountry(catalog, countryname, video):
    """
    Adiciona un pais a lista de paises, la cual guarda referencias
    a los videos de dicho pais
    """
    countries = catalog['countries']
    poscountry = lt.isPresent(countries, countryname)

    if poscountry > 0:
        country = lt.getElement(countries, poscountry)

    else:
        country  = newContry(countryname)
        lt.addLast(countries, country)
    lt.addLast(country['videos'], video)

def addChannel(catalog, channelname, video):
    """
    Adiciona un canal a lista de canales, la cual guarda referencias
    a los videos de dichos canales
    """
    channel= catalog['channels']
    poschannel = lt.isPresent(channels, channelname)

    if poschannel > 0:
        channel = lt.getElement(channels, poschannel)
        
    else:
        channel = newChannel(channelname)
        lt.addLast(channels, channel)
    lt.addLast(channel['videos'], video)   

def addTag(catalog, tagname, video):
    """
    Adiciona un tag a lista de tags, la cual guarda referencias
    a los videos de dichos tags
    """
    tag= catalog['tags']
    postag = lt.isPresent(tags, tagname)

    if postag > 0:
        tag = lt.getElement(tags, postag)

    else:
        tag = newTag(tagname)
        lt.addLast(tags, tag)
    lt.addLast(tag['videos'], video)  


def addCategory(catalog, category):
    """
    Adiciona una categoria a la lista de categorías
    """
    c = newCategory(category['id'], category['name'])
    lt.addLast(catalog['categories'], c)


# Funciones para creacion de datos

def newCountry(name):
    """
    Crea una nueva estructura para modelar los videos de
    un pais.
    """
    country = {'name': "", "videos": None}
    country['name'] = name
    country['videos'] = lt.newList('ARRAY_LIST')
    return country

def newChannel(name):
    """
    Crea una nueva estructura para modelar los videos de
    un canal.
    """
    channel= {'name': "", "videos": None}
    channel['name'] = name
    channel['videos'] = lt.newList('ARRAY_LIST')
    return channel

def newTag(name):
    """
    Crea una nueva estructura para modelar los videos de
    un tag.
    """
    tag= {'name': "", "videos": None}
    tag['name'] = name
    tag['videos'] = lt.newList('ARRAY_LIST')
    return tag

def newCategory(id, name):
    """
    Esta estructura almancena las categorías utilizados para marcar videos.
    """
    category = {'name': '', 'id': ''}
    category['name'] = name
    category['id'] = id
    return category

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def comparecountries(countryname, country2):
    if (countryname.lower() in country2['name'].lower()):
        return 0
    return -1

def comparechannels(channelname, channel2):
    if (channelname.lower() in channel2['name'].lower()):
        return 0
    return -1

def comparetags(tagname, tag2):
    if (tagname.lower() in tag2['name'].lower()):
        return 0
    return -1

def comparecategories(categoryname, category):
    return (categoryname == category['name'])

def cmpVideosByViews(video1, video2):
    """ 
     Devuelve verdadero (True) si los 'views' de video1 son menores que los del video2 
     Args: 
     video1: informacion del primer video que incluye su valor 'views' 
     video2: informacion del segundo video que incluye su valor 'views' """

    if video1['views'] < video2['views']:
        return True
    return False

# Funciones de ordenamiento

def sortVideos(catalog, size, tipo_ordenamiento): 
    sub_list = lt.subList(catalog['videos'], 0, size) 
    sub_list = sub_list.copy() 
    start_time = time.process_time() 
    if tipo_ordenamiento == 1:
        sorted_list = ss.sort(sub_list, cmpVideosByViews) 
    elif tipo_ordenamiento == 2:
        sorted_list = ins.sort(sub_list, cmpVideosByViews)
    elif tipo_ordenamiento == 3:
        sorted_list = sa.sort(sub_list, cmpVideosByViews)
    elif tipo_ordenamiento == 4:
        sorted_list = mg.sort(sub_list, cmpVideosByViews)
    else:
        sorted_list = qs.sort(sub_list, cmpVideosByViews)

    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000 
    return elapsed_time_mseg, sorted_list

    
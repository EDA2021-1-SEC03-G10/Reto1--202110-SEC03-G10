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

def newCatalog():
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
     Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2 
     Args: 
     video1: informacion del primer video que incluye su valor 'views' 
     video2: informacion del segundo video que incluye su valor 'views' """

    if video1['views'] > video2['views']:
        return True
    return False

# Funciones de ordenamiento

def sortVideos(catalog, n, country, category):

    index_category = 1

    while category.lower() not in lt.getElement(catalog["categories"], index_category)["name"].lower() :
        index_category += 1

    id_category = lt.getElement(catalog["categories"],index_category)["id"]

    por_pais= mg.sort (catalog ["videos"], cmpVideosByCountry)
    index_inicio = 1

    while country not in lt.getElement(por_pais, index_inicio)["country"] :
        index_inicio += 1

    index_fin = index_inicio

    while country in lt.getElement(por_pais, index_fin)["country"] :
        index_fin += 1
        if index_fin > lt.size(por_pais):
            break

    sub_list = lt.subList(por_pais, index_inicio, index_fin-index_inicio)
    
    por_categoria= mg.sort (sub_list, cmpVideosByCategory)
    index_inicio = 1

    while lt.getElement(por_categoria, index_inicio)["category_id"] != id_category :
        index_inicio += 1

    index_fin = index_inicio

    while lt.getElement(por_categoria, index_fin)["category_id"] == id_category  :
        index_fin += 1

    sub_list = lt.subList(por_categoria, index_inicio, index_fin-index_inicio)

    por_vistas = mg.sort(sub_list, cmpVideosByViews)

    sub_list = lt.subList(por_vistas, 1, n)


    return sub_list

def getTrendingVideoByCountry(catalog, country):
    por_pais= mg.sort (catalog ["videos"], cmpVideosByCountry)

    index_inicio = 1

    while country not in lt.getElement(por_pais, index_inicio)["country"] :
        index_inicio += 1

    index_fin = index_inicio

    while country == lt.getElement(por_pais, index_fin)["country"] :
        index_fin += 1
        if index_fin > lt.size(por_pais):
            break
    
    sub_list = lt.subList(por_pais, index_inicio, index_fin-index_inicio)

    

    por_nombre = mg.sort (sub_list, cmpVideosByName)

    name = ""
    max_index = 0
    max_count = 0
    count = 0
    index = 0
    i = 1

    while i <= lt.size(por_nombre):
        if name.lower() == lt.getElement(por_nombre, i)["title"]:
            count += 1
        else:
            name = lt.getElement(por_nombre, i)["title"]
            index = i
            count = 1
        
        if count > max_count:
            max_index = index
            max_count = count
        i += 1

    return [lt.getElement(por_nombre, max_index), max_count]



def getTrendingVideoByCategory(catalog, category):

    index_category = 1

    while category.lower() not in lt.getElement(catalog["categories"], index_category)["id"].lower() :
        index_category += 1

    id_category = lt.getElement(catalog["categories"],index_category)["id"]
    por_categoria= qs.sort (catalog["videos"], cmpVideosByCategory)
    index_inicio = 1

    while lt.getElement(por_categoria, index_inicio)["category_id"] != id_category :
        index_inicio += 1

    index_fin = index_inicio

    while lt.getElement(por_categoria, index_fin)["category_id"] == id_category  :
        index_fin += 1

    sub_list = lt.subList(por_categoria, index_inicio, index_fin-index_inicio)

    por_nombre = mg.sort (sub_list, cmpVideosByName)

    name = ""
    cannel=""
    max_index = 0
    max_count = 0
    count = 0
    index = 0
    i = 1
    id=0
    while i <= lt.size(por_nombre):
        if name.lower() == lt.getElement(por_nombre, i)["title"]:
            count += 1
        else:
           
            index = i
            count = 1
        
        if count > max_count:
            max_index = index
            max_count = count
            name = lt.getElement(por_nombre["title"], i)["title"]
            cannel=lt.getElement(por_nombre["channel_title"],i)["channel"]
            id=int(lt.getElement(por_nombre["category_id"],i)["category_id"])

        i += 1
    result= {"Titulo: ":name , "Canal: ":cannel, "Id: ":id, "Dias tendencia: ": max_count}
    return result
        

    
def getTrendingVideoByLikes(catalog,country,tag):

    por_pais= mg.sort (catalog ["videos"], cmpVideosByCountry)
    index_inicio=1

    while country not in lt.getElement(por_pais, index_inicio)["country"] :
        index_inicio +=1

    index_fin = index_inicio

    while country in lt.getElement(por_pais, index_fin)["country"] :
        index_fin += 1

    sub_list = lt.subList(por_pais, index_inicio, index_fin-index_inicio)
    
    por_tag= qs.sort (sub_list, cmpVideosByTag)
    index_inicio = 1
    
    while lt.getElement(por_tag, index_inicio)["tags"] != tag :
        index_inicio += 1

    index_fin = index_inicio

    while lt.getElement(por_tag, index_fin)["tags"] == tag :
        index_fin += 1

    sub_list = lt.subList(por_tag, index_inicio, index_fin-index_inicio)

    por_likes = qs.sort(sub_list, cmpVideosByLikes)

    video1=[lt.getElement(por_likes["title"],1)["title"],lt.getElement(por_likes["cannel_title"],1)["cannel_title"],lt.getElement(por_likes["publish_time"],1)["publish_time"],lt.getElement(por_likes["views"],1)["views"],lt.getElement(por_likes["likes"],1)["likes"],lt.getElement(por_likes["dislikes"],1)["dislikes"],lt.getElement(por_likes["tags"],1)["tags"]]
    video2=[lt.getElement(por_likes["title"],2)["title"],lt.getElement(por_likes["cannel_title"],2)["cannel_title"],lt.getElement(por_likes["publish_time"],2)["publish_time"],lt.getElement(por_likes["views"],2)["views"],lt.getElement(por_likes["likes"],2)["likes"],lt.getElement(por_likes["dislikes"],2)["dislikes"],lt.getElement(por_likes["tags"],2)["tags"]]
    video3=[lt.getElement(por_likes["title"],3)["title"],lt.getElement(por_likes["cannel_title"],3)["cannel_title"],lt.getElement(por_likes["publish_time"],3)["publish_time"],lt.getElement(por_likes["views"],3)["views"],lt.getElement(por_likes["likes"],3)["likes"],lt.getElement(por_likes["dislikes"],3)["dislikes"],lt.getElement(por_likes["tags"],3)["tags"]]

    return [video1,video2,video3]
    
def cmpVideosByCountry(video1, video2):
    """ 
     Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2 
     Args: 
     video1: informacion del primer video que incluye su valor 'views' 
     video2: informacion del segundo video que incluye su valor 'views' """

    if video1['country'].lower() > video2['country'].lower():
        return True
    return False

def cmpVideosByCategory(video1, video2):
    """ 
     Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2 
     Args: 
     video1: informacion del primer video que incluye su valor 'views' 
     video2: informacion del segundo video que incluye su valor 'views' """

    if video1['category_id'] > video2['category_id']:
        return True
    return False  

def cmpVideosByName(video1, video2):
    if video1['title'].lower() > video2['title'].lower():
        return True
    return False

def cmpVideosByTag(video1,video2):
    if video1["tag"].lower() > video2["tag"].lower():
        return True
    return False

def cmpVideosByLikes(video1,video2):
    if video1["likes"].lower()>video2["likes"].lower():
        return True

    return False
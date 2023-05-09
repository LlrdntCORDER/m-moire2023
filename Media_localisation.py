import json
from tqdm import tqdm
import time
import os
import re

###############################################################################
#DIVERS#

def result_write(list):
    """
    Création d'un fichier texte 'result.txt' sur base d'une liste de :
    - str
    - int
    """
    with open ("result.txt", "a+", encoding = "utf-8") as rf:
        for i in list:
            rf.write(i)

def fusion (dict1,dict2):
    """
    Fusion de deux dictionnaires (-> prend deux dictionnaires en entrée):
    - mise en commun des keys identiques (dict1[key]+dict2[key])
    - rassemblement des keys !=
    """
    for i in dict1:
        if i in dict2:
            if type(dict1[i]) is str:
                pass
            else:
                dict2[i]+=dict1[i]
        else:
            dict2[i] = dict1[i]
    return(dict2)


###############################################################################
#PREPARATION#

def __create_list (json_database,mode):
    """
    Création d'une liste de noms de médias créée sur base du document json
    reprenant une série de médias nationaux.

    => MODIFIER LA STRUCTURE POUR Y JOINDRE PLUS D'INFORMATIONS
    """
    list_temp = []
    if mode == "name_mention":
        with open(json_database, "r+", encoding = "utf-8") as file:
            doclist =file.readlines()
            for j in doclist:
                item = json.loads(j)
                list_temp.append(item["name"])
        media_list = [x.lower() for x in list_temp]
    elif mode == "rsid_publication" :
        with open(json_database, "r+", encoding = "utf-8") as file:
            doclist =file.readlines()
            for j in doclist:
                item = json.loads(j)
                list_temp.append(item["RS_ID"])
        media_list = list_temp
    elif mode == "rsid_mention":
        with open(json_database, "r+", encoding = "utf-8") as file:
            doclist =file.readlines()
            for j in doclist:
                item = json.loads(j)
                list_temp.append(str(item["RS_ID"]))
        media_list = list_temp
    return media_list

###############################################################################
#ANALYSE#

def __find_terms_in_tweet_content_LIST (str, list, prec):
    """
    Vérifie si un terme mentionné dans une liste apparait dans le contenu
    d'un tweet.

    Prend en entrée un str (contenu du tweet) et une liste de str.
    """
    final_list = []
    str = str.lower()
    for m in list :
        if prec == "relative":
            if m in str:
                final_list.append(m)
            else:
                pass
        elif prec == "strict":
            if m in str:
                final_list.append(m)
            else:
                pass
    return (final_list)

def __term_counter (file,medialist,mode):
    """
    Recense le nombre de fois qu'un terme est identifié dans un tweet pour un
    document json complet.

    Retourne une dictionnaire en sortie.
    """
    result = {}
    with open (file, "r", encoding = "utf-8") as file:
        list_tweet = file.readlines()
        for i in list_tweet:
            item = json.loads(i)
            if mode == "content":
                temp_list=__find_terms_in_tweet_content_LIST(item["content"],medialist,"relative") #changer nom de fonction ici
            else :
                temp_list=__find_terms_in_tweet_content_LIST(item["user"]["username"],medialist,"relative") #changer nom de fonction ici
            for j in temp_list :
                if j in result:
                    result[j]+=1
                else:
                    result[j]=1
    return result

def __publication_counter(file,medialist):
    result = {}
    with open (file, "r", encoding = "utf-8") as file:
        list_tweet = file.readlines()
        for i in list_tweet:
            item = json.loads(i)
            account = item["user"]["username"]
            for j in medialist:
                if j == account:
                    if j in result:
                        result[j]+=1
                    else:
                        result[j]=1
    return result

def analyse_global (folder,json_db,mode):
    """
    Permet l'analyse globale de la database selon la structure :
    - Data
        - #metoo
            - 2017
            - 2018
            - ...
            - 2022
        - #metooindia
        -...
    Prend d'office en entrée le dossier 'data'
    """
    list_year = []
    if mode not in ["rsid_publication","rsid_mention","name_mention"]:
        print ("Mode non pris en charge")
    else:
        final_result={}
        dir_list = os.listdir(folder)
        if mode =="name_mention":
            medialist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __term_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist,"content")
                        final_result = fusion(final_result,counter)
                    list_year.append(final_result)
            return final_result
        elif mode == "rsid_publication":
            medialist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __term_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist,"content")
                        final_result = fusion(final_result,counter)
                    list_year.append(final_result)
            return final_result
        elif mode == "rsid_mention":
            medialist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __publication_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist)
                        final_result = fusion(final_result,counter)
                    list_year.append(final_result)
            return final_result

def analyse_month_by_month(folder,json_db,mode):
    """
    Permet l'analyse globale de la database selon la structure :
    - Data
        - #metoo
            - 2017
            - 2018
            - ...
            - 2022
        - #metooindia
        -...
    Prend d'office en entrée le dossier 'data'
    """
    if mode not in ["rsid_publication","rsid_mention","name_mention"]:
        print ("Mode non pris en charge")
    else:
        final_result={}
        final_list=[]
        dir_list = os.listdir(folder)
        if mode == "name_mention":
            medialist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __term_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist,"content")
                        final_result["Dynamic"] = str(j)
                        final_result["Year"] = str(k)
                        final_result["Month"] = str(l)
                        final_result["Counter_content"] = counter
                        print (final_result)
                        final_list.append(final_result)
                        final_result={}
            return final_list
        elif mode == "rsid_publication":
            medialist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __term_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist,"rsid_publication")
                        final_result["Dynamic"] = str(j)
                        final_result["Year"] = str(k)
                        final_result["Month"] = str(l)
                        final_result["Rsid_publication_counter"] = counter
                        print (final_result)
                        final_list.append(final_result)
                        final_result={}
            return final_list
        elif mode == "rsid_mention":
            termlist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __term_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist,"content")
                        final_result["Dynamic"] = str(j)
                        final_result["Year"] = str(k)
                        final_result["Month"] = str(l)
                        final_result["Rsid_mention_counter"] = counter
                        print (final_result)
                        final_list.append(final_result)
                        final_result={}
        elif mode == "rsid_mention":
            termlist = __create_list(json_db,mode)
            for j in dir_list : #secondary movments
                secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
                for k in secondary_movments_list: #year_list
                    year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                    print (k)
                    for l in tqdm(year_list):
                        counter = __term_counter(str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l),medialist,"content")
                        final_result["Dynamic"] = str(j)
                        final_result["Year"] = str(k)
                        final_result["Month"] = str(l)
                        final_result["rsid_mention_counter"] = counter
                        print (final_result)
                        final_list.append(final_result)
                        final_result={}
            return final_list

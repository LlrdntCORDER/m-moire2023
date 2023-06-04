###############################################################################
#Import de modules externes#
import json
from tqdm import tqdm
import os
###############################################################################
#Fonctions diverses#

def result_write(list):
    """
    Création d'un fichier texte 'result.txt' sur base d'une liste (mentionnée en argument) de :
    - str
    - int
    """
    with open ("result.txt", "a+", encoding = "utf-8") as rf:
        for i in list:
            rf.write(i)

def fusion (dict1,dict2):
    """
    Cette fonction permet de fusionner de deux dictionnaires mentionnés en argument :
    - mise en commun des valeurs comprises dans des clefs identiques (dict1[key]+dict2[key])
    - ajout des clefs différentes

    Retourne un dictionnaire issu de la fusion des deux dictionnaires mentionnés en arguments.
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
#Préparation#

def __create_list (json_database,mode):
    """
    Création d'une liste de noms de médias créée sur base du document json
    reprenant une série de médias nationaux.

    Ce programme peut fonctionner avec différents modes (à mentionner en argument): 
        - name_mention - la liste créée comprendra alors le nom des médias
        - rsid_publication ou rsid_mention - la liste créée comprendra alors l'identifiant twitter des médias
    
    Nécessite le(s) module(s) externe(s):
        - json
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
#Analyse#

def __find_terms_in_tweet_content_LIST (str, list, prec):
    """
    Le programme prend en argument une chaine de caractère (str), une liste de termes, et un mode (prec).
    Il vérifie si les termes compris dans la liste apparaissent dans une chaine de caractère.

    Ce programme fonctionne sur base de deux modes de précision à préciser en argument (prec):
        - relative (vérification si un terme apparait "dans" un terme)
            Pour illustrer:
                abba in abbam -> TRUE
        - strict (vérification si un terme est équivalent à un autre terme)
            Pour illustrer:
                abba == abbam -> FALSE
    
    Le programme retourne une liste des termes de la liste trouvés dans la chaine de caractère.
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
            if m == str:
                final_list.append(m)
            else:
                pass
            
    return (final_list)

def __term_counter (file,medialist,mode):
    """
    Cette fonction va nous permettre de vérifier combien de fois les termes compris dans une liste (medialist)
    apparaissent dans un ensemble de tweets comme compris dans notre base de données 'data' (file). Il retourne
    un dictionnaire construit sur cette structure : {terme_de_la_liste : nombre d'occurences}.

    Ce programme fonctionne selon différents modes :
        - content : recherche dans l'attribut 'content' du tweet
        - Username : recherche dans l'attribut 'username' du tweet
    
    Nécessite le(s) module(s) externe(s):
        - json
    """
    result = {}
    with open (file, "r", encoding = "utf-8") as file:
        list_tweet = file.readlines()
        for i in list_tweet:
            item = json.loads(i)
            if mode == "content":
                temp_list=__find_terms_in_tweet_content_LIST(item["content"],medialist,"relative") #changer nom de fonction ici
            elif mode == "username":
                temp_list=__find_terms_in_tweet_content_LIST(item["user"]["username"],medialist,"relative") #changer nom de fonction ici
            for j in temp_list :
                if j in result:
                    result[j]+=1
                else:
                    result[j]=1
    return result

def __publication_counter(file,medialist):
    """
    Ce programme permet de compter le nombre de tweets publiés par les comptes compris dans une liste
    d'identifiants twitter (mentionné en argument - medialist).
    Il fonctionne sur base d'une base de données compris dans une
    base de données construite sur base de cette structure:
    - Data
        - #metoo
            - 2017
            - 2018
            - ...
            - 2022
        - #metooindia
        -...
    
    Il retourne un dictionnaire reprenant chaque identifiant de compte et son nombre de publications.

    Nécessite le(s) module(s) externe(s):
        - json
    """
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
    Permet l'analyse globale de la base de données construite sur base de cette structure :
    - Data
        - #metoo
            - 2017
            - 2018
            - ...
            - 2022
        - #metooindia
        -...
    
    Le programme prend en entrée :
        - une base de données (folder)
        - une base de données json reprenant une liste de compte que l'on comprendra dans notre analyse.
        Ce dictionnaire doit comprendre des éléménets structurés de cette manière :
        {"name": "The New York Times", "RS_ID": "@nytimes", "country": "United States"}

    Le dernier argument représente le mode d'analyse:
        -rsid_publication -> analyse (sur base de l'identifiant Twitter d'un compte) du nombre de publications partagées par les comptes compris dans la base de
        données json_db.
        -rsid_mention ->  analyse (sur base de l'identifiant Twitter d'un compte) du nombre de publications partagées par les comptes compris dans la base de
        données json_db.
        -name_mention ->  analyse (sur base du nom d'un compte) du nombre de publications partagées par les comptes compris dans la base de
        données json_db.
    
    Le programme une liste de dictionnaires reprenant les résultats globaux de l'analyse.
    
    Nécessite le(s) module(s) externe(s):
        - json
        - os
        - tqdm
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
    Permet l'analyse globale de la base de données construite sur base de cette structure :
    - Data
        - #metoo
            - 2017
            - 2018
            - ...
            - 2022
        - #metooindia
        -...
    
    Le programme prend en entrée :
        - une base de données (folder)
        - une base de données json reprenant une liste de compte que l'on comprendra dans notre analyse.
        Ce dictionnaire doit comprendre des éléménets structurés de cette manière :
        {"name": "The New York Times", "RS_ID": "@nytimes", "country": "United States"}

    Le dernier argument représente le mode d'analyse:
        -rsid_publication -> analyse (sur base de l'identifiant Twitter d'un compte) du nombre de publications partagées par les comptes compris dans la base de
        données json_db.
        -rsid_mention ->  analyse (sur base de l'identifiant Twitter d'un compte) du nombre de publications partagées par les comptes compris dans la base de
        données json_db.
        -name_mention ->  analyse (sur base du nom d'un compte) du nombre de publications partagées par les comptes compris dans la base de
        données json_db.
    
    Le programme une liste de dictionnaires reprenant les résultats mensuels de l'analyse.
    
    Nécessite le(s) module(s) externe(s):
        - json
        - os
        - tqdm
        
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

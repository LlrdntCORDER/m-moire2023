###############################################################################
#Import de modules externes#
from langdetect import detect

###############################################################################
#Pré-traitement#
def __pre_clean_url (str):
    """
    Fonction permettant de supprimer des liens dans une chaîne de caractère mentionnée en argument
    de la fonction.
    """
    list = str.split()
    counter=0
    for i in list:
        if "https" in i:
            if len(i) == 23:
                list.remove(i)
                counter+=1
            else:
                new_i = i [23:(len(i))]
                list[counter] = new_i
                counter+=1
        else:
            counter+=1
            pass
    result = ""
    for j in list:
        if j != list[len(list)-1]:
            result+=j
            result+=" "
        else :
            result+=j
    return result

def __detection(str):
    """
    Fonction permettant la détection du langage utilisé dans une chaine de caractère mentionnée en
    entrée.

    Retourne en sortie l'identifiant de langage selon la norme ISO639-1

    Module utilisé :
    - langdetect
    """
    try:
        return (detect(str))
    except:
        pass

###############################################################################
#Analyse#

def language_analyse (str):
    """
    Analyse plus globale effectuée sur base des deux fonctions de
    pré-traitement:
    - Suppression des possibles urls
    - Définition de la langue utilsée

    Modules :
    - langdetect
    """
    str_result = __pre_clean_url (str)
    if len(str)>0:
        lg = __detection(str_result)
        return (lg)
    else:
        pass

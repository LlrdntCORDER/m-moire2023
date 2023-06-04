###############################################################################
#Import de modules externes#
import json
from tqdm import tqdm
import time
import os
import media_localisation.py as ml

###############################################################################
#Fonction#

def analyse_year(folder, outfile):
    """
    FONCTION PERMETTANT DE REPÉRER L'ENSEMBLE DES MENTIONS EFFECTUÉES DANS UN CORPUS DE 
    TWEETS ET DE CREER UN DOCUMENT CSV ADAPTE AU LOGICIEL GEPHY (représentation de réseau
    des mentions effectuées)
    
   Ce programme prend en entrée le dossier 'data' construit selon la structure :
    - Data
        - #metoo
            - 2017
            - 2018
            - ...
            - 2022
        - #metooindia
        -...
    Il retourne un document (nommé selon l'argument 'outfile') au format .csv (extension à mentionner dans le 
    nom du document)).
    Le document .csv de sortie sera structuré selon cette structure:
    'identifiant de l'utilisateur ayant mentionné, identifiant de l'utilisateur  mentionné'
    """
    with open (outfile,"w",encoding='utf-8') as result_file:
        dir_list = os.listdir(folder)
        for j in dir_list : #secondary movments
            secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
            print(j)
            for k in tqdm(secondary_movments_list): #year_list
                year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                for l in year_list:
                    with open ((str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l)),'r',encoding='utf-8') as file:
                        tweet_list=file.readlines()
                        for it in tweet_list:
                            item = json.loads(it)
                            user = "@"+str(item['user']['username'])
                            text = item['content']
                            list_term = text.split()
                            for term in list_term:
                                if term[0] == "@":
                                    result_file.write (str(user)+","+str(term)+"\n")
                                else:
                                    pass






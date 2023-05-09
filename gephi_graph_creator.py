import json
from tqdm import tqdm
import time
import os
import re

#import media_localisation.py as ml

###############################################################################
#DIVERS#

def analyse_year_crotte(folder):
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
    global_result={}
    global_dict={}
    dir_list = os.listdir(folder)
    for j in dir_list : #secondary movments
        secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
        print(j)
        for k in tqdm(secondary_movments_list): #year_list
            year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
            for l in year_list:
                with open ((str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l)),'r',encoding='utf-8') as file:
                    tweet_list=file.readlines()
                    monthly_dict={}
                    for it in tweet_list:
                        item = json.loads(it)
                        user = "@"+str(item['user']['username'])
                        print ("1: "+str(user))
                        text = item['content']
                        list_term = text.split()
                        for term in list_term:
                            if term[0] == "@":
                                print ("2: "+str(term))
                                monthly_dict[user]=term
                                global_dict[user]=term
                                print(global_dict)
                                time.sleep(4)
                            else:
                                pass
                    global_result[l]=monthly_dict
    print (global_dict)
    with open ("RESULT_GEPHY2016_TEST.csv","w",encoding='utf-8') as result_file:
        for global_counted in global_dict:
            result_file.write (str(global_counted)+","+str(global_dict[global_counted]))
            result_file.write("\n")


def analyse_year(folder):
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
    with open ("RESULT_GEPHY2022_FULL.csv","w",encoding='utf-8') as result_file:
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




analyse_year('Data_BIS')

###############################################################################
#Import de modules externes#
import json
from tqdm import tqdm
import media_localisation as ml
import os

###############################################################################
#Analyse#
def metadata_analyse_year(folder,json_db):
    """
    Cette fonction permet d'analyser les métadonnées des tweets partagés par les comptes
    compris dans une base de données .json (mentionnée en argument)

    Le programme prend en entrée :
        - une base de données (folder)
        - une base de données json reprenant une liste de compte que l'on comprendra dans notre analyse.
        Ce dictionnaire doit comprendre des éléménets structurés de cette manière :
        {"name": "The New York Times", "RS_ID": "@nytimes", "country": "United States"}
    
    Il retourne un dictionnaire reprenant le totals du nombre de mentions 'like', de retweets et de réponses
    engendrées par les comptes mentionnés dans liste 'json_db' (et le nombre total de tweets analysés afin de nous
    permettre de calculer les moyennes ultérieurement). 

     Nécessite le(s) module(s) externe(s):
        - json
    """
    global_result={}
    global_dict={}
    medialist = ml.__create_list (json_db,'rsid_mention')
    dir_list = os.listdir(folder)
    print (dir_list)
    with open ("md_result_AVERAGETOTAL.csv",'w',encoding='utf-8') as result_file:
        for j in tqdm(dir_list) : #secondary movments
            secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
            for k in secondary_movments_list: #year_list
                year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                for l in year_list:
                    with open ((str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l)),'r',encoding='utf-8') as file:
                        count=0
                        tweet_list=file.readlines()
                        global_result={'dynamic':"O",'like_month':0,'retweet_month':0,'reply_month':0,'count':0}
                        global_result['Dynamic']=j
                        global_result['Date']=l
                        for it in tqdm(tweet_list):
                            item = json.loads(it)
                            user="@"+str(item['user']['username'])
                            if user in medialist:
                                global_result['like_month']+=item['likeCount']
                                global_result['retweet_month']+=item['retweetCount']
                                global_result['reply_month']+=item['replyCount']
                                global_result['count']+=1
                        dynamique=global_result['Dynamic']

                        datum=global_result['Date']
                        result_file.write(str(dynamique)+","+str(datum)+","+str(global_result['like_month'])+","+str(global_result['retweet_month'])+","+str(global_result['reply_month'])+","+str(global_result['count'])+"\n")



def metadata_analyse (folder):
    """
    Cette fonction permet d'analyser les métadonnées des tweets compris dans une base de données 'folder'

    Le programme prend en entrée :
        - une base de données (folder
    
    Il retourne un dictionnaire reprenant le totals du nombre de mentions 'like', de retweets et de réponses
    engendrées par les tweets compris dans la base de données(et le nombre total de tweets analysés afin de nous
    permettre de calculer les moyennes ultérieurement). 

     Nécessite le(s) module(s) externe(s):
        - json
    """
    global_result={}
    global_dict={}
    dir_list = os.listdir(folder)
    with open ("md_result_bis.csv",'w',encoding='utf-8') as result_file:
        for j in tqdm(dir_list) : #secondary movments
            secondary_movments_list = os.listdir (str(folder)+"\\"+str(j))
            for k in secondary_movments_list: #year_list
                year_list = os.listdir (str(folder)+"\\"+str(j)+"\\"+str(k))
                for l in year_list:
                    print(l)
                    with open ((str(folder)+"\\"+str(j)+"\\"+str(k)+"\\"+str(l)),'r',encoding='utf-8') as file:
                        count=0
                        tweet_list=file.readlines()
                        if l in global_result:
                            pass
                        else:
                            global_result[l]={'like_month':0,'retweet_month':0,'reply_month':0,'count':0}
                        for it in tweet_list:
                            item = json.loads(it)
                            global_result[l]['like_month']+=item['likeCount']
                            global_result[l]['retweet_month']+=item['retweetCount']
                            global_result[l]['reply_month']+=item['replyCount']
                            global_result[l]['count']+=1
        print (global_result)
        for month in global_result:
            result_file.write(str(month)+","+str(global_result[month]['like_month'])+","+str(global_result[month]['retweet_month'])+","+str(global_result[month]['reply_month'])+","+str(global_result['count'])+"\n")


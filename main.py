import language_recognition as lr
import media_localisation as ml
import pandas as pd
import json

def analyse_media():
    return(ml.analyse ("Data","media.json","name"))
def analyse_arobase():
    return(ml.analyse ("Data","media.json","arobase"))
def analyse_account():
    return(ml.analyse ("Data","media.json","account"))


dict=analyse_account()

def search_media(term, media_file):
    with open ("medi@.json","r",encoding="utf-8") as media_file:
        list_of_dict = media_file.readlines()
        for k in list_of_dict:
            print
            media=json.loads(k)
            if term.lower() in media["name"].lower() or term.lower() in media["RS_ID"].lower():
                return media
            else:
                pass


def result_out(dict):
    list_to_wrt=[]
    for i in dict:
        media_dict=search_media(i,"medi@.json")
        if media_dict != "Empty":
            media_dict["count"]=int(dict[i])
            list_to_wrt.append(media_dict)
        else:
            pass
    with open ("result.json","w",encoding="utf-8") as wrt_file:
        for j in list_to_wrt:
            wrt_file.write(str(j))
            wrt_file.write("\n")

result_out(dict)


#wrt_file.write('"{"+"name:"+str(i)+","+"count:"+str(dict[i])+"}")
#wrt_file.write("\n")

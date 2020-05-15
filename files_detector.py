import os
import time
def get_finished_words(max_pics_num):
    candidates_words=os.listdir("downloads")
    finished_words=[]
    for candidates_word in candidates_words:
        if(len(os.listdir("downloads/"+candidates_word))>=max_pics_num):
            finished_words.append(candidates_word)
    return finished_words

def get_candidate_words(max_pics_num):
    candidates_words=os.listdir("downloads")
    return candidates_words
def get_files_info():
    finished_words_50=get_finished_words(50)
    finished_words_30=get_finished_words(30)
    finished_words_10=get_finished_words(10)
    print("已完成（50pics）",len(finished_words_50),'  ',len(finished_words_50)/30,"%")
    print("已完成（30pics）",len(finished_words_30),'  ',len(finished_words_30)/30,"%")
    print("已完成（10pics）",len(finished_words_10),'  ',len(finished_words_10)/30,"%")
    #files
    files_num=0
    words=os.listdir("downloads")
    for word in words:
        files_num=files_num+len(os.listdir("downloads/"+word))
    print("文件总数",files_num)

def info_loop():
    while(1):
        get_files_info()
        time.sleep(5)
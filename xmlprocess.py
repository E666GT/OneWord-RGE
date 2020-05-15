from bs4 import BeautifulSoup
from google_images_download import google_images_download  # importing the library
import threading
import time
import files_detector
import requests
class DownloadOperator():
    def __init__(self):
        pass

    #google downloader
    def download_word(self,word,limit=50,offset=0):
        # global current_living_thread
        # current_living_thread=current_living_thread+1
        response = google_images_download.googleimagesdownload()  # class instantiation
        arguments = {
            "keywords": word,
            "limit": limit,#20
            "print_urls": True,
            "offset": offset,
            "chromedriver":"chromedriver.exe",
        }  # creating list of arguments
        paths = response.download(arguments)  # passing the arguments to the function
        # current_living_thread=current_living_thread-1
        # print(word)
    def download_wordlist(self,word_list,limit,finished_word_list):
        for word in word_list:
            if(word in finished_word_list):
                continue
            self.download_word(word,limit=limit)

    #general Downloader
    def UrlDownload(self,url,path):
        try:
            image_url = url
            r = requests.get(image_url)
            with open(path, 'wb') as f:
                f.write(r.content)
        except Exception as err:
            print("UrlDownload Download fail:",err)
    @staticmethod
    def chunks(l,n):
        for i in range(0,len(l),n):
            yield l[i:i+n]

# class  GeneralDownloadOperator():
#     def __init__(self):
#         pass
#     def ImgDownload(self,url,SavePath):


class ynm_processor(object):
    def __init__(self):
        self.ynm_xml = open("ynm3000.xml", 'rb')
        self.ynm_word_list_txt = open("ynm_word_list.txt", "w")
        self.ynm_bs = BeautifulSoup(self.ynm_xml, "xml")
        self.items=self.ynm_bs.find_all("item")
        self.ynm_word_list = []
        for item in self.items:
            word_item = item.find_all("word")[0]
            self.ynm_word_list.append(word_item.get_text())
        # 去重
        self.ynm_word_list = list(set(self.ynm_word_list))
    def getWordList(self):
        return self.ynm_word_list
    def getWordAns(self):
        return 0
    def getFullbs(self):
        return self.ynm_bs
    def getWordTrans(self,word):
        try:
            target_words=self.ynm_bs.find_all("word",text=word)
            target_word=target_words[0]
            target_item=target_word.parent
            # target_trans=target_item["trans"]
            target_trans=target_item.find_all("trans")[0].text
            # for son in target_item.contents:
            #     print(son.__dict__)
            return target_trans
        except:
            return "当前词库无翻译，等待更新"

if __name__=="__main__":
    now=time.time()
    ynmOP=ynm_processor()
    print(time.time()-now)
    # downloader=DownloadOperator()
    # url="http://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=http%3A%2F%2Fimg04.hc360.com%2Fcoatings%2F201605%2F201605261752025642.jpg&thumburl=http%3A%2F%2Fimg3.imgtn.bdimg.com%2Fit%2Fu%3D2903151429%2C728494500%26fm%3D26%26gp%3D0.jpg"
    # word="abandon"
    # filename="test55.jpg"
    # path="downloads/"+word+"/"+filename

    # downloader.UrlDownload(url=url,path=path)

    # ynmOP=ynm_processor()
    # print(ynmOP.getWordList())
    # print(ynmOP.getFullbs().prettify())
    # print(ynmOP.getWordTrans("veto"))

    # global max_thread_allowed
    # max_thread_allowed = 50
    # global current_living_thread
    # current_living_thread = 0
    #
    # max_pics_num = 50
    #
    # ynm_xml=open("ynm3000.xml",'rb')
    # ynm_word_list_txt=open("ynm_word_list.txt","w")
    # ynm_bs = BeautifulSoup(ynm_xml,"xml")
    # items=ynm_bs.find_all("item")
    # ynm_word_list=[]
    # for item in items:
    #     word_item=item.find_all("word")[0]
    #     ynm_word_list.append(word_item.get_text())
    # #去重
    # ynm_word_list=list(set(ynm_word_list))
    #
    # #换行
    # words_str=""
    # for word in ynm_word_list:
    #     word=word+"\n"
    #     words_str+=word
    # ynm_word_list_txt.write(words_str)
    # ynm_word_list_txt.close()
    # # print(ynm_word_list)
    # print(len(ynm_word_list))
    #
    #
    # #downlaod
    # # op=operator()
    # # current_living_thread=0
    # # finished_words=files_detector.get_finished_words(30)
    # #
    # # print(list(op.chunks(ynm_word_list,300)))
    # #
    # # for word_list in list(op.chunks(ynm_word_list,300)):
    # #     thread = threading.Thread(target=op.download_wordlist,args=(word_list,50,finished_words,))
    # #     thread.start()
    #
    #


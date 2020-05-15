import random as random
import os
import pandas as pd
import numpy as np
class GlobalOperator(object):
    def __init__(self):
        # self.WordList=["abandon"]#,"abase","abash"
        # self.WordList=["abandon","abase","abash"]#
        # self.WordList=os.listdir("downloads")[:10]
        self.WordList=list(set(os.listdir("downloads")))
        # self.ImageMaxHeight = 1000
        self.ImageMaxWidth = 200
        self.ImageColumns=3
        #打开全局数据库

        self.globaldfFile="global.csv"
        self.GlobalDF=self.InitGlobalDF()
        self.GlobalDF.sort_values("难度",ascending=False)
        pass
    def InitGlobalDF(self):
        globaldfFile=self.globaldfFile
        try:
            GlobalDF = pd.read_csv(globaldfFile)
        except:
            print("需要初始化数据库请稍后")
            GlobalDF = pd.DataFrame(columns=["单词名","忘记次数","记得次数","需要背这个单词","难度","已查看次数"])
            # 初始化df
            loops=0
            for word in self.WordList:
                if (not (word in list(GlobalDF["单词名"]))):
                    print(loops)
                    loops=loops+1
                    # print("not in")
                    GlobalDF.loc[GlobalDF.shape[0] + 1] = {"单词名":word,"忘记次数":0,"记得次数":0,"需要背这个单词":1,"难度":1,"已查看次数":0}
            GlobalDF.to_csv(globaldfFile, index=False)
        return GlobalDF
    def GlobalDf_save(self):
        self.GlobalDF.to_csv(self.globaldfFile,index=False)
    def GetAWord(self):
        return random.choice(self.WordList)
    def GetABatchWordList(self,len,NeedyFilter=1):
        wordlist=self.GetWordListbyDifficulty(ascending=False)[:len]
        wordlist_res=[]
        if(NeedyFilter):
            for word in wordlist:
                if(self.GetWordNeedy(word)): #需要背的单词才载入
                    wordlist_res.append(word)
        return wordlist_res
    def GetAImagePath(self,word):
        path="downloads/"+word+"/test.jpg"
        return path
    def GetAImagePathRoot(self,word):
        path="downloads/"+word+"/"
        return path
    def GetImagesName(self,word):
        images=[]
        # not_allowed_files=[""]
        for file in os.listdir(self.GetAImagePathRoot(word)):
            if(".npy" in file):
                continue
            if(".csv" in file):
                continue
            images.append(file)
        # images=os.listdir(self.GetAImagePathRoot(word))

        return images
    def GetAdaptiveImageSize(self,width,height):
        ratio=height/width
        # if(height>self.ImageMaxHeight):
        #     newh=self.ImageMaxHeight
        #     neww=newh/ratio
        if(width>self.ImageMaxWidth):
            neww=self.ImageMaxWidth
            newh=neww*ratio
        else:
            neww,newh=width,height
        return neww,newh
    # def GetAdaptiveImageScaleRatio(self,width,height):
    #     nw,nh=self.GetAdaptiveImageSize(width,height)
    #     scaleratio_w,scaleratio_h=nw/width,nh/height
    #     return scaleratio_w,scaleratio_h

    #single word
    def GetWordDifficulty(self,word):
        mask = self.GlobalDF["单词名"].str.contains(word)
        difficulty = self.GlobalDF.loc[mask, "难度"].values[0]  # 0~10 10bad 0 health
        return difficulty
    def GetWordNeedy(self,word):
        mask = self.GlobalDF["单词名"].str.contains(word)
        needy = self.GlobalDF.loc[mask, "需要背这个单词"].values[0]  # 0~10 10bad 0 health
        return needy
    def GetWordMemNoTimes(self, word):
        mask = self.GlobalDF["单词名"].str.contains(word)
        memnotimes = self.GlobalDF.loc[mask, "忘记次数"].values[0]  # 0~10 10bad 0 health
        return memnotimes
    def GetWordMemYesTimes(self, word):
        mask = self.GlobalDF["单词名"].str.contains(word)
        times = self.GlobalDF.loc[mask, "记得次数"].values[0]  # 0~10 10bad 0 health
        return times
    def GetWordReadTimes(self, word):
        mask = self.GlobalDF["单词名"].str.contains(word)
        times = self.GlobalDF.loc[mask, "已查看次数"].values[0]  # 0~10 10bad 0 health
        return times

    def AddWordNote(self, word, note):
        word = word
        mask = self.GlobalDF["单词名"].str.contains(word)
        notes = self.GlobalDF.loc[self.GlobalDF["单词名"].str.contains(word), "评论"].values[0]
        if (pd.isna(notes)):
            notes = str(note)
        else:
            notes = notes + "\n" + str(note)
        self.GlobalDF.loc[mask, "评论"] = str(notes)
        self.GlobalDf_save()
        return True
    def SetWordNote(self, word, note):
        word = word
        mask = self.GlobalDF["单词名"].str.contains(word)
        self.GlobalDF.loc[mask, "评论"] = str(note)
        self.GlobalDf_save()
        return True
    def GetWordNote(self,word):
        try:
            notes_already = self.GlobalDF.loc[self.GlobalDF["单词名"].str.contains(word), "评论"].values[0]
        except:
            notes_already=""
            self.SetWordNote(word,notes_already)
        return notes_already

    def SetWordImgHelpful(self, word, ImgHelpful=0):
        word = word
        mask = self.GlobalDF["单词名"].str.contains(word)
        self.GlobalDF.loc[mask, "图片有用"] = ImgHelpful
        self.GlobalDf_save()
        return True

    def GetWordImgHelpful(self, word):
        try:
            ImgHelpful = self.GlobalDF.loc[self.GlobalDF["单词名"].str.contains(word), "图片有用"].values[0]
        except:
            ImgHelpful=1
            self.SetWordImgHelpful(ImgHelpful)
            # return 1
        return ImgHelpful

    #word list
    def GetWordListbyDifficulty(self,ascending=True):
        self.GlobalDF = self.GlobalDF.sort_values("难度", ascending=ascending)
        WordList = list(self.GlobalDF.loc[:, "单词名"])
        return WordList

    #df
    def GetDFNeedy(self,needy=1):
        df = self.GlobalDF[self.GlobalDF["需要背这个单词"]==needy]
        return df
    # def GetDFDifficultyFilter(self,lower_diff=1):
    #     df = self.GlobalDF[self.GlobalDF["需要背这个单词"]==needy]
    #statistics
    def GetWordsNum(self,needy=1):
        df=self.GetDFNeedy(needy)
        # print(df.shape[0])
        num=df.shape[0]
        print(num)
        return num

    @staticmethod
    def GetDownloadIndexFromImageNames(ImageNames):
        IndexesList=[]
        for imageName in ImageNames:
            index=imageName.split('.')[0]
            index=int(index)
            IndexesList.append(index)
        IndexesList.sort()
        return IndexesList
if __name__=="__main__":
    op=GlobalOperator()
    print(str(op.GetImagesName("abandon")))
    globaldf=op.GlobalDF.sort_values("难度", ascending=True)
    print(op.GetWordsNum(1))
    # op.GlobalDF[op.GlobalDF["单词名"]=="abandon"]["评论"]="test"
    word="abandon"
    mask = op.GlobalDF["单词名"].str.contains(word)
    op.GlobalDF.loc[mask,"评论"]="test"
    notes_already=op.GlobalDF.loc[op.GlobalDF["单词名"].str.contains("bawdy"),"评论"].values[0]
    # print(notes_already)
    # print(np.isnan(notes_already))
    word="bawdy"
    op.AddWordNote(word,"b note")
    notes_already=op.GlobalDF.loc[op.GlobalDF["单词名"].str.contains(word),"评论"].values[0]
    print(op.GetWordNote(word))
    op.SetWordNote(word,"")
    # notes_already=op.GlobalDF.loc[op.GlobalDF["单词名"].str.contains(word),"评论"].values[0]
    print(op.GetWordNote(word))
    # print(np.isnan(notes_already))
    # print(op.GlobalDF)
    # op.SetWordImgHelpful(word,1)
    print(op.GetWordImgHelpful("abandon"))
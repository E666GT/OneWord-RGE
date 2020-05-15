# -*- coding: utf-8 -*-
print("process...0%")
import sys 	
from PyQt5.QtWidgets import QApplication , QMainWindow, QAction,QSizePolicy,QLabel,QPushButton,QMessageBox,QWidget
from main_window import Ui_Form
# from main_window_b import  Ui_Form as Ui_Form_b
from farm_widget_ui import Ui_FarmWidget
from PyQt5.QtCore import pyqtSignal , Qt ,QRect,QStringListModel,QSize,QTimer,QCoreApplication
from GlobalOperator import GlobalOperator
from PyQt5.QtGui import *

# from PyQt5.QtMultimediaWidgets import QAudio
from PyQt5.QtMultimedia import QSound
# from PyQt5.QtMultimediaWidgets import
# from PyQt5 import QtMultimediaWidgets
# from PyQt5.QtMultimedia import Qsound


import random
import numpy as np
import pandas as pd
import os
import xmlprocess
import threading
import time
print("process...5%")
class ImageSuperLabel(QLabel):
	def __init__(self,parent = None,df=pd.DataFrame,DFfile="",mainwindow=None):
		super(ImageSuperLabel,self).__init__(parent)
		self.df=df
		self.DFfile=DFfile
		self.MainWindow=mainwindow
	def mousePressEvent(self, e):
		try:
			file_name=self.objectName()
			print(file_name)
			mask=self.df["文件名"].str.contains(file_name)
			# print("mask:",mask)
			# print("列名有：",self.df.columns)
			self.df.loc[mask,"点赞数"] = self.df.loc[mask,"点赞数"]+1

			print("点赞数+1：",self.df.loc[mask] )
			self.df.to_csv(self.DFfile,index=False)
			self.MainWindow.ClickSound(1)
		except Exception as err:
			print("something wrong with:",err)
		# print("全表：",self.df)
	def mouseReleaseEvent(self, QMouseEvent):
		# print('you have release the mouse')
		pass
print("process...6%")
class FarmItemButton(QPushButton):
	def __init__(self,parent= None,farm=None,word=""):
		super(FarmItemButton,self).__init__(parent)
		self.word=word
		self.farm=farm
	def mousePressEvent(self,e):
		print(self.word)
		# self.farm.Father.CurrentWord = self.word
		self.farm.Father.ShowWord(self.word)
		# print("clicked'")
print("process...7%")

class MyMainWindow(QMainWindow, Ui_Form):

	helpSignal = pyqtSignal(str)
	printSignal = pyqtSignal(list)
	# 声明一个多重载版本的信号，包括了一个带int和str类型参数的信号，以及带str参数的信号
	previewSignal = pyqtSignal([int,str],[str])
	ShowAnsSignal=pyqtSignal(bool)
	ShowImgSignal=pyqtSignal(bool)
	WordSignal = pyqtSignal(str)
	MemYesSignal=pyqtSignal(bool)
	MemNoSignal=pyqtSignal(bool)
	MemNoMoreSignal=pyqtSignal(bool)
	CurrentAlreadyMemListClickedSignal=pyqtSignal(bool)
	MemNotSureSignal = pyqtSignal(bool)
	MoreImageSignal = pyqtSignal(bool)
	OpenFarmSignal = pyqtSignal(bool)
	SearchWordSignal = pyqtSignal(bool)
	CounterTimeStartOrCloseSignal = pyqtSignal(bool)
	ShowCurrentAlreadyMemListSignal = pyqtSignal(bool)
	# ynmOP=xmlprocess.ynm_processor()
	def __init__(self, parent=None,ynmOP=None):
		pass

		super(MyMainWindow, self).__init__(parent)

		self.CounterTimeBool=False
		self.CounterTimer=QTimer()
		self.CounterValueIntDefault=8
		self.CounterValueInt=self.CounterValueIntDefault
		self.CounterTimer.timeout.connect(self.CounterTimeOperations)

		print("process...30%")
		self.ynmOP=ynmOP
		self.setupUi(self)
		self.initUI()
		self.createActions()
		self.createMenus()
		self.createToolBars()
		print("process...50%")
		# self.form=Ui_Form
		#global database temp
		self.op=GlobalOperator()
		print(self.op.ImageMaxWidth)
		self.op.ImageMaxWidth=self.scrollAreaWidgetContents.width()/self.op.ImageColumns
		print(self.op.ImageMaxWidth)
		# self.ShowAnsSignal=[True,""]
		self.downloadOP=xmlprocess.DownloadOperator()
		self.ShowAnsBool=True

		#获得一批单词，作为任务
		self.CurrentBatchWordList=[]
		self.NextBatch()
		self.CurrentWord=self.GetANextWordFromBatch()
		# self.ynmOP=
		self.CurrentTrans=self.ynmOP.getWordTrans(self.CurrentWord)

		self.CurrentWordImgHistoryDF = pd.DataFrame()
		self.CurrentAlreadyMemNum=0
		self.CurrentAlreadyMemList=[]
		self.CurrentMemNoClicked=False

		#
		self.CurrentMatchMemYesList=[]#当前批已经记住的单词
		print(self.CurrentBatchWordList)

		print("process...80%")

		# self.OpenFarm()

		self.Sounds=[QSound("click.wav"),QSound("water.wav"),QSound("happy.wav")]
		# self.clicksound=QSound("click.wav")

		# 初始化单词的显示
		self.GetWordButton.click()

		#主窗口隐藏 农场显示
		self.FarmWidget = MyFarmWidget(MainWindow=self)
		self.hide()
		self.OpenFarm()
		self.ClickSound(2)
		print("process...100%")
	def initUI(self):
		self.helpSignal.connect(self.showHelpMessage)
		self.printSignal.connect(self.printPaper) #信号 -connect->函数(执行任务,参数为signal)
		self.ShowAnsSignal.connect(self.ShowOrHideWord) #触发函数
		self.WordSignal.connect(self.ShowWord)
		self.ShowImgSignal.connect(self.ShowImg)
		self.previewSignal[str].connect(self.previewPaper)
		self.previewSignal[int,str].connect(self.previewPaperWithArgs)
		self.MemYesSignal.connect(self.MemYes)
		self.MemNoSignal.connect(self.MemNo)
		self.MemNoMoreSignal.connect(self.MemNoMore)

		self.printButton.clicked.connect(self.emitPrintSignal) #动作 ->函数(发送信号) -》
		self.previewButton.clicked.connect(self.emitPreviewSignal)
		self.ShowAnsButton.clicked.connect(self.emitShowAnsSignal)
		self.GetWordButton.clicked.connect(self.emitWordSignal)
		self.ShowImageButton.clicked.connect(self.emitShowImgSignal)
		self.WordsListViewer.clicked.connect(self.CurrentAlreadyMemListClicked)
		self.MemYesButton.clicked.connect(self.emitMemYesSignal)
		self.MemNoButton.clicked.connect(self.emitMemNoSignal)
		self.MemNotSureButton.clicked.connect(self.MemNotSure)
		self.MemNoMoreButton.clicked.connect(self.emitMemNoMoreSignal)
		self.MoreImageButton.clicked.connect(self.MoreImage)
		self.OpenFarmButton.clicked.connect(self.OpenFarm)
		self.WordSearchButton.clicked.connect(self.SearchWord)
		self.CounterTimeButton.clicked.connect(self.CounterTimeStartOrClose)
		self.AleradyMemListShowButton.clicked.connect(self.ShowCurrentAlreadyMemList)
		self.ThisBatchWordsListListShowButton.clicked.connect(self.ShowCurrentBatchWordList)
		self.ThisBatchNotReadyListShowButton.clicked.connect(self.ShowThisBatchNotReadyWordList)
		self.NextBatchButton.clicked.connect(self.NextBatch)
		self.URLDownloadButton.clicked.connect(self.URLImageDownlaod)
		self.TakeNotePublishpushButton.clicked.connect(self.PublishNote)
		self.ImgHelpfulYesButton.clicked.connect(self.ImgHelpfulYes)
		self.ImgHelpfulNoButton.clicked.connect(self.ImgHelpfulNo)
		self.ImgHelpfulLabel.hide()
		self.resultLabel.setText("这里显示 后台info信息!")


		# self.GetWordButton.show()
		# self.MemYesButton.hide()
		# self.MemNoButton.hide()
		# self.MemNotSureButton.hide()
	def ImgHelpfulYes(self):
		self.op.SetWordImgHelpful(self.CurrentWord,ImgHelpful=1)
		self.emitShowImgSignal()
	def ImgHelpfulNo(self):
		self.op.SetWordImgHelpful(self.CurrentWord,ImgHelpful=0)
		self.emitShowImgSignal()
	def PublishNote(self):
		word=self.CurrentWord
		note=self.TakeNotetextEdit.toPlainText()
		self.op.AddWordNote(word,note)
		self.ShowOrHideWord(1)
	def URLImageDownlaod(self):
		url=self.URLDownloadInputlineEdit.text()
		word=self.CurrentWord
		#get max index
		ImagesNames = self.op.GetImagesName(word)
		ImagesNames.sort()
		ImagesIndexes = self.op.GetDownloadIndexFromImageNames(ImagesNames)
		MaxIndex = ImagesIndexes[-1]


		filename = str(MaxIndex + 1) + ".URLDownloadImage." + "jpg"
		path = "downloads/" + word + "/" + filename
		self.downloadOP.UrlDownload(url=url, path=path)
		filename = str(MaxIndex + 2) + ".URLDownloadImage." + "png"
		path = "downloads/" + word + "/" + filename
		self.downloadOP.UrlDownload(url=url, path=path)

		self.DebugShow("下载完成~")
	def NextBatch(self):
		length=eval(self.BatchLengthLineEdit.text())
		self.CurrentBatchWordList = self.op.GetABatchWordList(length)
		self.CurrentMatchMemYesList=[]
		self.ShowCurrentBatchWordList()
	def GetANextWordFromBatch(self):
		RemainWordList=list(set(self.CurrentBatchWordList)-set(self.CurrentMatchMemYesList))
		if(len(RemainWordList)):
			return random.choice(RemainWordList)
		else:
			print("已经没有单词了")
			QMessageBox.warning(self, "congratulation!", "恭喜你这批小花已经成功施肥~\n赶快去照顾下一批吧！", QMessageBox.Cancel)
			return False
		pass
	def ClickSound(self,id):
		# pass
		print("sound")
		self.Sounds[id].play()
		# self.clicksound.play()
	def SearchWord(self):
		word=self.WordSearchLineEdit.text()
		print(word)
		self.ShowWord(word)
	def OpenFarm(self):
		self.DebugShow("OpenFarm")
		# self.MainWidget.hide()
		# self.MainWidget.show()
		# farm_ui= Ui_FarmWidget()
		# farm_ui.setupUi(self.FarmWidget)
		self.FarmWidget.show()
		# self.FarmWidget.pushButton.setText("testsssss")

		pass
	def MoreImage(self):

		word=self.CurrentWord

		#get offset
		#get limit

		ImagesNames = self.op.GetImagesName(word)
		ImagesNames.sort()
		ImagesIndexes = self.op.GetDownloadIndexFromImageNames(ImagesNames)
		MaxIndex = ImagesIndexes[-1]
		print("maxindex:", MaxIndex)
		setoff = MaxIndex + 1
		print("setoff", setoff)
		# limit=setoff+50
		threadNum = 6
		for threadId in range(threadNum):
			thislimit = setoff + (threadId + 1) * 10
			thissetoff = setoff + threadId * 10 + 1
			DownloadThread = threading.Thread(target=self.downloadOP.download_word, args=(word, thislimit, thissetoff))
			DownloadThread.start()


		#Reinit Img Show
		self.ShowImg(1)  # make sure word database is good

		# self.downloadOP.download_word(word=self.CurrentWord,limit=limit,offset=offset)
		self.DebugShow("正在后台下载\n你先去背一下其他单词...")
	def MemNotSure(self):
		self.ShowOrHideWord(1)
		self.MemNotSureButton.hide()
	def MemYes(self):
		# self.DebugShow("")
		self.ClickSound(0)
		self.CurrentMatchMemYesList.append(self.CurrentWord)#添加入 当前批次已记得

		mask = self.op.GlobalDF["单词名"].str.contains(self.CurrentWord)
		self.op.GlobalDF.loc[mask, "记得次数"] = self.op.GlobalDF.loc[mask, "记得次数"]+ 1
		difficulty=self.op.GlobalDF.loc[mask, "难度"].values[0]
		MemNoTimes=self.op.GetWordMemNoTimes(self.CurrentWord)
		MemReadTimes=self.op.GetWordReadTimes(self.CurrentWord)
		#计算回答正确时的难度衰减率：越难的应该衰减的慢
		difficulty_damp_ratio=0.6+0.4*(MemNoTimes/(MemReadTimes*1.5))
		print("作物增长了！",difficulty_damp_ratio)
		self.op.GlobalDF.loc[mask, "难度"]=difficulty*difficulty_damp_ratio
		self.op.GlobalDf_save()
		self.DebugShow("施肥成功！")
		self.emitWordSignal()
		self.ShowWordHistory()

		# self.MemYesButton.hide()
	def MemNo(self):
		self.DebugShow("浇水成功！")
		self.CurrentMemNoClicked=True
		mask = self.op.GlobalDF["单词名"].str.contains(self.CurrentWord)
		self.op.GlobalDF.loc[mask, "忘记次数"] = self.op.GlobalDF.loc[mask, "忘记次数"]+ 1
		difficulty=self.op.GlobalDF.loc[mask, "难度"].values[0]
		self.op.GlobalDF.loc[mask, "难度"]=difficulty+(10-difficulty)/2
		self.op.GlobalDf_save()
		self.DebugShow("No")
		self.ShowAnsBool=1
		self.emitShowAnsSignal()
		if(self.ShowImgWhenMemNoAutoCheckBox.isChecked()):
			self.emitShowImgSignal()
		self.ShowWordHistory()
		self.MemNoButton.hide()
		self.MemYesButton.hide()
		self.MemNotSureButton.hide()
		self.GetWordButton.show()
	def MemNoMore(self):
		mask = self.op.GlobalDF["单词名"].str.contains(self.CurrentWord)
		self.op.GlobalDF.loc[mask, "需要背这个单词"] = 0
		self.op.GlobalDf_save()
		self.DebugShow("No More this word")
		self.ShowWordHistory()
	def emitMemYesSignal(self):

		self.MemYesSignal[bool].emit(1)
	def emitMemNoSignal(self):
		self.MemNoSignal[bool].emit(1)
	def emitMemNoMoreSignal(self):
		self.MemNoMoreSignal[bool].emit(1)

	def CounterTimeStartOrClose(self):
		self.CounterTimeBool = 1 - self.CounterTimeBool
		if(self.CounterTimeBool):
			#start

			self.CounterTimer.start(300)
			pass
		else:
			self.CounterTimer.stop()
			self.CounterTimeLabel.setText("_____")
			#stop
			pass
	def CounterTimeOperations(self):
		self.CounterTimeLabel.setText(str(self.CounterValueInt))
		self.CounterValueInt=self.CounterValueInt-1
		if(self.CounterValueInt==4):
			self.ShowOrHideWord(1)
		# if(self.CounterValueInt)
		if(self.CounterValueInt==-1):
			self.CounterValueInt=self.CounterValueIntDefault
			self.emitWordSignal()
		# self.CounterTimeLabel.setText(str(random.randint(0,10)))
	def CurrentAlreadyMemListClicked(self,qModelIndex):
		print(qModelIndex.data(),"clicked")
		word_clicked=qModelIndex.data()
		# word_clicked=self.CurrentAlreadyMemList[qModelIndex.row()]
		# word_clicked=self.WordsListViewer.SelectItems[]
		# self.CurrentWord=word_clicked
		# self.CurrentTrans = self.ynmOP.getWordTrans(self.CurrentWord)
		self.ShowWord(word_clicked)
		self.ShowOrHideWord(0)
		# QMessageBox.information(self, 'ListWidget', '你选择了：' + self.CurrentAlreadyMemList[qModelIndex.row()])

	def DebugShow(self,input_str):
		input_str=str(input_str)
		self.resultLabel.setText(input_str)
	def emitWordSignal(self):
		# self.ClickSound(1)
		new_word=self.GetANextWordFromBatch()
		if(new_word==False):
			print("该批次已经没有单词了。无法显示。")
			return False
		else:
			# self.CurrentWord=self.op.GetAWord()
			self.CurrentWord=new_word
			self.CurrentTrans = self.ynmOP.getWordTrans(self.CurrentWord)
			self.ShowAnsBool=False
			self.emitShowAnsSignal()
		# self.ShowAnsTemp[2]=self.CurrentWord
		self.WordSignal[str].emit(self.CurrentWord)
	# def ClickWordImage(self):
	# 	print("click")
	def ShowImg(self,showbool):
		VLayout_list = [self.scrollAreaV1, self.scrollAreaV2, self.scrollAreaV3, self.scrollAreaV4, self.scrollAreaV5]
		self.DebugShow("使用图片工具\n帮助浇水哦")
		ImgHelpful=self.op.GetWordImgHelpful(self.CurrentWord)
		if(ImgHelpful==0):
			self.DebugShow("不适合用图片记忆")
			self.ImgHelpfulLabel.setText("您之前标记过，该作物不建议使用图片工具浇水~\n将不提供图片\n撤销点击下方<图片有用>")
			self.ImgHelpfulLabel.show()
			# self.
			# return False
			showbool=0
		else:
			# pass
			self.ImgHelpfulLabel.hide()

		if(showbool):
			word=self.CurrentWord
			if(word=="WORD"):
				print("请先加载单词")
				self.scrollAreaWidgetContents.setWindowIconText("请先加载单词")
				return 0
			# 加载该单词的小数据库
			ImagesNames = self.op.GetImagesName(word)
			# print(ImagesNames)
			# print(word)
			DfFile = "downloads/" + word + "/" + word + ".csv"
			try:
				ImgHistoryDf = pd.read_csv(DfFile)
			except:
				ImgHistoryDf = pd.DataFrame(columns=["文件名", "点赞数"])
				# print(ImgHistoryDf)

			# 初始化df
			for ImageName in ImagesNames:
				if (not (ImageName in list(ImgHistoryDf["文件名"]))):
					print("not in")
					ImgHistoryDf.loc[ImgHistoryDf.shape[0] + 1] = {"文件名": ImageName, "点赞数": 0}
			ImgHistoryDf.to_csv(DfFile, index=False)

			ImgHistoryDf = ImgHistoryDf.sort_values("点赞数", ascending=False)
			# print(ImgHistoryDf)
			ImagesNames = list(ImgHistoryDf.loc[:, "文件名"])
			# print(self.op.GetImagesName(word))
			# self.DebugShow(self.op.GetImagesName(word))
			# 展示单词图片
			ImagesNum = len(ImagesNames)
			QimageLabel_list = []
			# 清空VLayout_list widght
			for vlayout in VLayout_list:
				for i in range(vlayout.count()):
					vlayout.itemAt(i).widget().deleteLater()
			# print("delet")
			Image_list_total_height = [0, 0, 0, 0, 0]  # 第一列总高度，第二列总高度，第三列总高度
			for i in range(ImagesNum):
				imagePath = "downloads/" + word + "/" + ImagesNames[i]

				self.image = QImage()
				self.imageLabelNew = ImageSuperLabel(df=ImgHistoryDf, DFfile=DfFile,mainwindow=self)
				self.imageLabelNew.setObjectName(ImagesNames[i])
				self.imageLabelNew.setText(ImagesNames[i])
				if self.image.load(imagePath):
					w, h = self.op.GetAdaptiveImageSize(self.image.width(), self.image.height())  # self.image.size(w,h)
					Image_list_total_height[i % 5] = Image_list_total_height[i % 5] + h
					# self.image.scaled(w, h, Qt.IgnoreAspectRatio)
					# print("w,h", w, h)
					self.imageLabelNew.setPixmap(QPixmap.fromImage(self.image.scaled(w, h, Qt.IgnoreAspectRatio)))
					# self.imageLabelNew.resize(w,h)
					self.imageLabelNew.setScaledContents(True)  # self.imageLabelNew.move(600,600)
					VLayout_list[i % 5].addWidget(self.imageLabelNew)
					if(random.random()<0.3):
						bigword=QLabel()
						bigword.setText(word)
						bigword.setAlignment(Qt.AlignCenter)
						bigword.setFont(QFont("Adobe Devanagari",40))
						VLayout_list[i % 5].addWidget(bigword)
					QimageLabel_list.append(self.imageLabelNew)
			self.scrollArea.verticalScrollBar().setValue(0)
			max_height = max(Image_list_total_height)
			min_height = min(Image_list_total_height)
			# print("max_height",max_height)
			print("av height=",(max_height + min_height) / 2)

			self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1440, (max_height + min_height) / 2+100))
			self.scrollAreaWidgetContents.setMinimumSize(QSize(1440, (max_height + min_height) / 2+100))
			self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 1440,(max_height + min_height) / 2))
			# self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1440, 300))
			self.CurrentWordImgHistoryDF=ImgHistoryDf
			self.ShowWordHistory()
			return ImgHistoryDf
		else:
			# 清空VLayout_list widght
			for vlayout in VLayout_list:
				for i in range(vlayout.count()):
					vlayout.itemAt(i).widget().deleteLater()
			# print("delet")
			return False
	def ShowCurrentAlreadyMemNum(self):
		self.CurrentAlreadyMemNumLabel.setText("本次已记忆："+str(self.CurrentAlreadyMemNum))

	def ShowCurrentAlreadyMemList(self):
		# self.CurrentAlreadyMemListtextBrowser.setText("")
		# settext=''
		# for word in self.CurrentAlreadyMemList:
		# 	settext=settext+word
		# 	settext=settext+"\n"
		# self.CurrentAlreadyMemListtextBrowser.setText(settext)

		# 实例化列表模型，添加数据
		slm = QStringListModel()
		# 设置模型列表视图，加载数据列表
		slm.setStringList(self.CurrentAlreadyMemList)
		# 设置列表视图的模型
		self.WordsListViewer.setModel(slm)

	def ShowCurrentBatchWordList(self):
		# self.CurrentAlreadyMemListtextBrowser.setText("")
		# settext=''
		# for word in self.CurrentAlreadyMemList:
		# 	settext=settext+word
		# 	settext=settext+"\n"
		# self.CurrentAlreadyMemListtextBrowser.setText(settext)

		slm = QStringListModel()
		# 设置模型列表视图，加载数据列表
		slm.setStringList(self.CurrentBatchWordList)
		# 设置列表视图的模型
		self.WordsListViewer.setModel(slm)
	def ShowThisBatchNotReadyWordList(self):
		RemainWordList = list(set(self.CurrentBatchWordList) - set(self.CurrentMatchMemYesList))
		slm = QStringListModel()
		# 设置模型列表视图，加载数据列表
		slm.setStringList(RemainWordList)
		# 设置列表视图的模型
		self.WordsListViewer.setModel(slm)
	def ShowWordHistory(self):
		mask = self.op.GlobalDF["单词名"].str.contains(self.CurrentWord)
		MemYesTimes=self.op.GlobalDF.loc[mask, "记得次数"].values[0]
		MemNoTimes=self.op.GlobalDF.loc[mask, "忘记次数"].values[0]
		if(MemNoTimes>3):
			self.DebugShow("忘记太多次？\n试试百度图片")
		MemLookTimes = self.op.GlobalDF.loc[mask, "已查看次数"].values[0]
		difficulty=self.op.GlobalDF.loc[mask, "难度"].values[0]
		# difficulty = round(1 - MemYesTimes / (MemLookTimes+MemNoTimes), 4)*10
		# self.op.GlobalDF.loc[mask, "难度"] = difficulty
		HistoryStr="记得次数："+str(MemYesTimes)+"        忘记次数："+str(MemNoTimes)+"\n已查看次数："+str(MemLookTimes)+"\n难度："+str(difficulty)+"/10"
		HistoryStr=HistoryStr+"     已加载图片数："+str(self.CurrentWordImgHistoryDF.shape[0])
		self.WordHistory.setText(HistoryStr)
		self.op.GlobalDf_save()
	def ShowWord(self,word):
		self.CurrentMemNoClicked=False
		self.GetWordButton.hide()
		self.MemYesButton.show()
		self.MemNoButton.show()
		self.MemNotSureButton.show()

		# self.CounterValueInt=self.CounterValueIntDefault
		if(word in self.op.WordList):
			pass
		else:
			self.DebugShow("无此单词")
			return False
		self.CurrentWord=word
		self.CurrentTrans = self.ynmOP.getWordTrans(self.CurrentWord)
		#该单词是否需要背？
		mask = self.op.GlobalDF["单词名"].str.contains(word)
		# print("mask=",mask)
		need=self.op.GlobalDF.loc[mask,"需要背这个单词"].values[0]
		# print("need=",need)
		if(need):
			print(word,"加载成功！")
			pass
		else:
			print(word,"该单词已经不需要背了,将加载新的单词！")
			self.emitWordSignal()
			return False

		#展示单词
		self.WordLabel.setText(word)
		self.WordSmallLabel.setText(word)
		self.CurrentWord=word

		#更新单词难度 展示单词历史：
		mask = self.op.GlobalDF["单词名"].str.contains(self.CurrentWord)
		# MemYesTimes=self.op.GlobalDF.loc[mask, "记得次数"].values[0]
		# MemNoTimes=self.op.GlobalDF.loc[mask, "忘记次数"].values[0]
		self.op.GlobalDF.loc[mask, "已查看次数"]=self.op.GlobalDF.loc[mask, "已查看次数"].values[0]+1
		difficulty = self.op.GlobalDF.loc[mask, "难度"].values[0]
		self.op.GlobalDF.loc[mask, "难度"]=difficulty*0.9
		# MemLookTimes=self.op.GlobalDF.loc[mask, "已查看次数"].values[0]
		# difficulty=round(1 - MemYesTimes / MemLookTimes, 3)
		# self.op.GlobalDF.loc[mask, "难度"] = difficulty



		# HistoryStr="记得次数："+str(MemYesTimes)+"        忘记次数："+str(MemNoTimes)+"\n已查看次数："+str(MemLookTimes)+"\n难度："+str(difficulty)
		# self.WordHistory.setText(HistoryStr)



		#清空图片or展示图片
		self.ShowImgSignal[bool].emit(self.ShowImgAutoCheckBox.isChecked())

		#本次已记忆+1
		if(word in self.CurrentAlreadyMemList):
			pass
		else:
			self.CurrentAlreadyMemList.append(word)
		# self.ShowCurrentAlreadyMemList()
		self.CurrentAlreadyMemNum=len(self.CurrentAlreadyMemList)
		self.ShowCurrentAlreadyMemNum()
		self.ShowWordHistory()

	def emitShowImgSignal(self):
		self.ShowImgSignal[bool].emit(True)
	def emitShowAnsSignal(self):
		print('here')
		self.ShowAnsSignal[bool].emit(self.ShowAnsBool)
	def ShowOrHideWord(self,show_bool):
		print("showed")
		if(show_bool):
			current_note=str(self.op.GetWordNote(self.CurrentWord))
			self.WordDetailtextBrowser.setText("我的笔记:"+current_note+"\n"+self.CurrentTrans)
		else:
			self.WordDetailtextBrowser.setText("<单词示意已隐藏>")
		self.ShowAnsBool=1-self.ShowAnsBool

	# 发射预览信号
	def emitPreviewSignal(self):
		if self.previewStatus.isChecked() == True:
			self.previewSignal[int,str].emit(1080," Full Screen")
		elif self.previewStatus.isChecked() == False:
			self.previewSignal[str].emit("Preview")
	# 发射打印信号
	def emitPrintSignal(self):
		pList = []
		pList.append(self.numberSpinBox.value() )
		pList.append(self.styleCombo.currentText())
		self.printSignal.emit(pList)
	def printPaper(self,list):
		self.resultLabel.setText("打印: "+"份数："+ str(list[0]) +" 纸张："+str(list[1]))
	def previewPaperWithArgs(self,style,text):
		self.resultLabel.setText(str(style)+text)
	def previewPaper(self,text):
		self.resultLabel.setText(text)

    # 重载点击键盘事件
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_F1:
			self.helpSignal.emit("help message")

		# if event.key() == Qt.Key_Space:
		# 	# self.GetWordButton.
		# 	self.MemYesButton.click()
		if event.key() == Qt.Key_A:
			if(self.CurrentMemNoClicked):
				self.emitWordSignal()
			else:
				self.MemNoButton.click()
		if event.key() == Qt.Key_S:
			self.MemNotSureButton.click()
		if event.key() == Qt.Key_D:
			if(self.CurrentMemNoClicked):
				self.emitWordSignal()
			else:
				self.MemYesButton.click()
		if event.key() == Qt.Key_Q:
			self.ShowAnsButton.click()
		if event.key() == Qt.Key_P:
			self.ShowImageButton.click()
		if event.key() == Qt.Key_T:
			# self.ClickSound(0)
			# self.ClickSound(1)
			self.hide()
	def mousePressEvent(self, event):
		print("click")
		print(event.x())
		print(event.y())
	def eventFilter(self, object, event):
		if	event.type() == QtCore.QEvent.HoverMove:
			print(f'鼠标移动到按钮上')
			return True
		elif event.type() == QtCore.QEvent.MouseMove:
			print(f'按钮被点击')
			return True

    # 显示帮助消息
	def showHelpMessage(self,message):
		self.resultLabel.setText(message)
		self.statusBar().showMessage(message)
	def createActions(self):
		self.PrintAction = QAction(QIcon("./images/printer.png"), self.tr("打印"), self)
		self.PrintAction.setShortcut("Ctrl+P")
		self.PrintAction.setStatusTip(self.tr("打印"))
		# self.PrintAction.triggered.connect(self.slotPrint)
	def createMenus(self):
		PrintMenu = self.menuBar().addMenu(self.tr("打印"))
		PrintMenu.addAction(self.PrintAction)
	def createToolBars(self):
		pass
		# fileToolBar = self.addToolBar("Print")
		# fileToolBar.addAction(self.PrintAction)

print("process...7.2%")
class MainWindow_test(QMainWindow):
	count = 0
	helpSignal = pyqtSignal(str)

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.mdi = QMdiArea()
		self.setCentralWidget(self.mdi)
		bar = self.menuBar()
		file = bar.addMenu("File")
		file.addAction("New")
		file.addAction("cascade")
		file.addAction("Tiled")
		file.triggered[QAction].connect(self.windowaction)
		self.setWindowTitle("MDI demo")
		# self.loops=0
		self.q1()
		self.helpSignal.connect(self.q1)
		self.bt = QPushButton()
		self.bt.clicked.connect(self.q1)

	def windowaction(self, q):
		print("triggered")

		if q.text() == "New":
			MainWindow.count = MainWindow.count + 1
			sub = QMdiSubWindow()
			sub.setWidget(QTextEdit())
			sub.setWindowTitle("subwindow" + str(MainWindow.count))
			self.mdi.addSubWindow(sub)
			sub.show()
		if q.text() == "cascade":
			self.mdi.cascadeSubWindows()
		if q.text() == "Tiled":
			self.mdi.tileSubWindows()

	def q1(self):
		self.loops = 50000000
		while self.loops:
			self.q = self.q2()
			self.loops = self.loops - 1
		# print(self.q)
		pass

	def q2(self):
		return self.loops / time.time()
		pass


print("process...7.5%")
class MyFarmWidget(QWidget, Ui_FarmWidget):
	UpdateFarmItemsSignal = pyqtSignal(bool)
	def __init__(self, parent=None, ynmOP=None,MainWindow=None):
		super(MyFarmWidget, self).__init__(parent)
		self.setupUi(self)
		self.initUI()
		self.Father=MainWindow
		self.GlobalDF = self.Father.op.GlobalDF.sort_values("难度", ascending=True)

		self.FarmItemsButtons=[]
		self.InitFarmItems()
		self.InitFarmDetail()

		self.FarmInfoUpdate()
	def initUI(self):
		self.UpdateFarmItemsSignal.connect(self.updateFarmItems)
		self.FreshFarmButton.clicked.connect(self.emitUpdateFarmItemsSignal)
		self.FreshFarmByHealthOrderButton.clicked.connect(self.FreshFarmByHealthOrder_temp)
		self.GoMainWindowButton.clicked.connect(self.ShowMainWIndow)
		self.FarmInfoUpdatepushButton.clicked.connect(self.FarmInfoUpdate)

		pass

	def FarmInfoUpdate(self):
		ItemsNum=self.Father.op.GetWordsNum(1)
		HealthNum=self.Father.op.GlobalDF[self.Father.op.GlobalDF["难度"]<5].shape[0]
		SubHealthNum=self.Father.op.GlobalDF[self.Father.op.GlobalDF["难度"]<8].shape[0]
		IveReadNum=self.Father.op.GlobalDF[self.Father.op.GlobalDF["难度"]<10].shape[0]
		info_text=("我的作物总数："+str(ItemsNum)
				   +"\n健康作物："+str(HealthNum)
				   +"        亚健康作物："+str(SubHealthNum)
				   +"\n我已见过的："+str(IveReadNum)
				   +"        我未曾见过的："+str(ItemsNum-IveReadNum)
				   )
		self.FarmInfotextBrowser.setText(info_text)
	def ShowMainWIndow(self):
		self.Father.show()
	def FreshFarmByHealthOrder_temp(self):
		# self.InitFarmDetail()
		self.InitFarmItems()
		self.InitFarmDetail()
	def emitUpdateFarmItemsSignal(self):
		print("emit")
		self.UpdateFarmItemsSignal[bool].emit(1)
	def InitFarmItems(self):
		self.FarmItemsButtons=[]
		self.GlobalDF=self.Father.op.GlobalDF.sort_values("难度", ascending=True)
		WordList= list(self.GlobalDF.loc[:, "单词名"])
		TotalNum=len(WordList)
		WordList=WordList[:TotalNum]

		#重载所有item
		for i in range(TotalNum):

			word=WordList[i]
			difficulty=self.Father.op.GetWordDifficulty(word)
			health,color_r_and_b=self.Difficulty_to_Health_and_ColorRB(difficulty)
			newbutton=FarmItemButton(farm=self,word=word)
			newbutton.setText(word)#+str(difficulty))
			newbutton.setFont(QFont("Microsoft Yahei",13))
			newbutton.setStyleSheet("background-color:rgb("+str(color_r_and_b)+",255,"+str(color_r_and_b)+")");
			# self.Father.CurrentWord=word
			# newbutton.clicked.connect(self.FarmItemClicked)
			# newbutton.
			self.FarmItemsButtons.append(newbutton)

		print("items 初始化完毕")
		pass
	def InitFarmDetail(self):
		# self.GlobalDF=self.Father.op.GlobalDF.sort_values("难度", ascending=True)
		# print(Globaldf)

		WordList= list(self.GlobalDF.loc[:, "单词名"])
		TotalNum=len(WordList)
		WordList=WordList[:TotalNum]
		rowIndex=0
		colIndex=0
		MaxCoIndex=140

		#清空itme
		for i in range(self.FarmDetailScrollAreaGridLayout.count()):
			self.FarmDetailScrollAreaGridLayout.itemAt(i).widget().deleteLater()
		print("农场已经清空")

		#加载标准色item
		standardbutton=QPushButton()
		standardbutton.setText("健康色")
		standardbutton.setFont(QFont("Microsoft Yahei", 10))
		standardbutton.setStyleSheet("background-color:rgb(" + str(0) + ",255," + str(0) + ")");
		wordlen=10
		self.FarmDetailScrollAreaGridLayout.addWidget(standardbutton, rowIndex, colIndex, 1, wordlen)
		colIndex=colIndex+wordlen

		#重载所有item
		for i in range(TotalNum):
			newbutton=self.FarmItemsButtons[i]
			word=newbutton.word
			difficulty=self.Father.op.GetWordDifficulty(word)
			helth,color_r_and_b=self.Difficulty_to_Health_and_ColorRB(difficulty)
			wordlen=len(word)+1

			if((colIndex+wordlen)>MaxCoIndex):
				colIndex=0
				rowIndex=rowIndex+1
			# newbutton=FarmItemButton(farm=self,word=word)
			# newbutton.setText(word)#+str(difficulty))
			# newbutton.setFont(QFont("Microsoft Yahei",13))
			# newbutton.setStyleSheet("background-color:rgb("+str(color_r_and_b)+",255,"+str(color_r_and_b)+")");

			# self.FarmItemsButtons.append(newbutton)
			self.FarmDetailScrollAreaGridLayout.addWidget(newbutton,rowIndex,colIndex,1,wordlen)
			colIndex=colIndex+wordlen

		# print(rowIndex)
		layout_height=rowIndex*30
		self.FarmDetailScrollAreaContents.setMinimumSize(QSize(0, layout_height))
		self.gridLayoutWidget.setGeometry(QRect(0, 0, 1581, layout_height))
		self.FarmDetailScrollAreaGridLayout.setContentsMargins(0,0,0,0)
		print("农场加载完毕")
		pass
	def updateFarmItems(self):
		print("更新完成")
		self.GlobalDF = self.Father.op.GlobalDF.sort_values("难度", ascending=True)
		#重新上色
		for button in self.FarmItemsButtons:
			# print(button.word)
			# button.setText("test?")
			word=button.word
			difficulty=self.Father.op.GetWordDifficulty(word)
			health,color_r_and_b=self.Difficulty_to_Health_and_ColorRB(difficulty)
			button.setStyleSheet("background-color:rgb(" + str(color_r_and_b) + ",255," + str(color_r_and_b) + ")");
		# button.setText(str(health))

		print("更新完成")
		# #重新排序
		#
		# print("updating here")
		# WordListByDifficulty=self.Father.op.GetWordListbyDifficulty()
		# print(WordListByDifficulty)
		#
		# print("updating finished")

	def FarmItemClicked(self):
		self.Father.ShowWord(self.Father.CurrentWord)

	@staticmethod
	def Difficulty_to_Health_and_ColorRB(difficulty):
		health = round(1 - difficulty / 10,2)  # health=0~1,1 health,0 bad
		color_r_and_b = 255 - health * 255
		return health,color_r_and_b
if __name__=="__main__":
	print("process...8%")
	ynmOP=xmlprocess.ynm_processor()
	# ynmOP=None
	print("process...10%")
	app = QApplication(sys.argv)  
	win = MyMainWindow(ynmOP=ynmOP)
	# win.show()
	sys.exit(app.exec_())  

def __init__(self):
    super(HelpWindow, self).__init__()
    self.setWindowTitle('帮助文档')
    self.topFiller = QWidget()
    self.topFiller.setMinimumSize(1000, 2000)  #######设置滚动条的尺寸
    self.label3 = QLabel(self.topFiller)
    self.label3.setAlignment(Qt.AlignCenter)  # 设置文本标签居中显示
    self.label3.setScaledContents(True)
    pixmap = QPixmap('test.jpg')
    # Qt.KeepAspectRatio设置为等比例缩放
    # Qt.IgnoreAspectRatio为不按比例缩放
    scaredPixmap = pixmap.scaled(QSize(1000, 2000), aspectRatioMode=Qt.KeepAspectRatio)
    self.label3.setScaledContents(True)
    self.label3.setPixmap(scaredPixmap)

    # 最里层是加了图片的QLabel，
    # QLabel加到QWidget的布局里，
    # QWidget加到QScrollArea的布局里，
    # 最后把QScrollArea加到大界面的布局里

    ##创建一个滚动条
    self.scroll = QScrollArea()
    self.scroll.setWidget(self.topFiller)
    self.hSb = self.scroll.verticalScrollBar()

    vbox1 = QVBoxLayout()
    vbox1.addWidget(self.label3)
    self.topFiller.setLayout(vbox1)

    vbox2 = QVBoxLayout()
    vbox2.addWidget(self.topFiller)
    self.scroll.setLayout(vbox2)

    self.vbox = QVBoxLayout()
    self.vbox.addWidget(self.scroll)
    self.setLayout(self.vbox)

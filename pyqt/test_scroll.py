import sys
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, ):
        super(QMainWindow, self).__init__()
        self.number = 0

        w = QWidget()
        self.setCentralWidget(w)

        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(350, 2000)  #Qwighet是容器，容纳了40张图
        for filename in range(20):
            self.MapButton = QPushButton(self.topFiller)
            self.MapButton.setText(str(filename))
            self.MapButton.move(10, filename * 40)


        self.scroll = QScrollArea() #ScrollArea的setWidghet设置为QWidget上述的容器。表示，这个容器为scrollArea的子。
        self.scroll.setWidget(self.topFiller)

        self.vbox = QVBoxLayout()#竖直列表。子为ScrollArea
        self.vbox.addWidget(self.scroll)

        w.setLayout(self.vbox)#将主列表设为Vbox

        self.statusBar().showMessage("底部信息栏")
        self.resize(300, 500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
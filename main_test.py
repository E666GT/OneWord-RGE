import xmlprocess
from main import MyMainWindow
if __name__ =="__main__":
    print("process...8%")
    ynmOP = xmlprocess.ynm_processor()
    print("process...10%")
    app = QApplication(sys.argv)
    win = MyMainWindow(ynmOP=ynmOP)
    # win.show()
    sys.exit(app.exec_())

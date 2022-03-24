import sys
sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\DCOPPharse\\')
sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\CycleQueue\\')
sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\DCOPGenetor\\')
from PyQt5 import QtCore, QtGui, QtWidgets
from GUIGenetor import *
from multiprocessing import Process
import threading
from DCOPGenetor import *
def task():
    app=QtWidgets.QApplication(sys.argv) 
    formObj=QtWidgets.QMainWindow()  #注意，这里和我们一开始创建窗体时使用的界面类型相同  
    ui=Ui_DCOPGenetor()    
    ui.setupUi(formObj)    
    formObj.show()    
    sys.exit(app.exec_()) 
    
  


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv) 
    formObj=QtWidgets.QMainWindow()  #注意，这里和我们一开始创建窗体时使用的界面类型相同  
    ui=Ui_DCOPGenetor()    
    ui.setupUi(formObj)    
    formObj.show()    
    sys.exit(app.exec_())  

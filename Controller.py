#Written by Raymond
import sys
from PyQt5 import Qt, QtGui, QtCore, uic, QtWidgets
import time 
import ctypes
# import exceptions
myappid = 'MakShanLab.ProScanIIIController'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

path = sys.path[0]

UI_path = path + r"\MainWindow.ui"
MainWindowUI, QtBaseClass = uic.loadUiType(UI_path)

class MainWindow(QtWidgets.QMainWindow, MainWindowUI):
    """ The following section initializes, or defines the initialization of the GUI and 
    connecting to servers."""
    def __init__(self, reactor, parent=None):
        
        super(MainWindow, self).__init__(parent)
        self.reactor = reactor
        self.setupUi(self)
        self.setupAdditionalUi()
        self.Stage = 0
        
        self.pushButton_Connect.clicked.connect(self.connect())
        self.pushButton_SetStepSize.clicked.connect(lambda: self.write('X ' + str(self.lineEdit_StepSize.text()) + ',' + str(self.lineEdit_StepSize.text())))
        self.pushButton_Up.clicked.connect(lambda: self.write('F'))
        self.pushButton_Down.clicked.connect(lambda: self.write('B'))
        self.pushButton_Left.clicked.connect(lambda: self.write('L'))
        self.pushButton_Right.clicked.connect(lambda: self.write('R'))

        
        #Move to default position
        self.moveDefault()
        
    def setupAdditionalUi(self):
        """Some UI elements would not set properly from Qt Designer. These initializations are done here."""
        pass
        
#----------------------------------------------------------------------------------------------#

    def moveDefault(self):
        self.move(10,10)
        
    def connect(self):
        self.Stage = serial.Serial('COM' + str(self.lineEdit_COM.text()), 9600, timeout=0)
        self.write('*IDN?')

    def write(self, string):
        self.Stage.write(bytes(string, encoding="ascii") + 'r')
            
#----------------------------------------------------------------------------------------------#     
""" The following runs the GUI"""

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    from twisted.internet import reactor
    window = MainWindow(reactor)
    window.show()
#    reactor.runReturn()
    sys.exit(app.exec_())

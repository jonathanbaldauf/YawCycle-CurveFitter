import sys
import numpy as np
import pandas as pd
from mystic.solvers import fmin
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTool
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QTabWidget,
    QPushButton,
    QComboBox,
    QStackedLayout,
    QCheckBox,
    QFileDialog as fd,
    )
import equationdatabase as equs
from create_canvas import MplCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Best Fit Solver')
        
        # layout to hold all 
        self.mainlayout = QHBoxLayout()
        
        # layout for button menu
        self.leftlayout = QVBoxLayout()
        
        # layout for button submenus
        self.rightlayout = QStackedLayout()
        
        # plot holder
        self.plottabWidget = QTabWidget()
        
        # results holder
        self.resultstabWidget = QTabWidget()
        
        # add widgets to leftlayout
        self.loadfilebutton = QPushButton('Load File')
        self.loadfilebutton.clicked.connect(lambda : self.loadFile())
        self.leftlayout.addWidget(self.loadfilebutton)
        
        self.sheetDrop = QComboBox()
        self.leftlayout.addWidget(self.sheetDrop)
        
        self.selectequations = QPushButton('Select Equation')
        self.selectequations.clicked.connect(lambda : self.rightlayout.setCurrentIndex(2))
        self.leftlayout.addWidget(self.selectequations)
        
        self.solvebutton = QPushButton('Solve')
        self.solvebutton.clicked.connect(lambda : self.runSolver())
        self.leftlayout.addWidget(self.solvebutton)
        
        self.showparams = QPushButton('Show Parameters')
        self.showparams.clicked.connect(lambda : self.rightlayout.setCurrentIndex(0))
        self.leftlayout.addWidget(self.showparams)
        
        self.showgraphs = QPushButton('Show Graphs')
        self.showgraphs.clicked.connect(lambda : self.showGraphs())
        self.leftlayout.addWidget(self.showgraphs)
        
        
        self.leftlayout.addStretch()
        self.clearresults = QPushButton('Clear Results')
        self.clearresults.clicked.connect(lambda : self.resultstabWidget.clear())
        self.leftlayout.addWidget(self.clearresults)
        
        self.cleargraphs = QPushButton('Clear Graphs')
        self.cleargraphs.clicked.connect(lambda : self.plottabWidget.clear())
        self.leftlayout.addWidget(self.cleargraphs)
        
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(lambda : self.close())
        self.leftlayout.addWidget(self.quitbutton)
        
        
        # add param and plot tab widget to rightlayout
        self.rightlayout.addWidget(self.resultstabWidget)
        self.rightlayout.addWidget(self.plottabWidget)
        
        # create back button for second right side page
        self.back = QPushButton('Back')
        self.back.clicked.connect(lambda : self.rightlayout.setCurrentIndex(0))
        
        # create layout for second page of rightlayout 
        self.right2layout = QVBoxLayout()
        self.right2layout.addWidget(self.back)
        
        # creates empty list for equations
        self.equationlist = []
        # create row 1 for equations
        self.equrow1 = QHBoxLayout()
        
        # create layout for P/L equations 
        self.PLEqu = QVBoxLayout()
        
        # checkbox list for P/L equations
        self.PLEqu.addWidget(QLabel('P/L Equations'))
        self.lob = QCheckBox('Lanz-Odermatt Basic')
        self.lob.toggled.connect(lambda : self.addtoSolver(equs.lanzOdermattBasic))
        self.PLEqu.addWidget(self.lob)
        self.loe = QCheckBox('Lanz-Odermatt Extras')
        self.loe.toggled.connect(lambda : self.addtoSolver(equs.lanzOdermattExtra))
        self.PLEqu.addWidget(self.loe)
        self.PLEqu.addStretch()
        
        self.YawFitEqu = QVBoxLayout()
        
        # checkbox list for P/L equations
        self.YawFitEqu.addWidget(QLabel('Yaw Fit Equations'))
        self.yawfitbutton = QCheckBox('Yaw Fit Equation')
        self.yawfitbutton.toggled.connect(lambda: self.addtoSolver(YawFit))
        self.yawfitbutton.setChecked(True)  #YawFit is default eqn selected
        self.YawFitEqu.addWidget(self.yawfitbutton)
        self.YawFitEqu.addStretch()
        
        # add equ Lists to Equ Row1
        self.equrow1.addLayout(self.PLEqu)
        self.equrow1.addLayout(self.YawFitEqu)
        self.equrow1.addStretch()
        
        # add equrow1 to right2layout
        self.right2layout.addLayout(self.equrow1)
        self.right2layout.addStretch()
        
        self.secondpage = QWidget()
        self.secondpage.setLayout(self.right2layout)
        
        # add second page widget to rightlayout
        self.rightlayout.addWidget(self.secondpage)
        
        
        # add left and right layouts to mainlayout
        self.mainlayout.addLayout(self.leftlayout)
        self.mainlayout.addLayout(self.rightlayout)
        
        
        # create widget to hold mainlayout
        maincontainer = QWidget()
        maincontainer.setLayout(self.mainlayout)
        
        # places our main container widget into our main window 
        # (funciton of QMainWindow) 
        self.setMinimumSize(750, 600)
        self.setCentralWidget(maincontainer)
        
        
    def addtoSolver(self, equation):
        self=self
        if equation not in self.equationlist:
            self.equationlist.append(equation)
        else:
            self.equationlist.remove(equation)
        
        
    def showGraphs(self):
        self.rightlayout.setCurrentIndex(1)
        for i in range(self.plottabWidget.count()):
            self.plottabWidget.setTabVisible(i, True)
        
        
    def loadFile(self):
        options = fd.Options()
        self.fileName, _ = fd.getOpenFileName(self, options=options)
        excelfile = pd.ExcelFile(self.fileName)
        sheets = excelfile.sheet_names
        self.populateSheetBox(sheets)
        
        
    def populateSheetBox(self, sheets):
        self.sheetDrop.clear()
        for i in sheets:
            self.sheetDrop.addItem(i)
    
    def runSolver(self):
        self.sheet = self.sheetDrop.currentText()
        datapath = self.fileName
        for i, v in enumerate(self.equationlist):
            temp = v(datapath, self.sheet)
            temp.solveFun()
            temp.createParamBox()
            self.resultstabWidget.addTab(temp.parambox, temp.name)
            temp.createGraph()
            for j, w in enumerate(temp.graphList):    
                vbl = QVBoxLayout()
                vbl.addWidget(w)
                vbl.addWidget(NavTool(w, self))
                container = QWidget()
                container.setLayout(vbl)
                self.plottabWidget.addTab(container, temp.graphList[w])
                self.plottabWidget.setTabVisible(i+j, False)

class YawFit:
    def __init__(self, datapath, sheet):
        self.datapath = datapath
        self.sheet = sheet
        self.name = "Yaw Fit"
        self.paramnames = ['phif', 'phis', 'kfast', 'phif0', 'kslow', 'phis0']
        self.xm = np.arange(0, 90.25, 0.25)
        data = pd.read_excel(self.datapath, self.sheet)
        
        self.phi = np.array(data.iloc[7:19, 5], dtype=float)
        self.station_locations_x_m = np.array(data.iloc[7:19, 3], dtype=float)
        self.station_locations_x_m = self.station_locations_x_m[~np.isnan(self.phi)]
        self.phi = self.phi[~np.isnan(self.phi)]
        self.total_yaw = np.array(data.iloc[7:19, 6], dtype=float) 
        self.total_yaw = self.total_yaw[~np.isnan(self.total_yaw)]
        self.alpha = self.total_yaw*np.cos(np.pi/180*self.phi)
        self.beta = self.total_yaw*np.sin(np.pi/180*self.phi)
        self.gamma = np.sqrt(self.alpha**2+self.beta**2)
        self.parameters = np.array(data.iloc[2:12, 24])
        
        phif, phis, kfast, phif0, kslow, phis0 = 1, -1, 1, 360, 1, 1
        self.x0 = (phif, phis, kfast, phif0, kslow, phis0)
        
    def solveFun(self):
        self.finalx0 = fmin(self.objective, self.x0, constraints=self.constraint)
        self.finalrms = self.objective(self.finalx0)
        phif, phis, kfast, phif0, kslow, phis0 = self.finalx0
        x0 = self.parameters[0]
        lamf, lams, betar = self.parameters[7:10]
        self.afinal = kfast*np.exp(lamf*(self.xm-x0))*np.cos(np.pi/180*(phif0+phif*(self.xm-x0)))+kslow*np.exp(lams*(self.xm-x0))*np.cos(np.pi/180*(phis0+phis*(self.xm-x0)))
        self.bfinal = betar+kfast*np.exp(lamf*(self.xm-x0))*np.sin(np.pi/180*(phif0+phif*(self.xm-x0)))+kslow*np.exp(lams*(self.xm-x0))*np.sin(np.pi/180*(phis0+phis*(self.xm-x0)))
        self.gfinal = np.sqrt(self.afinal**2+self.bfinal**2)
        
        self.atarget = kfast*np.exp(lamf*(self.station_locations_x_m[-1]-x0))*np.cos(np.pi/180*(phif0+phif*(self.station_locations_x_m[-1]-x0)))+kslow*np.exp(lams*(self.station_locations_x_m[-1]-x0))*np.cos(np.pi/180*(phis0+phis*(self.station_locations_x_m[-1]-x0)))
        self.btarget = betar+kfast*np.exp(lamf*(self.station_locations_x_m[-1]-x0))*np.sin(np.pi/180*(phif0+phif*(self.station_locations_x_m[-1]-x0)))+kslow*np.exp(lams*(self.station_locations_x_m[-1]-x0))*np.sin(np.pi/180*(phis0+phis*(self.station_locations_x_m[-1]-x0)))
        self.gtarget = np.sqrt(self.atarget**2+self.btarget**2)
        
    def constraint(self, x):
        x[1] = -x[0]
        return x
    
    def objective(self, x):
        phif, phis, kfast, phif0, kslow, phis0 = x
        station_locations_x_m = self.station_locations_x_m
        x0 = self.parameters[0]
        lamf, lams, betar = self.parameters[7:10]
        a = kfast*np.exp(lamf*(station_locations_x_m-x0))*np.cos(np.pi/180*(phif0+phif*(station_locations_x_m-x0)))+kslow*np.exp(lams*(station_locations_x_m-x0))*np.cos(np.pi/180*(phis0+phis*(station_locations_x_m-x0)))
        b = betar+kfast*np.exp(lamf*(station_locations_x_m-x0))*np.sin(np.pi/180*(phif0+phif*(station_locations_x_m-x0)))+kslow*np.exp(lams*(station_locations_x_m-x0))*np.sin(np.pi/180*(phis0+phis*(station_locations_x_m-x0)))
        return self.rms(a, b)
    
    def rms(self, a, b):
        adiff = self.alpha-a
        bdiff = self.beta-b
        arms = adiff**2
        brms = bdiff**2
        return np.sqrt(np.mean([arms, brms]))
    
    def createGraph(self):
        
        self.graph1 = MplCanvas(self, width=5, height=4, dpi=100)
        graph1 = self.graph1.axes
        yawrangefit, = graph1.plot(self.xm, self.gfinal, 'k')
        graph1.annotate('RMS: {:.8f}'.format(self.finalrms), [0, 10], xycoords='figure pixels')
        # yawrangepoint, = plt.plot(station_locations_x_m, gammaanapoint, 'ko')
        yawrangeexp, = graph1.plot(self.station_locations_x_m, self.gamma, 'ko', markerfacecolor= 'w')
        yawrangetargetfit, = graph1.plot(self.station_locations_x_m[-1], self.gtarget, 'ro', markeredgecolor='k')
        yawrangefit.set_label('Fit')
        # yawrangepoint.set_label('Analytical Fit')
        yawrangeexp.set_label('Data')
        graph1.set_title('EF-9 Shot {}'.format(self.sheet))
        graph1.set_xlabel("Range Location (m)")
        graph1.set_ylabel("Total Yaw (deg)")
        graph1.legend(loc='best')
        graph1.grid()
        
        self.graph2 = MplCanvas(self, width=5, height=4, dpi=100)
        graph2 = self.graph2.axes
        yawpitchfit, = graph2.plot(self.bfinal, self.afinal, 'k')
        graph2.annotate('RMS: {:.8f}'.format(self.finalrms), [0, 10], xycoords='figure pixels')
        yawpitchtargetfit, = graph2.plot(self.btarget, self.atarget, 'ro', markeredgecolor='k')
        yawpitchexp, = graph2.plot(self.beta, self.alpha, 'ko', markerfacecolor='w')
        yawpitchfit.set_label('Fit')
        yawpitchexp.set_label('Data')
        graph2.axis([-5.0, 5.0, -5.0, 5.0])
        graph2.set_title('EF-9 Shot {}'.format(self.sheet))
        graph2.set_xlabel("Yaw Angle (deg)")
        graph2.set_ylabel("Pitch Angle (deg)")
        graph2.legend(loc='best')
        graph2.grid()
        
        self.graph3 = MplCanvas(self, width=5, height=4, dpi=100)
        graph3 = self.graph3.axes
        alpharangefit, = graph3.plot(self.xm, self.afinal, 'k')
        graph3.annotate('RMS: {:.8f}'.format(self.finalrms), [0, 10], xycoords='figure pixels')
        alpharangeexp, = graph3.plot(self.station_locations_x_m, self.alpha, 'ko', markerfacecolor='w')
        alpharangefit.set_label('Fit')
        alpharangeexp.set_label('Data')
        graph3.set_title('EF-9 Shot {}'.format(self.sheet))
        graph3.set_xlabel("Range Location (m)")
        graph3.set_ylabel("Alpha (deg)")
        graph3.legend(loc='best')
        graph3.grid()
        
        self.graph4 = MplCanvas(self, width=5, height=4, dpi=100)
        graph4 = self.graph4.axes
        betarangefit, = graph4.plot(self.xm, self.bfinal, 'k')
        graph4.annotate('RMS: {:.8f}'.format(self.finalrms), [0, 10], xycoords='figure pixels')
        betarangeexp, = graph4.plot(self.station_locations_x_m, self.beta, 'ko', markerfacecolor='w')
        betarangefit.set_label('Fit')
        betarangeexp.set_label('Data')
        graph4.set_title('EF-9 Shot {}'.format(self.sheet))
        graph4.set_xlabel("Range Location (m)")
        graph4.set_ylabel("Beta (deg)")
        graph4.legend(loc='best')
        graph4.grid()
        
        self.graphList = {self.graph1:'Total Yaw vs Range {}'.format(self.sheet), 
                          self.graph2:'Yaw vs Pitch {}'.format(self.sheet), 
                          self.graph3:'Pitch vs Range {}'.format(self.sheet), 
                          self.graph4:'Yaw vs Range {}'.format(self.sheet)}
        
    def createParamBox(self):
        paramlist = zip(self.paramnames, self.finalx0)
        paramstr = "RMS: {} \nParameters \n".format(self.finalrms)
        texttocopy = ""
        for i in paramlist:
            paramstr += "{}: {}\n".format(i[0], i[1])
            texttocopy += "{}\n".format(i[1])
        self.parambox = QLabel(paramstr)
        #Add copyable text of the results to clipboard
        QApplication.clipboard().setText(texttocopy)
        

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
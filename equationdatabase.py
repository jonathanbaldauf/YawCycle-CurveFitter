import numpy as np

from mystic.solvers import fmin
from create_canvas import MplCanvas, MplCanvas3d
import pandas as pd
from PyQt5.QtWidgets import QLabel

class lanzOdermattBasic:
    def __init__(self, datapath, sheet):
        self.datapath = datapath
        self.sheet = sheet
        self.name = 'Lanz-Odermatt Basic'
        self.vel = np.arange(0.05, 5, 0.05)
        data = pd.read_excel(self.datapath, self.sheet)
        self.epL = np.array(data.iloc[2:9, 3], dtype=float)
        self.expvel = np.array(data.iloc[2:9, 2], dtype=float)
        self.params = (self.epL, self.expvel)
        a, b = 1, 1
        self.x0 = (a, b)
        
    def solveFun(self):
        self.finalx0 = fmin(self.objective, self.x0, args=self.params)
        self.finalrms = self.objective(self.finalx0, *self.params)
        a, b = self.finalx0
        self.p_over_L = a * np.exp(-(b ** 2 / self.vel ** 2))
        
    def constraint(self):
        self=self

    def objective(self, x0, *params):
        a, b = x0
        v = self.expvel
        p_over_L = a * np.exp(-(b ** 2 / v ** 2))
        return self.rms(p_over_L)
    
    def rms(self, apL):
        error = apL - self.epL
        error_squared = error ** 2
        rms = np.sqrt(np.average(error_squared))
        return rms
    
    def createGraph(self):
        self.graph = MplCanvas(self, width=5, height=4, dpi=100)
        graph = self.graph.axes
        bestfit, = graph.plot(self.vel, self.p_over_L, 'k')
        graph.annotate('RMS: {:.8f}'.format(self.finalrms), [350, 100], xycoords='figure pixels')
        exp_fit, = graph.plot(self.expvel, self.epL, markerfacecolor = 'w', markeredgecolor='k', marker='o', linestyle='none')
        exp_fit.set_label('Experimental Fit')
        bestfit.set_label('Best Fit')
        graph.set_title("Velocity vs P/L")
        graph.set_xlabel("Velocity (km/s)")
        graph.set_ylabel("P/L")
        graph.legend(loc='best')
        graph.grid()
        self.graphList = {self.graph: self.name}
        
    def createParamBox(self):
        params = ['a', 'b']
        paramlist = zip(params, self.finalx0)
        paramstr = "RMS: {} \nParameters \n".format(self.finalrms)
        for i in paramlist:
            paramstr += "{}: {}\n".format(i[0], i[1])
        self.parambox = QLabel(paramstr)
        
        
class lanzOdermattExtra:
    def __init__(self, datapath, sheet):
        self.datapath = datapath
        self.sheet = sheet
        self.name = 'Lanz-Odermatt Extras'
        self.vel = np.arange(0.05, 5, 0.05)
        data = pd.read_excel(self.datapath, self.sheet)
        self.epL = np.array(data.iloc[2:6, 3], dtype=float)
        self.expvel = np.array(data.iloc[2:6, 2], dtype=float)
        self.target_uts = data.iloc[4,6]
        self.params = tuple(data.iloc[9:15, 6])
        a1, a2, m = 1, 1, 1
        self.x0 = (a1, a2, m)
        
    def solveFun(self):
        self.finalx0 = fmin(self.objective, self.x0, args=self.params)
        self.finalrms = self.objective(self.finalx0, *self.params)
        a1, a2, m = self.finalx0
        penetrator_density, target_density, target_obliquity, penetrator_ld, _, c_parameter = self.params
        ld_function = 1 + (a1 * (1 / penetrator_ld)) * (1 - np.tanh((penetrator_ld - 10) / a2))
        self.p_over_L = ld_function*np.cos((np.pi/180)*target_obliquity)**m*np.sqrt(penetrator_density/target_density)*np.exp(-(c_parameter*self.target_uts)/(penetrator_density*self.vel**2))
        
    def constraint(self):
        self=self
        
    def objective(self, x0, *params):
        a1, a2, m = x0
        target_uts = self.target_uts
        v = self.expvel
        penetrator_density, target_density, target_obliquity, penetrator_ld, _, c_parameter = params
        ld_function = 1 + (a1 * (1 / penetrator_ld)) * (1 - np.tanh((penetrator_ld - 10) / a2))
        p_over_L = ld_function*np.cos((np.pi/180)*target_obliquity)**m*np.sqrt(penetrator_density/target_density)*np.exp(-(c_parameter*target_uts)/(penetrator_density*v**2))
        return self.rms(p_over_L)
    
    def rms(self, apL):
        error = apL - self.epL
        error_squared = error ** 2
        rms = np.sqrt(np.average(error_squared))
        return rms
    
    def createGraph(self):
        self.graph = MplCanvas(self, width=5, height=4, dpi=100)
        graph = self.graph.axes
        bestfit, = graph.plot(self.vel, self.p_over_L, 'k')
        graph.annotate('RMS: {:.8f}'.format(self.finalrms), [350, 100], xycoords='figure pixels')
        exp_fit, = graph.plot(self.expvel, self.epL, markerfacecolor = 'w', markeredgecolor='k', marker='o', linestyle='none')
        exp_fit.set_label('Experimental Fit')
        bestfit.set_label('Best Fit')
        graph.set_title("Velocity vs P/L")
        graph.set_xlabel("Velocity (km/s)")
        graph.set_ylabel("P/L")
        graph.legend(loc='best')
        graph.grid()
        self.graphList = {self.graph: self.name}
        
    def createParamBox(self):
        params = ['a1', 'a2', 'm']
        paramlist = zip(params, self.finalx0)
        paramstr = "RMS: {} \nParameters \n".format(self.finalrms)
        for i in paramlist:
            paramstr += "{}: {}\n".format(i[0], i[1])
        self.parambox = QLabel(paramstr)


class YawFit:
    def __init__(self, datapath, sheet):
        self.datapath = datapath
        self.sheet = sheet
        self.name = "Yaw Fit"
        self.paramnames = ['phif', 'phis', 'kfast', 'phif0', 'kslow', 'phis0']
        self.xm = np.arange(0, 90.25, 0.25)
        data = pd.read_excel(self.datapath, self.sheet)
        
        self.phi = np.array(data.iloc[7:18, 5], dtype=float)
        self.station_locations_x_m = np.array(data.iloc[7:18, 3], dtype=float)
        self.station_locations_x_m = self.station_locations_x_m[~np.isnan(self.phi)]
        self.phi = self.phi[~np.isnan(self.phi)]
        self.total_yaw = np.array(data.iloc[7:18, 6], dtype=float) 
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
        for i in paramlist:
            paramstr += "{}: {}\n".format(i[0], i[1])
        self.parambox = QLabel(paramstr)
        
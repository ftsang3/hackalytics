import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QHBoxLayout,
    QListView,
    QAbstractItemView,
    QMessageBox,
    QLineEdit,
    QMainWindow,
    QLabel
)

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem
) 

# new imports above this line

from mpl_toolkits import mplot3d
#%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import RegularPolygon
from matplotlib.patches import Arc
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl
import pandas as pd


#new stuff below this line
mpl.use('QT5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#change csv inputs here
df = pd.read_csv("02_02_21_Scrimmage.csv")
validlist = df.index[~np.isnan(df['HangTime'])].tolist()
validlist = [i+1 for i in validlist]
valid = ', '.join(str(e) for e in validlist)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("3D Baseball Batting Visualization")
        
        # a figure instance to plot on
        #self.figure = Figure()
        
        self.setGeometry(450, 250, 640, 480)

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        #self.canvas = FigureCanvas(self.figure)
        
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        self.validpitchlabel = QLabel("Valid Pitches (pitches with bats): %s" % valid)
        self.validpitchlabel.setWordWrap(True)

        self.pitchnumberlabel = QLabel("Pitch Number(s)")
        self.pitchnumberedit = QLineEdit(self)
        #self.pitchnumberedit.setPlaceholderText("None")

        
        #self.batternamelabel = QLabel("Batter Name")
        #self.batternameedit = QLineEdit(self)
        #self.batternameedit.setPlaceholderText("None")
        

        #self.pitchnumberlabel = QLabel("File Name")
        #self.textbox1 = QLineEdit(self)
        #self.textbox2 = QLineEdit(self)
        
        # Just some button connected to `plot` method
        self.plotbutton = QPushButton('Plot')
        self.plotbutton.clicked.connect(self.plotbuttonfunction)
        
        
        '''

        self.add_button = QPushButton("+")
        self.add_button.setEnabled(False)

        self.minus_button = QPushButton("-")
        self.minus_button.setEnabled(False)

        self.multiply_button = QPushButton("*")
        self.multiply_button.setEnabled(False)

        self.divide_button = QPushButton("/")
        self.divide_button.setEnabled(False)


        self.add_button.clicked.connect(self.add_items)

        self.minus_button.clicked.connect(self.minus_items)

        self.multiply_button.clicked.connect(self.multiply_items)

        self.divide_button.clicked.connect(self.divide_items)

        '''



        vbox = QVBoxLayout()
        vbox.addWidget(self.validpitchlabel)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.pitchnumberlabel)
        hbox1.addWidget(self.pitchnumberedit)
        vbox.addLayout(hbox1)
        
        #hbox2 = QHBoxLayout()
        #hbox2.addWidget(self.batternamelabel)
        #hbox2.addWidget(self.batternameedit)
        #vbox.addLayout(hbox2)
        
        vbox.addWidget(self.plotbutton)
        self.setLayout(vbox)

        

        '''
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        '''

    def plotbuttonfunction(self):
        if self.pitchnumberedit.text():
            pitchnumbers = self.pitchnumberedit.text()
            pitchnumberslist = pitchnumbers.split(",")

            for pitchno in pitchnumberslist:
                if np.isnan(df['HangTime'][int(pitchno)-1]):
                    self.w = isnanwindow()
                    self.w.show()
                    return
            
            fig = plt.figure(figsize = (10,10))
            ax = plt.axes(projection='3d')
            ax.grid()
            
            
            # default ranges
            '''
            ax.set_xlim(-10, 90)
            ax.set_ylim(-50, 50)
            ax.set_zlim(-25, 25)
            '''
            
            # top right view
            #'''
            ax.view_init(elev = 15., azim = -157)
            ax.set_xlim(-10, 90)
            ax.set_ylim(-50, 50)
            ax.set_zlim(-25, 25)
            
            ax.dist = 9
            #'''

            # batter view
            '''
            ax.view_init(elev = 7., azim = -180)
            ax.set_xlim(-10, 90)
            ax.set_ylim(-50, 50)
            ax.set_zlim(-25, 25)
            
            ax.dist = 9
            '''

            # top right view
            '''
            ax.view_init(elev = 15., azim = -157)
            ax.set_xlim(-10, 90)
            ax.set_ylim(-50, 50)
            ax.set_zlim(-25, 25)
            
            ax.dist = 9
            '''                            
            
            
            for pitchno in pitchnumberslist:
                pitchtraj_x0 = df['HitTrajectoryXc0'][int(pitchno)-1]
                pitchtraj_x1 = df['HitTrajectoryXc1'][int(pitchno)-1]
                pitchtraj_x2 = df['HitTrajectoryXc2'][int(pitchno)-1]
                pitchtraj_x3 = df['HitTrajectoryXc3'][int(pitchno)-1]
                pitchtraj_x4 = df['HitTrajectoryXc4'][int(pitchno)-1]
                pitchtraj_x5 = df['HitTrajectoryXc5'][int(pitchno)-1]
                pitchtraj_x6 = df['HitTrajectoryXc6'][int(pitchno)-1]
                pitchtraj_x7 = df['HitTrajectoryXc7'][int(pitchno)-1]
                pitchtraj_x8 = df['HitTrajectoryXc8'][int(pitchno)-1]
                
                pitchtraj_y0 = df['HitTrajectoryYc0'][int(pitchno)-1]
                pitchtraj_y1 = df['HitTrajectoryYc1'][int(pitchno)-1]
                pitchtraj_y2 = df['HitTrajectoryYc2'][int(pitchno)-1]
                pitchtraj_y3 = df['HitTrajectoryYc3'][int(pitchno)-1]
                pitchtraj_y4 = df['HitTrajectoryYc4'][int(pitchno)-1]
                pitchtraj_y5 = df['HitTrajectoryYc5'][int(pitchno)-1]
                pitchtraj_y6 = df['HitTrajectoryYc6'][int(pitchno)-1]
                pitchtraj_y7 = df['HitTrajectoryYc7'][int(pitchno)-1]
                pitchtraj_y8 = df['HitTrajectoryYc8'][int(pitchno)-1]
                
                pitchtraj_z0 = df['HitTrajectoryZc0'][int(pitchno)-1]
                pitchtraj_z1 = df['HitTrajectoryZc1'][int(pitchno)-1]
                pitchtraj_z2 = df['HitTrajectoryZc2'][int(pitchno)-1]
                pitchtraj_z3 = df['HitTrajectoryZc3'][int(pitchno)-1]
                pitchtraj_z4 = df['HitTrajectoryZc4'][int(pitchno)-1]
                pitchtraj_z5 = df['HitTrajectoryZc5'][int(pitchno)-1]
                pitchtraj_z6 = df['HitTrajectoryZc6'][int(pitchno)-1]
                pitchtraj_z7 = df['HitTrajectoryZc7'][int(pitchno)-1]
                pitchtraj_z8 = df['HitTrajectoryZc8'][int(pitchno)-1]
                
                hangtime = df['HangTime'][int(pitchno)-1]
                                    
                t = np.arange(0, (hangtime), 0.001)
                
                if np.isnan(pitchtraj_x2):
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1     
                    
                    '''
                    xfunc = lambda t: x0 + x1 * t 
                    yfunc = lambda t: -y0 - y1 * t 
                    zfunc = lambda t: z0 + z1 * t 
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc, otypes = [int])
                    yfunction = np.vectorize(yfunc, otypes = [int])
                    zfunction = np.vectorize(zfunc, otypes = [int])
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    '''
                    x = [x0 + x1 * time for time in t]
                    y = [-y0 - y1 * time for time in t]
                    z = [z0 + z1 * time for time in t]
                    
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(x0 + x1 * (hangtime), -y0 - y1 * (hangtime), z0 + z1 * (hangtime))
                    
                    axes = plt.gca()
                
                    axes.xaxis.label.set_size(20)
                    axes.yaxis.label.set_size(1)
                    
                    
                    plt.axis('off')
                    
                    
                    #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
                    
                    pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
                    ax.add_patch(pitching_mound)
                    art3d.pathpatch_2d_to_3d(pitching_mound)
                    
                    pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
                    ax.add_patch(pitchers_rubber)
                    art3d.pathpatch_2d_to_3d(pitchers_rubber)
                    
                    polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
                    ax.add_patch(polygon)
                    art3d.pathpatch_2d_to_3d(polygon)
                    
                    '''
                    strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
                    ax.add_patch(strikezone)
                    art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
                    '''
                    
                    outerarc = Arc((60.5, -1), width = 95, height = 95, angle = 0.0, theta1 = 0, theta2 = 90)
                    ax.add_patch(outerarc)
                    art3d.pathpatch_2d_to_3d(outerarc)
                    
                    thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(thirdbase)
                    art3d.pathpatch_2d_to_3d(thirdbase)
                    
                    firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(firstbase)
                    art3d.pathpatch_2d_to_3d(firstbase)
                    
                    secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(secondbase)
                    art3d.pathpatch_2d_to_3d(secondbase)
            
            
                    """                                                                                                                                                    
                    Scaling is done from here...                                                                                                                           
                    """
                    x_scale=1
                    y_scale=1
                    z_scale=0.5
                    
                    scale=np.diag([x_scale, y_scale, z_scale, 1.0])
                    scale=scale*(1.0/scale.max())
                    scale[3,3]=1.0
                    
                    def short_proj():
                      return np.dot(Axes3D.get_proj(ax), scale)
                    
                    ax.get_proj=short_proj
                    
                    plt.show()
            

            #self.canvas.draw()
                
                elif np.isnan(pitchtraj_x3):
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    x2 = pitchtraj_x2
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    y2 = pitchtraj_z2
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1  
                    z2 = pitchtraj_y2
                    
                    '''
                    xfunc = lambda t: x0 + x1 * t + x2 * t**2 
                    yfunc = lambda t: -y0 - y1 * t - y2 * t**2 
                    zfunc = lambda t: z0 + z1 * t + z2 * t**2 
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc, otypes = [int])
                    yfunction = np.vectorize(yfunc, otypes = [int])
                    zfunction = np.vectorize(zfunc, otypes = [int])
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    '''
                    
                    x = [x0 + x1 * time + x2 * time**2 for time in t]
                    y = [-y0 - y1 * time - y2 * time**2 for time in t]
                    z = [z0 + z1 * time + z2 * time**2 for time in t]
                    
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(x0 + x1 * hangtime + x2 * hangtime**2, -y0 - y1 * hangtime - y2 * hangtime**2, z0 + z1 * hangtime + z2 * hangtime**2)
                
                    axes = plt.gca()
        
                    axes.xaxis.label.set_size(20)
                    axes.yaxis.label.set_size(1)
                    
                    
                    plt.axis('off')
                    
                    
                    #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
                    
                    pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
                    ax.add_patch(pitching_mound)
                    art3d.pathpatch_2d_to_3d(pitching_mound)
                    
                    pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
                    ax.add_patch(pitchers_rubber)
                    art3d.pathpatch_2d_to_3d(pitchers_rubber)
                    
                    polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
                    ax.add_patch(polygon)
                    art3d.pathpatch_2d_to_3d(polygon)
                    
                    '''
                    strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
                    ax.add_patch(strikezone)
                    art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
                    '''
                    
                    thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(thirdbase)
                    art3d.pathpatch_2d_to_3d(thirdbase)
                    
                    firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(firstbase)
                    art3d.pathpatch_2d_to_3d(firstbase)
                    
                    secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(secondbase)
                    art3d.pathpatch_2d_to_3d(secondbase)
            
            
                    """                                                                                                                                                    
                    Scaling is done from here...                                                                                                                           
                    """
                    x_scale=1
                    y_scale=1
                    z_scale=0.5
                    
                    scale=np.diag([x_scale, y_scale, z_scale, 1.0])
                    scale=scale*(1.0/scale.max())
                    scale[3,3]=1.0
                    
                    def short_proj():
                      return np.dot(Axes3D.get_proj(ax), scale)
                    
                    ax.get_proj=short_proj
                    
                    plt.show()
                    
    
                    #self.canvas.draw()
                else:
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    x2 = pitchtraj_x2
                    x3 = pitchtraj_x3
                    x4 = pitchtraj_x4
                    x5 = pitchtraj_x5
                    x6 = pitchtraj_x6
                    x7 = pitchtraj_x7
                    x8 = pitchtraj_x8
                    
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    y2 = pitchtraj_z2
                    y3 = pitchtraj_z3
                    y4 = pitchtraj_z4
                    y5 = pitchtraj_z5
                    y6 = pitchtraj_z6
                    y7 = pitchtraj_z7
                    y8 = pitchtraj_z8
                    
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1
                    z2 = pitchtraj_y2
                    z3 = pitchtraj_y3
                    z4 = pitchtraj_y4
                    z5 = pitchtraj_y5
                    z6 = pitchtraj_y6
                    z7 = pitchtraj_y7
                    z8 = pitchtraj_y8
                    
                    
                    '''
                    xfunc = lambda t: x0 + x1 * t + x2 * t**2 + x3 * t**3 + x4 * t**4 + x5 * t**5 + x6 * t**6 + x7 * t**7 + x8 * t**8 
                    yfunc = lambda t: -y0 - y1 * t - y2 * t**2 - y3 * t**3 - y4 * t**4 - y5 * t**5 - y6 * t**6 -  y7 * t**7 - y8 * t**8
                    zfunc = lambda t: z0 + z1 * t + z2 * t**2 + z3 * t**3 + z4 * t**4 + z5 * t**5 + z6 * t**6 + z7 * t**7 + z8 * t**8
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc, otypes = [int])
                    yfunction = np.vectorize(yfunc, otypes = [int])
                    zfunction = np.vectorize(zfunc, otypes = [int])
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    '''
                    x = [x0 + x1 * time + x2 * time**2 + x3 * time**3 + x4 * time**4 + x5 * time**5 + x6 * time**6 + x7 * time**7 + x8 * time**8  for time in t]
                    y = [-y0 - y1 * time - y2 * time**2 - y3 * time**3 - y4 * time**4 - y5 * time**5 - y6 * time**6 -  y7 * time**7 - y8 * time**8 for time in t]
                    z = [z0 + z1 * time + z2 * time**2 + z3 * time**3 + z4 * time**4 + z5 * time**5 + z6 * time**6 + z7 * time**7 + z8 * time**8 for time in t]
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(x0 + x1 * hangtime + x2 * hangtime**2 + x3 * hangtime**3 + x4 * hangtime**4 + x5 * hangtime**5 + x6 * hangtime**6 + x7 * hangtime**7 + x8 * hangtime**8, -y0 - y1 * hangtime - y2 * hangtime**2 - y3 * hangtime**3 - y4 * hangtime**4 - y5 * hangtime**5 - y6 * hangtime**6 -  y7 * hangtime**7 - y8 * hangtime**8, z0 + z1 * hangtime + z2 * hangtime**2 + z3 * hangtime**3 + z4 * hangtime**4 + z5 * hangtime**5 + z6 * hangtime**6 + z7 * hangtime**7 + z8 * hangtime**8)
                    
                    
                    axes = plt.gca()
                
                    axes.xaxis.label.set_size(20)
                    axes.yaxis.label.set_size(1)
                    
                    
                    plt.axis('off')
                    
                    
                    #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
                    
                    pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
                    ax.add_patch(pitching_mound)
                    art3d.pathpatch_2d_to_3d(pitching_mound)
                    
                    pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
                    ax.add_patch(pitchers_rubber)
                    art3d.pathpatch_2d_to_3d(pitchers_rubber)
                    
                    polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
                    ax.add_patch(polygon)
                    art3d.pathpatch_2d_to_3d(polygon)
                    
                    '''
                    strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
                    ax.add_patch(strikezone)
                    art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
                    '''
            
                    thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(thirdbase)
                    art3d.pathpatch_2d_to_3d(thirdbase)
                    
                    firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(firstbase)
                    art3d.pathpatch_2d_to_3d(firstbase)
                    
                    secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = False, color = 'b')
                    ax.add_patch(secondbase)
                    art3d.pathpatch_2d_to_3d(secondbase)
            
                    """                                                                                                                                                    
                    Scaling is done from here...                                                                                                                           
                    """
                    x_scale=1
                    y_scale=1
                    z_scale=0.5
                    
                    scale=np.diag([x_scale, y_scale, z_scale, 1.0])
                    scale=scale*(1.0/scale.max())
                    scale[3,3]=1.0
                    
                    def short_proj():
                      return np.dot(Axes3D.get_proj(ax), scale)
                    
                    ax.get_proj=short_proj
                    
                    plt.show()
                    
    
                    #self.canvas.draw()
                    
                '''  
                axes = plt.gca()
            
                axes.xaxis.label.set_size(20)
                axes.yaxis.label.set_size(1)
                
                
                plt.axis('off')
                
                
                #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
                
                pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
                ax.add_patch(pitching_mound)
                art3d.pathpatch_2d_to_3d(pitching_mound)
                
                pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
                ax.add_patch(pitchers_rubber)
                art3d.pathpatch_2d_to_3d(pitchers_rubber)
                
                polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
                ax.add_patch(polygon)
                art3d.pathpatch_2d_to_3d(polygon)
                
                strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
                ax.add_patch(strikezone)
                art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
        
        
                """                                                                                                                                                    
                Scaling is done from here...                                                                                                                           
                """
                x_scale=1
                y_scale=0.5
                z_scale=0.5
                
                scale=np.diag([x_scale, y_scale, z_scale, 1.0])
                scale=scale*(1.0/scale.max())
                scale[3,3]=1.0
                
                def short_proj():
                  return np.dot(Axes3D.get_proj(ax), scale)
                
                ax.get_proj=short_proj
                

                #self.canvas.draw()
                '''
            
        else:
            '''
            if self.batternameedit.text():
                battername = self.batternameedit.text()
                battername = battername.strip()
                pitchnumberslist = df.index[df['Batter'] == battername].tolist()
                
                fig = plt.figure(figsize = (10,10))
                ax = plt.axes(projection='3d')
                ax.grid()
                
                ax.set_xlim(-10, 90)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                for pitchno in pitchnumberslist:
                    pitchtraj_x0 = df['PitchTrajectoryXc0'][int(pitchno)]
                    pitchtraj_x1 = df['PitchTrajectoryXc1'][int(pitchno)]
                    pitchtraj_x2 = df['PitchTrajectoryXc2'][int(pitchno)]
                    pitchtraj_y0 = df['PitchTrajectoryYc0'][int(pitchno)]
                    pitchtraj_y1 = df['PitchTrajectoryYc1'][int(pitchno)]
                    pitchtraj_y2 = df['PitchTrajectoryYc2'][int(pitchno)]
                    pitchtraj_z0 = df['PitchTrajectoryZc0'][int(pitchno)]
                    pitchtraj_z1 = df['PitchTrajectoryZc1'][int(pitchno)]
                    pitchtraj_z2 = df['PitchTrajectoryZc2'][int(pitchno)]
                    zonetime = df['ZoneTime'][int(pitchno)]
                                        
                    t = np.arange(0, zonetime, 0.001)
                    
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    x2 = pitchtraj_x2
                    
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    y2 = pitchtraj_z2
                    
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1
                    z2 = pitchtraj_y2
                    
                    xfunc = lambda t: x0 + x1 * t + x2 * t**2
                    yfunc = lambda t: -y0 - y1 * t - y2 * t**2
                    zfunc = lambda t: z0 + z1 * t + z2 * t**2
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc)
                    yfunction = np.vectorize(yfunc)
                    zfunction = np.vectorize(zfunc)
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(xfunc(zonetime), yfunc(zonetime), zfunc(zonetime))
                    #ax.set_title('3D Parametric Plot')
                    
                    # Set axes label
                    #ax.set_xlabel('x', labelpad=20)
                    #ax.set_ylabel('y', labelpad=20)
                    #ax.set_zlabel('z', labelpad=20)
                    
                    #ax.view_init(0, 90)
                    
                axes = plt.gca()
            
                axes.xaxis.label.set_size(20)
                axes.yaxis.label.set_size(1)
                
                
                plt.axis('off')
                
                
                #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
                
                pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
                ax.add_patch(pitching_mound)
                art3d.pathpatch_2d_to_3d(pitching_mound)
                
                pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
                ax.add_patch(pitchers_rubber)
                art3d.pathpatch_2d_to_3d(pitchers_rubber)
                
                polygon = RegularPolygon((0, 0), numVertices = 5, radius = 1, orientation = 1.57)
                ax.add_patch(polygon)
                art3d.pathpatch_2d_to_3d(polygon)
        
                strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
                ax.add_patch(strikezone)
                art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
        
                """                                                                                                                                                    
                Scaling is done from here...                                                                                                                           
                """
                x_scale=1
                y_scale=0.5
                z_scale=0.5
                
                scale=np.diag([x_scale, y_scale, z_scale, 1.0])
                scale=scale*(1.0/scale.max())
                scale[3,3]=1.0
                
                def short_proj():
                  return np.dot(Axes3D.get_proj(ax), scale)
                
                ax.get_proj=short_proj
            '''
            hitnumberslist = df.index[~np.isnan(df['HangTime'])].tolist()
            fig = plt.figure(figsize = (10,10))
            ax = plt.axes(projection='3d')
            ax.grid()
            
            
            ax.set_xlim(-10, 90)
            ax.set_ylim(-50, 50)
            ax.set_zlim(-25, 25)
            
            for hitno in hitnumberslist:
                pitchtraj_x0 = df['HitTrajectoryXc0'][int(hitno)]
                pitchtraj_x1 = df['HitTrajectoryXc1'][int(hitno)]
                pitchtraj_x2 = df['HitTrajectoryXc2'][int(hitno)]
                pitchtraj_x3 = df['HitTrajectoryXc3'][int(hitno)]
                pitchtraj_x4 = df['HitTrajectoryXc4'][int(hitno)]
                pitchtraj_x5 = df['HitTrajectoryXc5'][int(hitno)]
                pitchtraj_x6 = df['HitTrajectoryXc6'][int(hitno)]
                pitchtraj_x7 = df['HitTrajectoryXc7'][int(hitno)]
                pitchtraj_x8 = df['HitTrajectoryXc8'][int(hitno)]
                
                pitchtraj_y0 = df['HitTrajectoryYc0'][int(hitno)]
                pitchtraj_y1 = df['HitTrajectoryYc1'][int(hitno)]
                pitchtraj_y2 = df['HitTrajectoryYc2'][int(hitno)]
                pitchtraj_y3 = df['HitTrajectoryYc3'][int(hitno)]
                pitchtraj_y4 = df['HitTrajectoryYc4'][int(hitno)]
                pitchtraj_y5 = df['HitTrajectoryYc5'][int(hitno)]
                pitchtraj_y6 = df['HitTrajectoryYc6'][int(hitno)]
                pitchtraj_y7 = df['HitTrajectoryYc7'][int(hitno)]
                pitchtraj_y8 = df['HitTrajectoryYc8'][int(hitno)]
                
                pitchtraj_z0 = df['HitTrajectoryZc0'][int(hitno)]
                pitchtraj_z1 = df['HitTrajectoryZc1'][int(hitno)]
                pitchtraj_z2 = df['HitTrajectoryZc2'][int(hitno)]
                pitchtraj_z3 = df['HitTrajectoryZc3'][int(hitno)]
                pitchtraj_z4 = df['HitTrajectoryZc4'][int(hitno)]
                pitchtraj_z5 = df['HitTrajectoryZc5'][int(hitno)]
                pitchtraj_z6 = df['HitTrajectoryZc6'][int(hitno)]
                pitchtraj_z7 = df['HitTrajectoryZc7'][int(hitno)]
                pitchtraj_z8 = df['HitTrajectoryZc8'][int(hitno)]
                
                hangtime = df['HangTime'][int(hitno)]
                                    
                t = np.arange(0, (hangtime), 0.001)
                
                if np.isnan(pitchtraj_x2):
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1     
                    
                    '''
                    xfunc = lambda t: x0 + x1 * t 
                    yfunc = lambda t: -y0 - y1 * t 
                    zfunc = lambda t: z0 + z1 * t 
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc, otypes = [int])
                    yfunction = np.vectorize(yfunc, otypes = [int])
                    zfunction = np.vectorize(zfunc, otypes = [int])
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    '''
                    x = [x0 + x1 * time for time in t]
                    y = [-y0 - y1 * time for time in t]
                    z = [z0 + z1 * time for time in t]
                    
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(x0 + x1 * (hangtime), -y0 - y1 * (hangtime), z0 + z1 * (hangtime))
                
                elif np.isnan(pitchtraj_x3):
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    x2 = pitchtraj_x2
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    y2 = pitchtraj_z2
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1  
                    z2 = pitchtraj_y2
                    
                    '''
                    xfunc = lambda t: x0 + x1 * t + x2 * t**2 
                    yfunc = lambda t: -y0 - y1 * t - y2 * t**2 
                    zfunc = lambda t: z0 + z1 * t + z2 * t**2 
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc, otypes = [int])
                    yfunction = np.vectorize(yfunc, otypes = [int])
                    zfunction = np.vectorize(zfunc, otypes = [int])
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    '''
                    
                    x = [x0 + x1 * time + x2 * time**2 for time in t]
                    y = [-y0 - y1 * time - y2 * time**2 for time in t]
                    z = [z0 + z1 * time + z2 * time**2 for time in t]
                    
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(x0 + x1 * hangtime + x2 * hangtime**2, -y0 - y1 * hangtime - y2 * hangtime**2, z0 + z1 * hangtime + z2 * hangtime**2)
                
                else:
                    x0 = pitchtraj_x0
                    x1 = pitchtraj_x1
                    x2 = pitchtraj_x2
                    x3 = pitchtraj_x3
                    x4 = pitchtraj_x4
                    x5 = pitchtraj_x5
                    x6 = pitchtraj_x6
                    x7 = pitchtraj_x7
                    x8 = pitchtraj_x8
                    
                    y0 = pitchtraj_z0
                    y1 = pitchtraj_z1
                    y2 = pitchtraj_z2
                    y3 = pitchtraj_z3
                    y4 = pitchtraj_z4
                    y5 = pitchtraj_z5
                    y6 = pitchtraj_z6
                    y7 = pitchtraj_z7
                    y8 = pitchtraj_z8
                    
                    z0 = pitchtraj_y0
                    z1 = pitchtraj_y1
                    z2 = pitchtraj_y2
                    z3 = pitchtraj_y3
                    z4 = pitchtraj_y4
                    z5 = pitchtraj_y5
                    z6 = pitchtraj_y6
                    z7 = pitchtraj_y7
                    z8 = pitchtraj_y8
                    
                    
                    '''
                    xfunc = lambda t: x0 + x1 * t + x2 * t**2 + x3 * t**3 + x4 * t**4 + x5 * t**5 + x6 * t**6 + x7 * t**7 + x8 * t**8 
                    yfunc = lambda t: -y0 - y1 * t - y2 * t**2 - y3 * t**3 - y4 * t**4 - y5 * t**5 - y6 * t**6 -  y7 * t**7 - y8 * t**8
                    zfunc = lambda t: z0 + z1 * t + z2 * t**2 + z3 * t**3 + z4 * t**4 + z5 * t**5 + z6 * t**6 + z7 * t**7 + z8 * t**8
                    #x = 55.24204 - 128.23749*t + 14.74645*t^2
                    #y = 6.07255 - 2.40942*t - 10.1644*t^2
                    #z = 2 - 3*t + 4*t^2
                    
                    xfunction = np.vectorize(xfunc, otypes = [int])
                    yfunction = np.vectorize(yfunc, otypes = [int])
                    zfunction = np.vectorize(zfunc, otypes = [int])
                    
                    
                    x = xfunction(t)
                    y = yfunction(t)
                    z = zfunction(t)
                    '''
                    x = [x0 + x1 * time + x2 * time**2 + x3 * time**3 + x4 * time**4 + x5 * time**5 + x6 * time**6 + x7 * time**7 + x8 * time**8  for time in t]
                    y = [-y0 - y1 * time - y2 * time**2 - y3 * time**3 - y4 * time**4 - y5 * time**5 - y6 * time**6 -  y7 * time**7 - y8 * time**8 for time in t]
                    z = [z0 + z1 * time + z2 * time**2 + z3 * time**3 + z4 * time**4 + z5 * time**5 + z6 * time**6 + z7 * time**7 + z8 * time**8 for time in t]
                    ax.plot3D(x, y, z)
                    
                    ax.scatter(x0 + x1 * hangtime + x2 * hangtime**2 + x3 * hangtime**3 + x4 * hangtime**4 + x5 * hangtime**5 + x6 * hangtime**6 + x7 * hangtime**7 + x8 * hangtime**8, -y0 - y1 * hangtime - y2 * hangtime**2 - y3 * hangtime**3 - y4 * hangtime**4 - y5 * hangtime**5 - y6 * hangtime**6 -  y7 * hangtime**7 - y8 * hangtime**8, z0 + z1 * hangtime + z2 * hangtime**2 + z3 * hangtime**3 + z4 * hangtime**4 + z5 * hangtime**5 + z6 * hangtime**6 + z7 * hangtime**7 + z8 * hangtime**8)

                '''
                if np.isnan(pitchtraj_x0):
                    x0 = 0
                else:
                    x0 = pitchtraj_x0
                    
                if np.isnan(pitchtraj_x1):
                    x1 = 0
                else:
                    x1 = pitchtraj_x1
                    
                if np.isnan(pitchtraj_x2):
                    x2 = 0
                else:
                    x2 = pitchtraj_x2
                    
                if np.isnan(pitchtraj_x3):
                    x3 = 0
                else:
                    x3 = pitchtraj_x3
                    
                if np.isnan(pitchtraj_x4):
                    x4 = 0
                else:
                    x4 = pitchtraj_x4
                    
                if np.isnan(pitchtraj_x5):
                    x5 = 0
                else:
                    x5 = pitchtraj_x5
                    
                if np.isnan(pitchtraj_x6):
                    x6 = 0
                else:
                    x6 = pitchtraj_x6
                    
                if np.isnan(pitchtraj_x7):
                    x7 = 0
                else:
                    x7 = pitchtraj_x7
                    
                if np.isnan(pitchtraj_x8):
                    x8 = 0
                else:
                    x8 = pitchtraj_x8
                    
                if np.isnan(pitchtraj_y0):
                    y0 = 0
                else:
                    y0 = pitchtraj_y0
                                            
                if np.isnan(pitchtraj_y1):
                    y1 = 0
                else:
                    y1 = pitchtraj_y1
                                            
                if np.isnan(pitchtraj_y2):
                    y2 = 0
                else:
                    y2 = pitchtraj_y2
                                            
                if np.isnan(pitchtraj_y3):
                    y3 = 0
                else:
                    y3 = pitchtraj_y3
                                            
                if np.isnan(pitchtraj_y4):
                    y4 = 0
                else:
                    y4 = pitchtraj_y4
                                            
                if np.isnan(pitchtraj_y5):
                    y5 = 0
                else:
                    y5 = pitchtraj_y5
                                            
                if np.isnan(pitchtraj_y6):
                    y6 = 0
                else:
                    y6 = pitchtraj_y6
                                            
                if np.isnan(pitchtraj_y7):
                    y7 = 0
                else:
                    y7 = pitchtraj_y7
                                            
                if np.isnan(pitchtraj_y8):
                    y8 = 0
                else:
                    y8 = pitchtraj_y8
                    
                if np.isnan(pitchtraj_z0):
                    z0 = 0
                else:
                    z0 = pitchtraj_z0
                                            
                if np.isnan(pitchtraj_z1):
                    z1 = 0
                else:
                    z1 = pitchtraj_z1
                                            
                if np.isnan(pitchtraj_z2):
                    z2 = 0
                else:
                    z2 = pitchtraj_z2
                                            
                if np.isnan(pitchtraj_z3):
                    z3 = 0
                else:
                    z3 = pitchtraj_z3
                                            
                if np.isnan(pitchtraj_z4):
                    z4 = 0
                else:
                    z4 = pitchtraj_z4
                                            
                if np.isnan(pitchtraj_z5):
                    z5 = 0
                else:
                    z5 = pitchtraj_z5
                                            
                if np.isnan(pitchtraj_z6):
                    z6 = 0
                else:
                    z6 = pitchtraj_z6
                                            
                if np.isnan(pitchtraj_z7):
                    z7 = 0
                else:
                    z7 = pitchtraj_z7
                                            
                if np.isnan(pitchtraj_z8):
                    z8 = 0
                else:
                    z8 = pitchtraj_z8
                
                '''
                
                '''
                x0 = pitchtraj_x0
                x1 = pitchtraj_x1
                x2 = pitchtraj_x2
                x3 = pitchtraj_x3
                x4 = pitchtraj_x4
                x5 = pitchtraj_x5
                x6 = pitchtraj_x6
                x7 = pitchtraj_x7
                x8 = pitchtraj_x8
                
                y0 = pitchtraj_z0
                y1 = pitchtraj_z1
                y2 = pitchtraj_z2
                y3 = pitchtraj_z3
                y4 = pitchtraj_z4
                y5 = pitchtraj_z5
                y6 = pitchtraj_z6
                y7 = pitchtraj_z7
                y8 = pitchtraj_z8
                
                z0 = pitchtraj_y0
                z1 = pitchtraj_y1
                z2 = pitchtraj_y2
                z3 = pitchtraj_y3
                z4 = pitchtraj_y4
                z5 = pitchtraj_y5
                z6 = pitchtraj_y6
                z7 = pitchtraj_y7
                z8 = pitchtraj_y8
                
                xfunc = lambda t: x0 + x1 * t + x2 * t**2 + x3 * t**3 + x4 * t**4 + x5 * t**5 + x6 * t**6 + x7 * t**7 + x8 * t**8 
                yfunc = lambda t: -y0 - y1 * t - y2 * t**2 - y3 * t**3 - y4 * t**4 - y5 * t**5 - y6 * t**6 -  y7 * t**7 - y8 * t**8
                zfunc = lambda t: z0 + z1 * t + z2 * t**2 + z3 * t**3 + z4 * t**4 + z5 * t**5 + z6 * t**6 + z7 * t**7 + z8 * t**8
                #x = 55.24204 - 128.23749*t + 14.74645*t^2
                #y = 6.07255 - 2.40942*t - 10.1644*t^2
                #z = 2 - 3*t + 4*t^2
                
                xfunction = np.vectorize(xfunc)
                yfunction = np.vectorize(yfunc)
                zfunction = np.vectorize(zfunc)
                
                
                x = xfunction(t)
                y = yfunction(t)
                z = zfunction(t)
                
                ax.plot3D(x, y, z)
                
                ax.scatter(xfunc(hangtime), yfunc(hangtime), zfunc(hangtime))
                #ax.set_title('3D Parametric Plot')
                
                # Set axes label
                #ax.set_xlabel('x', labelpad=20)
                #ax.set_ylabel('y', labelpad=20)
                #ax.set_zlabel('z', labelpad=20)
                
                #ax.view_init(0, 90)
                '''
                
            axes = plt.gca()
        
            axes.xaxis.label.set_size(20)
            axes.yaxis.label.set_size(1)
            
            
            plt.axis('off')
            
            
            #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
            
            pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
            ax.add_patch(pitching_mound)
            art3d.pathpatch_2d_to_3d(pitching_mound)
            
            pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
            ax.add_patch(pitchers_rubber)
            art3d.pathpatch_2d_to_3d(pitchers_rubber)
            
            polygon = RegularPolygon((0, 0), numVertices = 5, radius = 1, orientation = 1.57)
            ax.add_patch(polygon)
            art3d.pathpatch_2d_to_3d(polygon)
            
            '''
            strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
            ax.add_patch(strikezone)
            art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
            '''
    
            thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
            ax.add_patch(thirdbase)
            art3d.pathpatch_2d_to_3d(thirdbase)
            
            firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = False, color = 'b')
            ax.add_patch(firstbase)
            art3d.pathpatch_2d_to_3d(firstbase)
            
            secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = False, color = 'b')
            ax.add_patch(secondbase)
            art3d.pathpatch_2d_to_3d(secondbase)
    
            """                                                                                                                                                    
            Scaling is done from here...                                                                                                                           
            """
            x_scale=1
            y_scale=1
            z_scale=0.5
            
            scale=np.diag([x_scale, y_scale, z_scale, 1.0])
            scale=scale*(1.0/scale.max())
            scale[3,3]=1.0
            
            def short_proj():
              return np.dot(Axes3D.get_proj(ax), scale)
            
            ax.get_proj=short_proj
            
            plt.show()
    '''        
    def plot(self):
        
        #input desired pitcher here. Potentially have a function that takes in pitcher's name and outputs that pitcher val
        pitchno = self.pitchnumberedit.text()
        
        pitchtraj_x0 = df['PitchTrajectoryXc0'][int(pitchno)-1]
        pitchtraj_x1 = df['PitchTrajectoryXc1'][int(pitchno)-1]
        pitchtraj_x2 = df['PitchTrajectoryXc2'][int(pitchno)-1]
        pitchtraj_y0 = df['PitchTrajectoryYc0'][int(pitchno)-1]
        pitchtraj_y1 = df['PitchTrajectoryYc1'][int(pitchno)-1]
        pitchtraj_y2 = df['PitchTrajectoryYc2'][int(pitchno)-1]
        pitchtraj_z0 = df['PitchTrajectoryZc0'][int(pitchno)-1]
        pitchtraj_z1 = df['PitchTrajectoryZc1'][int(pitchno)-1]
        pitchtraj_z2 = df['PitchTrajectoryZc2'][int(pitchno)-1]
        zonetime = df['ZoneTime'][int(pitchno)-1]
        
        
        fig = plt.figure(figsize = (10,10))
        ax = plt.axes(projection='3d')
        ax.grid()
        t = np.arange(0, zonetime, 0.001)
        
        x0 = pitchtraj_x0
        x1 = pitchtraj_x1
        x2 = pitchtraj_x2
        
        y0 = pitchtraj_z0
        y1 = pitchtraj_z1
        y2 = pitchtraj_z2
        
        z0 = pitchtraj_y0
        z1 = pitchtraj_y1
        z2 = pitchtraj_y2
        
        xfunc = lambda t: x0 + x1 * t + x2 * t**2
        yfunc = lambda t: -y0 - y1 * t - y2 * t**2
        zfunc = lambda t: z0 + z1 * t + z2 * t**2
        #x = 55.24204 - 128.23749*t + 14.74645*t^2
        #y = 6.07255 - 2.40942*t - 10.1644*t^2
        #z = 2 - 3*t + 4*t^2
        
        xfunction = np.vectorize(xfunc)
        yfunction = np.vectorize(yfunc)
        zfunction = np.vectorize(zfunc)
        
        ax.set_xlim(-10, 90)
        ax.set_ylim(-25, 25)
        ax.set_zlim(-25, 25)
        
        x = xfunction(t)
        y = yfunction(t)
        z = zfunction(t)
        
        ax.plot3D(x, y, z)
        #ax.set_title('3D Parametric Plot')
        
        # Set axes label
        ax.set_xlabel('x', labelpad=20)
        ax.set_ylabel('y', labelpad=20)
        ax.set_zlabel('z', labelpad=20)
        
        ax.view_init(0, 90)
        
        
        axes = plt.gca()
        
        axes.xaxis.label.set_size(20)
        axes.yaxis.label.set_size(1)
        
        
        plt.axis('off')
        
        ax.scatter(xfunc(zonetime), yfunc(zonetime), zfunc(zonetime))
        #ax.scatter(xfunc(0), yfunc(0), zfunc(0))
        
        pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
        ax.add_patch(pitching_mound)
        art3d.pathpatch_2d_to_3d(pitching_mound)
        
        pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = False)
        ax.add_patch(pitchers_rubber)
        art3d.pathpatch_2d_to_3d(pitchers_rubber)
        
        polygon = RegularPolygon((0, 0), numVertices = 5, radius = 1, orientation = 1.57)
        ax.add_patch(polygon)
        art3d.pathpatch_2d_to_3d(polygon)


        """                                                                                                                                                    
        Scaling is done from here...                                                                                                                           
        """
        x_scale=1
        y_scale=0.5
        z_scale=0.5
        
        scale=np.diag([x_scale, y_scale, z_scale, 1.0])
        scale=scale*(1.0/scale.max())
        scale[3,3]=1.0
        
        def short_proj():
          return np.dot(Axes3D.get_proj(ax), scale)
        
        ax.get_proj=short_proj
        
        
        self.canvas.draw()
        
        
        #plt.show()
    '''
        
        
    ''' plot some random stuff '''
    '''
    # random data
    data = [random.random() for i in range(10)]

    # create an axis
    ax = self.figure.add_subplot(111)

    # discards the old graph
    ax.clear()

    # plot data
    ax.plot(data, '*-')

    # refresh canvas
    self.canvas.draw()
    '''
        
class toomanyinputswindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        
        # a figure instance to plot on
        #self.figure = Figure()
        
        self.setGeometry(100, 100, 480, 320)
        
        layout = QVBoxLayout()
        self.label = QLabel("Please do not enter data into both text boxes. Only enter a pitch number(s) or a batter's name.")
        layout.addWidget(self.label)
        self.setLayout(layout)

class notenoughinputswindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        
        # a figure instance to plot on
        #self.figure = Figure()
        
        self.setGeometry(100, 100, 480, 320)
        
        layout = QVBoxLayout()
        self.label = QLabel("Please enter data to exactly one text box. Only enter a pitch number(s) or a batter's name.")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
class isnanwindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        
        # a figure instance to plot on
        #self.figure = Figure()
        
        self.setGeometry(100, 100, 480, 320)
        
        layout = QVBoxLayout()
        self.label = QLabel("A pitch does not have a bat. Only enter a pitches where the batter hits the ball.")
        layout.addWidget(self.label)
        self.setLayout(layout)        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())








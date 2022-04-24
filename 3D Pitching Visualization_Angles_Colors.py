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

import matplotlib as mpl
mpl.use('QT5Agg')

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import RegularPolygon
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import pandas as pd


#new stuff below this line

#mpl.use('TKAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#change csv inputs here
df = pd.read_csv("02_02_21_Scrimmage.csv")


# All units are in feet




class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("3D Baseball Pitch Visualization")
        
        # a figure instance to plot on
        #self.figure = Figure()
        
        self.setGeometry(600, 250, 300, 480)

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        #self.canvas = FigureCanvas(self.figure)
        
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        self.colorlabel = QLabel("Color Codes:\n Fastball = Red \n Curveball = Blue \n ChangeUp = Green")
        self.colorlabel.setWordWrap(True)

        self.pitchnumberlabel = QLabel("Pitch Number(s)")
        self.pitchnumberedit = QLineEdit(self)
        #self.pitchnumberedit.setPlaceholderText("None")

        
        self.batternamelabel = QLabel("Batter Name")
        self.batternameedit = QLineEdit(self)
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
        vbox.addWidget(self.colorlabel)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.pitchnumberlabel)
        hbox1.addWidget(self.pitchnumberedit)
        vbox.addLayout(hbox1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.batternamelabel)
        hbox2.addWidget(self.batternameedit)
        vbox.addLayout(hbox2)
        
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
            if self.batternameedit.text():
                self.w = toomanyinputswindow()
                self.w.show()
            else:
                pitchnumbers = self.pitchnumberedit.text()
                pitchnumberslist = pitchnumbers.split(",")
                
                fig = plt.figure(figsize = (10,10))
                ax = plt.axes(projection='3d')
                ax.grid()
                
                # default ranges
                '''
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                '''
                
                # top right view 1 - good
                # zoom in more
                '''
                ax.view_init(elev = 5., azim = -172)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.5
                '''
                
                # top right view 2
                '''
                ax.view_init(elev = 10., azim = -169)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.8
                '''
                
                # umpire view - good
                #'''
                ax.view_init(elev = 3., azim = -180)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 0.7
                #'''
                
                # top down view
                '''
                ax.view_init(elev = 90., azim = 180)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 5.5
                '''
                
                # right side view
                '''
                ax.view_init(elev = 0., azim = -90)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 4.2
                '''           
                
                # LLH umpire view #1
                '''
                ax.view_init(elev = 3.3, azim = -179)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 0.7
                '''

                # right side batter view #2 - Lok
                '''
                ax.view_init(elev = 2.8, azim = -178.7)
                ax.set_xlim(0, 100)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 0.9
                '''
                
                # LLH batter view #3 - close up - good
                '''
                ax.view_init(elev = 2, azim = -178.9)
                ax.set_xlim(40, 140)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.5
                '''

                # RRH batter view - close up - good
                '''
                ax.view_init(elev = 2, azim = 1.1)
                ax.set_xlim(40, 140)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.5
                '''                


                
                for pitchno in pitchnumberslist:
                    pitchno = pitchno.strip()
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
                    pitchtype = df['TaggedPitchType'][int(pitchno)-1]
                    pitchcall = df['PitchCall'][int(pitchno)-1]
                                        
                    if (pitchtype == "Curveball"):
                        col = "blue"
                    elif (pitchtype == "Fastball"):
                        col = "red"
                    elif (pitchtype == "ChangeUp"):
                        col = "green"
                        
                    
                      
                    if (pitchcall == "BallCalled"):
                        markcol = "blue"
                    elif (pitchcall == "InPlay"):
                        markcol = "green"
                    elif (pitchcall == "StrikeSwinging"):
                        markcol = "red"
                    elif (pitchcall == "FoulBall"):
                        markcol = "orange"
                    
                    
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
                    
                    
                    ax.plot3D(x, y, z, color = col)
                    
                    #color = color of marker
                    #marker = shape of marker
                    #s = size of marker in points^2
                    ax.scatter(xfunc(zonetime), yfunc(zonetime), zfunc(zonetime), color = markcol, s = 122.5, marker = "^")
                    #ax.set_title('3D Parametric Plot')
                    
                    #strikezone_circle = Circle((yfunc(zonetime), zfunc(zonetime)), 0.11975, fill = True, color = markcol)
                    #ax.add_patch(strikezone_circle)
                    #art3d.pathpatch_2d_to_3d(strikezone_circle, zdir = 'x', z = 1.1)                    
                    
                    # Set axes label
                    #ax.set_xlabel('x', labelpad=20)
                    #ax.set_ylabel('y', labelpad=20)
                    #ax.set_zlabel('z', labelpad=20)
                    
                    #ax.view_init(-180, 0)
                    
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
                
                # y = 1.5 to 3.6 feet - originally was 2.3333 feet instead of 2.1 feet
                # x = ???
                strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.1, fill = False, color = 'b')
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
                '''
        
        
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
                
                plt.show()
                

                #self.canvas.draw()
            
        else:
            if self.batternameedit.text():
                battername = self.batternameedit.text()
                battername = battername.strip()
                pitchnumberslist = df.index[df['Batter'] == battername].tolist()
                
                fig = plt.figure(figsize = (10,10))
                ax = plt.axes(projection='3d')
                ax.grid()
                
                # default ranges
                '''
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                '''
                
                # top right view 1 - good
                '''
                ax.view_init(elev = 5., azim = -172)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.5
                '''
                
                # top right view 2
                '''
                ax.view_init(elev = 10., azim = -169)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.8
                '''
                
                # batter view - good
                #'''
                ax.view_init(elev = 3., azim = -180)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 0.8
                #'''
                
                # top down view
                '''
                ax.view_init(elev = 90., azim = 180)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 5.5
                '''
                
                # right side view
                '''
                ax.view_init(elev = 0., azim = -90)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 4.2
                '''           
                
                # right side batter view #1
                '''
                ax.view_init(elev = 3.3, azim = -179)
                ax.set_xlim(-20, 80)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 0.7
                '''

                # right side batter view #2 - Lok
                '''
                ax.view_init(elev = 2.8, azim = -178.7)
                ax.set_xlim(0, 100)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 0.9
                '''
                
                # right side batter view #3 - close up
                '''
                ax.view_init(elev = 2, azim = -178.9)
                ax.set_xlim(40, 140)
                ax.set_ylim(-25, 25)
                ax.set_zlim(-25, 25)
                
                ax.dist = 1.1
                '''

                
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
                    pitchtype = df['TaggedPitchType'][int(pitchno)]
                    pitchcall = df['PitchCall'][int(pitchno)]
                                        
                    if (pitchtype == "Curveball"):
                        col = "blue"
                    elif (pitchtype == "Fastball"):
                        col = "red"
                    elif (pitchtype == "ChangeUp"):
                        col = "green"
                    
                    if (pitchcall == "BallCalled"):
                        markcol = "blue"
                    elif (pitchcall == "InPlay"):
                        markcol = "green"
                    elif (pitchcall == "StrikeSwinging"):
                        markcol = "red"
                    elif (pitchcall == "FoulBall"):
                        markcol = "orange"
                    
                                        
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
                    
                    ax.plot3D(x, y, z, color = col)
                    
                    #ax.scatter(xfunc(zonetime), yfunc(zonetime), zfunc(zonetime), color = col)
                    #ax.set_title('3D Parametric Plot')
                    
                    strikezone_circle = Circle((yfunc(zonetime), zfunc(zonetime)), 0.11975, fill = True, color = markcol)
                    ax.add_patch(strikezone_circle)
                    art3d.pathpatch_2d_to_3d(strikezone_circle, zdir = 'x', z = 1.1)                    
                    

                    
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
                
                polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57)
                ax.add_patch(polygon)
                art3d.pathpatch_2d_to_3d(polygon)
        
                strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.1, fill = False, color = 'b')
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
                '''
        
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
                
                plt.show()
                
            else:
                self.w = notenoughinputswindow()
                self.w.show()
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
        
        ax.set_xlim(-20, 80)
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
        y_scale=0.5
        z_scale=0.5
        
        scale=np.diag([x_scale, y_scale, z_scale, 1.0])
        scale=scale*(1.0/scale.max())
        scale[3,3]=1.0
        
        def short_proj():
          return np.dot(Axes3D.get_proj(ax), scale)
        
        ax.get_proj=short_proj
        
        
        self.canvas.draw()
    '''
        
        
        #plt.show()
        
        
        
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


if __name__ == '__main__':
    '''
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
    '''
    
    QApplication.setStyle('Fusion')
    app = QApplication(sys.argv)
    display = MainWindow()
    display.show()
    sys.exit(app.exec_())








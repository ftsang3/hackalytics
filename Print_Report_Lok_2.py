# -*- coding: utf-8 -*-
"""
Created on Sun May 22 00:54:09 2022

@author: Frank
"""


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
from matplotlib.patches import Circle, FancyArrow, Wedge, ConnectionPatch
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

from collections import OrderedDict

import fpdf
from fpdf import FPDF
import dataframe_image as dfi

import math
import os.path
from PIL import Image

# assumes that for each plate appearance, there is only 1 pitcher and 1 batter (they do not change) --> used to determine pitcher name, pitcher side, batter name, etc.
# speed = RelSpeed





#change csv inputs here
df = pd.read_csv("20220422-GeorgiaTech-1_unverified.csv")
df.set_index('PitchNo', inplace = True)
#away team first, home team second
teamNames = []
teamNames.append(df["AwayTeam"][1])
teamNames.append(df["HomeTeam"][1])
#teamNames = ['Duke','GT']   #in Order of batting,

pitchdict = OrderedDict()

for pitchnumber in df.index:
    if (df["Inning"][pitchnumber], df["Top/Bottom"][pitchnumber], df["PAofInning"][pitchnumber]) in pitchdict:
        pitchdict[df["Inning"][pitchnumber], df["Top/Bottom"][pitchnumber], df["PAofInning"][pitchnumber]].append(pitchnumber)
    else:
        pitchdict[df["Inning"][pitchnumber], df["Top/Bottom"][pitchnumber], df["PAofInning"][pitchnumber]] = [pitchnumber]
    
pitchdictkeys = list(pitchdict.keys())


#print(pitchdictkeys)
#for key, value in pitchdict.items():
    #print(key, value)

for uniquepa in pitchdictkeys:
    pitchnumberslist = pitchdict[uniquepa]

    pitchername = df["Pitcher"][pitchnumberslist[0]]
    pitcherside = df["PitcherThrows"][pitchnumberslist[0]]
    battername = df["Batter"][pitchnumberslist[0]]
    batterside = df["BatterSide"][pitchnumberslist[0]]

    fig = plt.figure(figsize = (10,10))
    ax = plt.axes(projection='3d')
    ax.grid()
    

    if batterside == "Left":
        # LLH batter view #3 - close up - good
        ax.view_init(elev = 2, azim = -178.9)
        ax.set_xlim(40, 140)
        ax.set_ylim(-25, 25)
        ax.set_zlim(-25, 25)
        ax.dist = 1.45
        marksize = 500
        labelsize = 70
    
    if batterside == "Right":
        # RRH batter view - close up - good
        ax.view_init(elev = 2, azim = 178.9)
        ax.set_xlim(40, 140)
        ax.set_ylim(-25, 25)
        ax.set_zlim(-25, 25)
        ax.dist = 1.45
        marksize = 500
        labelsize = 70
    
    
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
        playresult = df['PlayResult'][int(pitchno)]
        pitchofpa = df['PitchofPA'][int(pitchno)]
        
        # color of the pitch (path of the ball) = pitchtype                    
        if (pitchtype == "Curveball"):
            col = "blue"
        elif (pitchtype == "Fastball"):
            col = "red"
        elif (pitchtype == "ChangeUp"):
            col = "green"
        elif (pitchtype == "Slider"):
            col = "purple"
        elif (pitchtype == "Cutter"):
            col = "orange" 
        else:
            col = "black"
        
        # color of the marker = pitchcall
        if (pitchcall == "BallCalled"):
            markcol = "blue"
        elif (pitchcall == "InPlay"):
            markcol = "green"
        elif (pitchcall == "StrikeSwinging"):
            markcol = "red"
        elif (pitchcall == "FoulBall"):
            markcol = "orange"
        elif (pitchcall == "StrikeCalled"):
            markcol = "purple"
        else:
            markcol = "black"
            
        # shape of the marker = playresult
        if (playresult == "Single"):
            markshape = ">"
        elif (playresult == "Double"):
            markshape = "^"
        elif (playresult == "Triple"):
            markshape = "<"
        elif (playresult == "HomeRun"):
            markshape = "v"
        elif (playresult == "Undefined"):
            markshape = "o"
        else:
            markshape = "s"
        
        
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
        #s = size of marker in points^
        ax.scatter(xfunc(zonetime), yfunc(zonetime), zfunc(zonetime), color = markcol, s = marksize, marker = markshape)
        ax.scatter(xfunc(zonetime), yfunc(zonetime), zfunc(zonetime), color = "yellow", s = labelsize, marker = "$"+str(pitchofpa)+"$")
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
    
    # #plt.show()
    plotname = str(uniquepa)[1:-1] + " Pitch" + ".png"
    plt.savefig(plotname, format = "png")
    
    plt.close('all')
    
    if (os.path.exists(plotname)):
        im = Image.open(plotname)
        cropped = im.crop((75, 230, 655, 630))
        cropped.save(plotname, format = "png")

    
    #self.canvas.draw()
    
for uniquepa in pitchdictkeys:
    pitchnumberslist = pitchdict[uniquepa]
    
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
    '''
    ax.view_init(elev = 15., azim = -157)
    ax.set_xlim(-10, 90)
    ax.set_ylim(-50, 50)
    ax.set_zlim(-25, 25)
    
    ax.dist = 9
    '''

    # batter view
    #'''
    ax.view_init(elev = 20., azim = -180)
    ax.set_xlim(-10, 90)
    ax.set_ylim(-50, 50)
    ax.set_zlim(-25, 25)
    
    ax.dist = 33
    #'''

    # top right view
    '''
    ax.view_init(elev = 15., azim = -157)
    ax.set_xlim(-10, 90)
    ax.set_ylim(-50, 50)
    ax.set_zlim(-25, 25)
    
    ax.dist = 9
    '''                            
    
    
    for pitchno in pitchnumberslist:
        if np.isnan(df['HangTime'][int(pitchno)]):
            continue
        
        pitchtraj_x0 = df['HitTrajectoryXc0'][int(pitchno)]
        pitchtraj_x1 = df['HitTrajectoryXc1'][int(pitchno)]
        pitchtraj_x2 = df['HitTrajectoryXc2'][int(pitchno)]
        pitchtraj_x3 = df['HitTrajectoryXc3'][int(pitchno)]
        pitchtraj_x4 = df['HitTrajectoryXc4'][int(pitchno)]
        pitchtraj_x5 = df['HitTrajectoryXc5'][int(pitchno)]
        pitchtraj_x6 = df['HitTrajectoryXc6'][int(pitchno)]
        pitchtraj_x7 = df['HitTrajectoryXc7'][int(pitchno)]
        pitchtraj_x8 = df['HitTrajectoryXc8'][int(pitchno)]
        
        pitchtraj_y0 = df['HitTrajectoryYc0'][int(pitchno)]
        pitchtraj_y1 = df['HitTrajectoryYc1'][int(pitchno)]
        pitchtraj_y2 = df['HitTrajectoryYc2'][int(pitchno)]
        pitchtraj_y3 = df['HitTrajectoryYc3'][int(pitchno)]
        pitchtraj_y4 = df['HitTrajectoryYc4'][int(pitchno)]
        pitchtraj_y5 = df['HitTrajectoryYc5'][int(pitchno)]
        pitchtraj_y6 = df['HitTrajectoryYc6'][int(pitchno)]
        pitchtraj_y7 = df['HitTrajectoryYc7'][int(pitchno)]
        pitchtraj_y8 = df['HitTrajectoryYc8'][int(pitchno)]
        
        pitchtraj_z0 = df['HitTrajectoryZc0'][int(pitchno)]
        pitchtraj_z1 = df['HitTrajectoryZc1'][int(pitchno)]
        pitchtraj_z2 = df['HitTrajectoryZc2'][int(pitchno)]
        pitchtraj_z3 = df['HitTrajectoryZc3'][int(pitchno)]
        pitchtraj_z4 = df['HitTrajectoryZc4'][int(pitchno)]
        pitchtraj_z5 = df['HitTrajectoryZc5'][int(pitchno)]
        pitchtraj_z6 = df['HitTrajectoryZc6'][int(pitchno)]
        pitchtraj_z7 = df['HitTrajectoryZc7'][int(pitchno)]
        pitchtraj_z8 = df['HitTrajectoryZc8'][int(pitchno)]
        
        hangtime = df['HangTime'][int(pitchno)]
                            
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

            leftfieldline = FancyArrow(.45, 0,220,232.63, width = 0.3, length_includes_head=False, head_width=None, head_length=None, shape='full',color = 'b')
            ax.add_patch(leftfieldline)
            art3d.pathpatch_2d_to_3d(leftfieldline)

            rightfieldline = FancyArrow(.45, 0, 230, -236.17, width=0.3, length_includes_head=False,
                                        head_width=None, head_length=None, shape='full', color='b')
            ax.add_patch(rightfieldline)
            art3d.pathpatch_2d_to_3d(rightfieldline)

            Bwedge = Wedge((.45, 0),380,-45.75,46.5,225, edgecolor='forestgreen',fc = 'none')
            ax.add_patch(Bwedge)
            art3d.pathpatch_2d_to_3d(Bwedge)

            Bswedge = Wedge((.45, 0), 155, -45.75, 46.5, edgecolor='wheat',fc = 'none')
            ax.add_patch(Bswedge)
            art3d.pathpatch_2d_to_3d(Bswedge)
            
            pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
            ax.add_patch(pitching_mound)
            art3d.pathpatch_2d_to_3d(pitching_mound)
            
            pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = True)
            ax.add_patch(pitchers_rubber)
            art3d.pathpatch_2d_to_3d(pitchers_rubber)
            
            polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
            ax.add_patch(polygon)
            art3d.pathpatch_2d_to_3d(polygon)

            #sq = RegularPolygon((64, .45), numVertices = 4, radius = 64, orientation = 0, fill = False , color = 'g')
            #ax.add_patch(sq)
            #art3d.pathpatch_2d_to_3d(sq)


            '''
            strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
            ax.add_patch(strikezone)
            art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
            '''
            
            #outerarc = Arc((60.5, -1), width = 95, height = 95, angle = 0.0, theta1 = 0, theta2 = 90)
            #ax.add_patch(outerarc)
            #art3d.pathpatch_2d_to_3d(outerarc)
            
            thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(thirdbase)
            art3d.pathpatch_2d_to_3d(thirdbase)
            
            firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(firstbase)
            art3d.pathpatch_2d_to_3d(firstbase)
            
            secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(secondbase)
            art3d.pathpatch_2d_to_3d(secondbase)

            c1 = ConnectionPatch((63, 63.3),(126, 0.8),"data","data")
            ax.add_patch(c1)
            art3d.pathpatch_2d_to_3d(c1)

            c2 = ConnectionPatch((63, -62.2), (126, 0.8),"data","data")
            ax.add_patch(c2)
            art3d.pathpatch_2d_to_3d(c2)


    
    
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
            
            # plt.show()
            plotname = str(uniquepa)[1:-1] + " Bat" + ".png"
            plt.savefig(plotname, format = "png")

            plt.close('all')
            #self.canvas.draw()
            
            if (os.path.exists(plotname)):
                im = Image.open(plotname)
                cropped = im.crop((100, 200, 650, 400))
                cropped.save(plotname, format = "png")
    

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
            leftfieldline = FancyArrow(.45, 0,220,232.63, width = 0.3, length_includes_head=False, head_width=None, head_length=None, shape='full',color = 'b')
            ax.add_patch(leftfieldline)
            art3d.pathpatch_2d_to_3d(leftfieldline)

            rightfieldline = FancyArrow(.45, 0, 230, -236.17, width=0.3, length_includes_head=False,
                                        head_width=None, head_length=None, shape='full', color='b')
            ax.add_patch(rightfieldline)
            art3d.pathpatch_2d_to_3d(rightfieldline)

            Bwedge = Wedge((.45, 0),380,-45.75,46.5,225, edgecolor='forestgreen',fc = 'none')
            ax.add_patch(Bwedge)
            art3d.pathpatch_2d_to_3d(Bwedge)

            Bswedge = Wedge((.45, 0), 155, -45.75, 46.5, edgecolor='wheat',fc = 'none')
            ax.add_patch(Bswedge)
            art3d.pathpatch_2d_to_3d(Bswedge)
            
            pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
            ax.add_patch(pitching_mound)
            art3d.pathpatch_2d_to_3d(pitching_mound)
            
            pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = True)
            ax.add_patch(pitchers_rubber)
            art3d.pathpatch_2d_to_3d(pitchers_rubber)
            
            polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
            ax.add_patch(polygon)
            art3d.pathpatch_2d_to_3d(polygon)

            #sq = RegularPolygon((64, .45), numVertices = 4, radius = 64, orientation = 0, fill = False , color = 'g')
            #ax.add_patch(sq)
            #art3d.pathpatch_2d_to_3d(sq)


            '''
            strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
            ax.add_patch(strikezone)
            art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
            '''
            
            #outerarc = Arc((60.5, -1), width = 95, height = 95, angle = 0.0, theta1 = 0, theta2 = 90)
            #ax.add_patch(outerarc)
            #art3d.pathpatch_2d_to_3d(outerarc)
            
            thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(thirdbase)
            art3d.pathpatch_2d_to_3d(thirdbase)
            
            firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(firstbase)
            art3d.pathpatch_2d_to_3d(firstbase)
            
            secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(secondbase)
            art3d.pathpatch_2d_to_3d(secondbase)

            c1 = ConnectionPatch((63, 63.3),(126, 0.8),"data","data")
            ax.add_patch(c1)
            art3d.pathpatch_2d_to_3d(c1)

            c2 = ConnectionPatch((63, -62.2), (126, 0.8),"data","data")
            ax.add_patch(c2)
            art3d.pathpatch_2d_to_3d(c2)

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
            
            # plt.show()
            plotname = str(uniquepa)[1:-1] + " Bat" + ".png"
            plt.savefig(plotname, format = "png")

            plt.close('all')
            #self.canvas.draw()
            
            if (os.path.exists(plotname)):
                im = Image.open(plotname)
                cropped = im.crop((100, 200, 650, 400))
                cropped.save(plotname, format = "png")
        
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
            leftfieldline = FancyArrow(.45, 0,220,232.63, width = 0.3, length_includes_head=False, head_width=None, head_length=None, shape='full',color = 'b')
            ax.add_patch(leftfieldline)
            art3d.pathpatch_2d_to_3d(leftfieldline)

            rightfieldline = FancyArrow(.45, 0, 230, -236.17, width=0.3, length_includes_head=False,
                                        head_width=None, head_length=None, shape='full', color='b')
            ax.add_patch(rightfieldline)
            art3d.pathpatch_2d_to_3d(rightfieldline)

            Bwedge = Wedge((.45, 0),380,-45.75,46.5,225, edgecolor='forestgreen',fc = 'none')
            ax.add_patch(Bwedge)
            art3d.pathpatch_2d_to_3d(Bwedge)

            Bswedge = Wedge((.45, 0), 155, -45.75, 46.5, edgecolor='wheat',fc = 'none')
            ax.add_patch(Bswedge)
            art3d.pathpatch_2d_to_3d(Bswedge)
            
            pitching_mound = Circle((60.5, 0), 9, fill = False, color = 'b')
            ax.add_patch(pitching_mound)
            art3d.pathpatch_2d_to_3d(pitching_mound)
            
            pitchers_rubber = Rectangle((60.5, -1), 2, 0.5, 90, color = 'b', fill = True)
            ax.add_patch(pitchers_rubber)
            art3d.pathpatch_2d_to_3d(pitchers_rubber)
            
            polygon = RegularPolygon((.45, 0), numVertices = 5, radius = 1, orientation = 1.57, color = 'b')
            ax.add_patch(polygon)
            art3d.pathpatch_2d_to_3d(polygon)

            #sq = RegularPolygon((64, .45), numVertices = 4, radius = 64, orientation = 0, fill = False , color = 'g')
            #ax.add_patch(sq)
            #art3d.pathpatch_2d_to_3d(sq)


            '''
            strikezone = Rectangle((-0.70833, 1.5), 1.41666, 2.33333, fill = False, color = 'b')
            ax.add_patch(strikezone)
            art3d.pathpatch_2d_to_3d(strikezone, zdir = 'x', z = 1.1)
            '''
            
            #outerarc = Arc((60.5, -1), width = 95, height = 95, angle = 0.0, theta1 = 0, theta2 = 90)
            #ax.add_patch(outerarc)
            #art3d.pathpatch_2d_to_3d(outerarc)
            
            thirdbase = Rectangle((63, 63.5), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(thirdbase)
            art3d.pathpatch_2d_to_3d(thirdbase)
            
            firstbase = Rectangle((63, -63.5), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(firstbase)
            art3d.pathpatch_2d_to_3d(firstbase)
            
            secondbase = Rectangle((127, 0), 1.25, 1.25, angle = 45, fill = True, color = 'b')
            ax.add_patch(secondbase)
            art3d.pathpatch_2d_to_3d(secondbase)

            c1 = ConnectionPatch((63, 63.3),(126, 0.8),"data","data")
            ax.add_patch(c1)
            art3d.pathpatch_2d_to_3d(c1)

            c2 = ConnectionPatch((63, -62.2), (126, 0.8),"data","data")
            ax.add_patch(c2)
            art3d.pathpatch_2d_to_3d(c2)

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
            
            # plt.show()
            plotname = str(uniquepa)[1:-1] + " Bat" + ".png"
            plt.savefig(plotname, format = "png")

            plt.close('all')
            #self.canvas.draw()
            
            if (os.path.exists(plotname)):
                im = Image.open(plotname)
                cropped = im.crop((100, 200, 650, 400))
                cropped.save(plotname, format = "png")
        
        

listpitchbat = []

listpitches = []
    
for uniquepa in pitchdictkeys:
    pitchnumberslist = pitchdict[uniquepa]

    pitchername = df["Pitcher"][pitchnumberslist[0]]
    pitcherside = df["PitcherThrows"][pitchnumberslist[0]]
    if pitcherside == "Right":
        pitcherside = "RHP"
    elif pitcherside == "Left":
        pitcherside = "LHP"
    battername = df["Batter"][pitchnumberslist[0]]
    batterside = df["BatterSide"][pitchnumberslist[0]]
    if batterside == "Right":
        batterside = "RHH"
    elif batterside == "Left":
        batterside = "LHH"
    
    # listpitchbat.append("Pitching: " + str(pitchername) + " (" + pitcherside + ") \n" + "Bat: " + str(battername) + " (" + batterside + ")")
    
    pitchnumberslist = pitchdict[uniquepa]
    
    strpitches = ""
    i = 1
    data1 = [] #holds list of dicts which have info for each dataframe row
    
    for pitchno in pitchnumberslist:
        pitchtype = df['TaggedPitchType'][int(pitchno)]
        pitchcall = df['PitchCall'][int(pitchno)]
        playresult = df['PlayResult'][int(pitchno)]
        pitchofpa = df['PitchofPA'][int(pitchno)] 
        speed = df['RelSpeed'][int(pitchno)]
        balls = df['Balls'][int(pitchno)]
        strikes = df['Strikes'][int(pitchno)]
        korbb = df['KorBB'][int(pitchno)]
        
        if playresult == "FieldersChoice":
            playresult = "FC"

        if pitchcall == "InPlay":
            pitchcall = "InPlay " + str(playresult)
        
        strpitches += str(pitchcall) + "    " + str(balls) + "-" + str(strikes) + "\n" + str(speed)[:4] + " mph " + str(pitchtype) + "\n"
    
        #a = {"#":i, "PitchCall":str(pitchcall), "B-S":(str(balls)+ "-" + str(strikes)), "Speed":(str(speed)[:4]+ " mph "), "PitchType":str(pitchtype)}
        a = {"PitchCall":str(pitchcall), "B-S":(str(balls)+ "-" + str(strikes)), "Speed":(str(speed)[:4]+ " mph "), "PitchType":str(pitchtype)}
        data1.append(a)
        i += 1
        pitchframe = pd.DataFrame(data1, columns = [*data1[0]])
        
        if pitchno == pitchnumberslist[-1]:
            if playresult != "Undefined":
                listpitchbat.append("Pitch: " + str(pitchername) + " (" + pitcherside + ") \n" + "Bat: " + str(battername) + " (" + batterside + ")" + " - " + str(playresult))
            elif korbb != "Undefined":
                listpitchbat.append("Pitch: " + str(pitchername) + " (" + pitcherside + ") \n" + "Bat: " + str(battername) + " (" + batterside + ")" + " - " + str(korbb))
            else:
                listpitchbat.append("Pitch: " + str(pitchername) + " (" + pitcherside + ") \n" + "Bat: " + str(battername) + " (" + batterside + ")" + " - " + str(pitchcall))

    pitchframe.index += 1
    listpitches.append(pitchframe)
    data1 = []

innum = pitchdictkeys[len(pitchdictkeys)-1][0]
numpages = math.ceil(len(pitchdictkeys) / 2)
stopindexes = [i for i in range(0,(numpages*2)-1,2)]

scorelist = []
innings = [i for i in range(1,innum+1)]
teams = ['Top','Bottom']


for page in stopindexes:
    score = pd.DataFrame(columns = innings, index = teamNames, dtype=pd.Int64Dtype())
    score = score.fillna(0)
    for plate in pitchdictkeys:
        if plate == pitchdictkeys[page]:
            score['R'] = score.sum(axis=1)
            score['R'] = score['R'].astype('int')
            for i in range(plate[0]+1, innum+1):
                score[i] = score[i].astype(str)
                score[i] = score[i].replace('0', '')
            # score = score.reset_index(drop=True)
            # score['Team'] = teamNames
            # score = score.set_index(['Team'])
            # score = score.rename_axis('Team').rename_axis('Team', axis='columns')
            # score = score.rename_axis('')
            subsets = pd.IndexSlice[teamNames[teams.index(plate[1])], plate[0]]
            score = score.style.applymap(lambda x: "background-color: green", subset=subsets)
            scorelist.append(score)
            break
        pitchnumberslist = pitchdict[plate]
        plateSum = df.loc[pitchnumberslist, ['RunsScored']].sum()
        score.at[teamNames[teams.index(plate[1])], plate[0]] += plateSum

#scorelist contains a dataframe that contains the scoredataframe for each page in order

intcounter = 0

for platedf in listpitches:
    filename = str(pitchdictkeys[intcounter])[1:-1] + ' Table' + '.png'
    dfi.export(platedf, filename)
    intcounter += 1

intcounter = 1

for pagedf in scorelist:
    fname2 = 'Page ' + str(intcounter) + ' Score' + '.png'
    dfi.export(pagedf, fname2)
    intcounter += 1

def create_title(title, pdf):
    
    # Add main title
    pdf.set_font('Helvetica', 'b', 20)  
    pdf.write(5, title)
    pdf.ln(10)
    
    # Add date of report
    #pdf.set_font('Helvetica', '', 14)
    #pdf.set_text_color(r=128,g=128,b=128)
    #pdf.write(4, f'{today}')
    
    # Add line break
    #pdf.ln(10)

def write_to_pdf(pdf, words):
    
    # Set text colour, font size, and font type
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Helvetica', '', 12)
    
    pdf.write(5, words)
    


class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
        
        
# Global Variables
TITLE = "Game Report"
WIDTH = 210
HEIGHT = 297

# Create PDF
pdf = FPDF(orientation = "L") # A4 (210 by 297 mm)


#str(uniquepa)[1:-1] + " Pitch" + ".png"

numpages = math.floor(len(pitchdictkeys) / 2)

intpa = 0
pagenum = 1

for i in range(numpages):
    pdf.add_page()
    create_title(TITLE, pdf)
       
    # Add some words to PDF
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Helvetica', '', 12)
    #write_to_pdf(pdf, "Report of 1st Plate Appearance")
    #pdf.ln(15)
    #print(intpa)
    # Add table
    pdf.set_xy(10, 0)
    
    filename_temp = 'Page ' + str(pagenum) + ' Score' + '.png'
    if (os.path.exists(filename_temp)):
        # print("yes")
        pdf.image(filename_temp, x = 110, y = 5, w = 70)
        
    # Add table
    pdf.set_xy(10, 30)
    pdf.multi_cell(w = 80, h = 6, txt = listpitchbat[intpa], border = 1, align = "L")
    #pdf.multi_cell(w = 50, h = 8, txt = listpitches[intpa], border = 1, align = "L")
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Table" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp,  x = 10, y = 45, w = 80)
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Pitch" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp,  x = 105, y = 25, h = 60, w = 80)
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Bat" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp, x = 200, y = 30, h = 55, w = 90)
    pdf.ln(10)
    
    intpa += 1
    
    pdf.set_xy(10, 120)
    pdf.multi_cell(w = 80, h = 6, txt = listpitchbat[intpa], border = 1, align = "L")
    #pdf.multi_cell(w = 50, h = 8, txt = listpitches[intpa], border = 1, align = "L")
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Table" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp,  x = 10, y = 135, w = 80)
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Pitch" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp,  x = 105, y = 115, h = 60, w = 80)
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Bat" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp, x = 200, y = 120, h = 55, w = 90)
    
    intpa += 1
    pagenum += 1
    
    # Add some words to PDF
    #write_to_pdf(pdf, "2. The visualisations below shows the trend of total sales for Heicoders Academy and the breakdown of revenue for year 2016:")
    
    # Add the generated visualisations to the PDF
    #pdf.image("resources/heicoders_annual_sales.png", 5, 200, WIDTH/2-10)
    #pdf.image("resources/heicoders_2016_sales_breakdown.png", WIDTH/2, 200, WIDTH/2-10)

    
if len(pitchdictkeys) % 2 == 1:
    pdf.add_page()
    create_title(TITLE, pdf)
    # Add some words to PDF
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Helvetica', '', 12)
    #write_to_pdf(pdf, "Report of 1st Plate Appearance")
    #pdf.ln(15)
    
    # Add table
    pdf.set_xy(10, 0)
    
    filename_temp = 'Page ' + str(pagenum) + ' Score' + '.png'
    if (os.path.exists(filename_temp)):
        # print("yes")
        pdf.image(filename_temp, x = 110, y = 5, w = 70)
        
    # Add table
    pdf.set_xy(10, 30)
    pdf.multi_cell(w = 80, h = 6, txt = listpitchbat[intpa], border = 1, align = "L")
    #pdf.multi_cell(w = 50, h = 8, txt = listpitches[intpa], border = 1, align = "L")
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Table" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp,  x = 10, y = 45, w = 80)
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Pitch" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp,  x = 105, y = 25, h = 60, w = 80)
    filename_temp = str(pitchdictkeys[intpa])[1:-1] + " Bat" + ".png"
    if (os.path.exists(filename_temp)):
        pdf.image(filename_temp, x = 200, y = 30, h = 55, w = 90)
    pdf.ln(10)

pdf.output("GameReport.pdf", 'F')     

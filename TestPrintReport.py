# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:40:06 2022

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


#change csv inputs here
df = pd.read_csv("20220422-GeorgiaTech-1_unverified.csv")
df.set_index('PitchNo', inplace = True)

pitchdict = OrderedDict()

for pitchnumber in df.index:
    if (df["Inning"][pitchnumber], df["Top/Bottom"][pitchnumber], df["PAofInning"][pitchnumber]) in pitchdict:
        pitchdict[df["Inning"][pitchnumber], df["Top/Bottom"][pitchnumber], df["PAofInning"][pitchnumber]].append(pitchnumber)
    else:
        pitchdict[df["Inning"][pitchnumber], df["Top/Bottom"][pitchnumber], df["PAofInning"][pitchnumber]] = [pitchnumber]
    
pitchdictkeys = list(pitchdict.keys())


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
    
    listpitchbat.append("Pitching: \n" + str(pitchername) + " (" + pitcherside + ") \n" + "AT BAT: \n" + str(battername) + " (" + batterside + ")")
    
    pitchnumberslist = pitchdict[uniquepa]
    
    strpitches = ""
    
    for pitchno in pitchnumberslist:
        pitchtype = df['TaggedPitchType'][int(pitchno)]
        pitchcall = df['PitchCall'][int(pitchno)]
        playresult = df['PlayResult'][int(pitchno)]
        pitchofpa = df['PitchofPA'][int(pitchno)] 
        speed = df['EffectiveVelo'][int(pitchno)]
        balls = df['Balls'][int(pitchno)]
        strikes = df['Strikes'][int(pitchno)]
        
        if pitchcall == "InPlay":
            pitchcall = "InPlay " + str(playresult)
        
        strpitches += str(pitchcall) + "    " + str(balls) + "-" + str(strikes) + "\n" + str(speed)[:4] + " mph " + str(pitchtype) + "\n"
    
    listpitches.append(strpitches)

    
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


'''
First Page of PDF
'''
# Add Page
pdf.add_page()

# Add title
create_title(TITLE, pdf)

# Add some words to PDF
pdf.set_text_color(r=0,g=0,b=0)
pdf.set_font('Helvetica', '', 12)
#write_to_pdf(pdf, "Report of 1st Plate Appearance")
#pdf.ln(15)

# Add table
pdf.set_xy(10, 30)
pdf.multi_cell(w = 50, h = 10, txt = listpitchbat[1], border = 1, align = "L")
pdf.set_xy(60, 30)
pdf.multi_cell(w = 50, h = 8, txt = listpitches[1], border = 1, align = "L")
pdf.image("1, 'Top', 2 Pitch.png",  x = 120, y = 0, h = 100, w = 100)
pdf.image("1, 'Top', 2 Bat.png", x = 180, y = 0, h = 150, w = 120)
pdf.ln(10)

pdf.set_xy(10, 120)
pdf.multi_cell(w = 50, h = 10, txt = listpitchbat[2], border = 1, align = "L")
pdf.set_xy(60, 120)
pdf.multi_cell(w = 50, h = 8, txt = listpitches[2], border = 1, align = "L")
pdf.image("1, 'Top', 3 Pitch.png",  x = 120, y = 90, h = 100, w = 100)
pdf.image("1, 'Top', 3 Bat.png", x = 180, y = 90, h = 150, w = 120)

# Add some words to PDF
#write_to_pdf(pdf, "2. The visualisations below shows the trend of total sales for Heicoders Academy and the breakdown of revenue for year 2016:")

# Add the generated visualisations to the PDF
#pdf.image("resources/heicoders_annual_sales.png", 5, 200, WIDTH/2-10)
#pdf.image("resources/heicoders_2016_sales_breakdown.png", WIDTH/2, 200, WIDTH/2-10)
pdf.ln(10)


'''
Second Page of PDF
'''

# Add Page
pdf.add_page()

# Add title
create_title(TITLE, pdf)


# Add some words to PDF
pdf.ln(40)
#write_to_pdf(pdf, "3. In conclusion, the year-on-year sales of Heicoders Academy continue to show a healthy upward trend. Majority of the sales could be attributed to the global sales which accounts for 58.0% of sales in 2016.")
pdf.ln(15)

# Generate the PDF
pdf.output("GameReportTest.pdf", 'F')          



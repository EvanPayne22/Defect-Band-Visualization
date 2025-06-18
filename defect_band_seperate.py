# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 00:52:18 2025

@author: epayne
"""

import matplotlib.pyplot as plt
import argparse
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator

parser = argparse.ArgumentParser(description="Arguments for charge defect ",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-hseext", nargs='?', type=bool, default = False, help="shows HSE region on PBE or alt plots")
parser.add_argument("-fileloc", nargs='?', default = "./eigenVal.txt", help="set the location of the file")
parser.add_argument("-saveloc", nargs='?', default = "./pbehseeigplot.png", help="sets the location of the file")
parser.add_argument("-linewidth", nargs='?', type=int, default = 2, help="sets line thickness")
parser.add_argument("-dotsize", nargs='?', type=int, default = 100, help="sets size of the dotd on plots")
parser.add_argument("-fontsize", nargs='?', type=int, default = 18, help="sets fontsize")
parser.add_argument("-plotwidth", nargs='?', type=int, default = 6, help="sets width of the plots (I recommend 6 per plot)")
args = parser.parse_args()
config = vars(args)

#Function to format defect names with subscript
def format_label(label):
    base, subscript = label.split('_')
    return f"{base}$_{{{subscript}}}$"

data = config["fileloc"]

f = open(data)
eigenVal = f.readlines()

numberOfDefects = 0 #The number of defects being plotted

for i in range (0, len(eigenVal)):
    if (eigenVal[i][0] == 'd'): #Countes the Number of Defects Being Plotted
        numberOfDefects += 1
    eigenVal[i] = eigenVal[i].split()
    
    
count = 0 #Counter for reading eigenVal file
plotNum = 1 #Counter to store which sub plot data is stored for

energy = [] #Energy Level of the Defect in energy Gap
occupancy = [] #Occupancy of Defect States
dotSize = config["dotsize"] #Size of the dots on the plot
fontSize = config["fontsize"] #Default value for font size
lineWidth = config["linewidth"] #Sets the thickness of the lines

plt.subplots(1,numberOfDefects, figsize=(config["plotwidth"],4)) #Sets the number of subplots

for i in range (0, len(eigenVal)):
    if(count == 0):
        band_edge = float(eigenVal[i][1])
    count = count + 1
    
    #Reads All Energies and Occupancies for Nuetral Defect
    if(eigenVal[i][0] == 'done'):
        
        #Sets read range based on input file
        if(config['hseext'] == True):
           jmin = 2
           jmax = len(energy) - 2
        else:
            jmin = 1
            jmax = len(energy) - 1
        
        i = i + 1
        defect_name = eigenVal[i - count][3] #Gets the name of the defect from file
        defect_name = format_label(defect_name) #Forats the defect name for plot
        
        plt.subplot(1, numberOfDefects, plotNum)
        plt.tick_params(labelbottom=False,bottom=False, top=False, labeltop=False, labelright=False, labelleft=True, left=True, right=False)
        
        for j in range(jmin, jmax):
            if(occupancy[j] < 0.2): #Plots the unoccupied states
                plt.axhline(energy[j], color = 'black', lw = lineWidth)
                plt.scatter([0.25, 0.75], [energy[j], energy[j]], facecolors='white', edgecolors='black', zorder = 3, s = dotSize)
            elif(occupancy[j] > 0.8): #Plots the occupied states
                plt.axhline(energy[j], color = 'black', lw = lineWidth)
                plt.scatter([0.25, 0.75], [energy[j], energy[j]], color = 'black', zorder = 3, s = dotSize)
            else: #Plots the half-occupied states and splits the levels based on ISPIN = 2 Calculation
                filledState = float(eigenVal[i - (len(energy) - j) - 1][3]) - band_edge
                emptyState = float(eigenVal[i - (len(energy) - j) - 1][4]) - band_edge
                plt.axhline(filledState, color = 'black', xmax = 0.5, lw = lineWidth)
                plt.axhline(emptyState, color = 'black', xmin = 0.5, lw = lineWidth)
                plt.scatter(0.25, filledState, color='black', zorder = 3, s = dotSize)
                plt.scatter(0.75, emptyState, facecolors='white', edgecolors='black', zorder = 3, s = dotSize)
                plt.plot([0.5,0.5], [filledState, emptyState], color = 'black', linestyle = 'dashed', lw = lineWidth)
        
        cond_band_edge = energy[len(energy) - 1] #Conduction Band Edge
        
        if(config['hseext'] == True):
            cond_band_edge_pbe = energy[len(energy) - 2] #CBM for PBE
            val_band_edge_pbe = energy[1] #VBM for PBE
            plt.fill([0,0,1,1], [0, val_band_edge_pbe, val_band_edge_pbe, 0], color = 'grey')
            plt.fill([0,0,1,1], [cond_band_edge_pbe, cond_band_edge, cond_band_edge, cond_band_edge_pbe], color = 'grey')
        
        ax = plt.gca()  # Get current subplot (Axes) instance

        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.tick_params(axis='y', labelsize=fontSize)  # Change 10 to your desired font size
        ax.yaxis.set_minor_locator(MultipleLocator(0.25))
        ax.tick_params(axis='y', which='minor', length=4, width=1, labelsize=0, label1On=False)
        
        if(plotNum == 1):
            plt.ylabel("Energy (eV)", fontsize = fontSize)
        
        plt.xlabel(defect_name, fontsize = fontSize)
        plt.xlim(0,1)
        plt.ylim(0, cond_band_edge)
        
        energy, occupancy = [], []
        count = 0
        plotNum = plotNum + 1
        
        if(i > len(eigenVal) - 1):
            break
    if(count != 0):
        energy.append(float(eigenVal[i][1]) - band_edge)
        occupancy.append(float(eigenVal[i][2]))

plt.savefig(config["saveloc"])  
plt.show()  

del(count, data, f, i, j, jmin, jmax, defect_name, dotSize, energy, occupancy, emptyState, filledState)

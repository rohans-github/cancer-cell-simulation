import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def update(array1, fighters): # Update function creates new spacial plot
    array2 = [[0]*30]*30 # Creates a 30 by 30 array of 0
    array2 = np.array(array2) # Converts the array to a numpy array
    fighterX = [] # Array to store the x values of the fighter cells
    fighterY = [] # Array to store the y values of the fighter cells
    for i in range(30): # For loop for each row
        for j in range(30): # For loop for each column
            if array1[i][j] == 2: # If the position is a fighter cell
                fighterX.append(i) # Store x value of fighter cell
                fighterY.append(j) # Store y value of fighter cell
            if array1[i][j] == 1: # If the position is a cancer cell
                prob1 = 0.025 # Set probability of multiplication to 2.5%
                
                # For Moore neighborhood with radius 2
                for k in range(5):
                    for l in range(5):
                        if i - 2 + k < 30 and j - 2 + l < 30 and i - 2 + k >= 0 and j - 2 + k >= 0: # Checks for bounds
                            if (array1[i - 2 + k][j - 2 + l]) == 2: # If the neighbor is a fighter cell
                                prob1 = -10 # Set probability of multiplication to -10000%
                
                # For Moore neighborhood with radius 1
                for x in range(3):
                    for z in range(3):
                        if i - 1 + x < 30 and j - 1 + z < 30 and i - 1 + x >= 0 and j - 1 + z >= 0: # Checks for bounds
                            if (array1[i - 1 + x][j - 1 + z]) == 1: # If the neighbor is a cancer cell
                                prob1 = prob1 + 0.05 # Add 5 to probability of multiplication

                # For Moore neighborhood with radius 1
                for a in range(3):
                    for b in range(3):
                        if i - 1 + a < 30 and j - 1 + b < 30 and i - 1 + a >= 0 and j - 1 + b >= 0: # Checks for bounds
                            randNum = random.random() # Generate random number between 0 and 1
                            if (array1[i - 1 + a][j - 1 + b]) == 1: # If the neighbor is a cancer cell
                                array2[i - 1 + a][j - 1 + b] = 1 # Keep cancer cell as cancer cell
                            if (array1[i - 1 + a][j - 1 + b]) == 0: # If the neighbor is a healthy cell
                                if prob1 > randNum: # If probability of multiplication is greater than random number
                                    array2[i - 1 + a][j - 1 + b] = 1 # Change healthy cell to cancer cell
                                else:
                                    array2[i - 1 + a][j - 1 + b] = 0 # Keep healthy cell as healthy cell

    for z in range(len(fighterX)): # For each fighter cell
        randNum1 = random.random() # Generate random number between 0 and 1

        # For Moore neighborhood with radius 1
        for k in range(3):
            for l in range(3):
             if fighterX[z] - 1 + k < 30 and fighterY[z] - 1 + l < 30 and fighterX[z] - 1 + k >= 0 and fighterY[z] - 1 + k >= 0: # Checks for bounds
                    if randNum1 < 0.65: # Probability of 65%
                        array2[fighterX[z] - 1 + k][fighterY[z] - 1 + l] = 0 # Change neighbor to healthy cell

    while np.count_nonzero(array2 == 2) < fighters: # For the number of fighters
        randNum1 = int(random.random()*30) # Generate random x position
        randNum2 = int(random.random()*30) # Generate random y position
        array2[randNum1][randNum2] = 2 # Place fighter cell 
    return array2 # Return new plot

def plotSpatial(data, fileNumber): # Plots the spacial after each update
    cmap = colors.ListedColormap(['lawngreen', 'red', 'blue']) # Colors
    plt.figure(figsize=(7, 6)) # Size
    plt.pcolor(data, cmap=cmap, edgecolors='k', linewidths=1, vmin=0, vmax=2)
    
    # Legend
    cbar = plt.colorbar(label="", orientation="vertical", ticks=[0.33, 1, 1.66])
    cbar.ax.set_yticklabels(['Healthy', 'Cancer', "Fighter"])
    plt.savefig('figure_' + str(fileNumber) + '.jpg', bbox_inches='tight', pad_inches=0.02) # Save
    plt.close()

def plotDynamics(data): # Plots the line graph
    fig, axes = plt.subplots(figsize=(7, 6)) # Size
    axes.plot(data[0], data[1], label='healthy', color='green') # Plot healthy cells
    axes.plot(data[0], data[2], label='cancer', color='blue') # Plot cancer cells
    axes.set_xlabel('Time (weeks)') # X axis label
    axes.set_ylabel('Number of cells') # Y axis label
    axes.legend(bbox_to_anchor=(.3, 1), fontsize=13, fancybox=False, shadow=False, frameon=False) # Legend
    plt.savefig('temporalDynamics.pdf', bbox_inches='tight', pad_inches=0.02) # Save
    plt.close()

def main():
    random.seed(time.time()) # Seed
    sizeX, sizeY = 30, 30 # Size of plot
    domain = np.array([0 for x in range(sizeX*sizeY)]).reshape(sizeY, sizeX) # 2D numpy array
    cancer = input("Enter the initial number of cancer cells: ")
    
    while np.count_nonzero(domain == 1) < int(cancer): # For the number of inputted cancer cells
        randNum1 = int(random.random() * 30) # Random x position
        randNum2 = int(random.random() * 30) # Random y position
        domain[randNum1][randNum2] = 1 # Set as cancer cell
    
    simTime, healthy, cancer = [], [], [] # Blank arrays
    currTime = 0 # Time variable
    plotSpatial(domain, currTime) # Plot spacial plot
    simTime.append(currTime) # Log time
    healthy.append(np.count_nonzero(domain == 0)+np.count_nonzero(domain == 2)) # Log number of healthy cells
    cancer.append(np.count_nonzero(domain == 1)) # Log number of cancer cells
    count = 0 # Number of fighter cells

    for currTime in range(1, 101): # 101 iterations
        domain = update(domain, count) # Update
        count = count + 1 # Add one fighter cell
        if np.count_nonzero(domain == 1) > 700: # If there are more than 700 cancer cells
            count = count - 1 # Subtract one fighter cell
        
        plotSpatial(domain, currTime) # Plot Spacial
        simTime.append(currTime) # Log time
        healthy.append(np.count_nonzero(domain == 0)+np.count_nonzero(domain == 2)) # Log number of healthy cells
        cancer.append(np.count_nonzero(domain == 1)) # Log number of cancer cells
    temporal_dynamics = [simTime, healthy, cancer] # Combine 3 arrays
    plotDynamics(temporal_dynamics) # Line graph

main()
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Data
data = [{'frequency': 20, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 20, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 20, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 30, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 30, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 30, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 40, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 40, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 40, 'decibel': -35, 'response': 'Yes'}, 
        {'frequency': 50, 'decibel': -45, 'response': 'Yes'}, 
        {'frequency': 50, 'decibel': -40, 'response': 'Yes'}, 
        {'frequency': 50, 'decibel': -35, 'response': 'Yes'}, 
        {'frequency': 12000, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 12000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 12000, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 12500, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 12500, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 12500, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 13000, 'decibel': -45, 'response': 'Yes'}, 
        {'frequency': 13000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 13000, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 13500, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 13500, 'decibel': -40, 'response': 'Yes'}, 
        {'frequency': 13500, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 14000, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 14000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 14000, 'decibel': -35, 'response': 'Yes'}, 
        {'frequency': 14500, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 14500, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 14500, 'decibel': -35, 'response': 'Yes'}, 
        {'frequency': 15000, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 15000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 15000, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 15500, 'decibel': -45, 'response': 'Yes'}, 
        {'frequency': 15500, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 15500, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 16000, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 16000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 16000, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 16500, 'decibel': -45, 'response': 'Yes'}, 
        {'frequency': 16500, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 16500, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 17000, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 17000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 17000, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 17500, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 17500, 'decibel': -40, 'response': 'Yes'}, 
        {'frequency': 17500, 'decibel': -35, 'response': 'No'}, 
        {'frequency': 18000, 'decibel': -45, 'response': 'No'}, 
        {'frequency': 18000, 'decibel': -40, 'response': 'No'}, 
        {'frequency': 18000, 'decibel': -35, 'response': 'No'}]

def create_2d_array(data, num_cols):
    # Split the data into chunks of size num_cols
    # result = [data[i:i + num_cols] for i in range(0, len(data), num_cols)]

    result = []
    length = len(data)
    for x in range(0, length, 3):
        chunk = [data[x], data[x+1], data[x+2]]
        result.append(chunk)
    return result

def main():
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Sample data (replace with your data)
    # frequencies = [20, 30, 40, 50, 12000, 12500, 13000, 13500, 14000, 14500]
    # decibels = [-45, -40, -35]
    # responses = [['No', 'No', 'Yes'], ['No', 'No', 'Yes'], ['No', 'Yes', 'Yes'],  # 10 rows for each frequency
    #              ['Yes', 'Yes', 'Yes'], ['No', 'No', 'No'], ['No', 'No', 'No'], 
    #              ['No', 'No', 'No'], ['No', 'No', 'No'], ['No', 'No', 'No'], ['No', 'No', 'No']]


    frequencies = df['frequency'].unique()
    decibels = df['decibel'].unique()
    responses = create_2d_array(df['response'], 3)
    # print(responses)

    # Create a figure and add 3D subplot
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Define the x, y, and z positions for the bars
    xpos, ypos = np.meshgrid(np.arange(len(frequencies)), np.arange(len(decibels)))
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(len(xpos))

    # Define bar widths and heights
    dx = dy = 0.5
    dz = np.array([1 if responses[i // len(decibels)][i % len(decibels)] == 'Yes' else 0 for i in range(len(xpos))])

    # Plot the 3D bars
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=['green' if d == 1 else 'red' for d in dz])

    # Setting the labels
    ax.set_xticks(np.arange(len(frequencies)))
    ax.set_xticklabels(frequencies)
    ax.set_yticks(np.arange(len(decibels)))
    ax.set_yticklabels(decibels)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Decibel (dB)')
    ax.set_zlabel('Response (Yes/No)')

    

    plt.savefig("image.png", bbox_inches='tight')
    # Show the plot
    plt.show()
    


main()
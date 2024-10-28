import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


img_save_path = "./static/imgs/result_img.png"

# Example usage
# age = 35
# responses = [
#     {'frequency': 100, 'decibel': -40, 'response': 'Yes'}, 
#     {'frequency': 100, 'decibel': -30, 'response': 'Yes'}, 
#     {'frequency': 110, 'decibel': -40, 'response': 'Yes'}, 
#     {'frequency': 110, 'decibel': -30, 'response': 'Yes'}, 
#     {'frequency': 120, 'decibel': -40, 'response': 'Yes'}, 
#     {'frequency': 120, 'decibel': -30, 'response': 'Yes'}, 
#     {'frequency': 130, 'decibel': -40, 'response': 'Yes'}, 
#     {'frequency': 130, 'decibel': -30, 'response': 'Yes'}, 
#     {'frequency': 140, 'decibel': -40, 'response': 'No'}, 
#     {'frequency': 140, 'decibel': -30, 'response': 'Yes'}
# ]

def transform_list(gender, age, responses):
    plot_and_save_responses_by_age(age, responses)
    response_array = [1 if r['response'] == 'Yes' else 0 for r in responses]
    response_array.insert(0, gender)
    response_array.insert(1, age)
    return response_array

def plot_and_save_responses_by_age(age, responses):
    filename = img_save_path
    frequencies = [entry['frequency'] for entry in responses]
    decibels = [entry['decibel'] for entry in responses]
    binary_responses = [1 if entry['response'] == 'Yes' else 0 for entry in responses]
    
    plt.figure(figsize=(10, 5))
    
    # Plot the responses
    plt.scatter(frequencies, binary_responses, c=decibels, cmap='viridis', label='Response', s=100)
    plt.colorbar(label='Decibel Level (dB)')  # Adds a color bar to represent decibel levels

    # Labeling the graph
    plt.title(f'Audiometric Test Responses for Age {age}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Response (1 = Yes, 0 = No)')
    plt.ylim(-0.1, 1.1)  # Ensures binary response stays between 0 and 1

    # Show grid
    plt.grid(True)

    # Save the figure to a file
    plt.savefig(filename, bbox_inches='tight')  # Saves the plot as an image
    # print(f"Graph saved as {filename}")
    # plt.show()
    plt.close()
    

# plot_and_save_responses_by_age(age, responses)
# print(transform_list(age, responses))

import json
import matplotlib.pyplot as plt
import os




def generate_heatmap(hold_matrix, board_setup) -> None:
    """Generate a heatmap of hold usage for a Moonboard setup

    Args:
        hold_matrix (list): A 2D list of hold usage data
        board_setup (str): The name of the Moonboard setup
    """
    fig, axes = plt.subplots()
    heatmap = axes.imshow(hold_matrix, cmap='magma', interpolation='nearest')
    axes.set_title(f"Hold use Heatmap for {board_setup}")
    plt.colorbar(heatmap, ax=axes)  # Add a colorbar to the heatmap
    plt.tight_layout()
    plt.axis("off")
    plt.savefig(f"heatmap_{board_setup}.png", dpi=300, bbox_inches='tight') # save the heatmap as a PNG file
    plt.close()
    
    
    
def collect_hold_data() -> None:
    """Collect hold usage data from Moonboard logbooks and generate heatmaps"""
    os.chdir("logbooks")
    for board_setup in os.listdir(): # loop through board setups
        os.chdir(board_setup)
        hold_matrix = [[0 for i in range(11)] for j in range(18)] # init hold use matrix
        sessions_folder = [file for file in os.listdir() if not (file.endswith('.json') or file.endswith('.png'))][0] # get sessions folder
        os.chdir(sessions_folder)
        for session in os.listdir(): # loop through sessions
            with open(session, 'r') as file:
                data = json.load(file)  # load the JSON content
                for boulder in data["Data"]:
                    for hold in boulder["Problem"]["Locations"]:
                        x, y = hold["X"], hold["Y"]
                        x = round((x-95)/50) # convert x and y to matrix indices
                        y = round((y-88)/50)
                        hold_matrix[y][x] += 1
        os.chdir("..") # return to parent directory
        with open('hold_matrix.json', 'w') as json_file: # save hold matrix
            json.dump(hold_matrix, json_file, indent=4)
        generate_heatmap(hold_matrix, board_setup) # create and save heatmap
        os.chdir("..") 
    os.chdir("..") # return to root directory

           

    
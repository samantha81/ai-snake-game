import os
import json
import numpy as np
import matplotlib.pyplot as plt


def load_weights(saved_dir):
    weights = {}
    biases = {}
    
    for fname in os.listdir(saved_dir):
        if fname.endswith('.npy'):
            key = fname[:-4]  # strip .npy
            key = key.strip()
            data = np.load(os.path.join(saved_dir, fname))
            if key.startswith('W'):
                weights[key] = data
            elif key.startswith('b'):
                biases[key] = data

    return weights, biases


def load_constructor_params(saved_dir):
    path = os.path.join(saved_dir, 'constructor_params.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}


def visualise_weights(weights, biases):
    for w_key in sorted(weights.keys()):
        layer_num = w_key[1:]  # extract layer number from "W1", "W2", etc.
        b_key = f"b{layer_num}"

        if b_key not in biases:
            print(f"Bias {b_key} not found for {w_key}, skipping...")
            continue

        w = weights[w_key]
        b = biases[b_key]

        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(w, cmap='coolwarm', aspect='auto')
        plt.title(f"Weights {w_key} ({w.shape[0]} → {w.shape[1]})")
        plt.colorbar()

        plt.subplot(1, 2, 2)
        plt.imshow(b.reshape(1, -1), cmap='coolwarm', aspect='auto')
        plt.title(f"Biases {b_key} ({b.shape[0]})")
        plt.colorbar()

        plt.tight_layout()
        plt.show()



def main():
    #Set this to your saved generation snake folder (here)
    saved_snake_dir = "C:/Code/SnakeAI-master/saved_snakes2/best_snake_gen164"

    if not os.path.exists(saved_snake_dir):
        print("Folder does not exist:", saved_snake_dir)
        return

    weights, biases = load_weights(saved_snake_dir)
    constructor = load_constructor_params(saved_snake_dir)

    print("Constructor Parameters:")
    for key, value in constructor.items():
        print(f"  {key}: {value}")

    visualise_weights(weights, biases)


if __name__ == "__main__":
    main()

'''
When each generation of snake is saved, there will be a file with the name W1, W2, W3, and b1, b2, b3, and a constructor_params.json and a settings.json
--------------------------------------------------------------------------------------
File      |      What it contains
--------------------------------------------------------------------------------------
W1.npy    |  Weight matrix between input layer and first hidden layer
b1.npy    |  Bias vector for the first hidden layer
W2.npy    |  Weights between first hidden layer and second hidden layer (if any)
b2.npy    |  Biases for the second hidden layer
...       |  Same pattern continues for deeper layers
--------------------------------------------------------------------------------------

Contructor parameters as JSON file (constructor_params.json)
Contains:
- start_pos: The snake's starting point
- apple_seed: The seed used to generate apple positions to ensure deterministic behaviour
- initial_velocity: Starting movement vector
- starting_direction: Initial direction

Hyperparameters (only saved once per population) (settings.json)
Contains:
- Network architecture
- Activation functions
- Mutation/crossover probabilities
- Selection strategy
- Lifespan, vision type, etc

------------------------------------------------------------
Visualising the weights and biases and its meaning
------------------------------------------------------------

The colous in the weight and bias visualisations (heatmaps) are a way to represent the magnitude and sign of each number (i.e., weight or bias value) in a neural network.
The colour in the heatmaps represent:
---------------------------------------------------------------------------------
Colour                     Value Type                          Meaning
---------------------------------------------------------------------------------
Blue                Negative weight/biases              Inhibits activation
White/Pale          Near Zero                           Little to no influence
Red                 Positive weight/biases              Excites activation
---------------------------------------------------------------------------------

The snake's neural network processes sensory inputs like "apple detected in direction X" or "wall ahead".
Each layer of weights determines:
- Which features are important
- Which outputs should be activated

So that means:
Strong Blue (high -ve) weight   : a strong negative influence --> If I see apple left, go left (example)
Neurtal (≈0) weight             : doesn't contribute much do decision-making
Strong Red (high +ve) weight    : a strong positive influence -> If I see wall ahead, avoid going (example)

Bias Colors
- Biases are thresholds for neuron activation
- Red = neuron is biased toward activation
- Blue = neuron is biased against activation

Summary
Red = Promotes activation
Blue = Inhibits activation
White = Has little effect
Brighter = stronger influence
'''
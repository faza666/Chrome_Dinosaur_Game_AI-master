import os
import pickle
import pygame
import neat
from game_resorses.game import GameMechanics
from game_resorses.dinosaur import Dinosaur
from game_resorses.game_handler import GameHandler
from neat_AI.neat_ import NEAT
from neat_AI import visualize


# Generate genomes
def eval_genomes(genomes, config):
    game = GameMechanics()
    # (genome_id, genome_object)
    for _, genome_object in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome_object, config)
        NEAT.nets.append(net)
        game.dinosaurs.append(Dinosaur())
        genome_object.fitness = 0
        NEAT.genome_list.append(genome_object)
    game.main_loop(neat_object, game_handler)


# Restore the winner dinosaur
def run_super_dinosaur(genome, config):
    game = GameMechanics()
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    NEAT.nets.append(net)
    game.dinosaurs.append(Dinosaur())
    genome.fitness = 0
    NEAT.genome_list.append(genome)
    game.main_loop(neat_object, game_handler)


# Receives a genome and draws a neural network with arbitrary topology
def draw_net(config, winner):
    node_names = {
        -1: 'dino y',
        -2: 'obs x',
        -3: 'obs top',
        -4: 'obs bottom',
        -5: 'obs type',
        -6: 'game speed',
        0: 'duck',
        1: 'jump'
    }
    visualize.draw_net(config, winner, True, node_names=node_names)


def run_training_mode(config):

    # Run generations until 'fitness_threshold' will be reached.
    # Put number of generations to run as second argument
    winner = neat_object.population.run(eval_genomes)

    # Save the winner genome description as text
    with open(os.path.join(local_directory, 'winner_genome', 'winner.pkl'), 'w') as file:
        file.write(str(winner))

    # Save the winner genome object to use it later
    with open(os.path.join(local_directory, 'winner_genome', 'winner.pkl'), 'wb') as file:
        pickle.dump(winner, file)

    # Display the winning genome.
    print(f'\nBest genome:\n{winner}')

    # Receives a genome and draws a neural network with arbitrary topology
    draw_net(config, winner)

    # Plots the population's average and best fitness
    visualize.plot_stats(neat_object.stats, ylog=False, view=True)

    # Visualizes speciation throughout evolution
    visualize.plot_species(neat_object.stats, view=True)


def run_winner_model(config):
    # Read the winner genome from file
    with open(os.path.join(local_directory, 'winner_genome', 'winner.pkl'), "rb") as file:
        winner = pickle.load(file)

    # Receives a genome and draws a neural network with arbitrary topology
    draw_net(config, winner)

    # Run winner genome
    # Having fun!!! )))
    run_super_dinosaur(winner, config)


if __name__ == '__main__':
    # Initializing pygame object
    pygame.init()

    # Initializing gameHandle object
    # to store all the data between games
    game_handler = GameHandler()

    # To run the script in model training mode - leave as it is
    # To run the script in use model mode:
    #   set "game_handler.training_mode" parameter to False
    game_handler.training_mode = True

    # Full name of the config file
    local_directory = os.path.dirname(__file__)
    config_file = os.path.join(local_directory, 'neat_AI', 'config.txt')

    # Initializing the NEAT object
    neat_object = NEAT(config_file)

    # Start reporting tools
    neat_object.population_statistics()

    if game_handler.training_mode:
        # If training model mode:
        run_training_mode(config=neat_object.config)

        # Save checkpoints in training mode every n generations
        # to restore from there if needed
        neat_object.save_checkpoint_interval = 10

        # If you need to restore from checkpoint, just put there a number of it
        # (works in training mode only)
        # Zero - start from beginning
        neat_object.restore_checkpoint = 0
    else:
        # I use model mode:
        run_winner_model(config=neat_object.config)

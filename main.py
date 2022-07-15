import os
import pickle
import pygame
import neat
from game_resorses.game import GameMechanics
from game_resorses.dinosaur import Dinosaur
from game_resorses.game_handler import GameHandler
from neat_AI.neat_ import NEAT
from neat_AI import visualize


# Restore the winner dinosaur
def run_super_dinosaur(genome, config, neat_object, game_handler):
    game = GameMechanics(neat_object, game_handler)
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    NEAT.nets.append(net)
    game.dinosaurs.append(Dinosaur())
    genome.fitness = 0
    NEAT.genome_list.append(genome)
    game.main_loop()


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


def run_training_mode(neat_object, game_handler, home_directory):

    # Generate genomes
    def eval_genomes(genomes, config):
        # Initialize game object
        game = GameMechanics(neat_object, game_handler)

        # (genome_id, genome_object)
        for _, genome_object in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome_object, config)
            NEAT.nets.append(net)
            game.dinosaurs.append(Dinosaur())
            genome_object.fitness = 0
            NEAT.genome_list.append(genome_object)

        # Run game
        game.main_loop()

    # Run generations until 'fitness_threshold' will be reached.
    # To stop after run some number of generations, put the number as a second argument (int)
    winner = neat_object.population.run(eval_genomes)

    # Save the winner genome description as text
    with open(os.path.join(home_directory, 'winner_genome', 'winner.txt'), 'w') as file:
        file.write(str(winner))

    # Save the winner genome object to use it later
    with open(os.path.join(home_directory, 'winner_genome', 'winner.pkl'), 'wb') as file:
        pickle.dump(winner, file)

    # Display the winning genome.
    print(f'\nBest genome:\n{winner}')

    # Receives a genome and draws a neural network with arbitrary topology
    draw_net(neat_object.config, winner)

    # Plots the population's average and best fitness
    visualize.plot_stats(neat_object.stats, ylog=False, view=True)

    # Visualizes speciation throughout evolution
    visualize.plot_species(neat_object.stats, view=True)


def run_winner_model(neat_object, game_handler, home_directory):
    # Read the winner genome from file
    with open(os.path.join(home_directory, 'winner_genome', 'winner.pkl'), "rb") as file:
        winner = pickle.load(file)

    # Receives a genome and draws a neural network with arbitrary topology
    draw_net(neat_object.config, winner)

    # Run winner genome
    # Having fun!!! )))
    run_super_dinosaur(winner, neat_object.config, neat_object, game_handler)


def main_menu(training_mode, checkpoint_interval, restore_checkpoint):
    # Initializing pygame object
    pygame.init()

    # Initializing gameHandle object
    # to store all the data between games
    game_handler = GameHandler()

    # Full name of the config file
    home_directory = os.path.dirname(__file__)
    config_file = os.path.join(home_directory, 'neat_AI', 'config.txt')

    if training_mode:
        # Initializing the NEAT object
        neat_object = NEAT(
            config_file=config_file,
            checkpoint_interval=checkpoint_interval,
            restore_checkpoint=restore_checkpoint
        )

        # If training model mode:
        run_training_mode(neat_object=neat_object, game_handler=game_handler, home_directory=home_directory)
    else:
        # Initializing the NEAT object
        neat_object = NEAT(
            config_file=config_file,
            checkpoint_interval=0,
            restore_checkpoint=0
        )
        # I use model mode:
        run_winner_model(neat_object=neat_object, game_handler=game_handler, home_directory=home_directory)


if __name__ == '__main__':
    # To run the script in model training mode:
    #   set "script_mode" parameter to True
    # To run the script in use model mode:
    #   set "script_mode" parameter to False
    script_mode = False

    # Save checkpoints in training mode every n generations
    # to restore from there if needed
    # (works in training mode only)
    save_every_n_generations = 10

    # If you need to restore from checkpoint, just put there a number of it
    # Zero - start from beginning
    # (works in training mode only)
    restore_from_generation = 0

    main_menu(script_mode, save_every_n_generations, restore_from_generation)

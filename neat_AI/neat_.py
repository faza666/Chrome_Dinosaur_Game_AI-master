import neat


class NEAT:
    nets = []
    genome_list = []

    def __init__(self, config_file, checkpoint_interval=10, restore_checkpoint=0):
        self.stats = None
        self.config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file
        )
        self.population = None
        self.fitness_threshold = self.config.__getattribute__('fitness_threshold')
        self.restore_checkpoint = restore_checkpoint
        self.save_checkpoint_interval = checkpoint_interval
        self.population_statistics()

    def population_statistics(self):
        # Create the population, which is the top-level object for a NEAT run.
        if self.restore_checkpoint:
            self.population = neat.Checkpointer.restore_checkpoint(
                f'neat-checkpoint-{self.restore_checkpoint}'
            )
        else:
            self.population = neat.Population(self.config)
        # Add a stdout reporter to show progress in the terminal.
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)
        self.population.add_reporter(
            neat.Checkpointer(self.save_checkpoint_interval)
        )

from socket import if_nameindex
import numpy as np
from snake_lib import Snake


class GeneticAlgorithm:
    def __init__(self, pop_size, max_moves, start_position=(270,240)):
        self.pop_size = pop_size
        self.max_moves = max_moves
        self.mutation_rate = 0.15
        self.walls = [20,20,510,450]
        self.population = []
        self.generation = 1
        self.best_fitness = 0
        self.total_fitness = 0
        self.all_pos = [(x*10,y*10) for x in range(2,52) for y in range(2, 46)]
        for k in range(pop_size):
            self.population.append(self.place_snake())
    
    def place_snake(self, start_position=(270,240)):
        x_food = int(np.random.randint(2,52)*10)
        y_food = int(np.random.randint(2,46)*10)
        return Snake(start_position, (x_food, y_food))
    
    def play_snake(self, snake):
        snake.step()
        #Food
        if (snake.x, snake.y) == snake.food_pos:
            snake.add_body()
            available_pos = [x for x in self.all_pos if x not in snake.body]
            idx = np.random.randint(0, len(available_pos))
            snake.food_pos = available_pos[idx]
        if (snake.x, snake.y) in snake.body[1:]:
            snake.kill()
    
    def update(self):
        snakes_alive = 0
        one_alive = False
        select_snake = False
        for snake in self.population:
            if not snake.died:
                one_alive = True
                snakes_alive += 1
                self.play_snake(snake)
                if snake.lifetime>self.max_moves*(len(snake.body)-2): snake.kill()
                # Show snake
                if not select_snake:
                    show_snake = snake
                    select_snake = True
        info = {}
        info['gen'] = self.generation
        info['pop'] = snakes_alive
        info['bf'] = self.best_fitness
        info['tf'] = self.total_fitness

        if not one_alive:
            best_fitness = -1
            self.total_fitness = 0
            for snake in self.population:
                self.total_fitness += snake.fitness
                if snake.fitness > best_fitness:
                    best_fitness = snake.fitness
                    best_snake = snake
            self.best_fitness = best_fitness
            test_snake = self.place_snake()
            test_snake.brain = best_snake.brain
            info['status'] = 'test'
            return test_snake, info
        info['status'] = 'train'
        return show_snake, info
    
    def next_gen(self):
        self.generation += 1
        self.population.sort(key= lambda x: x.fitness, reverse=True)
        new_pop = []
        for k in range(self.pop_size):
            new_snake = self.place_snake()
            first_parent = self.select_parent()
            second_parent = self.select_parent()
            new_snake.brain = first_parent.brain.crossover(second_parent.brain)
            new_snake.brain.mutate(self.mutation_rate)
            new_pop.append(new_snake)
        self.population = new_pop

    def select_parent(self):
        fitness_count = 0
        idx = np.random.randint(0, int(self.total_fitness*0.75))
        for snake in self.population:
            fitness_count += snake.fitness
            if idx < fitness_count:
                return snake
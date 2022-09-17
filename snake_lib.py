from nnet import NNet
import numpy as np

class Snake:
    def __init__(self, start_position, food_pos=None):
        self.x = start_position[0]
        self.y = start_position[1]
        self.brain = NNet(24, 24, 4)
        self.body = [(self.x, self.y), (self.x+10, self.y), (self.x+20, self.y)]
        self.food_pos = food_pos
        self.died = False
        self.lifetime = 0
        self.walls = [20,20,510,450]

    def step(self):
        inputs = self.get_inputs()
        results = self.brain.forward(inputs)
        idx = np.argmax(results)
        if idx==0: self.x -= 10
        elif idx==1: self.x += 10
        elif idx==2: self.y -= 10
        else: self.y += 10
        self.body.insert(0, (self.x, self.y))
        self.last_block = self.body.pop()
        self.lifetime += 1
        x, y = self.x, self.y
        if x<self.walls[0] or x>self.walls[2] or y<self.walls[1] or y>self.walls[3]:
            self.kill()

    def kill(self):
        self.died = True
        if len(self.body) < 10:
            fitness = self.lifetime*(2**(len(self.body)-3))
            if len(self.body)< 4: fitness = int(fitness/100) + 1
        else:
            fitness = self.lifetime*(2**10)*(len(self.body)-9)
        self.fitness = int(fitness)
    
    def add_body(self):
        self.body.append(self.last_block)

    def get_inputs(self):
        inputs = [0 for x in range(24)]
        # Up dir
        vars = self.measure_in_dir(0, -10)
        inputs[0] = vars[0]
        inputs[1] = vars[1]
        inputs[2] = vars[2]
        # Up-left dir
        vars = self.measure_in_dir(-10, -10)
        inputs[3] = vars[0]
        inputs[4] = vars[1]
        inputs[5] = vars[2]
        # Up dir
        vars = self.measure_in_dir(-10, 0)
        inputs[6] = vars[0]
        inputs[7] = vars[1]
        inputs[8] = vars[2]
        # Up dir
        vars = self.measure_in_dir(-10, 10)
        inputs[9] = vars[0]
        inputs[10] = vars[1]
        inputs[11] = vars[2]
        # Up dir
        vars = self.measure_in_dir(0, 10)
        inputs[12] = vars[0]
        inputs[13] = vars[1]
        inputs[14] = vars[2]
        # Up dir
        vars = self.measure_in_dir(10, 10)
        inputs[15] = vars[0]
        inputs[16] = vars[1]
        inputs[17] = vars[2]
        # Up dir
        vars = self.measure_in_dir(10, 0)
        inputs[18] = vars[0]
        inputs[19] = vars[1]
        inputs[20] = vars[2]
        # Up dir
        vars = self.measure_in_dir(10, -10)
        inputs[21] = vars[0]
        inputs[22] = vars[1]
        inputs[23] = vars[2]

        inputs = np.array(inputs)
        inputs = np.expand_dims(inputs, axis=0)
        return inputs

    def measure_in_dir(self, dx, dy):
        vals = [0,0,0]
        found_wall = False
        found_tail = False
        found_food = False
        x, y = self.x+dx, self.y+dy
        distance = 1
        while not found_wall:
            if x<self.walls[0] or x>self.walls[2] or y<self.walls[1] or y>self.walls[3]:
                found_wall = True
            if not found_food and (x,y) == self.food_pos:
                vals[0] = 1
                found_food = True
            if not found_tail and (x,y) in self.body:
                vals[1] = 1/distance
                found_tail = True
            distance += 1
            x += dx
            y += dy
        vals[2] = 1/distance
        return vals

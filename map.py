import json
import pygame
import numpy as np


class Map:
    def __init__(self, map_file):
        self.map_file = map_file
        self.map = self.load_map()
        self.inner_points = self.map['inner_points']
        self.outer_points = self.map['outer_points']
        self.inner_points.append(self.inner_points[0])
        self.inner_points.reverse()
        self.outer_points.append(self.outer_points[0])
        self.outer_points += self.inner_points
        # for i in range(len(self.inner_points)):
        #     self.inner_points[i] = np.array(self.inner_points[i])
        for i in range(len(self.outer_points)):
            self.outer_points[i] = np.array(self.outer_points[i])
        # self.inner_points = np.array(self.inner_points)
        self.outer_points = np.array(self.outer_points)
        self.rewards=[np.array(reward) for reward in self.map['rewards']]
        self.collected=[False for _ in self.rewards]

    def load_map(self):
        return json.load(open(self.map_file))

    def draw(self, win):
        pygame.draw.polygon(win, (255, 255, 255), self.outer_points, 1)
        # pygame.draw.polygon(win, (255, 255, 255), self.inner_points, 1)
        for ind in range(len(self.rewards)):
            if not self.collected[ind]:
                pygame.draw.circle(win, (255, 0, 0), self.rewards[ind], 5)

    def check_reward(self, position):
        for i in range(len(self.rewards)):
            if not self.collected[i] and np.linalg.norm(self.rewards[i] - position) < 20:
                print("collected")
                self.collected[i]=True
                return True
        return False
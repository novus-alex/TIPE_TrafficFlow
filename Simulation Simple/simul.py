import pygame
from math import *
import matplotlib.pyplot as plt
import time
import numpy as np

class Screen:
    def __init__(self):
        pygame.init()
        self.max_x, self.max_y = 1000, 500
        self.scr = pygame.display.set_mode([self.max_x, self.max_y])

        self.dt = 0.3
        self.N = 5000
        pygame.time.delay(100)

        self.veh = [(0, self.max_y//2)]
        self.v = [Vehicle(0.01, self.veh[-1])]

        self.running = True
        self._handle()

    def _handle(self):
        for i in range(self.N):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            self._refresh()
            time.sleep(0.001/self.dt)
            pygame.display.flip()
        pygame.quit()

    def _struct(self):
        self.scr.fill((255, 255, 255))
        pygame.draw.rect(self.scr, (100, 0, 255), pygame.Rect(-2, self.max_y//2, self.max_x + 4, 20), 2)

    def _veh(self):
        if self.v[-1].x > 100:
            self.veh.append((0, self.max_y//2))
            self.v.append(Vehicle(0.01, self.veh[-1]))

        for i in range(len(self.veh)):
            self.v[i].update(i, self.v, self.dt)
            pygame.draw.rect(self.scr, (0, 0, 0), self.v[i].get_model())

    def _test(self):
        pygame.draw.circle(self.scr, (0, 0, 255), (250, 250), 75)

    def _refresh(self):
        self._struct()
        self._veh()
        pygame.display.update()


class Vehicle:
    def __init__(self, speed, coord):
        self.speed = speed
        self.x, self.y = coord[0], coord[1]

        self.dist = 50

        self.pos = []; self.err = []

        self.l = 4
        self.s0 = 8
        self.T = 0.8
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def get_model(self):
        return pygame.Rect((self.x, 255, 20, 10))

    def update(self, i, veh, dt):
        if i > 0:
            lead = veh[i-1]

            if self.v + self.a*dt < 0:
                self.x -= 1/2*self.v*self.v/self.a
                self.v = 0
            else:
                self.v += self.a*dt
                self.x += self.v*dt + self.a*dt*dt/2
            
            # Update acceleration
            alpha = 0
            if lead:
                delta_x = lead.x - self.x - lead.l
                delta_v = self.v - lead.v

                alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

                self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

                if delta_x < 100:
                    self.a = self.a = -self.b_max*self.v/self.v_max
            
        else:
            if self.x < 500:
                self.speed = self.v_max
            elif self.x > 500 and self.x < 700:
                self.speed = self.v_max*0.3
            else:
                self.v = 0
            self.x += self.speed*dt


if __name__ == "__main__":
    t = Screen()

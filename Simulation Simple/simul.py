import pygame
from math import *

class Screen:
    def __init__(self):
        pygame.init()
        self.max_x, self.max_y = 1000, 500
        self.scr = pygame.display.set_mode([self.max_x, self.max_y])

        self.dt = 10
        pygame.time.delay(self.dt)

        self.veh = [(0, self.max_y//2)]
        self.v = [Vehicle(0.001, self.veh[-1])]

        self.running = True
        self._handle()

    def _handle(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self._refresh()
            pygame.display.flip()
        pygame.quit()

    def _struct(self):
        self.scr.fill((255, 255, 255))
        pygame.draw.rect(self.scr, (100, 0, 255), pygame.Rect(-2, self.max_y//2, self.max_x + 4, 40), 2)

    def _veh(self):
        if self.veh[-1][0] > 100:
            self.veh.append((0, self.max_y//2))
            self.v.append(Vehicle(0.001, self.veh[-1]))

        for i in range(len(self.veh)):
            self.v[i].update(i, self.veh, self.dt)
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

        self.speed_pid = PID(0.5, 0, 0)

        self.dist = 10

    def get_model(self):
        return pygame.Rect((self.x, 255, 40, 30))

    def update(self, i, veh, dt):
        if i > 0:
            output = self.speed_pid.compute(abs(veh[i-1][0] - veh[i][0]), self.dist, dt)/dt
            if self.speed > 0:
                self.speed += output
            else:
                self.speed = 0

        else:
            self.speed = 0.1*abs(cos(self.x/2*pi*1000))

        self.x += self.speed*dt
        veh[i] = (self.x, veh[i][1])


class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.l_e = [0, 0]
        self.c = 0

    def compute(self, position, target, dt):
        e = position - target

        self.l_e[self.c%2] = e
        self.c += 1
        return (self.kp + self.ki*dt + self.kd/dt)*e + (-self.kp - 2*self.kd/dt)*self.l_e[0] + self.l_e[1]*self.kd/dt




if __name__ == "__main__":
    t = Screen()

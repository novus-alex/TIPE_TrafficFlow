import copy, time
import numpy as np

dt = 0.01

class Road():
    def __init__(self, start, stop):
        self.start, self.stop = start, stop
        self.veh = []

    def add(self, v):
        self.veh.append(v)

    def update(self):
        for veh in self.veh:
            veh.update()


Roads = [Road((0,0), (10,10)), Road((0,0), (100,100))]


class Vehicle:
    def __init__(self, road, v):
        self.r = road
        self.x, self.y = self.r.start[0], self.r.start[1]

        self.l = 4
        self.s0 = 8
        self.T = 0.8
        self.v_max = v
        self.a_max = 3
        self.b_max = 4.61

        self.v = self.v_max
        self.a = 0
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self.veh_len = 2

    def update(self):
        lead = -1
        alpha = 0
        
        if len(self.r.veh) != 0:
            if len(self.r.veh) > 1:
                for i in range(len(self.r.veh)-1):
                    if self.r.veh[i] == self:
                        lead = i-1

                if self.r.veh[lead] != self:
                    delta_x = self.r.veh[lead].x - self.x - self.veh_len
                    delta_v = self.v - self.r.veh[lead].v
                else:
                    delta_x = self.r.stop[0]
                    delta_v = self.v_max - self.v
            else:
                delta_x = self.r.stop[0]
                delta_v = self.v_max - self.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

            self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

            if self.v + self.a*dt < 0:
                self.x -= 1/2*self.v*self.v/self.a
                self.v = 0
            else:
                self.v += self.a*dt
                self.x += self.v*dt + self.a*dt*dt/2

            if self.x > self.r.stop[0]:
                for road in Roads:
                    if road.start[0] < self.x and road.stop[0] > self.x:
                        try:
                            self.insertion(road)
                        except InsertionError:
                            self.v = 0
                            pass
                    

    def insertion(self, r):
        if len(r.veh) > 1:
            for i in range(1, len(r.veh)):
                if r.veh[i].x > self.x + self.veh_len and r.veh[i-1].x < self.x - self.veh_len:
                    print("changing road")
                    veh_copy = copy.deepcopy(r.veh)
                    r.veh = veh_copy[:i] + [self] + veh_copy[i:]
                    self.r.veh.pop()
                    self.r = r
                else:
                    print("cannot change road")
                    raise InsertionError
        elif len(r.veh) == 1:
            if r.veh[0].x < self.x - self.veh_len:
                    veh_copy = copy.deepcopy(r.veh)
                    r.veh = veh_copy + [self]
                    self.r.veh.pop()
                    self.r = r
            elif r.veh[0].x > self.x + self.veh_len:
                veh_copy = copy.deepcopy(r.veh)
                r.veh = [self] + veh_copy
                self.r.veh.pop()
                self.r = r
            else:
                raise InsertionError
        else:
            self.r.veh.pop()
            r.add(self)
            self.r = r


class InsertionError(Exception):
    pass


Roads[0].add(Vehicle(Roads[0], 5))
Roads[1].add(Vehicle(Roads[1], 5))

for i in range(1000):
    R_cmd = []
    for r in Roads:
        r.update()
        r_cmd = ['-']*(r.stop[0]-r.start[0] + 2)
        for veh in r.veh:
            r_cmd[int(veh.x)] = 'x'
        s = ""
        for c in r_cmd:
            s += c
        R_cmd.append(s)
        
        time.sleep(dt)

    print('\n'.join(r for r in R_cmd))
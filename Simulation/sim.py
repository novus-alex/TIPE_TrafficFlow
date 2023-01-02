import copy, time

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
        self.v = v

        self.veh_len = 2

    def update(self):
        lead = -1
        if len(self.r.veh) != 0:
            if len(self.r.veh) > 1:
                for i in range(len(self.r.veh)):
                    if self.r.veh[i] == self:
                        lead = i-1
                d = self.r.veh[lead].x - self.x
            else:
                d = self.r.stop[0] - self.x

            self.a = d*dt**2
            self.v += self.a*dt
            self.x += self.v*dt

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
                    r.veh = veh_copy[:i]; r.veh.append(self); r.veh += veh_copy[i:]
                    self.r.veh.pop()
                    self.r = r
                else:
                    print("cannot change road")
                    raise InsertionError
        elif len(r.veh) == 1:
            if r.veh[0].x < self.x - self.veh_len:
                    veh_copy = copy.deepcopy(r.veh)
                    r.veh = veh_copy; r.veh.append(self)
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
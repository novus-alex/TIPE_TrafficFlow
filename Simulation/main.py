from road import Road
from copy import deepcopy
from vehicle_generator import VehicleGenerator
from curve import *
from win import *

class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        self.generators = []
        self.traffic_signals = []

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def update(self):
        # Update every road
        for road in self.roads:
            road.update(self.dt)

        # Add vehicles
        for gen in self.generators:
            gen.update()

        for signal in self.traffic_signals:
            signal.update(self)

        # Check roads for out of bounds vehicle
        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue
            # If not
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Create a copy and reset some vehicle properties
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                # In all cases, remove it from its road
                road.vehicles.popleft() 
        # Increment time
        self.t += self.dt
        self.frame_count += 1


    def run(self, steps):
        for _ in range(steps):
            self.update()


if __name__ == "__main__":
    n = 15

    s = Simulation()
    s.create_roads([
        ((-10, 106), (290, 106)),
        ((-10, 102), (290, 102)),

        ((290, 98), (-10, 98)),
        ((290, 94), (80, 94)),
        ((80, 94), (-10, 94)),

        ((101, 90), (80, 94)),
        ((160, 90), (100, 90)),

        *curve_road((250, 10), (160, 90), (210, 90), resolution=n)
    ])

    s.create_gen({
        'vehicle_rate': 30,
        'vehicles': [
            [3, {"path": [3, 4]}],
    
            [1, {"path": [*range(7, 7+n), 6, 5, 4]}]

        ]
    })

    w = Window(sim=s)
    w.offset = (-145, -95)
    w.run(steps_per_update=3)
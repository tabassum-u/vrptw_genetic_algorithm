import os
import io
import random

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
X_COORD = 'x'
Y_COORD = 'y'
COORDINATES = 'coordinates'
INSTANCE_NAME = 'instance_name'
MAX_VEHICLE_NUMBER = 'max_vehicle_number'
VEHICLE_CAPACITY = 'vehicle_capacity'
DEPART = 'depart'
DEMAND = 'demand'
READY_TIME = 'ready_time'
DUE_TIME = 'due_time'
SERVICE_TIME = 'service_time'
DISTANCE_MATRIX = 'distance_matrix'
UNCERTAIN_DEMAND = 'uncertain_demand'


def calculate_distance(cust_1, cust_2):
    x_diff = cust_1[COORDINATES][X_COORD] - cust_2[COORDINATES][X_COORD]
    y_diff = cust_1[COORDINATES][Y_COORD] - cust_2[COORDINATES][Y_COORD]
    distance_coordinate = (x_diff ** 2 + y_diff ** 2) ** 0.5
    return distance_coordinate


def load_problem_instance(problem_name):
    cust_num = 0
    text_file = os.path.join(BASE_DIR, 'data', problem_name + '.txt')
    parsed_data = {}

    print()
    with io.open(text_file, 'rt', newline='') as fo:
        for line_count, line in enumerate(fo, start=1):
            if line_count == 1:
                parsed_data[INSTANCE_NAME] = line.strip()
                print('parsed data instance name', parsed_data[INSTANCE_NAME])
            elif line_count == 5:
                values = line.strip().split()
                parsed_data[MAX_VEHICLE_NUMBER] = int(values[0])
                parsed_data[VEHICLE_CAPACITY] = float(values[1])
            elif line_count == 10:
                # DEPART
                values = line.strip().split()
                parsed_data[DEPART] = {
                    COORDINATES: {
                        X_COORD: float(values[1]),
                        Y_COORD: float(values[2]),
                    },
                    DEMAND: float(values[3]),
                    READY_TIME: float(values[4]),
                    DUE_TIME: float(values[5]),
                    SERVICE_TIME: float(values[6]),
                }
            elif line_count > 10:
                # CUSTOMERS
                values = line.strip().split()  # split the values ['1', '41', '49', '10', '161', '171', '10']
                random_generate = random.uniform(0.96, 1.04)
                parsed_data[F'C_{values[0]}'] = {
                    COORDINATES: {
                        X_COORD: float(values[1]),
                        Y_COORD: float(values[2]),
                    },

                    DEMAND: float(values[3]) * random_generate,
                    READY_TIME: float(values[4]),
                    DUE_TIME: float(values[5]),
                    SERVICE_TIME: float(values[6]),
                }

                cust_num += 1

            else:
                pass

        customers = [DEPART] + [F'C_{x}' for x in range(1, cust_num+1)] # 101 times loop
        # ['depart', 'C_1', 'C_2', like this upto 'C_100'

        parsed_data[DISTANCE_MATRIX] = \
            [[calculate_distance(parsed_data[c1], parsed_data[c2]) for c1 in customers] for c2 in customers]

        # parsed data gives all data like, {'instance_name': 'R101', 'max_vehicle_number': 25, 'vehicle_capacity': 200.0
        # 'depart': {'coordinates': {'x': 35.0, 'y': 35.0},
        # 'C_1': {'coordinates': {'x': 41.0, 'y': 49.0},
        # 'C_2': {'coordinates': {'x': 35.0, 'y': 17.0},
        # 'C_100': {'coordinates': {'x': 18.0, 'y': 18.0}, 'demand': 17.0, 'ready_time': 185.0, 'due_time': 195.0,
        # 'service_time': 10.0},
        # 'distance_matrix': [[0.0, 15.231546211727817,
        return parsed_data


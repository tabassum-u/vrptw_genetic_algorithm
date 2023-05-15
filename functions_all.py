import operator
import math
import collections

from deap import base, creator, tools
from data_file import *


def create_route_from_ind(individual, data):

    vehicle_capacity = data[VEHICLE_CAPACITY]
    depart_due_time = data[DEPART][DUE_TIME]

    route = []
    sub_route = []
    vehicle_load = 0
    time_elapsed = 0
    previous_cust_id = 0
    for customer_id in individual:

        random_generate = random.uniform(0.96, 1.04)
        demand = data[F'C_{customer_id}'][DEMAND]

        updated_vehicle_load = vehicle_load + demand
        service_time = data[F'C_{customer_id}'][SERVICE_TIME]
        distance_for_return_time = data[DISTANCE_MATRIX][customer_id][0]
        return_time_before_uncertainty = (1.5 * distance_for_return_time + 0.2199)
        return_time = return_time_before_uncertainty * random_generate
        
        cust_to_cust_distance = data[DISTANCE_MATRIX][previous_cust_id][customer_id]

        travel_time_before_uncertainty = (1.5 * cust_to_cust_distance + 0.2199)

        travel_time = travel_time_before_uncertainty * random_generate

        provisional_time = time_elapsed + travel_time + service_time + return_time

        # Validate vehicle load and elapsed time
        if (updated_vehicle_load <= vehicle_capacity) and (provisional_time <= depart_due_time):
            # Add to current sub-route
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
            time_elapsed = provisional_time - return_time

        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = [customer_id]
            vehicle_load = demand
            cust_to_cust_distance = data[DISTANCE_MATRIX][0][customer_id]
            travel_time_before_uncertainty = (1.5 * cust_to_cust_distance + 0.2199)
            travel_time = travel_time_before_uncertainty * random_generate
            time_elapsed = travel_time + service_time

        # Update last customer ID
        previous_cust_id = customer_id
    if sub_route != []:
        # Save current sub-route before return if not empty
        route.append(sub_route)

    return route


def calculate_fitness(individual, data):

    constant_1 = 1.2068
    constant_2 = 0.0000404
    constant_3 = 0.0000005
    constant_4 = 0.04466

    vehicle_capacity = data[VEHICLE_CAPACITY]
    battery_capacity = 2420  # if it is electric vehicle

    route = create_route_from_ind(individual, data)
    total_energy_consumption = 9999999
    fitness = 0
    max_vehicles_count = data[MAX_VEHICLE_NUMBER]  # 40 vehicle here

    # checking if we have enough vehicles
    if len(route) <= max_vehicles_count:
        total_energy_consumption = 0
        sub_route_distance_sum = 0

        for sub_route in route:
            sub_route_distance = 0
            previous_cust_id = 0

            capacity_after_delivery = vehicle_capacity
            each_node_battery_capacity_after_consumption = battery_capacity

            for cust_id in sub_route:
                # Calculate section distance
                distance = data[DISTANCE_MATRIX][previous_cust_id][cust_id]
                # Update sub-route distance
                sub_route_distance = sub_route_distance + distance

                # Calculate uncertain demand
                demand = data[F'C_{cust_id}'][DEMAND]

                # capacity after delivery demand
                capacity_after_delivery -= demand

                # Each node energy consumption
                energy_consumption_part_1 = constant_1 * distance
                energy_consumption_part_2 = capacity_after_delivery * ((constant_2 * distance) + constant_3)
                each_node_energy_consumption = (energy_consumption_part_1 + energy_consumption_part_2 - constant_4)

                total_energy_consumption += each_node_energy_consumption

                # Each node battery capacity
                each_node_battery_capacity_after_consumption -= each_node_energy_consumption

                # Checking if battery capacity is 20%
                # Assumption -> when battery capacity 20%, recharge somehow at that same node
                if each_node_battery_capacity_after_consumption <= 484:
                    # recharge battery to full
                    battery_capacity = 2420

                # Update last customer ID
                previous_cust_id = cust_id

            # Calculate total energy consumption

            distance_depot = data[DISTANCE_MATRIX][previous_cust_id][0]

            sub_route_distance += distance_depot

            sub_route_distance_sum += sub_route_distance

            energy_consumption_part_1 = constant_1 * distance_depot

            energy_consumption_part_2 = capacity_after_delivery * ((constant_2 * distance_depot) - constant_3)
            consumption_going_to_depot = (energy_consumption_part_1 + energy_consumption_part_2 - constant_4)

            # Update energy consumption`
            total_energy_consumption += consumption_going_to_depot

        fitness = (10000 / total_energy_consumption)

    return (fitness,)


# Double point crossover
def crossover_pmx(ind1, ind2):

    ind_len = len(ind1)
    pos_ind1 = [0]*ind_len
    pos_ind2 = [0]*ind_len

    # position indices list
    for i in range(ind_len):
        pos_ind1[ind1[i]-1] = i
        pos_ind2[ind2[i]-1] = i

    # crossover points
    locus1 = random.randint(0, int(ind_len/2))
    locus2 = random.randint(int(ind_len/2)+1, ind_len-1)

    # crossover
    for i in range(locus1, locus2):
        temp1 = ind1[i]
        temp2 = ind2[i]
        # swap
        ind1[i], ind1[pos_ind1[temp2-1]] = temp2, temp1
        ind2[i], ind2[pos_ind2[temp1-1]] = temp1, temp2
        # save updated positions
        pos_ind1[temp1-1], pos_ind1[temp2-1] = pos_ind1[temp2-1], pos_ind1[temp1-1]
        pos_ind2[temp1-1], pos_ind2[temp2-1] = pos_ind2[temp2-1], pos_ind2[temp1-1]

    return ind1, ind2


# Chose 2 indexes and swap values between them
def mutate_swap(individual):

    ind_len = len(individual)
    locus1 = random.randint(0, int(ind_len / 2))
    locus2 = random.randint(int(ind_len / 2) + 1, ind_len - 1)

    temp = individual[locus1]
    individual[locus1] = individual[locus2]
    individual[locus2] = temp

    return individual,





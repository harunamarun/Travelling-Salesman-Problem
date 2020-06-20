#!/usr/bin/env python3

import math
import sys

from common import print_solution, read_input
import itertools


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calc_total_distance(N, path, dist):
    total = 0
    for i in range(N-1):
        total += dist[path[i]][path[i+1]]
    total += dist[path[0]][path[N-1]]
    return total


def create_dist_list(cities):
    num_cities = len(cities)
    dist = [[0] * num_cities for i in range(num_cities)]
    for i in range(num_cities):
        for j in range(num_cities):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist


def nearest_neigbor(start_city, N, dist):
    current_city = start_city
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=distance_from_current_city)
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city

    return solution


# def opt_2(N, path, dist):
#     is_opt = False
#     for i in range(N):
#         for j in range(i+2, N):
#             next_i = i+1
#             next_j = (j+1) % N
#             current = dist[path[i]][path[next_i]] + \
#                 dist[path[j]][path[next_j]]
#             switch_path = dist[path[i]][path[j]] + \
#                 dist[path[next_i]][path[next_j]]
#             if current > switch_path:
#                 is_opt = True
#                 left = i+1
#                 right = j
#                 while left < right:
#                     path[left], path[right] = path[right], path[left]
#                     left += 1
#                     right -= 1
#     return is_opt

def opt_2(N, path, dist):
    is_opt = False
    for i in range(N):
        max_inproved_cost = 0
        best_j = -1
        for j in range(i+2, N):
            next_i = i+1
            next_j = (j+1) % N
            current = dist[path[i]][path[next_i]] + \
                dist[path[j]][path[next_j]]
            switch_path = dist[path[i]][path[j]] + \
                dist[path[next_i]][path[next_j]]
            improved_cost = current - switch_path
            if max_inproved_cost < improved_cost:
                max_inproved_cost = improved_cost
                best_j = j
        if best_j != -1:
            is_opt = True
            left = i+1
            right = best_j
            while left < right:
                path[left], path[right] = path[right], path[left]
                left += 1
                right -= 1
    return is_opt


def or_opt(N, path, dist, num):
    is_update = False
    for i in range(N-1):
        for j in range(1, N-num):
            if i + 1 < j or j < i - (num-1):
                current = dist[path[i]][path[i+1]] + \
                    dist[path[j-1]][path[j]] + \
                    dist[path[j+(num-1)]][path[j+num]]
                insert_path = dist[path[i]][path[j]] + \
                    dist[path[j+(num-1)]][path[i+1]] + \
                    dist[path[j-1]][path[j+num]]
                if current > insert_path:
                    is_update = True
                    if i + 1 < j:
                        path = path[:i+1] + path[j:j+num] + \
                            path[i+1:j] + path[j+num:]
                    else:
                        path = path[:j] + path[j+num:i+1] + \
                            path[j:j+num] + path[i+1:]
    return is_update, path


def graham_scan(cities, dist):
    N = len(cities)
    # find 1st point
    mini_y = 10**5
    mini_index = 0
    for i, city in enumerate(cities):
        if mini_y > city[1]:
            mini_y = city[1]
            mini_index = i
    # calucrate angle
    angle = []
    for i, city in enumerate(cities):
        if i == mini_index:
            angle.append((i, 0))
        else:
            # print("dist", dist[i][mini_index])
            # print("y", (city[1]-cities[mini_index][1]))
            theta = math.degrees(
                math.atan2(city[1]-cities[mini_index][1],
                           city[0]-cities[mini_index][0])
            )
            if theta < 0:
                theta += 360
            angle.append((i, theta))
    angle.sort(key=lambda x: x[1])
    # print(angle)
    # remove inside point
    path = [mini_index]
    angle_base_index = 0
    while True:
        base_city_index = angle[angle_base_index][0]
        base_city = cities[base_city_index]
        angle_minimum = -1
        angle_minimum_index = -1

        for angle_candidate_index in range(angle_base_index+1, N+1):
            angle_candidate_index %= N
            if angle_base_index == angle_candidate_index:
                continue
            candidate_city_index = angle[angle_candidate_index][0]
            candidate_city = cities[candidate_city_index]
            angle_candidate = math.degrees(math.atan2(
                candidate_city[1]-base_city[1], candidate_city[0]-base_city[0]))
            if angle_candidate < 0:
                angle_candidate += 360
            if angle_minimum == -1 or angle_minimum > angle_candidate:
                angle_minimum = angle_candidate
                angle_minimum_index = angle_candidate_index

        if angle_minimum_index == 0:
            break

        path.append(angle[angle_minimum_index][0])
        angle_base_index = angle_minimum_index

    return path


def cheapest_insertion(cities, path, dist):
    visited_cities = set(path)
    minimum_cost = -1
    insert_city = -1
    insert_index = -1
    for city_index, city in enumerate(cities):
        if city_index in visited_cities:
            continue
        for path_start in range(len(path)):
            path_end = (path_start + 1) % len(path)
            path_start_city_index = path[path_start]
            path_end_city_index = path[path_end]
            cost = dist[path_start_city_index][city_index] + \
                dist[city_index][path_end_city_index] - \
                dist[path_start_city_index][path_end_city_index]
            if cost < minimum_cost or minimum_cost == -1:
                minimum_cost = cost
                insert_city = city_index
                insert_index = path_start + 1
    path.insert(insert_index, insert_city)


def optimize(N, current_path, dist):
    i = 0
    while True:
        path_updated = False
        print(i)
        while opt_2(N, current_path, dist):
            print("updating" + "(" + str(i) + ")")
            path_updated = True
        while True:
            is_update, current_path = or_opt(N, current_path, dist, 5)
            if not is_update:
                break
            path_updated = True
            print("insert1 updating" + "(" + str(i) + ")")
        while True:
            is_update, current_path = or_opt(N, current_path, dist, 4)
            if not is_update:
                break
            path_updated = True
            print("insert2 updating" + "(" + str(i) + ")")
        while True:
            is_update, current_path = or_opt(N, current_path, dist, 3)
            if not is_update:
                break
            path_updated = True
            print("insert3 updating" + "(" + str(i) + ")")
        while True:
            is_update, current_path = or_opt(N, current_path, dist, 2)
            if not is_update:
                break
            path_updated = True
            print("insert4 updating" + "(" + str(i) + ")")
        while True:
            is_update, current_path = or_opt(N, current_path, dist, 1)
            if not is_update:
                break
            path_updated = True
            print("insert5 updating" + "(" + str(i) + ")")
        print("path_updated = ", path_updated)
        if not path_updated:
            break
        i += 1
    return current_path


def solve(cities):
    N = len(cities)
    print(N)
    dist = create_dist_list(cities)

    mini_total_dist = -1
    best_path = []

    # path = graham_scan(cities, dist)
    # while len(path) < N:
    #     cheapest_insertion(cities, path, dist)
    start_range = range(N)
    if(N == 512):
        start_range = range(350, 400)
    if(N == 2048):
        start_range = range(1260, 1270)
    for i in start_range:
        print("nearest_neigher start from ", i)
        print("current_best = ", mini_total_dist)
        current_path = nearest_neigbor(i, N, dist)
        # current_path = graham_scan(cities, dist)
        # while len(current_path) < N:
        #     cheapest_insertion(cities, current_path, dist)



        current_path = optimize(N, current_path, dist)

        # Update best path
        calc_current_distance = calc_total_distance(N, current_path, dist)
        if mini_total_dist < 0 or mini_total_dist > calc_current_distance:
            mini_total_dist = calc_current_distance
            best_path = current_path

    print("td:", mini_total_dist)
    # Veridation check
    uniq_cities = set(best_path)
    if(len(uniq_cities) != N):
        print(uniq_cities)
        print("ERROR")
        exit(1)
    return best_path


if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = solve(read_input(sys.argv[1]))
    print_solution(solution)

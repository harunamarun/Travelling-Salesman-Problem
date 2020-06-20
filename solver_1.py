#!/usr/bin/env python3

import math
import sys

from common import print_solution, read_input
import random

random.seed(7)


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


def nearest_neigbor(start_city, N, dist, threth=0.0):
    current_city = start_city
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        unvisited_cities_list = sorted(
            list(unvisited_cities), key=distance_from_current_city)
        if len(unvisited_cities_list) > 1:
            if(random.random() < threth):
                next_city = unvisited_cities_list[1]
            else:
                next_city = unvisited_cities_list[0]
        else:
            next_city = unvisited_cities_list[0]
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city

    return solution


def opt_2(N, _path, dist):
    path = _path[:]
    is_opt = False
    total_improved_cost = 0

    for i in range(N):
        max_improved_cost = 0
        best_j = -1
        for j in range(i+2, N):
            next_i = i+1
            next_j = (j+1) % N
            current = dist[path[i]][path[next_i]] + \
                dist[path[j]][path[next_j]]
            switch_path = dist[path[i]][path[j]] + \
                dist[path[next_i]][path[next_j]]
            improved_cost = current - switch_path
            if max_improved_cost < improved_cost:
                max_improved_cost = improved_cost
                best_j = j
        if best_j != -1:
            is_opt = True
            total_improved_cost += max_improved_cost
            left = i+1
            right = best_j
            while left < right:
                path[left], path[right] = path[right], path[left]
                left += 1
                right -= 1
    return is_opt, path, total_improved_cost


def or_opt(N, path, dist, num):
    is_update = False
    total_improved_cost = 0

    for i in range(N-1):
        max_improved_cost = 0
        best_j = -1
        for j in range(1, N-num):
            if i + 1 < j or j < i - (num - 1):
                current = dist[path[i]][path[i+1]] + \
                    dist[path[j-1]][path[j]] + \
                    dist[path[j+(num-1)]][path[j+num]]
                insert_path = dist[path[i]][path[j]] + \
                    dist[path[j+(num-1)]][path[i+1]] + \
                    dist[path[j-1]][path[j+num]]
                improved_cost = current - insert_path

                if max_improved_cost < improved_cost:
                    max_improved_cost = improved_cost
                    best_j = j

        if best_j != -1:
            is_update = True
            total_improved_cost += max_improved_cost
            if i + 1 < best_j:
                path = path[:i+1] + path[best_j:best_j+num] + \
                    path[i+1:best_j] + path[best_j+num:]
            else:
                path = path[:best_j] + path[best_j+num:i+1] + \
                    path[best_j:best_j+num] + path[i+1:]
    return is_update, path, total_improved_cost


def solve(cities):
    N = len(cities)
    print(N)
    dist = create_dist_list(cities)
    start_range = range(N)
    if(N == 512):
        start_range = range(370, 380)
    if(N == 2048):
        start_range = range(1260, 1270)

    best_path = []
    best_path_dist = -1

    for nn_start in start_range:
        print("nn_start:", nn_start)
        print("current best_path:", best_path_dist)
        current_path = nearest_neigbor(nn_start, N, dist)
        current_paths = [(calc_total_distance(
            N, current_path, dist), current_path)]

        for depth in range(100):
            print("depth", depth)
            next_current_paths = []
            distance_count = {}

            for current_path_dist, current_path in current_paths:
                is_update, opt2_path, improved_cost = opt_2(
                    N, current_path, dist)
                if is_update:
                    distance = current_path_dist - improved_cost
                    count = distance_count.get(distance, 0)
                    if count < 2:
                        next_current_paths.append((distance, opt2_path))
                        distance_count[distance] = count + 1

                for opt_num in range(1, 6):
                    is_update, or_opt_path, improved_cost = or_opt(
                        N, current_path, dist, opt_num)
                    if is_update:
                        distance = current_path_dist - improved_cost
                        count = distance_count.get(distance, 0)
                        if count < 2:
                            next_current_paths.append((distance, or_opt_path))
                            distance_count[distance] = count + 1

            if not next_current_paths:
                break

            next_current_paths.sort()
            current_best_path_dist, current_best_path = next_current_paths[0]

            if best_path_dist == -1 or best_path_dist > current_best_path_dist:
                best_path_dist = current_best_path_dist
                best_path = current_best_path

            if len(next_current_paths) > 100:
                next_current_paths = next_current_paths[:100]
            current_paths = next_current_paths

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

#!/usr/bin/env python3

import sys
import math
import os
import multiprocessing
from common import print_solution, read_input
from convex_hull import graham_scan, cheapest_insertion


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calc_total_distance(path, dist):
    total_dist = 0
    for i in range(len(path)-1):
        total_dist += dist[path[i]][path[i+1]]
    total_dist += dist[path[-1]][path[0]]
    return total_dist


def create_dist_list(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist


def two_opt(path, dist):
    N = len(dist)
    is_update_2opt = False
    max_improved_cost = 0

    best_i = -1
    best_j = -1
    for i in range(N):
        next_i = (i+1) % N
        for j in range(i+2, N):
            next_j = (j+1) % N

            before_change_cost = dist[path[i]][path[next_i]] + \
                dist[path[j]][path[next_j]]
            after_change_cost = dist[path[i]][path[j]] + \
                dist[path[next_j]][path[next_i]]
            improved_cost = before_change_cost - after_change_cost

            if max_improved_cost < improved_cost:
                max_improved_cost = improved_cost
                best_j = j
                best_i = i

    if max_improved_cost != 0:
        is_update_2opt = True
        left = best_i + 1
        right = best_j
        while left < right:
            path[left], path[right] = path[right], path[left]
            left += 1
            right -= 1

    return is_update_2opt, path, max_improved_cost


def or_opt(path, dist, num):
    N = len(dist)
    is_update_oropt = False
    max_improved_cost = 0

    best_i = -1
    best_j = -1
    if N - num > 1:
        for i in range(N-1):
            for j in range(1, N-num):
                if i + 1 < j or j < i - (num - 1):
                    before_change_cost = dist[path[i]][path[i+1]] + \
                        dist[path[j-1]][path[j]] + \
                        dist[path[j+(num-1)]][path[j+num]]
                    after_change_cost = dist[path[i]][path[j]] + \
                        dist[path[j+(num-1)]][path[i+1]] + \
                        dist[path[j-1]][path[j+num]]
                    improved_cost = before_change_cost - after_change_cost

                    if max_improved_cost < improved_cost:
                        max_improved_cost = improved_cost
                        best_j = j
                        best_i = i

    if max_improved_cost != 0:
        is_update_oropt = True
        if best_i + 1 < best_j:
            path = path[:best_i+1] + path[best_j:best_j+num] + \
                path[best_i+1:best_j] + path[best_j+num:]
        else:
            path = path[:best_j] + path[best_j+num:best_i+1] + \
                path[best_j:best_j+num] + path[best_i+1:]
    return is_update_oropt, path, max_improved_cost


def worker_nn_start(dist, cities, task_queue, result_queue):
    best_path_of_worker = []
    best_dist_of_worker = -1

    while True:
        try:
            start_city = task_queue.get(timeout=1)
        except Exception:
            if best_dist_of_worker != -1:
                result_queue.put((best_dist_of_worker, best_path_of_worker))
            return
        print("[" + str(os.getpid()) + "] nn_start:", start_city)
        print("[" + str(os.getpid()) + "] best_dist_of_worker:",
              best_dist_of_worker)

        graham_path = graham_scan(cities, dist)
        while len(graham_path) < len(dist):
            cheapest_insertion(cities, graham_path, dist)
        current_dist = calc_total_distance(graham_path, dist)
        current_path = graham_path

        count_update_false = 0
        while True:
            # 2-opt
            while True:
                is_update_2, update_current_path, improved_cost = two_opt(
                    current_path, dist)
                current_dist -= improved_cost
                current_path = update_current_path
                if not is_update_2:
                    count_update_false -= 1
                    break
                count_update_false = 0

            # or-opt
            while True:
                for opt_num in range(1, 20):
                    is_update_or, update_current_path, improved_cost = or_opt(
                        current_path, dist, opt_num)
                    current_dist -= improved_cost
                    current_path = update_current_path

                if not is_update_or:
                    count_update_false -= 1
                    break
                count_update_false = 0

            if count_update_false < -3:
                break

        if best_dist_of_worker > current_dist or best_dist_of_worker == -1:
            best_dist_of_worker = current_dist
            best_path_of_worker = current_path


def solve(cities):
    N = len(cities)  # number of cities
    dist_list = create_dist_list(cities)
    print("N="+str(N))

    # create queue for multi processing
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    task_queue.put(1)

    process_list = []
    # start multi processing
    for idx in range(1):
        process_list.append(multiprocessing.Process(
            target=worker_nn_start,
            args=(dist_list, cities, task_queue, result_queue)))
        process_list[idx].start()
    # end multi processing
    for idx in range(1):
        process_list[idx].join()

    best_path = []
    best_dist = -1
    while not result_queue.empty():
        best_dist_of_worker, best_path_of_worker = result_queue.get()
        if best_dist > best_dist_of_worker or best_dist == -1:
            best_dist = best_dist_of_worker
            best_path = best_path_of_worker

    print("N:::"+str(N), " min distance:::"+str(best_dist))

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

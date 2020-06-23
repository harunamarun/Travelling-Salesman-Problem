import math
import sys
import os

from common import print_solution, read_input
import random
import multiprocessing

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


def nearest_neighbor(start_city, N, dist, threth=0.0):
    current_city = start_city
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        unvisited_cities_list = sorted(
            list(unvisited_cities), key=distance_from_current_city)
        if threth != 0 and len(unvisited_cities_list) > 1:
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


def work_nn_start(dist, task_queue, result_queue):
    N = len(dist)
    best_path = []
    best_path_dist = -1

    random.seed(7)
    # This is a parameter which is threth range
    # I changed this parameter for each N becouse of computational complexity.
    if N < 200:
        threth_range = [i / 10. for i in range(0, 10, 1)]
    elif N < 600:
        threth_range = [i / 10. for i in range(0, 2, 1)]
    else:
        threth_range = [0]

    # This is a parameter which is beam search width.
    # I changed this parameter for each N becouse of computational complexity.
    if N < 100:
        beam_width = 5000
    elif N < 200:
        beam_width = 1000
    elif N < 1000:
        beam_width = 300
    else:
        beam_width = 5

    while True:
        try:
            nn_start = task_queue.get(timeout=1)
        except Exception:
            if best_path_dist != -1:
                result_queue.put((best_path_dist, best_path))
                return
            return
        print("[" + str(os.getpid()) + "] nn_start:", nn_start)
        print("[" + str(os.getpid()) + "] current best_path:", best_path_dist)
        for threth in threth_range:
            current_path = nearest_neighbor(nn_start, N, dist, threth)
            current_paths = [(calc_total_distance(
                N, current_path, dist), current_path)]

            for depth in range(100):
                print("[" + str(os.getpid()) + "] nn_start: ",
                      nn_start, " depth:", depth)
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
                                next_current_paths.append(
                                    (distance, or_opt_path))
                                distance_count[distance] = count + 1

                if not next_current_paths:
                    break

                next_current_paths.sort()
                current_best_path_dist, current_best_path \
                    = next_current_paths[0]

                if best_path_dist == -1 or \
                        best_path_dist > current_best_path_dist:
                    best_path_dist = current_best_path_dist
                    best_path = current_best_path

                if len(next_current_paths) > beam_width:
                    next_current_paths = next_current_paths[:beam_width]
                current_paths = next_current_paths


def solve(cities):
    N = len(cities)
    print(N)
    dist = create_dist_list(cities)

    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    for nn_start in range(0, N):
        task_queue.put(nn_start)

    process_list = []
    # this range is how many cpu you use
    num_cpu = multiprocessing.cpu_count()
    for index in range(num_cpu):
        process_list.append(multiprocessing.Process(
            target=work_nn_start, args=(dist, task_queue, result_queue)))
        process_list[index].start()

    for index in range(num_cpu):
        process_list[index].join()

    best_path = []
    best_path_dist = -1
    while not result_queue.empty():
        path_dist, path = result_queue.get()
        if best_path_dist > path_dist or best_path_dist == -1:
            best_path_dist = path_dist
            best_path = path
    print("N:"+str(N)+"best_dist"+str(best_path_dist))
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

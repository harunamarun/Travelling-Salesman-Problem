import math


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
            theta = math.degrees(
                math.atan2(city[1]-cities[mini_index][1],
                           city[0]-cities[mini_index][0])
            )
            if theta < 0:
                theta += 360
            angle.append((i, theta))
    angle.sort(key=lambda x: x[1])

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
                candidate_city[1]-base_city[1],
                candidate_city[0]-base_city[0]))
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
    for city_index in range(len(cities)):
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

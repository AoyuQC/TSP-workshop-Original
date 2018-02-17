from collections import defaultdict
from math import asin, cos, radians, sin, sqrt
from models import City
from random import sample


def haversine_distance(cityA, cityB):
    coords = (*coordinates[cityA], *coordinates[cityB])
    # we convert from decimal degree to radians
    lat_cityA, lon_cityA, lat_cityB, lon_cityB = map(radians, coords)
    delta_lon = lon_cityB - lon_cityA
    delta_lat = lat_cityB - lat_cityA
    # haversine function
    hav = lambda t: sin(t/2)**2
    a = hav(delta_lat) + cos(lat_cityA) * cos(lat_cityB) * hav(delta_lon)
    c = 2 * asin(sqrt(a))
    # approximate radius of the Earth: 6371 km
    return c*6371


def compute_distances(cities):
    distances = defaultdict(dict)
    for cityA in cities:
        for cityB in cities:
            if cityB not in distances[cityA]:
                distance = haversine_distance(cityA, cityB)
                distances[cityA][cityB] = distance
                distances[cityB][cityA] = distance
    return distances


cities = [c.id for c in City.query.all()]
coordinates = {c.id: (c.latitude, c.longitude) for c in City.query.all()}
distances = compute_distances(cities)


class BaseAlgorithm():

    def __init__(self):
        self.size = len(cities)

    # add node k between node i and node j
    def add(self, i, j, k):
        return distances[i][k] + distances[k][j] - distances[i][j]

    def generate_solution(self):
        return sample(cities, len(cities))

    # computes the total geographical length of a solution
    def compute_length(self, solution):
        total_length = 0
        for i in range(len(solution)):
            length = distances[solution[i]][solution[(i+1) % len(solution)]]
            total_length += length
        return total_length

    def format_solution(self, solution):
        solution = solution + [solution[0]]
        return [coordinates[city] for city in solution]

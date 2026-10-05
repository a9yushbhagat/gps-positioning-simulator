import check
import math
import random
import matplotlib.pyplot as plt


class Point:
    '''
    Fields: x (Float), y (Float)
    '''

    def __init__(self, p1, p2):
        '''
        Constructor: Creates a Point object by calling
        Point(p1, p2).

        Effects: Mutates self

        __init__: Point Float Float -> None
        '''
        self.x = p1
        self.y = p2

    def __repr__(self):
        '''
        Returns a string representation of self.

        __repr__: Point -> Str
        '''
        s = "Point({0.x}, {0.y})"
        return s.format(self)
    
    def __eq__(self, other):
        '''
        Returns True if self and other are Points with the same
        x and y, and False otherwise.

        __eq__: Point Any -> Bool
        '''
        return isinstance(other, Point) and \
               self.x == other.x and \
               self.y == other.y
    

def distance(p, q):
    '''
    Returns the Euclidean distance between Points p and q.

    distance: Point Point -> Float

    Examples:
       distance(Point(0, 0), Point(3, 4)) => 5.0
       distance(Point(1, 1), Point(1, 1)) => 0.0
    '''
    a = (p.x - q.x) ** 2
    b = (p.y - q.y) ** 2
    d = math.sqrt(a + b)
    return d


def generate_distances(target, stations):
    '''
    Returns a list of the exact distances from target to each
    Point in stations, in the same order as stations.

    generate_distances: Point (listof Point) -> (listof Float)

    Examples:
       If stations = [Point(0,0), Point(10,0), Point(0,10)] and
       target = Point(3, 4), then
       generate_distances(target, stations)
          => [5.0, 8.06225, 6.70820]
    '''
    L = list(map (lambda x: distance(x, target), stations))
    return L


def estimate_position(stations, distances):
    '''
    Returns the estimated Point position of a target, found by
    subtracting the first circle equation from the other two to
    get a 2x2 linear system, then solving it with Cramer's rule.

    estimate_position: (listof Point) (listof Float) -> Point
    Requires: len(stations) == 3
              len(distances) == 3
              the stations are not collinear

    Examples:
       If stations = [Point(0,0), Point(10,0), Point(0,10)] and
       distances = [5.0, 8.06225, 6.70820], then
       estimate_position(stations, distances) => Point(3.0, 4.0)
    '''
    p1 = stations[0]
    p2 = stations[1]
    p3 = stations[2]
    d1 = distances[0]
    d2 = distances[1]
    d3 = distances[2]
    A = 2 * (p2.x - p1.x)
    B = 2 * (p2.y - p1.y)
    i = (p2.x ** 2) - (p1.x ** 2) + (p2.y ** 2) - (p1.y ** 2)
    E = (d1 ** 2) - (d2 ** 2) + i
    C = 2 * (p3.x - p1.x)
    D = 2 * (p3.y - p1.y)
    j = (p3.x ** 2) - (p1.x ** 2) + (p3.y ** 2) - (p1.y ** 2)
    F = (d1 ** 2) - (d3 ** 2) + j
    det = (A * D) - (B * C)
    x = ((E * D) - (B * F)) / det
    y = ((A * F) - (E * C)) / det
    return Point(x, y)


def position_error(true_point, estimate):
    '''
    Returns the distance between the true position true_point and
    the estimated position estimate.

    position_error: Point Point -> Float

    Examples:
       position_error(Point(3, 4), Point(3, 4)) => 0.0
       position_error(Point(0, 0), Point(3, 4)) => 5.0
    '''
    return distance(true_point, estimate)


def add_noise(distances, amount):
    '''
    Returns a new list where each distance in distances has a
    random value between -amount and amount added to it.

    add_noise: (listof Float) Float -> (listof Float)
    Requires: amount >= 0

    Examples:
       add_noise([5.0, 8.0, 6.7], 0.1) => [5.037, 7.981, 6.712]
       (the values differ on each call because they are random)

       add_noise([5.0], 0) => [5.0]
    '''
    M = list(map (lambda x: x + random.uniform(-amount, amount), distances))
    return M


def run_trial(target, stations, noises):
    '''
    Returns the position error of one simulated trial, in which
    exact distances from target to stations are generated, noise
    of size noises is added, and the position is estimated from
    the noisy distances.

    run_trial: Point (listof Point) Float -> Float
    Requires: len(stations) == 3
              noises >= 0

    Examples:
       If target = Point(3, 4) and
       stations = [Point(0,0), Point(10,0), Point(0,10)], then
       run_trial(target, stations, 0) => 0.0

       run_trial(target, stations, 0.1) => 0.05
       (the value differs on each call because the noise is random)
    '''
    i = generate_distances(target, stations)
    j = add_noise(i, noises)
    k = estimate_position(stations, j)
    return position_error(target, k)


def average_error(target, stations, noise, trials):
    '''
    Returns the average position error over the given number of
    trials, each run with noise of size noise.

    average_error: Point (listof Point) Float Nat -> Float
    Requires: len(stations) == 3
              noise >= 0
              trials > 0

    Examples:
       If target = Point(3, 4) and
       stations = [Point(0,0), Point(10,0), Point(0,10)], then
       average_error(target, stations, 0, 10) => 0.0

       average_error(target, stations, 0.1, 100) => 0.08
       (the value differs on each call because the noise is random)
    '''
    acc = 0
    p = 0
    while p < trials:
        acc += run_trial(target, stations, noise)
        p += 1
    return acc / trials


def plot_scene(stations, distances, true_point, estimate):
    '''
    Returns None.

    Effects: Displays a plot showing each station and a circle
             around it of radius equal to its measured distance,
             the true position, the estimated position, and a
             dashed line between them

    plot_scene: (listof Point) (listof Float) Point Point -> None
    Requires: len(stations) == len(distances)

    Examples:
       plot_scene([Point(0,0), Point(10,0), Point(0,10)],
                  [5.0, 8.06, 6.71], Point(3, 4),
                  Point(3.05, 3.98)) => None
       and displays the plot
    '''
    fig, ax = plt.subplots()
    for i in range(len(stations)):
        ax.plot(stations[i].x, stations[i].y, "bo")
        ax.annotate("S" + str(i + 1),
                    (stations[i].x, stations[i].y))
        circle = plt.Circle((stations[i].x, stations[i].y),
                            distances[i], fill=False, color="blue",
                            linewidth=0.5)
        ax.add_patch(circle)
    ax.plot(true_point.x, true_point.y, "go", label="True position")
    ax.plot(estimate.x, estimate.y, "rx", label="Estimated position")
    ax.plot([true_point.x, estimate.x], [true_point.y, estimate.y],
            "r--", linewidth=0.8)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()
    plt.title("GPS Positioning Simulator")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


## Tests:
s = [Point(0, 0), Point(10, 0), Point(0, 10)]
t = Point(3, 4)

check.expect("T1: point eq", Point(3, 4) == Point(3, 4), True)
check.within("T2: distance", distance(Point(0, 0), Point(3, 4)), 5.0, 0.001)
check.within("T3: generate first", generate_distances(t, s)[0], 5.0, 0.001)
check.within("T4: generate second", generate_distances(t, s)[1], 8.0623, 0.001)
check.within("T5: estimate x",
             estimate_position(s, generate_distances(t, s)).x, 3.0, 0.001)
check.within("T6: estimate y",
             estimate_position(s, generate_distances(t, s)).y, 4.0, 0.001)
check.within("T7: zero error", position_error(t, t), 0.0, 0.001)
check.within("T8: no noise trial", run_trial(t, s, 0), 0.0, 0.001)
check.within("T9: no noise average", average_error(t, s, 0, 10), 0.0, 0.001)

stations = [Point(0, 0), Point(10, 0), Point(0, 10)]
target = Point(3, 4)
exact = generate_distances(target, stations)
noisy = add_noise(exact, 0.1)
guess = estimate_position(stations, noisy)
plot_scene(stations, noisy, target, guess)
import random

class Orientation():
    def __init__(self, direction):
        self.direction = direction

    def get_output(self):
        random.randint(0, 1)

    def set_output(self, output: []):
        self.output = output


def create_direction():

    N = Orientation('N')
    NNE = Orientation('NNE')
    NE = Orientation('NE')
    ENE = Orientation('ENE')
    E = Orientation('E')
    ESE = Orientation('ESE')
    SE = Orientation('SE')
    SSE = Orientation('SSE')
    S = Orientation('S')
    SSW = Orientation('SSW')
    SW = Orientation('SW')
    WSW = Orientation('WSW')
    W = Orientation('W')
    WNW = Orientation('WNW')
    NW = Orientation('NW')
    NNW = Orientation('NNW')
    N.set_output([NNE, NNW])
    NNE.set_output([N, NE])
    NE.set_output([NNE, ENE])
    ENE.set_output([NE, E])
    E.set_output([ENE, ESE])
    ESE.set_output([E, SE])
    SE.set_output([ESE, SSE])
    SSE.set_output([SE, S])
    S.set_output([SSE, SSW])
    SSW.set_output([S, SW])
    SW.set_output([SSW, WSW])
    WSW.set_output([SW, W])
    W.set_output([WSW, WNW])
    WNW.set_output([W, NW])
    NW.set_output([WNW, NNW])
    NNW.set_output([NW, E])


def create_track():
    first_point = (73, 53)

    lines = []

    tmp_point = first_point

    for i in range(10):
        end_point = (tmp_point[0] + 10, tmp_point[1])
        lines.append([tmp_point, end_point])
        tmp_point = end_point

    return lines



if __name__ == '__main__':


    print(f'Lines: {create_track()}')
    for i in range(10):
        print(f'Random number: {random.randint(0,2)}')

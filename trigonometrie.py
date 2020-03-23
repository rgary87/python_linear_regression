from shapely.geometry import Point


def segment_intersect(line1, line2):

    s1_x = line1[1][0] - line1[0][0]
    s1_y = line1[1][1] - line1[0][1]
    s2_x = line2[1][0] - line2[0][0]
    s2_y = line2[1][1] - line2[0][1]


    s = (-s1_y * (line1[0][0] - line2[0][0]) + s1_x * (line1[0][1] - line2[0][1])) / (-s2_x * s1_y + s1_x * s2_y)
    t = (s2_x * (line1[0][1] - line2[0][1]) - s2_y * (line1[0][0] - line2[0][0])) / (-s2_x * s1_y + s1_x * s2_y)

    if 0 <= s <= 1 and 0 <= t <= 1:
        # Collision detected
        i_x = line1[0][0] + (t * s1_x)
        i_y = line1[0][1] + (t * s1_y)
        # print('INTERSECTED !')
        return i_x, i_y

    return None # No collision


def get_point_in_zone_x(polygons, position):
    p = Point(position[0], position[1])
    for i in range(len(polygons)):
        if polygons[i].contains(p):
            return i
    return None

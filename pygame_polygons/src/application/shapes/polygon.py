import math
from typing import Union
from pygame.math import Vector2

def draw_regular_polygon(vertex_count: int, radius: int, position: tuple) -> list[Vector2]:
    """@credit: https://stackoverflow.com/a/57638991/13903942 """
    n, r = vertex_count, radius
    x, y = position
    return [
        Vector2(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]

def get_polygon_centroid(polygon: list[Vector2]) -> Vector2:
    """Finds the centroid /  barycenter of a polygon

    :param polygon: list[Vector2]
    :return: Vector2 x,y coordinates of the centroid/ barycenter of the given polygon
    """
    # finds the center of a polygon
    vertices_x: list = []
    vertices_y: list = []
    for vertex in polygon:
        vertices_x.append(vertex[0])
        vertices_y.append(vertex[1])
    vertices_count: int = len(polygon)
    centroid = Vector2(sum(vertices_x) / vertices_count,
                       sum(vertices_y) / vertices_count)  # finds the center of a polygon
    return centroid


def polygon_move(polygon: list[Vector2], move_to: Vector2) -> None:
    """Move a polygon following its x, y coordinates

    :param polygon:
    :param move_to:
    :return:
    """
    centroid = get_polygon_centroid(polygon)  # get the polygon centroid

    pos_x, pos_y = move_to
    for vertex_index, vertex in enumerate(polygon):
        move_x = pos_x - centroid[0]
        move_y = pos_y - centroid[1]
        polygon[vertex_index][0] += move_x
        polygon[vertex_index][1] += move_y


def polygon_rotate(polygon: list[Vector2], centroid: Vector2, angle: Union[float, int]) -> list[Vector2]:
    """Rotates a polygon to its centroid as its origin by the given angle
    Positve angle: anti-clockwise
    Negative angle: clockwise

    :param polygon: list[Vector2]
    :param centroid: Vector2 Center of the polygon
    :param angle: float|int   Angle
    :return:
    """
    return [
        Vector2(
            centroid[0] + ((vertex[0] - centroid[0]) * math.cos(angle)) - ((vertex[1] - centroid[1]) * math.sin(angle)),
            centroid[1] + ((vertex[0] - centroid[0]) * math.sin(angle)) + ((vertex[1] - centroid[1]) * math.cos(angle))
        )
        for vertex_index, vertex in enumerate(polygon)
    ]

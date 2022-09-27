from math import pi, cos, sin
import pygame
from pygame.math import Vector2

from ..shapes import get_polygon_centroid, polygon_rotate, polygon_move, draw_regular_polygon


class ShapeController:

    def __init__(self):
        ...

    @staticmethod
    def make_polygon(vertex_count: int, radius: int, position: tuple):
        """Creates a polygon defined by its vertex count, radius (size) and x,y coordinates

        :param vertex_count: int min 3. Total amount of the polygon vertex
        :param radius: int the size of the polygon
        :param position: tuple x,y coordinates
        :return:
        """
        if vertex_count < 3:
            vertex_count = 3
        return draw_regular_polygon(vertex_count, radius, position)

    @staticmethod
    def shape_get_center(polygon: list[Vector2]) -> Vector2:
        return get_polygon_centroid(polygon)  # get the polygon centroid

    @staticmethod
    def shape_centroid_is_near_mouse_pointer(mouse: tuple, centroid: Vector2, margin: int) -> bool:
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        vertex_x_diff = abs(mouse_x - centroid[0])
        vertex_y_diff = abs(mouse_y - centroid[1])
        return vertex_y_diff < margin and vertex_x_diff < margin

    @staticmethod
    def shape_vertex_is_near_mouse_pointer(mouse: tuple, vertex: Vector2, margin: int) -> bool:
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        vertex_x = vertex[0]
        vertex_y = vertex[1]
        # we check how distance is the vertex
        vertex_x_diff = abs(mouse_x - vertex_x)
        vertex_y_diff = abs(mouse_y - vertex_y)
        return vertex_y_diff < margin and vertex_x_diff < margin


    @staticmethod
    def move_polygon(polygons: list[list[Vector2]], current_polygon: int, mouse_position: tuple[int, int]):
        """Move a polygon setting its center to the mouse position

        :param polygons: list[list[Vector2]] List of polygon
        :param current_polygon: int the current polygon to get
        :param mouse_position: tuple[int, int]  x, y coordinates of the mouse position in the screen
        :return:
        """
        try:
            polygon = polygons[current_polygon]  # get the polygon
        except IndexError:
            return
        polygon_move(polygon, Vector2(mouse_position[0], mouse_position[1]))

    @staticmethod
    def rotate_polygon(polygons: list[list[Vector2]], current_polygon: int, direction: str) -> None:
        """Rotates a Polygon clockwise - counter clock-wise

        :param polygons: list[list[Vector2]] List of polygon
        :param current_polygon: int the current polygon to get
        :param direction: str either clockwise or counter_clockwise
        :return: None
        """
        if not isinstance(current_polygon, int):
            return
        # angle works better (smoother rotation ) when is a '2' of any decimal place. So 2 works better then 3,4,15 ...
        # but also 0.2 works or 20 The smaller the more fine grained the rotation so 0.2 is a pretty good start
        # but for even better precision set the value ot 0.02
        angle = .2

        if direction == 'clockwise':
            angle = -angle

        try:
            polygon = polygons[current_polygon]  # get the polygon
        except IndexError:
            return

        centroid = get_polygon_centroid(polygon)  # get the polygon centroid
        polygon_rotated = polygon_rotate(polygon, centroid, angle)  # rotate polygon
        polygons[current_polygon] = polygon_rotated

    @staticmethod
    def draw_stars(screen: pygame.Surface, stars: list[list[Vector2]]) -> None:
        """Stars are drawn and rotating counter-clockwise

        :param screen: pygame.Surface Screen were stars needs to be drawn
        :param stars: list[list[Vector2]] list of the stars Vector Coordinates, updated in place
        :return: None
        """
        if not stars:
            return
            # make the star roating continously making double adges
        for i, star in enumerate(stars):
            centroid = get_polygon_centroid(star)
            pygame.draw.circle(screen, (79, 0, 153),  # draw red dot around vertex
                               Vector2(centroid[0], centroid[1]), 5)
            pygame.draw.polygon(screen, pygame.Color("pink"), star, width=2)
            star_rotated = polygon_rotate(star, centroid, -45)
            stars[i] = star_rotated

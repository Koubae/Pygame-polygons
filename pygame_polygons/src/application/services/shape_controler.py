from math import pi, cos, sin
import pygame
from pygame.math import Vector2

from ..shapes import Polygon
# from ...app import App

class ShapeController:

    def __init__(self):
        ...

    @staticmethod
    def make_polygon(app, vertex_count: int, radius: int, position: tuple) -> Polygon:
        """Creates a polygon defined by its vertex count, radius (size) and x,y coordinates

        :param screen: pygame.Surface
        :param vertex_count: int min 3. Total amount of the polygon vertex
        :param radius: int the size of the polygon
        :param position: tuple x,y coordinates
        :return: Polygon
        """
        if vertex_count < 3:
            vertex_count = 3

        polygon = Polygon(app, vertex_count, radius, Vector2(position[0], position[1]))

        return polygon

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
    def move_polygon(polygons: list[Polygon], current_polygon: int, mouse_position: tuple[int, int]) -> None:
        """Move a polygon setting its center to the mouse position

        :param polygons: list[list[Vector2]] List of polygon
        :param current_polygon: int the current polygon to get
        :param mouse_position: tuple[int, int]  x, y coordinates of the mouse position in the screen
        :return:
        """
        try:
            polygon: Polygon = polygons[current_polygon]  # get the polygon
        except IndexError:
            return
        polygon.move(Vector2(mouse_position[0], mouse_position[1]))

    @staticmethod
    def polygon_move_vertex(polygons: list[Polygon], indexes: tuple[int, int], mouse_position: tuple[int, int]) -> None:
        try:
            polygon: Polygon = polygons[indexes[0]]  # get the polygon
        except IndexError:
            return
        polygon.move_vertix(indexes[1],  Vector2(mouse_position[0], mouse_position[1]))

    @staticmethod
    def rotate_polygon(polygons: list[Polygon], current_polygon: int, direction: str) -> None:
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
            polygon: Polygon = polygons[current_polygon]  # get the polygon
        except IndexError:
            return
        vertices: list[Vector2] = polygon.vertices
        centroid = Polygon.get_polygon_centroid(vertices)  # get the polygon centroid
        polygon_rotated = Polygon.polygon_rotate(vertices, centroid, angle)  # rotate polygon
        polygon.update_vertices_positions(polygon_rotated)
        polygon.centroid = polygon.vertices  # reset the polygon centroid

    @staticmethod
    def draw_stars(screen: pygame.Surface, stars: list[Polygon]) -> None:
        """Stars are drawn and rotating counter-clockwise

        :param screen: pygame.Surface Screen were stars needs to be drawn
        :param stars: list[list[Vector2]] list of the stars Vector Coordinates, updated in place
        :return: None
        """
        if not stars:
            return
            # make the star roating continously making double adges
        for i, star in enumerate(stars):
            vertices: list[Vector2] = star.vertices

            centroid = Polygon.get_polygon_centroid(vertices)
            pygame.draw.circle(screen, (79, 0, 153),  # draw red dot around vertex
                               Vector2(centroid[0], centroid[1]), 5)
            pygame.draw.polygon(screen, pygame.Color("pink"), vertices, width=2)
            star_rotated = Polygon.polygon_rotate(vertices, centroid, -45)
            star.update_vertices_positions(star_rotated)

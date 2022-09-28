import math
from typing import Union
import pygame
from pygame.math import Vector2
import random

class Polygon:
    BORDER_WIDTH: int = 2
    DOT_CIRCLE_RADIUS: int = 5

    TEXT_COLOR: tuple[int, int, int] = (255, 255, 255)
    VERTEX_DOT_COLOR: tuple[int, int, int] = (255, 0, 0)
    CENTROID_DOT_COLOR: tuple[int, int, int] = (79, 0, 153)
    # TODO: Check https://superuser.com/questions/361297/what-colour-is-the-dark-green-on-old-fashioned-green-screen-computer-displays
    TERMINAL_COLORS: dict[str, tuple[int, int, int]] = {
        'amber': (255, 176, 0),
        'amber_l': (255, 204, 0),

        'green_1': (51, 255, 0),
        'apple': (51, 255, 51),
        'green_2': (0, 255, 51),

        'apple_llc': (102, 255, 102),
        'green_3': (0, 255, 102)
    }
    DEFAULT_TERMINAL_COLORS: tuple[str] = tuple(TERMINAL_COLORS.keys())

    def __init__(self, app, vertex_count: int, radius: int, position: Vector2):
        self.app = app
        self.screen: pygame.Surface = self.app.background
        self.vertex_count: int = 3
        self.radius: int
        self.position_initial: Vector2

        self._vertices: list[Vector2] = Polygon.draw_regular_polygon(vertex_count, radius, position)
        self._centroid: Vector2 = Polygon.get_polygon_centroid(self.vertices)

        self.border_color: tuple = self.TERMINAL_COLORS[self.DEFAULT_TERMINAL_COLORS[random.randint(0, len(self.DEFAULT_TERMINAL_COLORS) - 1)]]
        self.background_color: tuple = self.TERMINAL_COLORS[self.DEFAULT_TERMINAL_COLORS[random.randint(0, len(self.DEFAULT_TERMINAL_COLORS) - 1)]]

    @property
    def vertices(self) -> list[Vector2]:
        """The vertices property."""
        return self._vertices

    @vertices.setter
    def vertices(self, value: list[Vector2]) -> None:
        """Sets the vertices"""
        self._vertices = value

    @property
    def centroid(self) -> Vector2:
        """The radius property."""
        return self._centroid

    @centroid.setter
    def centroid(self, _: None = None) -> None:
        """Sets the Centroid"""
        self._centroid = Polygon.get_polygon_centroid(self.vertices)

    def draw(self):
        """ Draws a polygon and its center dot (centroid / barycenter)

        :return:
        """
        pygame.draw.circle(
            self.screen,
            self.CENTROID_DOT_COLOR,
            Vector2(self.centroid.x, self.centroid.y),
            self.DOT_CIRCLE_RADIUS
        )  # draw dot around center
        self.write_vertex_coords(self.centroid)
        pygame.draw.polygon(self.screen, self.border_color, self.vertices, width=self.BORDER_WIDTH)

    def vertex_focus(self, vertex_index: int) -> None:
        """Focus a Vertex, make it in a red dot

        :param vertex_index:
        :return:
        """
        try:
            vertex = self.vertices[vertex_index]
        except IndexError as err:
            print(str(err))
            return
        pygame.draw.circle(
            self.screen,
            self.VERTEX_DOT_COLOR,
            Vector2(vertex[0], vertex[1]),
            self.DOT_CIRCLE_RADIUS
        )  # draw red dot around vertex
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

    def write_vertex_coords(self, vertex: Vector2):
        """Write the coordinates of a particualr vertex"""
        # write vertex coordinates into the vertex
        about_text1 = f"{round(vertex.x, 2)}-{round(vertex.y, 2)}"
        font_img = self.app.font_small.render(about_text1, True, (255, 255, 255))
        self.screen.blit(font_img, Vector2(vertex.x + 5, vertex.y + 5))

    def update_vertices_positions(self, vertices: list[Vector2]):
        """Update the polygon's Vertices position

        :param vertices: list[Vector2]
        :return:
        """
        self.vertices = vertices

    # ----------------
    # Geometry methods
    # ----------------

    @staticmethod
    def draw_regular_polygon(vertex_count: int, radius: int, position: Vector2) -> list[Vector2]:
        """@credit: https://stackoverflow.com/a/57638991/13903942 """
        n, r = vertex_count, radius
        x, y = position
        return [
            Vector2(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n))
            for i in range(n)
        ]

    @staticmethod
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

    def move(self, move_to: Vector2) -> None:
        """Move a polygon following its x, y coordinates

        :param vertices:
        :param move_to:
        :return:
        """
        vertices: list[Vector2] = self._vertices
        centroid = Polygon.get_polygon_centroid(vertices)  # get the polygon centroid

        pos_x, pos_y = move_to
        for vertex_index, vertex in enumerate(vertices):
            move_x = pos_x - centroid[0]
            move_y = pos_y - centroid[1]
            vertices[vertex_index][0] += move_x
            vertices[vertex_index][1] += move_y

        self.centroid = vertices # reset the polygon centroid
    def move_vertix(self, vertex_index: int, position: Vector2) -> None:
        try:
            _: Vector2 = self._vertices[vertex_index]  # test check that the vertex exits
        except IndexError:
            return
        self._vertices[vertex_index] = position
        self.centroid = self._vertices  # reset the polygon centroid

    @staticmethod
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
                centroid[0] + ((vertex[0] - centroid[0]) * math.cos(angle)) - (
                        (vertex[1] - centroid[1]) * math.sin(angle)),
                centroid[1] + ((vertex[0] - centroid[0]) * math.sin(angle)) + (
                        (vertex[1] - centroid[1]) * math.cos(angle))
            )
            for vertex_index, vertex in enumerate(polygon)
        ]

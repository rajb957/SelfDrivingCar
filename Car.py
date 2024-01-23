import pygame
import math
import numpy as np


class Car:
    def __init__(self):
        self.position = np.array([150.0, 210.0])
        self.width = 20
        self.height = 40
        self.dimensions = np.array([20.0, 40.0])
        self.vel = 5
        self.angle = 180
        self.points = np.array([[-self.width / 2, self.height / 2],
                                [self.width / 2, self.height / 2],
                                [self.width / 2, -self.height / 2],
                                [-self.width / 2, -self.height / 2]])

        self.rotated_points = np.copy(self.points)

    def draw(self, win):

        rotated_points = self.rotated_points + np.array([self.position] * len(self.rotated_points))
        for point in rotated_points:
            pygame.draw.circle(win, (255, 0, 0), point, 5)
        pygame.draw.circle(win, (0, 255, 0), self.position, 5)
        pygame.draw.polygon(win, (255, 255, 255), rotated_points, 1)

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_vector = np.array([-self.vel * math.sin(math.radians(self.angle)),
                                    self.vel * math.cos(math.radians(self.angle))])
            self.position += move_vector

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_vector = np.array([self.vel * math.sin(math.radians(self.angle)),
                                    -self.vel * math.cos(math.radians(self.angle))])
            self.position += move_vector
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-1.5)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(1.5)

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 360
        rotation_matrix = np.array([[math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))],
                                    [-math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle))]])

        self.rotated_points = np.dot(self.points, rotation_matrix)

    def lidar(self, win, map):
        angles = [self.angle - 10, self.angle - 5, self.angle, self.angle + 5, self.angle + 10, self.angle]
        directions = [np.array((-math.sin(math.radians(angle)), math.cos(math.radians(angle)))) for angle in angles]
        for direction in directions:
            outer_point, outer_dist = self.intersection_point(map.outer_points, direction)
            if outer_point is None:
                continue
            else:
                pygame.draw.line(win, (255, 255, 255), self.position, outer_point)
                pygame.draw.circle(win, (0, 255, 0), outer_point, 5)
            # inner_point, inner_dist = self.intersection_point(map.inner_points, direction)
            # if outer_point is None and inner_point is None:
            #     return
            # if outer_dist < inner_dist:
            #     pygame.draw.line(win, (255, 255, 255), self.position, outer_point)
            #     pygame.draw.circle(win, (0, 255, 0), outer_point, 5)
            # else:
            #     pygame.draw.line(win, (255, 255, 255), self.position, inner_point)
            #     pygame.draw.circle(win, (0, 255, 0), inner_point, 5)

    def intersection_point(self, polygon, direction):
        min_dist = float('inf')
        min_point = None
        for i in range(len(polygon)):
            point_of_intersection, dist = self.find_intersection(direction, polygon[i], polygon[(i + 1) % len(polygon)])
            if dist and dist < min_dist:
                min_dist = dist
                min_point = point_of_intersection
        return min_point, min_dist

    def find_intersection(self, ray_direction, point1, point2):
        v1 = self.position - point1
        v2 = point2 - point1
        v3 = np.array([-ray_direction[1], ray_direction[0]])

        dot = np.dot(v2, v3)
        if abs(dot) < 0.000001:
            return None, None

        t1 = np.cross(v2, v1) / dot
        t2 = np.dot(v1, v3) / dot

        if t1 >= 0.0 and (t2 >= 0.0 and t2 <= 1.0):
            return self.position + t1 * ray_direction, np.linalg.norm(v1 - t1 * ray_direction)

        return None, None

    def check_collision(self, map):
        # check if car collides with outer wall or inner wall of track i.e. check if the polygon of car intersects with the polygon of track
        outer_collision = self.check_polygon_collision(map.outer_points)
        inner_collision = self.check_polygon_collision(map.inner_points)
        return outer_collision or inner_collision

    def check_polygon_collision(self, polygon):
        # check if polygon of car intersects with polygon of track
        for i in range(len(polygon)):
            for j in range(len(self.rotated_points)):
                if self.check_intersection(self.rotated_points[j] + self.position,
                                           self.rotated_points[(j + 1) % len(self.rotated_points)] + self.position,
                                           polygon[i], polygon[(i + 1) % len(polygon)]):
                    return True
        return False

    @staticmethod
    def check_intersection(p1, p2, p3, p4):
        # check if two line segments intersect i.e. line segment between point 1 and point 2 intersects with line
        # segment between point 3 and point 4
        def orientation(p, q, r):
            """

            :param p:
            :param q:
            :param r:
            :return:
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else 2  # Clockwise or Counterclockwise

        def on_segment(p, q, r):
            return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                    max(p[1], r[1]) >= q[1] >= min(p[1], r[1]))

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases

        # p1 , p2 and p3 are collinear and p3 lies on segment p1p2
        if o1 == 0 and on_segment(p1, p3, p2):
            return True

        # p1 , p2 and p4 are collinear and p4 lies on segment p1p2
        if o2 == 0 and on_segment(p1, p4, p2):
            return True

        # p3 , p4 and p1 are collinear and p1 lies on segment p3p4
        if o3 == 0 and on_segment(p3, p1, p4):
            return True

        # p3 , p4 and p2 are collinear and p2 lies on segment p3p4
        if o4 == 0 and on_segment(p3, p2, p4):
            return True

        return False


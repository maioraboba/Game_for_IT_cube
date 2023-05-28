import pygame
import math

from Game_IT_cube import WIDTH, HEIGHT
from Game_IT_cube import WIDTH_ZONE, HEIGHT_ZONE
from Game_IT_cube import Game, cells

from Game_IT_cube import font

from random import *

COLOR = ()


class Entity:
    FONT_COLOR = "#2a2a2c"

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass


class Cell(Entity):
    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.mass = 5
        self.x, self.y = randint(11, 2489), randint(11, 2489)
        self.color = (245, 0, 245)

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        place_spawn = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.color, place_spawn, int(self.mass * zoom))


class CellList(Entity):
    def __init__(self, surface, cam, num):
        super().__init__(surface, cam)
        self.cell_list = []
        for _ in range(num):
            self.cell_list.append(Cell(self.surface, self.camera))

    def new_cell(self, num=1):
        for _ in range(num):
            self.cell_list.append(Cell(self.surface, self.camera))

    def draw(self):
        for cell in self.cell_list:
            cell.draw()


class Enemy(Entity):
    def __init__(self, surface, camera,  name, color, outline_color):
        super().__init__(surface, camera)
        self.x, self.y = randint(300, 2200), randint(300, 2200)
        self.mass, self.speed = 20, 4
        self.outline_size = 3 + self.mass / 2
        self.name = name
        self.color = color
        self.outline_color = outline_color
        if not self.name:
            self.name = "Enemy"

    def collision_check(self, foods, entites):

        for entity in entites:

            if entity.x == self.x and entity.y == self.y:
                continue

            if Game().get_distance([entity.x, entity.y], [self.x, self.y]) <= self.mass / 2:
                self.mass += entity.mass
                entites.remove(entity)

        for food in foods:

            if Game().get_distance([food.x, food.y], [self.x, self.y]) <= self.mass / 2:
                self.mass += 0.25
                foods.remove(food)
                cells.new_cell(choice([1, 0, 1]))

    def move(self, foods, entites: list):
        for entity in entites:
            if math.dist((self.x, self.y), (entity.x, entity.x)) <= self.mass * 2:
                self.outline_size = 3 + self.mass / 2
                go_x, go_y = entity.x, entity.y
                rotation = math.atan2(go_y - float(HEIGHT) / 2, go_x - float(WIDTH) / 2)
                rotation *= 180 / math.pi
                normalized = (90 - abs(rotation)) / 90
                vx = self.speed * normalized
                if rotation < 0:
                    vy = -self.speed + abs(vx)
                else:
                    vy = self.speed - abs(vx)

                if self.x + vx - self.outline_size < 0:
                    self.x = self.outline_size
                elif self.x + vx + self.outline_size > WIDTH_ZONE:
                    self.x = WIDTH_ZONE - self.outline_size
                else:
                    self.x += vx

                if self.y + vy - self.outline_size < 0:
                    self.y = self.outline_size
                elif self.y + vy + self.outline_size > HEIGHT_ZONE:
                    self.y = HEIGHT_ZONE - self.outline_size
                else:
                    self.y += vy
                break

        for food in foods:
            if math.dist((self.x, self.y), (food.x, food.x)) <= self.mass * 2:
                self.outline_size = 3 + self.mass / 2
                go_x, go_y = food.x, food.y
                rotation = math.atan2(go_y - float(HEIGHT) / 2, go_x - float(WIDTH) / 2)
                rotation *= 180 / math.pi
                normalized = (90 - abs(rotation)) / 90
                vx = self.speed * normalized
                if rotation < 0:
                    vy = -self.speed + abs(vx)
                else:
                    vy = self.speed - abs(vx)

                if self.x + vx - self.outline_size < 0:
                    self.x = self.outline_size
                elif self.x + vx + self.outline_size > WIDTH_ZONE:
                    self.x = WIDTH_ZONE - self.outline_size
                else:
                    self.x += vx

                if self.y + vy - self.outline_size < 0:
                    self.y = self.outline_size
                elif self.y + vy + self.outline_size > HEIGHT_ZONE:
                    self.y = HEIGHT_ZONE - self.outline_size
                else:
                    self.y += vy
                break

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        # Draw the outline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outline_color, center, int((self.mass / 2 + 3) * zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        Game().drawtext(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                        Player.FONT_COLOR)


class EnemyList(Entity):
    def __init__(self, surface, cam, num):
        super().__init__(surface, cam)
        self.enemy_list = []
        for _ in range(num):
            self.enemy_list.append(Enemy(self.surface, self.camera, choice(COLOR), *choice(COLOR)))

    def new_cell(self, num=1):
        for _ in range(num):
            self.enemy_list.append(Enemy(self.surface, self.camera, choice(COLOR), *choice(COLOR)))

    def draw(self):
        for cell in self.enemy_list:
            cell.draw()


class Player(Entity):
    def __init__(self, surface, camera, name, color, outline_color):
        super().__init__(surface, camera)
        self.name = name
        self.x, self.y = randint(300, 2200), randint(300, 2200)
        self.mass, self.speed = 20, 4
        self.outline_size = 3 + self.mass / 2
        self.color = color
        self.outline_color = outline_color
        if not self.name:
            self.name = "YOU"

    def collision_check(self, foods, entites):
        for food in foods:
            if Game().get_distance([food.x, food.y], [self.x, self.y]) <= self.mass / 2:
                self.mass += 0.25
                foods.remove(food)
                cells.new_cell(choice([1, 0, 1]))
        for entity in entites:
            if Game().get_distance([entity.x, entity.y], [self.x, self.y]) <= self.mass / 2:
                self.mass += entity.mass
                entites.remove(entity)

    def move(self):
        go_x, go_y = pygame.mouse.get_pos()
        rotation = math.atan2(go_y - float(HEIGHT) / 2, go_x - float(WIDTH) / 2)
        rotation *= 180 / math.pi
        normalized = (90 - abs(rotation)) / 90
        vx = self.speed * normalized
        if rotation < 0:
            vy = -self.speed + abs(vx)
        else:
            vy = self.speed - abs(vx)

        if self.x + vx - self.outline_size < 0:
            self.x = self.mass / 2 + self.outline_size
        elif self.x + vx + self.outline_size > WIDTH_ZONE:
            self.x = WIDTH_ZONE - self.outline_size
        else:
            self.x += vx

        if self.y + vy - self.outline_size < 0:
            self.y = self.outline_size
        elif self.y + vy + self.outline_size > HEIGHT_ZONE:
            self.y = HEIGHT_ZONE - self.outline_size
        else:
            self.y += vy

    def feed(self):
        """Unsupported feature.
        """
        pass

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        # Draw the outline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outline_color, center, int((self.mass / 2 + 3) * zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        Game().drawtext(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                        Player.FONT_COLOR)

import pygame
import pygame_menu
import math
import random as rnd

WIDTH, HEIGHT = 1200, 800
WIDTH_ZONE, HEIGHT_ZONE = 2500, 2500
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# загрузка музыки
pygame.mixer.music.load("Lines of Code.mp3")

font = pygame.font.SysFont('Verdana.ttf', 20, True)
big_font = pygame.font.SysFont('Verdana.ttf', 24, True)


class Painter:
    def __init__(self):
        self.paints = []

    def add(self, canpaint):
        self.paints.append(canpaint)

    def paint(self):
        for d in self.paints:
            d.draw()


class MainMenu(pygame_menu.Menu):
    @classmethod
    def set_difficulty(cls, value, difficulty):
        print(value)
        print(difficulty)

    @classmethod
    def start_the_game(cls):
        game = Game()
        game.start()

    def level_menu(self):
        self._open(self.level)

    def __init__(self):
        super().__init__('Welcome', 800, 600, theme=pygame_menu.themes.THEME_SOLARIZED)
        self.add.text_input('Name: ', default='username', maxchar=20)
        self.add.button('Play', self.start_the_game)
        self.add.button('Levels', self.level_menu)
        self.add.button('Quit', pygame_menu.events.EXIT)

        self.level = pygame_menu.Menu('Select a Difficulty', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
        self.level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)


class PauseMenu(MainMenu):

    def __init__(self):
        super().__init__('Welcome', 800, 600, theme=pygame_menu.themes.THEME_SOLARIZED)
        self.add.button('Play', self.start_the_game)
        self.add.button('Quit', pygame_menu.events.EXIT)


class Game:
    def __init__(self):
        self.is_running = False
        self.pause_menu = False

    @classmethod
    def get_distance(cls, bac1, bac2):
        dist_x = abs(bac1[0] - bac2[0])
        dist_y = abs(bac1[1] - bac2[1])
        return (dist_x ** 2 + dist_y ** 2) ** 0.5  # длина между центрами окружностей

    @classmethod
    def drawtext(cls, message, pos, color=(255, 255, 255)):
        screen.blit(font.render(message, True, color), pos)

    def update(self):
        pass

    def start(self):
        global camera
        self.is_running = True
        while self.is_running:
            clock.tick(FPS)
            eventts = pygame.event.get()
            for e in eventts:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.is_running = False
                    if e.key == pygame.K_SPACE:
                        del camera
                        bacterium.split()
                    if e.key == pygame.K_w:
                        bacterium.feed()
                if e.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    quit()
                if bacterium.mass > 2400:
                    self.is_running = False
                    pygame.quit()
                    quit()

            bacterium.move()
            bacterium.collision_check(cells.cell_list)
            if camera is not None:
                camera.update(bacterium)
            screen.fill((8, 5, 30))
            painter.paint()

            if pausemenu.is_enabled():
                pausemenu.update(events)
                pausemenu.draw(screen)

            pygame.display.flip()


class CanPaint:
    def __init__(self, surface, cam):
        self.surface = surface
        self.camera = cam

    def draw(self):
        pass


class Camera:
    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = WIDTH, HEIGHT
        self.zoom = 0.5

    def centre(self, bacterium_or_position):
        if isinstance(bacterium_or_position, Player):
            x, y = bacterium_or_position.x, bacterium_or_position.y
            self.x = (WIDTH/2) - (x * self.zoom)
            self.y = (HEIGHT/2) - (y * self.zoom)
        elif type(bacterium_or_position) == tuple:
            self.x, self.y = bacterium_or_position

    def update(self, target):
        self.zoom = 100 / target.mass + 0.3
        self.centre(bacterium)


class Cell(CanPaint):
    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.mass = 5
        self.x, self.y = rnd.randint(11, 2489), rnd.randint(11, 2489)
        self.color = (245, 0, 245)

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        place_spawn = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.color, place_spawn, int(self.mass * zoom))


class CellList(CanPaint):
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


class Grid(CanPaint):
    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color_grid = "#00bfff"

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0, 2501, 50):
            pygame.draw.line(self.surface, self.color_grid, (x, y + i * zoom), (2500 * zoom + x, i * zoom + y), 3)
            pygame.draw.line(self.surface, self.color_grid, (x + i * zoom, y), (i * zoom + x, 2500 * zoom + y), 3)


class Player(CanPaint):
    FONT_COLOR = "#2a2a2c"

    def __init__(self, surface, cam, name=""):
        super().__init__(surface, cam)
        self.x, self.y = rnd.randint(300, 2200), rnd.randint(300, 2200)
        self.mass, self.speed = 20, 4
        self.color = "#1c5bed"
        self.outline_color = "#ccccff"
        if name:
            self.name = name
        else:
            self.name = "barabashka"

    def collision_check(self, foods):
        for food in foods:
            if Game().get_distance([food.x, food.y], [self.x, self.y]) <= self.mass / 2:
                self.mass += 0.25
                foods.remove(food)
                cells.new_cell(rnd.choice([1, 0, 1]))

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

        if self.x + vx - self.mass / 2 < 0:
            self.x = self.mass / 2
        elif self.x + vx + self.mass / 2 > WIDTH_ZONE:
            self.x = WIDTH_ZONE - self.mass / 2
        else:
            self.x += vx

        if self.y + vy - self.mass / 2 < 0:
            self.y = self.mass / 2
        elif self.y + vy + self.mass / 2 > HEIGHT_ZONE:
            self.y = HEIGHT_ZONE - self.mass / 2
        else:
            self.y += vy

    def feed(self):
        """Unsupported feature.
        """
        pass

    def split(self):
        """Unsupported feature.
        """
        pass

    def draw(self):
        """Draws the player as an outlined circle.
        """
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outline_color, center, int((self.mass / 2 + 3) * zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        Game().drawtext(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                        Player.FONT_COLOR)


# Initialize essential entities
camera = Camera()

grid = Grid(screen, camera)
cells = CellList(screen, camera, 1000)
bacterium = Player(screen, camera, "Bebrochka")

painter = Painter()
painter.add(grid)
painter.add(cells)
painter.add(bacterium)


pausemenu = PauseMenu()
mainmenu = MainMenu()
pygame.mixer.music.play(-1)
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and Game().is_running:
                pygame.quit()
                quit()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(screen)
    else:
        pygame.mixer.music.pause()
    pygame.display.update()

import pygame, sys
from pygame.locals import *
import math, random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

dispsurf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

dispsurf.fill((0,0,0))
pygame.display.set_caption("Matrix")

FONT_SIZE = 16

font = pygame.font.SysFont("yumincho36pkana", FONT_SIZE)


#font2 = pygame.font.SysFont("

alphabet = "0123456789abcdefghijlmnopqrstuvwxyz                   アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン"
#alphabet = "abcdefghijlmnopqrstuvwxyz"

def search_list(list_to_search, item):
    is_there = False
    for x in list_to_search:
        if x == item:
            is_there = True
        else:
            is_there = is_there
    return is_there

class Grid():
    def __init__(self):
        self.array = []
        self.xmax = math.floor(SCREEN_WIDTH / FONT_SIZE)
        self.ymax = math.floor(SCREEN_HEIGHT / FONT_SIZE)
        self.scroll_rate = 10
        self.some_of_top_row = []
        self.locked = False

    def initialize(self):
        count = 0
        for y in range(self.ymax):
            for x in range(self.xmax):
                self.array.append({"char": "0", "grid_pos": (x,y), "position": count})
                count += 1

    def scroll_column(self, column):
        new_cell = {"char": random.choice(alphabet), "grid_pos": (column, 0), "position": column}
        self.push_column_down(new_cell)


    def push_column_down(self, cell):
        cell_to_move = self.array[cell["position"]]
        self.array[cell["position"]] = cell
        cell_to_move["position"] += self.xmax
        if cell_to_move["position"] < len(self.array):
            cell_to_move["grid_pos"] = (cell_to_move["grid_pos"][0], cell_to_move["grid_pos"][1] + 1)
            self.push_column_down(cell_to_move)

    def draw(self, ds):
        for cell in self.array:
            rendered_char = font.render(cell["char"], True, (0,255,0))
            ds.blit(rendered_char, (cell["grid_pos"][0] * FONT_SIZE, cell["grid_pos"][1] * FONT_SIZE))

    def get_some_of_top_row(self):
        top_row = [cell["position"] for cell in self.array if cell["position"] < self.xmax]
        n_cols_to_move = round(((self.scroll_rate / 100) * self.xmax)) - len(self.some_of_top_row)
        x = random.sample(top_row, int(n_cols_to_move))
        self.some_of_top_row = x if not self.locked else self.some_of_top_row

    def rearrange_falling_columns(self):
        new_selected_columns = []
        for x in self.some_of_top_row:
            new_x = x + (-1 if bool(random.getrandbits(1)) else 1) if bool(random.getrandbits(1)) else 0
            if new_x > 0 and new_x < self.xmax and not search_list(new_selected_columns, new_x):
                new_selected_columns.append(new_x)
        self.some_of_top_row = new_selected_columns if not self.locked else self.some_of_top_row

    def update(self):
        if not len(self.some_of_top_row):
            self.get_some_of_top_row()
            for i in self.some_of_top_row:
                self.scroll_column(i)
        else:
            self.rearrange_falling_columns()
            for i in self.some_of_top_row:
                self.scroll_column(i)

    def handle_keydown(self, unicode):
        if (unicode == '=' and self.scroll_rate < 100):
            self.scroll_rate += 10
        if (unicode == '-' and self.scroll_rate > 0):
            self.scroll_rate -= 10
        if (unicode == ' '):
            self.locked = True

        #top_row =

    def handle_keyup(self, unicode):
        if (unicode == ' '):
            self.locked = False
        

The_Grid = Grid()
The_Grid.initialize()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            #print(event.unicode)
            The_Grid.handle_keydown(event.unicode)

        if event.type == KEYUP:
            The_Grid.handle_keyup(event.unicode)


    The_Grid.update()
    dispsurf.fill((0,0,0))
    The_Grid.draw(dispsurf)

    pygame.display.update()

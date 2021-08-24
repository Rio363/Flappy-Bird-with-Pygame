import pygame as pg
from os import path
import shelve

pg.mixer.init()

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

TITLE = "FLAPPY!"
WIDTH, HEIGHT = 380, 600
FPS = 60

ICON_IMG = pg.image.load(path.join(img_dir, "yellowbird-upflap.png"))

score_data = shelve.open("data")
score_data.setdefault("best_score", 0)

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game Vars
GRAVITY = 0.6
BG_SPEED = -0.3
BASE_SPEED = -4
JUMP_HEIGHT = -12
BASE_Y = HEIGHT - 112 


# Load All image Graphics
DAY_NIGHT = ['night', "day"][-1]
BIRD_COLOR = ["yellow", "blue", "red"][-1]
PIPE_COLOR = ["red", 'green'][0]

bg_img = pg.transform.scale(pg.image.load(path.join(img_dir, f"background-{DAY_NIGHT}.png")), (WIDTH, HEIGHT))
base_img = pg.transform.scale(pg.image.load(path.join(img_dir, "base.png")), (WIDTH, 112))

bird_images_lst = [pg.transform.scale(pg.image.load(path.join(img_dir, img)), (42, 30)) for img in [f"{BIRD_COLOR}bird-downflap.png", f"{BIRD_COLOR}bird-upflap.png", F"{BIRD_COLOR}bird-midflap.png"]]

pipe_img = pg.transform.scale(pg.image.load(path.join(img_dir, f"pipe-{PIPE_COLOR}.png")), (75, 320))
pipe_img_flipped = pg.transform.flip(pipe_img, False, True)

splash_screen_img = pg.transform.scale(pg.image.load(path.join(img_dir, "message.png")), (int(WIDTH * 0.6), int(HEIGHT * 0.55)))
splash_screen_img_rect = splash_screen_img.get_rect() # to have more control on x, y, center, etc...
splash_screen_img_rect.centerx = WIDTH / 2
splash_screen_img_rect.centery = HEIGHT / 2 - 25

game_over_img = pg.transform.scale(pg.image.load(path.join(img_dir, "gameover.png")), (int(WIDTH * 0.7), int(HEIGHT * 0.1)))
game_over_img_rect = splash_screen_img.get_rect() # to have more control on x, y, center, etc...
game_over_img_rect.centerx = WIDTH / 2 - 20
game_over_img_rect.centery = HEIGHT / 2 + 25

nums_lst = [pg.image.load(path.join(img_dir, f"{n}.png")) for n in range(10)]
nums_lst = [pg.transform.scale(num_img, (24, 36)) for num_img in nums_lst]

# Load all Sound effects...
flap_sound = pg.mixer.Sound(path.join(snd_dir, "wing.wav"))
hit_sound = pg.mixer.Sound(path.join(snd_dir, "hit.wav"))
swooshing_sound = pg.mixer.Sound(path.join(snd_dir, "swooshing.wav"))
point_sound = pg.mixer.Sound(path.join(snd_dir, "point.wav"))

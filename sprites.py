from settings import *
import random


class Bird(pg.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(groups)
		self.frame = 0
		self.image_orig = bird_images_lst[self.frame].convert()
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.rect.centerx = 80
		self.rect.centery = HEIGHT / 4

		self.speedy = 0

		self.last_animation = pg.time.get_ticks()
		self.anim_wait_time = 100
		self.anim_speed = 1

		self.rot_angle = 0
		self.last_rot = 0
		self.rot_speed = -3
		self.rot_wait_time = 10

	def update(self):
		self.movement()
		self.animate()
		self.rotate()


	def animate(self):
		now = pg.time.get_ticks()
		old_center = self.rect.center

		if now - self.last_animation >= self.anim_wait_time:
			self.last_animation = now

			self.frame = (self.frame + self.anim_speed) % len(bird_images_lst)
			
			self.image_orig = bird_images_lst[self.frame] = bird_images_lst[self.frame].convert()
			self.image = self.image_orig.copy()
			self.rect = self.image.get_rect()
			self.rect.center = old_center


	def rotate(self):
		now = pg.time.get_ticks()
		old_center = self.rect.center

		if now - self.last_rot >= self.rot_wait_time:
			self.last_rot = now
			self.rot_angle = (self.rot_angle + self.rot_speed) % 360
			self.image = pg.transform.rotate(self.image_orig, self.rot_angle)
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def jump(self):
		self.speedy = JUMP_HEIGHT
		self.rot_angle = 75
		flap_sound.play()

	def movement(self):
		self.speedy += GRAVITY
		self.rect.y += self.speedy


class Pipe(pg.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(groups)
		self.image = pipe_img
		self.rect = self.image.get_rect()
		self.rect.bottom = random.randint(HEIGHT - 50, HEIGHT + 150)
		self.rect.x = WIDTH + 10

		self.speedx = BASE_SPEED

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right <= 0:
			self.kill()


class PipeFlipped(pg.sprite.Sprite):
	def __init__(self, pipe_top, *groups):
		super().__init__(groups)
		self.image = pipe_img_flipped
		self.rect = self.image.get_rect()
		self.rect.bottom = pipe_top - random.randint(180, 200) # Gap between pipes
		self.rect.x = WIDTH + 10

		self.speedx = BASE_SPEED

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right <= 0:
			self.kill()
			swooshing_sound.play()
			point_sound.play()
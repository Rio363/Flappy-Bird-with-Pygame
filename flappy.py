from sprites import *

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
pg.display.set_icon(ICON_IMG)
clock = pg.time.Clock()
pg.mouse.set_visible(False)
font_name = pg.font.match_font("arial")


def draw_score(surf, score):
	gap = 25
	score_x = WIDTH / 2 - gap / 2
	distance = 0

	# Centering...
	if len(str(score)) >= 2:
		score_x = WIDTH / 2 - gap

	if len(str(score)) >= 3:	
		score_x = WIDTH / 2 - gap * 1.3

	if len(str(score)) >= 4:
		score_x = WIDTH / 2 - gap * 2

	if len(str(score)) >= 6:
		score_x = WIDTH / 2 - gap * 3

	for num in range(len(str(score))):
		surf.blit(nums_lst[int(str(score)[num])], (score_x + distance, 20))
		distance += gap


def write(surf, text, pos_x, pos_y, size=26):
	font = pg.font.Font(font_name, size)
	txt_surf = font.render(text, True, WHITE)
	txt_rect = txt_surf.get_rect(midtop = [pos_x, pos_y])
	surf.blit(txt_surf, txt_rect)


def auto_pilot():
	# Auto pilot
	if bird.rect.bottom + 30 >= BASE_Y:
		bird.jump()
	for p in pipes:
		if bird.rect.bottom + 10 >= p.rect.top and p not in pipes_flipped:
			bird.jump()


def show_splash_screen():
	screen.fill(BLACK)
	screen.blit(bg_img, (0, 0))
	screen.blit(splash_screen_img, splash_screen_img_rect)
	write(screen, f"Highest score: {score_data['best_score']}", WIDTH / 2, 20)

	
	base_pos = 0

	waiting = True
	while waiting:
		clock.tick(FPS)

		for event in pg.event.get():
			if event.type == pg.QUIT \
			 or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

		base_pos += BASE_SPEED
		if base_pos + WIDTH <= 0:
			base_pos = 0
		screen.blit(base_img, (base_pos, HEIGHT - 112))
		screen.blit(base_img, (base_pos + WIDTH, HEIGHT - 112))
		write(screen, "Press Any Key", WIDTH / 2, HEIGHT - 155, 30)	


		pg.display.flip()


def show_game_over_screen():
	screen.fill(BLACK)
	screen.blit(bg_img, (0, 0))
	screen.blit(game_over_img, game_over_img_rect)
	write(screen, f"Score: {score}", WIDTH / 2, 20, 30)	
	write(screen, f"Highest score: {score_data['best_score']}", WIDTH / 2, HEIGHT / 2, 30)


	base_pos = 0

	waiting = True
	while waiting:
		clock.tick(FPS)

		for event in pg.event.get():
			if event.type == pg.QUIT \
			 or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

		base_pos += BASE_SPEED
		if base_pos + WIDTH <= 0:
			base_pos = 0
		screen.blit(base_img, (base_pos, HEIGHT - 112))
		screen.blit(base_img, (base_pos + WIDTH, HEIGHT - 112))

		pg.display.flip()


background_pos = 0
base_pos = 0

PIPE_SPAWN_EVENT = pg.USEREVENT
pg.time.set_timer(PIPE_SPAWN_EVENT, 2500)

splash_screen = True
game_over_screen = False
running = True

while running:

	if splash_screen:
		show_splash_screen()
		all_sprites = pg.sprite.Group()
		pipes = pg.sprite.Group()
		pipes_flipped = pg.sprite.Group()
		
		bird = Bird(all_sprites)

		score = 0
		splash_screen = False

	if game_over_screen:
		show_game_over_screen()
		all_sprites = pg.sprite.Group()
		pipes = pg.sprite.Group()
		pipes_flipped = pg.sprite.Group()
		
		bird = Bird(all_sprites)

		score = 0
		game_over_screen = False


	for event in pg.event.get():
		if event.type == pg.QUIT \
		 or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				bird.jump()
		if event.type == PIPE_SPAWN_EVENT:
			p = Pipe(pipes, all_sprites)
			p_overhead = PipeFlipped(p.rect.top, all_sprites, pipes, pipes_flipped)

	clock.tick(FPS)
	screen.fill(BLACK)

	background_pos += BG_SPEED
	if background_pos + WIDTH <= 0:
		background_pos = 0
	screen.blit(bg_img, (background_pos, 0))
	screen.blit(bg_img, (background_pos + WIDTH, 0))


	all_sprites.update()
	all_sprites.draw(screen)
	draw_score(screen, score)

	base_pos += BASE_SPEED
	if base_pos + WIDTH <= 0:
		base_pos = 0
	screen.blit(base_img, (base_pos, BASE_Y))
	screen.blit(base_img, (base_pos + WIDTH, BASE_Y))

	# Collisions
	hits =  pg.sprite.spritecollide(bird, pipes, False)
	if hits:
		game_over_screen = True
		hit_sound.play()
	if bird.rect.bottom >= BASE_Y or bird.rect.top <= -220:
		game_over_screen = True
		hit_sound.play()

	# Add score...
	for p in pipes:
		if p not in pipes_flipped:
			if p.rect.centerx + 30 <= 0:
				score += 25
				if score > score_data["best_score"]:
					score_data['best_score'] = score

	auto_pilot()
	pg.display.flip()

pg.quit()

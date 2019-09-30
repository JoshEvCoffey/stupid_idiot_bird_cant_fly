import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import stupid_bird_sprite
import pipe_sprites
import cloud_sprites

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 648

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=WHITE, ocolor=BLACK, opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

class Game(object):
	""" Represents an instance of the game """
	
	def __init__(self):
		self.score = 0
		self.pipe_timer = 30
		self.pipe_gap = 225
		self.cloud_timer = 50
		self.game_over = False
		self.first_input_recieved = False
		
		self.gravity = 15
		self.player_x = 200
		self.player_y = SCREEN_HEIGHT / 2
		self.player_velo_y = 0
		
		self.hop_sound = pygame.mixer.Sound("resources/hop.ogg")
		self.hit_sound = pygame.mixer.Sound("resources/hit.ogg")
		self.background_image = pygame.image.load("resources/sky.png").convert()
		
		self.clouds_list = pygame.sprite.Group()
		self.pipes_list = pygame.sprite.Group()
		self.scorezone_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		
		self.bird = stupid_bird_sprite.Bird()
		self.bird.moveTo(self.player_x, self.player_y)
		self.all_sprites_list.add(self.bird)
		
	def hop(self):
		self.player_velo_y = -15
		self.hop_sound.play()
		
	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_SPACE and not self.game_over:
					self.hop()
					if not self.first_input_recieved:
						self.first_input_recieved = True
				elif event.key == pygame.K_r and self.game_over:
					self.__init__()
		
		return False
		
	def run_logic(self):
		self.pipe_timer += 1
		self.cloud_timer += 1
		horizontal_hit = False
		
		if self.pipe_timer >= 60 and self.first_input_recieved:
			self.pipe_timer = 0
			bottom_pipe = pipe_sprites.Bottom_pipe(self.pipe_gap)
			between_pipe = pipe_sprites.Between_pipe(bottom_pipe, self.pipe_gap)
			top_pipe = pipe_sprites.Top_pipe(bottom_pipe, self.pipe_gap)
			
			self.all_sprites_list.add(bottom_pipe)
			self.all_sprites_list.add(top_pipe)
			self.pipes_list.add(bottom_pipe)
			self.pipes_list.add(top_pipe)
			self.scorezone_list.add(between_pipe)
		
		if self.cloud_timer >= 55:
			self.cloud_timer = 0
			cloud = cloud_sprites.Cloud()
			
			self.clouds_list.add(cloud)
			
		self.player_y += self.player_velo_y
		
		if self.player_velo_y < self.gravity:
			self.player_velo_y += 1
		
		if self.player_y < 0:
			self.player_y = 0
		elif self.player_y > SCREEN_HEIGHT - 30:
			self.game_over = True
		
		
		
		if not self.game_over:
			self.all_sprites_list.update()
			self.clouds_list.update()
			self.scorezone_list.update()
		
		score_hit_list = pygame.sprite.spritecollide(self.bird, self.scorezone_list, True)
		pipe_hit_list = pygame.sprite.spritecollide(self.bird, self.pipes_list, False)
		
		for zone in score_hit_list:
			self.score += 1
			if self.score % 10 == 0:
				self.pipe_gap -= 10
		
		for pipe in pipe_hit_list:
			if not self.game_over:
				self.hit_sound.play()
			self.game_over = True
			horizontal_hit = True
		
		self.bird.moveTo(self.player_x, self.player_y)
		
		pipe_hit_list = pygame.sprite.spritecollide(self.bird, self.pipes_list, False)
		for pipe in pipe_hit_list:
			if not self.game_over:
				self.hit_sound.play()
			self.game_over = True
			if self.player_velo_y > 0 and isinstance(pipe, pipe_sprites.Bottom_pipe) and not horizontal_hit:
				self.bird.rect.bottom = pipe.rect.top
			elif self.player_velo_y < 0 and isinstance(pipe, pipe_sprites.Top_pipe) and not horizontal_hit: 
				self.bird.rect.top = pipe.rect.bottom
				self.player_velo_y = 0
		
		if not self.first_input_recieved and self.player_y > (SCREEN_HEIGHT / 2) + 30:
			self.hop()
		
	def display_frame(self, screen):
		screen.blit(self.background_image, [0, 0])
		
		self.clouds_list.draw(screen)
		self.all_sprites_list.draw(screen)
		font = pygame.font.SysFont("Calibri", 25, True, False)
		screen.blit(render('Score: ' + str(self.score), font), [10, 10])
		
		if not self.first_input_recieved:
			font = pygame.font.SysFont("Calibri", 30, True, False)
			text = font.render("press space to hop", True, WHITE)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			y = 500
			screen.blit(render("press space to hop", font), [center_x, y])
		
		if self.game_over:
			font = pygame.font.SysFont("Calibri", 40, True, False)
			text = font.render("Game Over, press r to restart", True, WHITE)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(render("Game Over, press r to restart", font), [center_x, center_y])
		
		pygame.display.flip()
		
def main():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()
	pygame.init()
	
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)
	icon = pygame.image.load("resources/icon.png")
	icon.set_colorkey(WHITE)
	
	pygame.display.set_icon(icon)
	pygame.display.set_caption("Stupid Idiot Bird Can't Fly")
	
	background = pygame.image.load("resources/sky.png").convert()
	play_button_image = pygame.image.load("resources/play_button.png").convert()
	play_button_image.set_colorkey(WHITE)
	play_button_hover_image = pygame.image.load("resources/play_button_hover.png").convert()
	play_button_hover_image.set_colorkey(WHITE)
	
	button_x_1 = SCREEN_WIDTH // 2 - 141
	button_x_2 = SCREEN_WIDTH // 2 + 140
	button_y_1 = 400
	button_y_2 = 533
	
	title_image = pygame.image.load("resources/title.png").convert()
	title_image.set_colorkey(WHITE)
	title_x = SCREEN_WIDTH // 2 - 217
	title_y = 50
	
	done = False
	clock = pygame.time.Clock()
	
	game = Game()
	
	intro = True
	
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				intro = False
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if event.pos[0] in range(button_x_1, button_x_2) and event.pos[1] in range(button_y_1, button_y_2):
						intro = False
		
		mouse = pygame.mouse.get_pos()
		
		screen.blit(background, [0, 0])
		
		screen.blit(title_image, [title_x, title_y])
		
		if mouse[0] in range(button_x_1, button_x_2) and mouse[1] in range(button_y_1, button_y_2):
			screen.blit(play_button_hover_image, [button_x_1, button_y_1])
		else:
			screen.blit(play_button_image, [button_x_1, button_y_1])
		
		pygame.display.flip()
	
	pygame.mouse.set_visible(False)
	
	while not done:
		done = game.process_events()
		
		game.run_logic()
		
		game.display_frame(screen)
		
		clock.tick(60)
	
	pygame.quit()
	
if __name__ == "__main__":
	main()
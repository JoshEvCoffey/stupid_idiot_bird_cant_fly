import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import ctypes
import pygame
import stupid_bird_sprite
import pipe_sprites
import cloud_sprites
import shelve
import time
import math

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY = (0, 204, 255)

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
		self.start_time = time.time()
		self.game_over = False
		self.first_input_recieved = False
		self.show_fps = False
		self.fps = 0
		self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
		
		self.gravity = 15
		self.player_x = self.screen_width / 5
		self.player_y = self.screen_height / 2
		self.player_velo_y = 0
		
		self.hop_sound = pygame.mixer.Sound("resources/hop.ogg")
		self.hit_sound = pygame.mixer.Sound("resources/hit.ogg")
		
		self.clouds_list = pygame.sprite.Group()
		self.pipes_list = pygame.sprite.Group()
		self.scorezone_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		
		self.bird = stupid_bird_sprite.Bird()
		self.bird.moveTo(self.player_x, self.player_y)
		self.all_sprites_list.add(self.bird)
		
		high_score_tracker = shelve.open('high_score.txt')
		try:
			self.high_score = high_score_tracker['high_score']
		except:
			self.high_score = 0
			high_score_tracker['high_score'] = 0
		high_score_tracker.close()
		
	def hop(self):
		self.player_velo_y = -15
		self.hop_sound.play()
		
	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				high_score_tracker = shelve.open('high_score.txt')
				if self.high_score > high_score_tracker['high_score']:
					high_score_tracker['high_score'] = self.high_score
				high_score_tracker.close()
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
					if not self.game_over:
						self.hop()
						if not self.first_input_recieved:
							self.first_input_recieved = True
				elif (event.key == pygame.K_r and self.game_over) or event.key == pygame.K_ESCAPE:
					high_score_tracker = shelve.open('high_score.txt')
					if self.high_score > high_score_tracker['high_score']:
						high_score_tracker['high_score'] = self.high_score
					high_score_tracker.close()
					if event.key == pygame.K_r:
						self.__init__()
					else:
						return False
				elif event.key == pygame.K_F3:
					self.show_fps = not self.show_fps
		
		return True
		
	def run_logic(self):
		self.pipe_timer += 1
		self.cloud_timer += 1
		
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
		elif self.player_y > self.screen_height - 30:
			self.game_over = True
		
		if not self.game_over:
			self.all_sprites_list.update()
			self.clouds_list.update()
			self.scorezone_list.update()
		
		score_hit_list = pygame.sprite.spritecollide(self.bird, self.scorezone_list, True)
		pipe_hit_list = pygame.sprite.spritecollide(self.bird, self.pipes_list, False)
		
		for zone in score_hit_list:
			self.score += 1
			if self.score % 10 == 0 and self.pipe_gap > 145:
				self.pipe_gap -= 10
		
		for pipe in pipe_hit_list:
			if not self.game_over:
				self.hit_sound.play()
			self.game_over = True
			self.player_x = pipe.rect.left - 47
		
		self.bird.moveTo(self.player_x, self.player_y)
		
		pipe_hit_list = pygame.sprite.spritecollide(self.bird, self.pipes_list, False)
		for pipe in pipe_hit_list:
			if not self.game_over:
				self.hit_sound.play()
			self.game_over = True
			if not self.game_over:
				self.hit_sound.play()
			self.game_over = True
			if self.player_velo_y > 0 and isinstance(pipe, pipe_sprites.Bottom_pipe):
				self.bird.rect.bottom = pipe.rect.top
				self.player_y = self.bird.rect.top
				self.bird.moveTo(self.player_x, self.player_y)
			elif self.player_velo_y < 0 and isinstance(pipe, pipe_sprites.Top_pipe): 
				self.bird.rect.top = pipe.rect.bottom
				self.player_velo_y = 0
				self.player_y = self.bird.rect.top
				self.bird.moveTo(self.player_x, self.player_y)
		
		if not self.first_input_recieved and self.player_y > (self.screen_height / 2) + 30:
			self.hop()
			
		if self.score > self.high_score:
			self.high_score = self.score
		
	def set_start_time(self, time):
		self.start_time = time
	
	def set_fps(self, frames):
		self.fps = frames
	
	def display_frame(self, screen):
		pygame.draw.rect(screen, SKY, pygame.Rect(0, 0, self.screen_width, self.screen_height))
		
		self.clouds_list.draw(screen)
		self.all_sprites_list.draw(screen)
		font = pygame.font.SysFont("Calibri", 25, True, False)
		screen.blit(render('Score: ' + str(self.score), font), [10, 10])
		if not self.high_score == 0:
			screen.blit(render('High Score: ' + str(self.high_score), font), [10, 40])
		
		if not self.first_input_recieved:
			font = pygame.font.SysFont("Calibri", 30, True, False)
			text = font.render("press space to hop", True, WHITE)
			center_x = (self.screen_width // 2) - (text.get_width() // 2)
			y = 500
			screen.blit(render("press space to hop", font), [center_x, y])
		
		if self.game_over:
			font = pygame.font.SysFont("Calibri", 40, True, False)
			text = font.render("Game Over, press r to restart", True, WHITE)
			center_x = (self.screen_width // 2) - (text.get_width() // 2)
			center_y = (self.screen_height // 2) - (text.get_height() // 2)
			screen.blit(render("Game Over, press r to restart", font), [center_x, center_y])
			
		if self.show_fps:
				font = pygame.font.SysFont("Calibri", 25, True, False)
				screen.blit(render(('FPS: ' + str(self.fps)), font), [self.screen_width - 100, 10])
		
		pygame.display.flip()
		
def main():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()
	pygame.init()
	
	ctypes.windll.user32.SetProcessDPIAware()
	true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
	screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN)
	#screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
	#screen_width, screen_height = pygame.display.get_surface().get_size()
	
	icon = pygame.image.load("resources/icon.png")
	icon.set_colorkey(WHITE)
	
	pygame.display.set_icon(icon)
	pygame.display.set_caption("Stupid Idiot Bird Can't Fly")
	
	title_image = pygame.image.load("resources/title.png").convert()
	title_image.set_colorkey(WHITE)
	title_x = screen_width // 2 - 217
	title_y = screen_height // 5
	
	play_button_image = pygame.image.load("resources/play_button.png").convert()
	play_button_image.set_colorkey(WHITE)
	play_button_hover_image = pygame.image.load("resources/play_button_hover.png").convert()
	play_button_hover_image.set_colorkey(WHITE)
	
	play_button_x_1 = screen_width // 5
	play_button_x_2 = screen_width // 5 + 281
	play_button_y_1 = title_y + 350
	play_button_y_2 = play_button_y_1 + 133
	
	quit_button_image = pygame.image.load("resources/quit_button.png").convert()
	quit_button_image.set_colorkey(WHITE)
	quit_button_hover_image = pygame.image.load("resources/quit_button_hover.png").convert()
	quit_button_hover_image.set_colorkey(WHITE)
	
	quit_button_x_1 = (3 * (screen_width // 5)) #- 141
	quit_button_x_2 = (3 * (screen_width // 5)) + 281
	quit_button_y_1 = title_y + 350
	quit_button_y_2 = quit_button_y_1 + 133
	
	click_sound = pygame.mixer.Sound("resources/click.ogg")
	
	done = False
	clock = pygame.time.Clock()
	
	game = Game()
	
	intro = True
	playing = True
	
	while not done:
		pygame.mouse.set_visible(True)
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					playing = False
					done = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if event.pos[0] in range(play_button_x_1, play_button_x_2) and event.pos[1] in range(play_button_y_1, play_button_y_2):
							click_sound.play()
							intro = False
							playing = True
						if event.pos[0] in range(quit_button_x_1, quit_button_x_2) and event.pos[1] in range(quit_button_y_1, quit_button_y_2):
							click_sound.play()
							intro = False
							playing = False
							done = True
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						intro = False
						playing = False
						done = True
						
						
			mouse = pygame.mouse.get_pos()
			
			pygame.draw.rect(screen, SKY, pygame.Rect(0, 0, screen_width, screen_height))
			
			screen.blit(title_image, [title_x, title_y])
			
			if mouse[0] in range(play_button_x_1, play_button_x_2) and mouse[1] in range(play_button_y_1, play_button_y_2):
				screen.blit(play_button_hover_image, [play_button_x_1, play_button_y_1])
			else:
				screen.blit(play_button_image, [play_button_x_1, play_button_y_1])
				
			if mouse[0] in range(quit_button_x_1, quit_button_x_2) and mouse[1] in range(quit_button_y_1, quit_button_y_2):
				screen.blit(quit_button_hover_image, [quit_button_x_1, quit_button_y_1])
			else:
				screen.blit(quit_button_image, [quit_button_x_1, quit_button_y_1])
			
			pygame.display.flip()
		
		intro = True
		pygame.mouse.set_visible(False)
		
		start_time = 0
		
		while playing:
			if game.show_fps:
				game.set_start_time(time.time())
				
			playing = game.process_events()
			
			game.run_logic()
			
			game.display_frame(screen)
			
			clock.tick(60)
			
			if game.show_fps:
				game.set_fps(math.floor(1.0 / (time.time() - game.start_time)))
	
	pygame.quit()
	
if __name__ == "__main__":
	main()
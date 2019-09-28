import pygame
import stupid_bird_sprite
import pipe_sprites

# Constants
WHITE = (255, 255, 255)
SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 648

class Game(object):
	""" Represents an instance of the game """
	
	def __init__(self):
		self.score = 0
		self.pipe_timer = 30
		self.game_over = False
		
		self.gravity = 8
		self.player_x = 200
		self.player_y = SCREEN_HEIGHT / 2
		self.player_velo_y = 0
		
		self.hop_sound = pygame.mixer.Sound("hop.ogg")
		self.background_image = pygame.image.load("stars.png").convert()
		
		self.pipes_list = pygame.sprite.Group()
		self.scorezone_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		
		self.bird = stupid_bird_sprite.Bird()
		self.bird.moveTo(self.player_x, self.player_y)
		self.all_sprites_list.add(self.bird)
		
	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_SPACE and not self.game_over:
					self.player_velo_y -= 20
					self.hop_sound.play()
				elif event.key == pygame.K_r and self.game_over:
					self.__init__()
		
		return False
		
	def run_logic(self):
		
		self.pipe_timer += 1
		
		if self.pipe_timer >= 60:
			self.pipe_timer = 0
			bottom_pipe = pipe_sprites.Bottom_pipe()
			between_pipe = pipe_sprites.Between_pipe(bottom_pipe)
			top_pipe = pipe_sprites.Top_pipe(bottom_pipe)
			
			self.all_sprites_list.add(bottom_pipe)
			self.all_sprites_list.add(top_pipe)
			self.pipes_list.add(bottom_pipe)
			self.pipes_list.add(top_pipe)
			self.scorezone_list.add(between_pipe)
			
		self.player_y += self.player_velo_y
		
		if self.player_velo_y < self.gravity:
			self.player_velo_y += 1
		
		if self.player_y < 0:
			self.player_y = 0
		elif self.player_y > SCREEN_HEIGHT - 30:
			self.game_over = True
		
		self.bird.moveTo(self.player_x, self.player_y)
		if not self.game_over:
			self.pipes_list.update()
			self.scorezone_list.update()
		
		score_hit_list = pygame.sprite.spritecollide(self.bird, self.scorezone_list, True)
		pipe_hit_list = pygame.sprite.spritecollide(self.bird, self.pipes_list, False)
		
		for zone in score_hit_list:
			self.score += 1
		
		for zone in pipe_hit_list:
			self.game_over = True
		
	def display_frame(self, screen):
		screen.blit(self.background_image, [0, 0])
		
		self.all_sprites_list.draw(screen)
		font = pygame.font.SysFont("Calibri", 25, True, False)
		text = font.render("Score: " + str(self.score), True, WHITE)
		screen.blit(text, [10, 10])
		
		if self.game_over:
			font = pygame.font.SysFont("Calibri", 40, True, False)
			text = font.render("Game Over, press r to restart", True, WHITE)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y])
		
		pygame.display.flip()
		
def main():
	pygame.init()
	
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)
	
	pygame.display.set_caption("Cool Game")
	pygame.mouse.set_visible(False)
	
	done = False
	clock = pygame.time.Clock()
	
	game = Game()
	
	while not done:
		done = game.process_events()
		
		game.run_logic()
		
		game.display_frame(screen)
		
		clock.tick(60)
	
	pygame.quit()
	
if __name__ == "__main__":
	main()
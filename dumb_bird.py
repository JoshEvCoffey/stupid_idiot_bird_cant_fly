import pygame
import math
import stupid_bird_sprite
import pipe_sprites

pygame.init()

WHITE = (255,255,255)

screen_width = 1152
screen_height = 648
size = (screen_width,screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cool Game")
background_image = pygame.image.load("stars.png").convert()

hop_sound = pygame.mixer.Sound("hop.ogg")
# Loop until the user clicks the close button
done = False

# used to manage how fast the game screen updates
clock = pygame.time.Clock()

x = 200
y = 324

gravity = 8
change_x = 0
change_y = 0

all_sprites_list = pygame.sprite.Group()
pipes_list = pygame.sprite.Group()
scorezone_list = pygame.sprite.Group()

pygame.mouse.set_visible(False)
bird = stupid_bird_sprite.Bird()
bird.moveTo(x,y)

all_sprites_list.add(bird)

pipe_timer = 30

score = 0
font = pygame.font.SysFont('Calibri', 25, True, False)
score_text = font.render("Score: " + str(score), True, WHITE)

controls_enabled = True

def reset():
    for sprite in all_sprites_list:
        sprite.kill()
    for sprite in scorezone_list:
        sprite.kill()
    score = 0
    pipe_timer = 30
    x = 200
    y = 324
    change_x = 0
    change_y = 0
    bird = stupid_bird_sprite.Bird() 
    bird.moveTo(x,y)
    all_sprites_list.add(bird)
    controls_enabled = True

# Main program loop
while not done:
    # Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        elif event.type == pygame.KEYDOWN:
            #Figure out if it was an arrow key. If so
            # adjust speed
            if event.key == pygame.K_UP and controls_enabled:
                change_y = -15
                hop_sound.play()
                
            if event.key == pygame.K_r:
                reset()
           
                
    # Game logic here
    pipe_timer += 1
    
    if pipe_timer >= 60:
        pipe_timer = 0
        bottom_pipe = pipe_sprites.Bottom_pipe()
        between_pipe = pipe_sprites.Between_pipe(bottom_pipe)
        top_pipe = pipe_sprites.Top_pipe(bottom_pipe)
        all_sprites_list.add(bottom_pipe)
        all_sprites_list.add(top_pipe)
        pipes_list.add(bottom_pipe)
        pipes_list.add(top_pipe)
        scorezone_list.add(between_pipe)
        
    
    x += change_x
    y += change_y
    
    
    if change_y < gravity:
        change_y += 1
    
    if x > screen_width - 47:
        x = screen_width - 47
    elif x < 0:
        x = 0;
    
    if y < 0:
        y = 0
    elif y > screen_height - 30:
        controls_enabled = False
        
    bird.moveTo(x,y)
    if controls_enabled:    
        pipes_list.update()
        scorezone_list.update()
    
    score_hit_list = pygame.sprite.spritecollide(bird, scorezone_list, True)
    pipe_hit_list = pygame.sprite.spritecollide(bird, pipes_list, False)
    
    for zone in score_hit_list:
        score += 1
        score_text = font.render("Score: " + str(score), True, WHITE)
    
    for pipe in pipe_hit_list:
        controls_enabled = False
        
    # Drawing code here

    screen.blit(background_image, [0, 0])
    all_sprites_list.draw(screen)
    screen.blit(score_text, [10, 10])
    
    #update the screen
    pygame.display.flip()
    
    # limit to 60 fps
    clock.tick(60)

pygame.quit()
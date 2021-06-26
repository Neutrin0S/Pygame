import pygame
import sys
import random
import time


def check_score():
    global high_score
    text_surface = font.render(f'Score: {str(int(score))}', True, (255,255,255))
    score_rect = text_surface.get_rect(center =(225,100))
    screen.blit(text_surface, score_rect)  
    if score >= high_score:
        high_score = score
def active_score():
    global high_score
    text_surface = font.render(str(int(score)), True, (255,255,255))
    score_rect = text_surface.get_rect(center =(225,100))
    screen.blit(text_surface, score_rect)
    
    if score >= high_score:
        high_score = score
def draw_ground():
    global player_x
    screen.blit(final_first_ground, (player_x, 670))
    screen.blit(final_first_ground, (player_x + 450, 670))
    if player_x <= -450:
        player_x = 0
    player_x -= 1
def create_pipe():
    random_y_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(510,random_y_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(510,random_y_pos-250))
    return bottom_pipe,top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    visible_pipes = [pipe for pipe in pipes if pipe.right >-5]
    return visible_pipes
def draw_pipes(pipes):

    for pipe in pipes:
        if pipe.bottom >= 730:
            screen.blit(pipe_surface, pipe)

        else:
            flipped_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flipped_pipe,pipe )
def check_collision(pipes):
    global hit, die
    for pipe in pipes:
        if player_rect.colliderect(pipe):
            hit.play()
           
            return False
    if player_rect.top <= -100 or player_rect.bottom >= 670:
        die.play()
        return False
    return True
def rotate_bird(bird):
    new_player = pygame.transform.rotozoom(player,-bird_movement*2, 1)
    return new_player
pygame.init()
screen = pygame.display.set_mode((450,730))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
background_surface = pygame.image.load("flappy_bird_BG.png")
final_bg=pygame.transform.scale(background_surface,(450,730))
first_ground = pygame.image.load('flappy_ground_final.png')
final_first_ground = pygame.transform.scale(first_ground,(450,130))
loading_message = pygame.image.load("loading_screen.png")
loading_message = pygame.transform.scale(loading_message,(300,390))
player_x = 0
player = pygame.image.load('flapbird_img.png')
player= pygame.transform.scale(player,(70,50))
player_rect = player.get_rect(center = (78.125,70))
gravity = .25
bird_movement = 0
pipe_surface = pygame.image.load('pipe_flap_bird.png')
pipe_surface = pygame.transform.scale(pipe_surface,(50,550))
pipe_list= []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,500,600]
active = False
score = 0
font = pygame.font.Font('04B_19.TTF', 40)
high_score = 0
flap_sound = pygame.mixer.Sound('sound_sfx_wing.wav')
point_sound = pygame.mixer.Sound('sound_sfx_point.wav')
hit = pygame.mixer.Sound('sound_sfx_hit.wav')
die = pygame.mixer.Sound('sound_sfx_die.wav')
score_time = pygame.USEREVENT
pygame.time.set_timer(score_time,1141)
credits_surface = font.render('neutrino', True , (255,255,255))
credits_surface = pygame.transform.scale(credits_surface,(75,30))
credits_rect = credits_surface.get_rect(topleft = (0,640))

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type  == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                bird_movement = 0
                bird_movement-= 9
                flap_sound.play()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == score_time and active == True:
            point_sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and active == False or event.key == pygame.K_UP and active == False:
                active = True
                bird_movement = 0
                pipe_list.clear()
                player_rect.center = 78.125, 70
                score = 0
     # Game backgrounds
    screen.blit(final_bg, (0, 0))
    # ground
    if active == False:
        check_score()
        high_score_surface = font.render(f'High score: {str(int(high_score))}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(220,600))
        screen.blit(loading_message, (70,150))
        screen.blit(high_score_surface, high_score_rect)
    if active:
        
        # bird
        active_score( )
        bird_movement += gravity
        new_player = rotate_bird(player)
        player_rect.centery += bird_movement
        screen.blit(new_player, player_rect)
      
     
            
      
        score+=0.01
       
       
         # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        move_pipes(pipe_list)
        if check_collision(pipe_list) == False:
            active = False
    draw_ground()
    screen.blit(credits_surface,credits_rect)
    pygame.display.update()
    clock.tick(120)
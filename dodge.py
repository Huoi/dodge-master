#IMPORT STUFF
import pygame
import time
import random


#INITIALIZING GAME
pygame.init()
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


#CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (150, 75, 0)
GREEN = (0, 100, 0)
GREEN2 = (0, 150, 0)
BLUE = (0, 0, 100)
BLUE2 = (0, 0, 150)


#LOAD IMAGES
rocket_img = pygame.image.load('rocket.png')
rocket_width = 63
rocket_img = pygame.transform.scale(rocket_img, (rocket_width, 133))
icon_img = pygame.image.load('icon.png')

#LOAD SOUNDS
crash_sfx = pygame.mixer.Sound('crash.wav')
pygame.mixer.music.load('music.wav')

#SET CAPTION AND CLOCK AND ICON
pygame.display.set_caption('Dodge Master')
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()

#SET GLOBAL VARIABLES
pause = False


#FUNCTIONS


#SCORE
def things_dodged(count):
    font = pygame.font.SysFont('agencyfb', 25)
    text = font.render('Score: ' + str(count), True, WHITE)
    game_display.blit(text, (10,10))


    
#DRAW OBSTACLE
def things(thingx, thingy, thingw, thingh, col):
    pygame.draw.rect(game_display, col, [thingx, thingy, thingw, thingh])



#DISPLAY ROCKET
def display_rocket(x,y):  
    game_display.blit(rocket_img,(x,y))



#MESSAGE DISPLAY
def text_objects(text,font):  
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()



#CRASHED FUNCTION
def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sfx)
    
    large_text = pygame.font.SysFont('monospace', 80)
    text_surf, text_rect = text_objects('Game Over', large_text)
    text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 3))
    game_display.blit(text_surf, text_rect)
    
    while True:       
        for event in pygame.event.get():           
            #print(event)
            if event.type == pygame.QUIT:   
                pygame.quit()
                quit()
                
        #game_display.fill(BLACK)

        button('Play Again', 200, 75, DISPLAY_WIDTH / 2 - 200 / 2, DISPLAY_HEIGHT / 1.5, GREEN, GREEN2, 30, 'start')
        
        pygame.display.update()
        clock.tick(15)




#BUTTON FUNCTION  
def button(msg, width, height, x, y, inactive_col, active_col, text_size, action = None):    
    mouse_pos = pygame.mouse.get_pos()
    #print(mouse_pos)
    
    click = pygame.mouse.get_pressed()
    #print(click)

    btn_width = width
    btn_height = height
    btnx = x
    btny = y

    if btnx + btn_width > mouse_pos[0] > btnx and btny + btn_height > mouse_pos[1] > btny:        
        pygame.draw.rect(game_display, active_col, (btnx, btny, btn_width, btn_height))
        
        if click[0] == 1 and action != None:            
            if action == 'start':                
                game_loop()
            elif action == 'resume':
                resume()
                
    else:
        pygame.draw.rect(game_display, inactive_col, (btnx, btny, btn_width, btn_height))

    small_text = pygame.font.SysFont('agencyfb', 30)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((btnx + btn_width / 2), (btny + btn_height / 2))
    game_display.blit(text_surf, text_rect)



#PAUSE AND RESUME FUNCTION
def paused():
    pygame.mixer.music.pause()
    
    large_text = pygame.font.SysFont('monospace', 80)
    text_surf, text_rect = text_objects('Game Paused', large_text)
    text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 3))
    game_display.blit(text_surf, text_rect)
    
    while pause:       
        for event in pygame.event.get():           
            #print(event)
            if event.type == pygame.QUIT:   
                pygame.quit()
                quit()
                
        #game_display.fill(BLACK)        

        button('Resume', 200, 75, DISPLAY_WIDTH / 2 - 200 / 2, DISPLAY_HEIGHT / 1.5, GREEN, GREEN2, 30, 'resume')
        
        pygame.display.update()
        clock.tick(15)


def resume():
    global pause
    pygame.mixer.music.unpause()
    pause = False


    
#GAME INTRO   
def game_intro():   
    intro = True

    while intro:
        
        for event in pygame.event.get():
           
            #print(event)
            if event.type == pygame.QUIT:   
                pygame.quit()
                quit()
                
        game_display.fill(BLACK)
        
        large_text = pygame.font.SysFont('monospace', 80)
        text_surf, text_rect = text_objects('Dodge Master', large_text)
        text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 3))
        game_display.blit(text_surf, text_rect)

        button('Start Game', 200, 75, DISPLAY_WIDTH / 2 - 200 / 2, DISPLAY_HEIGHT / 1.5, GREEN, GREEN2, 30, 'start')
        
        pygame.display.update()
        clock.tick(60)



#MAIN GAME LOOP   
def game_loop():   
    global pause

    pygame.mixer.music.play(-1)
    
    x = (DISPLAY_WIDTH * 0.45)
    y = (DISPLAY_HEIGHT * 0.75)

    speed = 10
    x_change = 0

    thing_startx = random.randrange(0, DISPLAY_WIDTH)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100

    dodged = 0
    
    game_exit = False
    
    while not game_exit:        
        #print(event)
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:        
                pygame.quit()
                quit()

            #CONTROLS
            if event.type == pygame.KEYDOWN:             
                if event.key == pygame.K_LEFT:
                    x_change = speed * -1
                    
                if event.key == pygame.K_RIGHT:
                    x_change = speed

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    pause = True
                    paused()
                
            if event.type == pygame.KEYUP:                
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        x += x_change

        game_display.fill(BLACK)
        
        things(thing_startx, thing_starty, thing_width, thing_height, BROWN)
        thing_starty += thing_speed
        
        display_rocket(x,y)

        things_dodged(dodged)
        
        if x > DISPLAY_WIDTH - rocket_width or x < 0:
            crash()

        if thing_starty > DISPLAY_HEIGHT:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, DISPLAY_WIDTH - thing_width)
            dodged += 1
            thing_speed += 1

        if y < thing_starty + thing_height:
            if thing_startx < x + rocket_width and thing_startx + thing_width > x:
                crash()
            
        clock.tick(60)
        pygame.display.update()

        
        
#OUT OF GAME LOOP
game_intro()
game_loop()
pygame.quit()
quit()

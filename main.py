import pygame
import time
import random
import os
from orcs import Orc
from projectileFile import Projectile
from playerFile import Player
from leaderboard import load_leaderboard, update_leaderboard, is_top_score

pygame.font.init()
pygame.mixer.init()

#Sound Effects
shoot_sound = pygame.mixer.Sound('Audio/shootSound.mp3')
hit_sound = pygame.mixer.Sound('Audio/playerGameOver.mp3')

#Background Sound
dungeon_sound = pygame.mixer.Sound('Audio/dungeonAir.mp3')
song = pygame.mixer.Sound('Audio/pixelSong1.mp3')

#Volume
shoot_sound.set_volume(0.03)
hit_sound.set_volume(0.4)
dungeon_sound.set_volume(0.5)
song.set_volume(0.075)

WIDTH, HEIGHT = 1000, 800
FULLSCREEN = False

os.environ['SDL_VIDEO_CENTERED'] = '1' #Centers the window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escaping Orcs")

BG = pygame.transform.scale(pygame.image.load("Stone Background.jpg"), (WIDTH, HEIGHT))

#Wizard Creation
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 90
PLAYER_VEL = 4

#Orc Creation
ORC_WIDTH = 65
ORC_HEIGHT = 85
ORC_VEL = 3

#orginal dimensions for scaling
original_width = WIDTH  
original_height = HEIGHT
original_player_width = PLAYER_WIDTH
original_player_height = PLAYER_HEIGHT
original_orc_width = ORC_WIDTH
original_orc_height = ORC_HEIGHT

picture = pygame.transform.scale(pygame.image.load("Gandalf.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
orc_image = pygame.image.load("orc.png").convert_alpha()
stronger_orc_image =  pygame.image.load("strongerOrc.png").convert_alpha()

FONT = pygame.font.SysFont("comicsans", 30)

pygame.event.set_grab(True) #Confine mouse cursor to game window
    
def scale_objects(player,orcs):
    global PLAYER_WIDTH, PLAYER_HEIGHT, ORC_WIDTH, ORC_HEIGHT, picture, BG, WIN
    scale_factor = min(WIDTH / original_width, HEIGHT / original_height)

    PLAYER_WIDTH = int(original_player_width * scale_factor)
    PLAYER_HEIGHT = int(original_player_height * scale_factor)
    ORC_WIDTH = int(original_orc_width * scale_factor)
    ORC_HEIGHT = int(original_orc_height * scale_factor)

    picture = pygame.transform.scale(pygame.image.load("Gandalf.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
    orc_image = pygame.transform.scale(pygame.image.load("orc.png").convert_alpha(),(ORC_WIDTH,ORC_HEIGHT))
    stronger_orc_image = pygame.transform.scale(pygame.image.load("strongerOrc.png").convert_alpha(),(ORC_WIDTH,ORC_HEIGHT))

    player.scale(scale_factor)

    for orc in orcs:
        orc.scale(scale_factor)

    BG = pygame.transform.scale(pygame.image.load("Stone Background.jpg"), (WIDTH, HEIGHT)) #resize background

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def draw(player, elapsed_time, orcs, projectiles):
    WIN.blit(BG, (0,0))
    time_text = FONT.render(f"Survived: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10,10))
    player.draw(WIN, picture)

    for orc in orcs:   
        orc.draw(WIN)

    for projectile in projectiles:
        projectile.draw(WIN)

    pygame.display.update()

def check_collision(player, orcs):
    for orc in orcs:
        if player.rect.colliderect(orc.hitbox):
            return True
    return False

def draw_game_over(elapsed_time, leaderboard):
    WIN.fill((0,0,0,128)) #Darken the Screen
    pygame.draw.rect(WIN, (255,0,0), (350,300,300,50)) #Play Again Button
    pygame.draw.rect(WIN, (255,0,0,0), (350, 400, 300, 50)) #Exit Game Button
    play_again_text = FONT.render("Play Again?", 1, (255,255,255))
    exit_game_text = FONT.render("Exit Game", 1, (255,255,255))
    WIN.blit(play_again_text, (450, 310))
    WIN.blit(exit_game_text, (450, 410))

    #LEADERBOARD
    leaderboard_text = FONT.render("Leaderboard", 1, (255, 255, 255))
    WIN.blit(leaderboard_text, (700, 50))
    for i, entry in enumerate(leaderboard):
        entry_text = FONT.render(f"{i+1}. {entry['name']} - {round(entry['time'], 2)}s", 1, (255, 255, 255))
        WIN.blit(entry_text, (700, 100 + i*30))

    pygame.display.update()


def pause_game():
    WIN.fill((0,0,0,128)) # Darken the Screen
    pause_text = FONT.render("Game Paused", 1, (255,255,255))
    pygame.draw.rect(WIN, (255,0,0), (350,250,300,50)) # Continue Button
    pygame.draw.rect(WIN, (255,0,0), (350,320,300,50)) #Visual Settings Button
    pygame.draw.rect(WIN, (255,0,0), (350,400,300,50)) # Quit Game Button
    continue_text = FONT.render("Continue", 1, (255,255,255))
    visual_settings_text = FONT.render("Visual Settings", 1,(255,255,255))
    quit_text = FONT.render("Quit Game", 1, (255,255,255))
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 200))
    WIN.blit(continue_text, (450, 260))
    WIN.blit(visual_settings_text, (420,330))
    WIN.blit(quit_text, (450, 410))
    pygame.display.update()

def draw_visual_settings():
    WIN.fill((0,0,0,128))  #Darken the screen
    settings_text = FONT.render("Visual Settings", 1, (255,255,255))
    pygame.draw.rect(WIN, (255,0,0), (350,250,300,50)) #fullscreen/windowed
    pygame.draw.rect(WIN, (255,0,0), (350,320,300,50)) # 640x360 Button
    pygame.draw.rect(WIN, (255,0,0), (350,390,300,50)) # 1280x720 Button
    pygame.draw.rect(WIN, (255,0,0), (350,460,300,50)) # 1920x1080 Button
    back_text = FONT.render("Back", 1, (255,255,255))
    toggle_fullscreen_text = FONT.render("Fullscreen Toggle", 1, (255,255,255))
    res_640x360_text = FONT.render("640x360", 1,(255,255,255))
    res_1280x720_text = FONT.render("1280x720", 1, (255,255,255))
    res_1920x1080_text = FONT.render("1920x1080", 1, (255,255,255))
    WIN.blit(settings_text, (WIDTH // 2 - settings_text.get_width() //2, 150))
    WIN.blit(toggle_fullscreen_text, (WIDTH // 2 - toggle_fullscreen_text.get_width() // 2, 260))
    WIN.blit(res_640x360_text, (450,330))
    WIN.blit(res_1280x720_text, (450,400))
    WIN.blit(res_1920x1080_text, (450,470))
    pygame.display.update()

def main():
    global WIN, WIDTH, HEIGHT, FULLSCREEN, BG

    dungeon_sound.play(-1)
    song.play(-1)

    run = True
    paused = False
    visual_settings = False
    player = Player(500, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    orc_add_increment = 4000
    orc_count = 0
    orcs = []
    projectiles = []
    game_over = False

    spawn_stronger_orcs_15_sec = False
    spawn_stronger_orcs_3_min = False

    while run:
        if not game_over and not paused and not visual_settings:
            pygame.event.set_grab(True)
            orc_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if elapsed_time > 90 and not spawn_stronger_orcs_3_min:
                spawn_stronger_orcs_3_min = True

           # if elapsed_time > 90:
                #orc.vel = orc.vel * 1.7

            if elapsed_time > 15 and not spawn_stronger_orcs_15_sec: #Add stronger orc at 15 seconds
                spawn_stronger_orcs_15_sec = True

            if orc_count >= orc_add_increment:
                if elapsed_time < 30:
                    num_orcs_to_spawn = 2
                elif elapsed_time >= 30 and elapsed_time < 60:
                    num_orcs_to_spawn = 3
                elif elapsed_time >= 60 and elapsed_time < 120:
                    num_orcs_to_spawn = 4
                elif elapsed_time >= 120 and elapsed_time < 240:
                    num_orcs_to_spawn = 5
                    for orc in orcs:
                        orc.vel = 2
                else:
                    num_orcs_to_spawn = 5 + int(elapsed_time - 240 // 60) #Number of orcs to add to make game harder

                for _ in range(num_orcs_to_spawn):
                    if random.choice([True, False]): #orc spawn offscreen
                        orc_x = random.choice([-ORC_WIDTH, WIDTH])
                        orc_y = random.randint(-ORC_HEIGHT, HEIGHT)
                    else:
                        orc_x = random.randint(-ORC_WIDTH, WIDTH)
                        orc_y = random.choice([-ORC_HEIGHT, HEIGHT])

                    if spawn_stronger_orcs_15_sec and not spawn_stronger_orcs_3_min:
                        if random.random() < 0.2:  # 20% chance to spawn a stronger orc
                            orcs.append(Orc(orc_x, orc_y, color=(0, 255, 0), hp=5, image=stronger_orc_image, stronger_orc=True))
                        else:
                            orcs.append(Orc(orc_x, orc_y, color=(0, 255, 0), hp=3, image=orc_image))
                    elif spawn_stronger_orcs_3_min:
                        if random.random() < 0.4:  # 40% chance to spawn a stronger orc
                            orcs.append(Orc(orc_x, orc_y, color=(0, 255, 0), hp=5, image=stronger_orc_image, stronger_orc=True))
                        else:
                            orcs.append(Orc(orc_x, orc_y, color=(0, 255, 0), hp=3, image=orc_image))
                    else:
                        orcs.append(Orc(orc_x, orc_y, color=(0,255,0), hp = 3, image=orc_image))

                orc_count = 0
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = True
                if event.type ==  pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()               #AIMING
                    projectiles.append(Projectile(player.x + player.width // 2,player.y + player.height // 2, mouse_x, mouse_y))
                    shoot_sound.play()

            #Movement Keys
            keys = pygame.key.get_pressed()
            player.move(keys, WIDTH, HEIGHT)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x = max(0, min(WIDTH, mouse_x))
            mouse_y = max(0, min(HEIGHT, mouse_y))
            pygame.mouse.set_pos(mouse_x,mouse_y)
            
            #Move orcs toward player
            for orc in orcs:
                orc.move_towards_player(player)

            #Shooting
            for projectile in projectiles[:]:
                projectile.move()
                if projectile.rect.left > WIDTH or projectile.rect.right < 0 or projectile.rect.top > HEIGHT or projectile.rect.bottom < 0:
                    projectiles.remove(projectile)

                else:
                    for orc in orcs[:]:
                        if projectile.rect.colliderect(orc.hitbox):
                            orc.hp -= 1
                            if orc.hp <= 0:
                                orcs.remove(orc)
                            projectiles.remove(projectile)
                            break

            #Collision = Game Over
            if check_collision(player, orcs):
                hit_sound.play()
                game_over = True
                
            draw(player, elapsed_time, orcs, projectiles)
        elif paused:
            pygame.event.set_grab(False)
            pygame.mixer.pause()
            pause_game()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False
                    pygame.mixer.unpause()
                    pygame.event.set_grab(True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 350 <= mouse_x <= 650 and 250 <= mouse_y <= 300:
                        # Continue button clicked
                        paused = False
                        pygame.mixer.unpause()
                        pygame.event.set_grab(True)
                    elif 350 <= mouse_x <= 650 and 320 <= mouse_y <= 370:
                        #Visual Settings button clicked
                        visual_settings = True
                        paused = False
                        pygame.mixer.unpause()
                    elif 350 <= mouse_x <= 650 and 400 <= mouse_y <= 450:
                        # Quit Game button clicked
                        run = False
        elif visual_settings:
            pygame.event.set_grab(False)
            pygame.mixer.pause()
            draw_visual_settings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                     run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    visual_settings = False
                    pygame.mixer.unpause()
                    pygame.event.set_grab(True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 350 <= mouse_x <= 650 and 250 <= mouse_y <= 300:  #ToggleFullscreen
                        FULLSCREEN = not FULLSCREEN
                        if FULLSCREEN:
                            WIN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
                        else:
                            WIN = pygame.display.set_mode((WIDTH,HEIGHT))
                        BG = pygame.transform.scale(pygame.image.load("Stone Background.jpg"), (WIDTH, HEIGHT))
                    elif 350 <= mouse_x <= 650 and 320 <= mouse_y <= 370:   #640x360
                        WIDTH, HEIGHT = 640,360
                        WIN = pygame.display.set_mode((WIDTH,HEIGHT))
                        scale_objects(player, orcs)
                        BG = pygame.transform.scale(pygame.image.load("Stone Background.jpg"), (WIDTH, HEIGHT))
                        visual_settings = False
                        pygame.mixer.unpause()
                    elif 350 <= mouse_x <= 650 and 390 <= mouse_y <= 440:
                        # 1280x720 button clicked
                        WIDTH, HEIGHT = 1280, 720
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                        scale_objects(player, orcs)
                        BG = pygame.transform.scale(pygame.image.load("Stone Background.jpg"), (WIDTH, HEIGHT))
                        visual_settings = False
                        pygame.mixer.unpause()
                    elif 350 <= mouse_x <= 650 and 460 <= mouse_y <= 510:
                        # 1920x1080 button clicked
                        WIDTH, HEIGHT = 1920, 1080
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                        scale_objects(player, orcs)
                        BG = pygame.transform.scale(pygame.image.load("Stone Background.jpg"), (WIDTH, HEIGHT))
                        visual_settings = False
                        pygame.mixer.unpause()
                    elif 10 <= mouse_x <= 110 and 10 <= mouse_y <= 60:
                        # Back button clickeda
                        visual_settings = False
                        pygame.mixer.unpause()
                        pygame.event.set_grab(True)
        else:
            leaderboard = load_leaderboard()
            if is_top_score(elapsed_time):
                if player.name is None:
                    player.name = player.get_player_name(WIN, FONT)
                if player.name:
                    leaderboard = update_leaderboard(player.name, elapsed_time)

            draw_game_over(elapsed_time, leaderboard)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 350 <= mouse_x <= 650 and 300 <= mouse_y <= 350:
                        # Play Again button clicked
                        main()  # Restart the game
                    elif 350 <= mouse_x <= 650 and 400 <= mouse_y <= 450:
                        # Exit Game button clicked
                        run = False

    pygame.mixer.stop()
    pygame.quit()

if __name__ == "__main__":
    main()

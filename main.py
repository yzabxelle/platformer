import pygame, sys, os, random
import data.engine as e
from pygame.locals import *

clock = pygame.time.Clock()

def main():
    pygame.init()

    # Window Settings
    TITLE = "Platformer"
    WINDOW_SIZE = (600, 400)
    FPS = 60

    window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pygame.Surface((300, 200))
    pygame.display.set_caption(TITLE)

    # Colors
    BG_COLOR = (0, 48, 59)
    WHITE = (255, 255, 255)

    # Tile Loading
    tile_img = pygame.image.load('data/images/tiles/tile.png')
    top_right_img = pygame.image.load('data/images/tiles/top_right.png')
    top_left_img = pygame.image.load('data/images/tiles/top_left.png')
    bot_right_img = pygame.image.load('data/images/tiles/bot_right.png')
    bot_left_img = pygame.image.load('data/images/tiles/bot_left.png')
    key_img = pygame.image.load('data/images/tiles/key.png')
    TILE_SIZE = 16
    background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]\

    # Animations + Load Objects
    e.load_animations('data/images/entities/')
    player = e.entity(200,100,14,16,'player')
    enemies = []
    keys = []

    # Movement + Physics
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    true_scroll = [0, 0]

    #Player Info
    player_alive = True
    player_level = 0

    enemy_distance = 300
    for i in range(2):
        enemies.append([0, e.entity(enemy_distance, 80, 16, 14, 'enemy')])
        enemy_distance += 100

    def load_map(path):
        game_map = []
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        for row in data:
            game_map.append(list(row))
        return game_map

    game_map = load_map('map')

    while True:
        if player_alive == True:
            display.fill(BG_COLOR)

            true_scroll[0] += (player.x - true_scroll[0] - 158)/20
            true_scroll[1] += (player.y - true_scroll[1] - 107)/20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            pygame.draw.rect(display,(255, 119, 119),pygame.Rect(0,120,300,80))
            for background_object in background_objects:
                obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], background_object[1][1] - scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
                if background_object[0] == 0.5:
                    pygame.draw.rect(display, (255, 163, 135), obj_rect)
                else:
                    pygame.draw.rect(display, (255, 119, 119), obj_rect)

            tile_rects = []
            y = 0
            for row in game_map:
                x = 0
                for tile in row:
                    if tile == '1':
                        display.blit(tile_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '2':
                        display.blit(top_right_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '3':
                        display.blit(top_left_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '4':
                        display.blit(bot_right_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '5':
                        display.blit(bot_left_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '6':
                        display.blit(key_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile != '0' and tile != 'i':
                        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    x += 1
                y += 1

            player_movement = [0, 0]
            if moving_right == True:
                player_movement[0] += 2
            if moving_left == True:
                player_movement[0] -= 2
            player_movement[1] += vertical_momentum
            vertical_momentum += 0.2
            if vertical_momentum > 3:
                vertical_momentum = 3

            if player_movement[0] == 0:
                player.set_action('idle')
            if player_movement[0] > 0:
                player.set_flip(False)
                player.set_action('run')
            if player_movement[0] < 0:
                player.set_flip(True)
                player.set_action('run')

            collision_types = player.move(player_movement, tile_rects)

            if collision_types['bottom'] == True:
                air_timer = 0
                vertical_momentum = 0
            else:
                air_timer += 1

            player.change_frame(1)
            player.display(display, scroll)

            display_r = pygame.Rect(scroll[0], scroll[1], 300, 200)

            for enemy in enemies:
                if display_r.colliderect(enemy[1].obj.rect):
                    enemy[0] += 0.2
                    if enemy[0] > 3:
                        enemy[0] = 3
                    enemy_movement = [0,enemy[0]]
                    if player.x > enemy[1].x + 5:
                        enemy_movement[0] = 1
                    if player.x < enemy[1].x - 5:
                        enemy_movement[0] = -1
                    collision_types = enemy[1].move(enemy_movement,tile_rects)
                    if collision_types['bottom'] == True:
                        enemy[0] += 0

                    enemy[1].display(display,scroll)

                    if player.obj.rect.colliderect(enemy[1].obj.rect):
                        player_alive = False

        else:
            display.fill(WHITE)    
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving_right = True
                if event.key == K_a:
                    moving_left = True
                if event.key == K_w:
                    if air_timer < 5:
                        vertical_momentum = -5
                if event.key == K_ESCAPE and player_alive == False:
                    player_alive = True
                    main()
                if event.key == K_q:
                    player_alive = False
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False
    
        window.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
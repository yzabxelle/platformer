from numpy import rec
import pygame, sys
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

    # Object Loading
    tile_img = pygame.image.load('tile.png')
    top_right_img = pygame.image.load('top_right.png')
    top_left_img = pygame.image.load('top_left.png')
    bot_right_img = pygame.image.load('bot_right.png')
    bot_left_img = pygame.image.load('bot_left.png')
    TILE_SIZE = 16
    background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]\

    # Animations + Load 

    player_action = 'idle'
    player_frame = 0
    player_flip = False
    global animation_frames 
    animation_frames = {}
    animation_database = {}

    # Movement + Physics
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    true_scroll = [0, 0]

    #Player Info
    player_alive = True
    player_level = 0
    
    player_rect = pygame.Rect(100,100,14,16)

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

    def load_animation (path, frame_durations):
        global animation_frames 
        animation_name = path.split('/') [-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + "_" + str(n)
            img_location = path + "/" + animation_frame_id + '.png'
            animation_img = pygame.image.load(img_location).convert()
            animation_img.set_colorkey(WHITE)
            animation_frames[animation_frame_id] = animation_img.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    def change_action(action_var, frame, new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame

    #animation_database['run'] = load_animation('player/run', [7, 7])
    animation_database['idle'] = load_animation('player/idle', [7, 7, 40])

    def collision_test(rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(rect, movement, tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        rect.x += movement[0]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types

    while True:
        if player_alive == True:
            display.fill(BG_COLOR)

            true_scroll[0] += (player_rect.x - true_scroll[0] - 158)/20
            true_scroll[1] += (player_rect.y - true_scroll[1] - 107)/20
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
                    if tile != '0':
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

            if player_movement[0] > 0:
                #player_action, player_frame = change_action(player_action, player_frame, 'run')
                player_flip = False
            if player_movement[0] == 0:
                player_action, player_frame = change_action(player_action, player_frame, 'idle')
            if player_movement[0] < 0:
                #player_action, player_frame = change_action(player_action, player_frame, 'run')
                player_flip = True
            #if vertical_momentum > 0:
                #player_action, player_frame = change_action(player_action, player_frame, 'jump')

            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            if collisions['bottom'] or collisions['top']:
                vertical_momentum = 0
                air_timer = 0
            else:
                air_timer += 1

            player_frame += 1
            if player_frame >= len(animation_database[player_action]):
                player_frame = 0
            player_img_id = animation_database[player_action] [player_frame]
            player_img = animation_frames[player_img_id]
            display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))

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

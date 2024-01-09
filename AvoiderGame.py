import sys, pygame, math, random

# Starter code for an avoider game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors: Sasha Rybalkina
#
#

def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one contacts the other.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap

def level_one():
    # background data
    blue_map = pygame.image.load("blue_level.png")
    blue_map_size = blue_map.get_size()
    blue_screen = pygame.display.set_mode(blue_map_size)
    blue_map = blue_map.convert_alpha()
    blue_map_rect = blue_map.get_rect()
    blue_map.set_colorkey((255, 255, 255))
    blue_map_mask = pygame.mask.from_surface(blue_map)

    # Create the player data
    player = pygame.image.load("cute_cat.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (75, 75))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # enemy data
    enemy1 = pygame.image.load("dog.png").convert_alpha()
    enemy1 = pygame.transform.smoothscale(enemy1, (120, 100))
    enemy1_rect = enemy1.get_rect()
    enemy1_mask = pygame.mask.from_surface(enemy1)
    enemy1_rect.center = (200, 300)

    # start label data
    start_label = pygame.image.load("start.png").convert_alpha()
    start_label = pygame.transform.smoothscale(start_label, (70, 70))
    start_label_rect = start_label.get_rect()
    start_label_mask = pygame.mask.from_surface(start_label)
    start_label_rect.center = (150, 560)

    # end goal
    ice_cream = pygame.image.load("ice_cream2.png").convert_alpha()
    ice_cream = pygame.transform.smoothscale(ice_cream, (85, 120))
    ice_cream_rect = ice_cream.get_rect()
    ice_cream_mask = pygame.mask.from_surface(ice_cream)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The first font is used for the game over message
    myfont = pygame.font.SysFont('monospace', 100)

    # The second font is for hints
    myfont2 = pygame.font.SysFont('monospace', 25)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if the player has touched a wall or the enemy
    is_alive = True

    # This state variable shows whether the key is found yet or not
    found_ice_cream = False

    # This state variable shows whether the player has touched anything they weren't supposed to
    game_over = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene

    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if pixel_collision(player_mask, player_rect, start_label_mask, start_label_rect) and event.type == pygame.MOUSEBUTTONDOWN:
                started = True
            if found_ice_cream:
                started = False

        # Position the player to the mouse location
        if game_over == False:
            pos = pygame.mouse.get_pos()
            player_rect.center = pos

        '''
        Ensures the player isn't able to cheat and get to the rectangle of the end goal until
        the game starts
        '''
        if started == False:
            ice_cream_rect.center = (1000,1000)
        if started == True:
            ice_cream_rect.center = (440, 80)

        if not found_ice_cream and pixel_collision(player_mask, player_rect, ice_cream_mask, ice_cream_rect):
            found_ice_cream = True

        if game_over == False and started == True:
            for moves in range(2):
                enemy1_rect.move_ip((1, 0))

        # Draw the background
        blue_screen.fill((250, 250, 250))
        blue_screen.blit(blue_map, blue_map_rect)

        '''
        These two functions are responsible for displaying a game_over message and preventing further
        progress if the player touches a wall or the cute yet deadly enemy
        '''
        if started == True and pixel_collision(player_mask, player_rect, blue_map_mask, blue_map_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            blue_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        if started == True and pixel_collision(player_mask, player_rect, enemy1_mask, enemy1_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            blue_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        # Only draw the walls and enemies if the key is not collected
        if not found_ice_cream and started == True:
            blue_screen.blit(ice_cream, ice_cream_rect)
            blue_screen.blit(enemy1, enemy1_rect)

        # Draw the start button
        blue_screen.blit(start_label, (150, 560))

        '''
        Here is where I display hints to the player about how the game works, and also give a warning
        about the start button being really close to the walls (I do realize I didn't put the start 
        button in the best place, but that's part of the challenge!)
        '''
        hint = myfont2.render("You might want to avoid the dog...", True, (0, 0, 255))
        blue_screen.blit(hint, (20, 200))

        hint2 = myfont2.render("Oh, and the blue isn't great to hit either", True, (0, 0, 255))
        blue_screen.blit(hint2, (290, 100))

        hint3 = myfont2.render("You have to be careful with the start button", True, (0, 0, 255))
        blue_screen.blit(hint3, (20, 400))

        # Draw the player character
        blue_screen.blit(player, player_rect)

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

        # Makes the level move on to the next level if the player had won.
        if found_ice_cream == True:
            return level_two()

def level_two():
    # Create the map data
    pink_map = pygame.image.load("pink_map.png")
    pink_map_size = pink_map.get_size()
    pink_screen = pygame.display.set_mode(pink_map_size)
    pink_map = pink_map.convert_alpha()
    pink_map_rect = pink_map.get_rect()
    pink_map.set_colorkey((255, 255, 255))
    pink_map_mask = pygame.mask.from_surface(pink_map)

    # Create the player data
    player = pygame.image.load("cute_cat.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (75, 75))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # Create data for the diamond, aka activation of the cake
    diamond = pygame.image.load("diamond.png").convert_alpha()
    diamond = pygame.transform.smoothscale(diamond, (100, 85))
    diamond_rect = diamond.get_rect()
    diamond_mask = pygame.mask.from_surface(diamond)
    diamond_rect.center = (410, 65)

    # Data for the first enemy
    enemy1 = pygame.image.load("foxy.png").convert_alpha()
    enemy1 = pygame.transform.smoothscale(enemy1, (170, 150))
    enemy1_rect = enemy1.get_rect()
    enemy1_mask = pygame.mask.from_surface(enemy1)
    enemy1_rect.center = (50, 250)

    # Data for the second enemy
    enemy2 = pygame.image.load("foxy.gif").convert_alpha()
    enemy2 = pygame.transform.smoothscale(enemy2, (170, 150))
    enemy2_rect = enemy2.get_rect()
    enemy2_mask = pygame.mask.from_surface(enemy2)
    enemy2_rect.center = (800, 200)

    # Create the data for the start button
    start_label = pygame.image.load("start.png").convert_alpha()
    start_label = pygame.transform.smoothscale(start_label, (70, 70))
    start_label_rect = start_label.get_rect()
    start_label_mask = pygame.mask.from_surface(start_label)
    start_label_rect.center = (30, 30)

    # Data for the end goal
    cake = pygame.image.load("cake.png").convert_alpha()
    cake = pygame.transform.smoothscale(cake, (100, 100))
    cake_rect = cake.get_rect()
    cake_mask = pygame.mask.from_surface(cake)
    cake_rect.center = (830, 50)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The first font is used for the game over message
    myfont = pygame.font.SysFont('monospace', 100)

    # The second font is used for hints
    myfont2 = pygame.font.SysFont('monospace', 30)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # This state variable shows whether the end goal is found yet or not
    found_cake = False

    # This state variable shows whether the diamond was found yet or not
    found_diamond = False

    win = False

    game_over = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene

    while is_alive:
        # Check events by looping over the list of events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if pixel_collision(player_mask, player_rect, start_label_mask, start_label_rect) and event.type == pygame.MOUSEBUTTONDOWN:
                started = True
            if pixel_collision(player_mask, player_rect, diamond_mask, diamond_rect):
                found_diamond = True
            if found_cake:
                win = True
                started = False

        # Position the player to the mouse location
        if game_over == False:
            pos = pygame.mouse.get_pos()
            player_rect.center = pos

        # Activates the end goal being found
        if not found_cake and pixel_collision(player_mask, player_rect, cake_mask, cake_rect):
            found_cake = True

        '''
        Only allows the enemies to move if the game has started and the player hasn't lost.
        '''
        if game_over == False and started == True:
            for moves1 in range(2):
                enemy1_rect.move_ip((1, 0))
            for moves2 in range(1):
                enemy2_rect.move_ip((-3, 2))

        # Draw the background
        pink_screen.fill((250, 250, 250))
        pink_screen.blit(pink_map, pink_map_rect)

        '''
        The three functions bellow are responsible for displaying a game over message
        and preventing further progress if the player touches a wall or enemy.
        '''
        if started == True and pixel_collision(player_mask, player_rect, pink_map_mask, pink_map_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            pink_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        if started == True and pixel_collision(player_mask, player_rect, enemy1_mask, enemy1_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            pink_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        if started == True and pixel_collision(player_mask, player_rect, enemy2_mask, enemy2_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            pink_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        # Only draw the diamond and enemies if end goal is not found
        if not found_cake and started:
            pink_screen.blit(diamond, diamond_rect)
            pink_screen.blit(enemy1, enemy1_rect)
            pink_screen.blit(enemy2, enemy2_rect)

        # Only draw the cake if the diamond was found
        if found_diamond == True:
            pink_screen.blit(cake, cake_rect)

        pink_screen.blit(start_label, (30, 30))

        # My hint to the player
        hint = myfont2.render("The diamond unlocks the treat!", True, (150, 0, 0))
        pink_screen.blit(hint, (300, 300))

        # Draw the player character
        pink_screen.blit(player, player_rect)

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

        # Makes the level move on to the next level if the player had won.
        if win == True:
            return level_three()

def level_three():
    # Create the background data
    kiwi_map = pygame.image.load("kiwi_level.png")
    kiwi_map_size = kiwi_map.get_size()
    kiwi_screen = pygame.display.set_mode(kiwi_map_size)
    kiwi_map = kiwi_map.convert_alpha()
    kiwi_map_rect = kiwi_map.get_rect()
    kiwi_map.set_colorkey((255, 255, 255))
    kiwi_map_mask = pygame.mask.from_surface(kiwi_map)

    # Create the player data
    player = pygame.image.load("cute_cat.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (75, 75))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # First enemy data
    enemy1 = pygame.image.load("bunny.png").convert_alpha()
    enemy1 = pygame.transform.smoothscale(enemy1, (144, 120))
    enemy1_rect = enemy1.get_rect()
    enemy1_mask = pygame.mask.from_surface(enemy1)
    enemy1_rect.center = (1000, 400)

    # Second enemy data
    enemy2 = pygame.image.load("bunny2.png").convert_alpha()
    enemy2 = pygame.transform.smoothscale(enemy2, (140, 140))
    enemy2_rect = enemy2.get_rect()
    enemy2_mask = pygame.mask.from_surface(enemy2)
    enemy2_rect.center = (100, 200)

    # Third enemy data
    enemy3 = pygame.image.load("kitty.png").convert_alpha()
    enemy3 = pygame.transform.smoothscale(enemy3, (140, 140))
    enemy3_rect = enemy3.get_rect()
    enemy3_mask = pygame.mask.from_surface(enemy3)
    enemy3_rect.center = (50, 200)

    # Create the start button
    start_label = pygame.image.load("start.png").convert_alpha()
    start_label = pygame.transform.smoothscale(start_label, (70, 70))
    start_label_rect = start_label.get_rect()
    start_label_mask = pygame.mask.from_surface(start_label)
    start_label_rect.center = (450, 550)

    # End goal data
    cup_cake = pygame.image.load("cup_cake.png").convert_alpha()
    cup_cake = pygame.transform.smoothscale(cup_cake, (100, 100))
    cup_cake_rect = cup_cake.get_rect()
    cup_cake_mask = pygame.mask.from_surface(cup_cake)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The first font is used to display the "game over"/"you win" message
    myfont = pygame.font.SysFont('monospace', 100)

    # The second font is used for hints
    myfont2 = pygame.font.SysFont('monospace', 35)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # records if the player has touched what they weren't supposed to
    game_over = False

    # The is_alive variable records if the player touched a wall or enemy
    is_alive = True

    # This state variable shows whether the end goal is found yet or not
    found_cup_cake = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    '''
    And this is where I create the countdown for the player to know that
    they are timed, and how much time they have left.
    '''
    count1 = myfont2.render("1", True, (0, 0, 0))
    count2 = myfont2.render("2", True, (0, 0, 0))
    count3 = myfont2.render("3", True, (0, 0, 0))
    count4 = myfont2.render("4", True, (0, 0, 0))
    count5 = myfont2.render("5", True, (0, 0, 0))
    count6 = myfont2.render("6", True, (0, 0, 0))
    count7 = myfont2.render("7", True, (0, 0, 0))
    count8 = myfont2.render("8", True, (0, 0, 0))
    count9 = myfont2.render("9", True, (0, 0, 0))
    count10 = myfont2.render("10", True, (0, 0, 0))
    count11 = myfont2.render("11", True, (0, 0, 0))
    count12 = myfont2.render("12", True, (0, 0, 0))
    count13 = myfont2.render("13", True, (0, 0, 0))
    count14 = myfont2.render("14", True, (0, 0, 0))
    count15 = myfont2.render("15", True, (0, 0, 0))
    count = [count15, count14, count13, count12, count11, count10, count9, count8, count7, count6, count5, count4, count3, count2, count1]

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if pixel_collision(player_mask, player_rect, start_label_mask, start_label_rect) and event.type == pygame.MOUSEBUTTONDOWN:
                started = True
            if found_cup_cake:
                started = False

        # Position the player to the mouse location
        if game_over == False:
            pos = pygame.mouse.get_pos()
            player_rect.center = pos

        '''
        These if statements ensure that the player cannot cheat and collide with the rectangle
        of the end goal before actually starting the game.
        '''
        if started == False:
            cup_cake_rect.center = (1000, 1000)
        if started == True:
            cup_cake_rect.center = (480, 220)

        '''
        This function only allows the enemies to move when the game has started and
        the player hasn't lost.
        '''
        if game_over == False and started == True:
            for moves1 in range(2):
                enemy1_rect.move_ip((-1, 0))
            for moves2 in range(2):
                enemy2_rect.move_ip((1, 1))
            for moves3 in range(2):
                enemy3_rect.move_ip((1, 0))

        # Activates the end goal being found
        if not found_cup_cake and pixel_collision(player_mask, player_rect, cup_cake_mask, cup_cake_rect):
            found_cup_cake = True

        # Draw the background
        kiwi_screen.fill((250, 250, 250))
        kiwi_screen.blit(kiwi_map, kiwi_map_rect)

        '''
        The four functions below are responsible for displaying a game over message
        and preventing the player from making progress if they touch a wall or an enemy.
        '''

        if started == True and pixel_collision(player_mask, player_rect, kiwi_map_mask, kiwi_map_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            kiwi_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        if started == True and pixel_collision(player_mask, player_rect, enemy1_mask, enemy1_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            kiwi_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        if started == True and pixel_collision(player_mask, player_rect, enemy2_mask, enemy2_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            kiwi_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        if started == True and pixel_collision(player_mask, player_rect, enemy3_mask, enemy3_rect):
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            kiwi_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        '''
        This function displays a message warning the player of their time limit, and 
        displays a second countdown below the message.
        '''
        if found_cup_cake == False and game_over == False:
            hint = myfont2.render("You have 15 seconds!", True, (0, 150, 0))
            kiwi_screen.blit(hint, (375, 340))
            kiwi_screen.blit(count[(frame_count // 30) % 15], (475, 400))

        '''
        This is where I draw enemies and the end goal if the game has started and the
        end goal is not yet found
        '''
        if not found_cup_cake and started == True:
            kiwi_screen.blit(cup_cake, cup_cake_rect)
            kiwi_screen.blit(enemy1, enemy1_rect)
            kiwi_screen.blit(enemy2, enemy2_rect)
            kiwi_screen.blit(enemy3, enemy3_rect)

        # Draw the start label
        kiwi_screen.blit(start_label, (450, 500))

        # Draw the player character
        kiwi_screen.blit(player, player_rect)

        '''
        This puts up a winning label when the level is completed
        '''
        if found_cup_cake:
            win_label = myfont.render("You Win!", True, (0, 175, 255))
            kiwi_screen.blit(win_label, (340, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        '''
        If the frame_count reaches 450, the game over label is displayed and the player
        cannot progress. This is what ensures the time limit displayed by the countdown.
        '''
        frame_count += 1

        if frame_count >= 450:
            game_over = True
            label = myfont.render("Game Over", True, (210, 0, 255))
            kiwi_screen.blit(label, (275, 275))
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_alive = False
                pygame.quit()

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)



def main():

    # Initialize pygame
    pygame.init()
    level_one()


# Start the program
main()

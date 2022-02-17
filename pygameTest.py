import pygame
pygame.init()

# Set up the drawing window
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Othello')
markers = []
player = 1
green = (0,255,0)
red = (255, 0,0)
line_width = 6

def draw_grid():
    color = (50,220,50)
    grid = (50,50,50)
    screen.fill(color)
    for x in range(1, 8):
        pygame.draw.line(screen, grid, (0, x*50), (screen_width, x*50), line_width)
        pygame.draw.line(screen, grid, (x*50, 0), (x*50, screen_height), line_width)
        row = [0] * 8
        markers.append(row)
    # Run until the user asks to quit

def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.circle(screen, green, (x_pos*50 + 25, y_pos*50 + 25), 20, line_width)
                if y ==  -1:
                    pygame.draw.circle(screen, red,( x_pos*50 + 25, y_pos*50 + 25), 20, line_width)
                y_pos+=1
            x_pos+=1
    
running = True
clicked = False
while running:
    draw_grid()
    draw_markers()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicker = False
            pos = pygame.mouse.get_pos()
            cell_x = pos[0]
            cell_y = pos[1]
            if markers[cell_x // 100][cell_y // 100] == 0:
                # this would be where to check if the move is possible
                markers[cell_x // 50][cell_y // 50] = player
                player *= -1
    # Fill the background with white#screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

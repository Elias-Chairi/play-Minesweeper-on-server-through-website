import random
import pygame

pygame.init()

WIDTH, HEIGHT = 550, 650

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

flag_IMG = pygame.image.load("python_pygame/media/flag.png")
flag_IMG = pygame.transform.scale(flag_IMG, (50, 50))
bomb_IMG = pygame.image.load("python_pygame/media/bomb.png")
bomb_IMG = pygame.transform.scale(bomb_IMG, (50, 50))
clock_IMG = pygame.image.load("python_pygame/media/clock.png")
clock_IMG = pygame.transform.scale(clock_IMG, (50, 50))

font = pygame.font.SysFont('Comic Sans MS', 30)

gridRects = []
hover_rect = pygame.Rect
mine_count = 10
mine_count_surface = font.render(str(mine_count), False, "white")
second_count = 0
second_count_surface = font.render(str(second_count), False, "white")

first_reveal = True
marked_bombs = []
grid_bombs = []
bomb_number_grid = []
revealed_grid = []
BOMBCOUNT = 10
no_bombs = False
hit_bomb = False
pygame.time.set_timer(pygame.USEREVENT, 100)

command_file = open("command_files/flask_command.txt","w") #clear file
command_file.write("\n")
command_file.write("\n")
command_file.write("new")
command_file.close()

command_file = open("command_files/pygame_command.txt","w") #clear file
command_file.close()

def create_grid(): #creating the gridlist
    rect_width = 500 / 10
    for y in range (10):
        for x in range (10):
            gridRects.append(pygame.Rect(rect_width/2 + rect_width * x, rect_width/2 + rect_width * y + 100, rect_width, rect_width))


def draw_menu():
    win.blit(flag_IMG, (100, 20)) #flag image
    win.blit(mine_count_surface, (160, 30)) #bomb ammount
    win.blit(clock_IMG, (300, 20)) #clock image
    win.blit(second_count_surface, (360, 30)) #timer


def draw():
    win.fill("black") #black background
    for rect in gridRects:
        if rect == hover_rect:
            pygame.draw.rect(win, "gray", rect) #gray fill when hovering

    for rect in revealed_grid:
        pygame.draw.rect(win, ("white"), rect) #revealed gridbox fill
        rect_index = gridRects.index(rect)
        if bomb_number_grid[rect_index] > 0:
            text_surface = font.render(str(bomb_number_grid[rect_index]), False, "black")
            win.blit(text_surface, (rect.x + 16, rect.y + 2)) #bomb ammount


    for rect in marked_bombs:
        win.blit(flag_IMG, (rect.x, rect.y)) #flag image

    if hit_bomb:
        for rect in grid_bombs:
            pygame.draw.rect(win, "red", rect) #red fill when hit bomb
            win.blit(bomb_IMG, (rect.x, rect.y)) #bomb image
    
    if no_bombs:
        for rect in grid_bombs:
            pygame.draw.rect(win, "green", rect) #green fill on bombs when cleared all spaces


    for rect in gridRects:
        pygame.draw.rect(win, "white", rect, 1) #white border on all grid rects
    
    draw_menu()
    
    pygame.display.update()


def updateHover():
    global hover_rect
    mousePos = pygame.mouse.get_pos()
    for rect in gridRects: # check if mouse is hovering over a grid box
        if mousePos[0] > rect.x and mousePos[0] < rect.x + rect.width and mousePos[1] > rect.y and mousePos[1] < rect.y + rect.height:
            hover_rect = rect
            return
    hover_rect = None


def update_mine_count(flag_change):
    global mine_count
    mine_count += flag_change
    global mine_count_surface
    mine_count_surface = font.render(str(mine_count), False, "white")


def mark_bomb(rect):
    if rect: #if not clicking but got sent command, use this
        global hover_rect
        hover_rect = rect

    if hover_rect: #if hovering over a box
        for rect in marked_bombs:
            if rect == hover_rect: #check if it allready exisists a flag and remove it
                marked_bombs.remove(hover_rect)
                update_mine_count(1)
                send_info()
                return
        for rect in revealed_grid: #dont add a flag if it is a revealed spot
            if rect == hover_rect:
                return
        marked_bombs.append(hover_rect) #add a flag if empty
        update_mine_count(-1)
        send_info()


def create_bombs():
    global first_reveal
    first_reveal = False
    for i in range(BOMBCOUNT):
        create_bomb()

def create_bomb():
    bomb = random.randrange(0, len(gridRects))
    hover_rect_index = gridRects.index(hover_rect)
    for rect in grid_bombs:
        if gridRects[bomb] == rect: #bomb there
            create_bomb()
            return
    if (gridRects[bomb] == hover_rect #the one clicked
        or hover_rect_index % 10 != 0 and gridRects[bomb] == gridRects[hover_rect_index - 1] #left
        or hover_rect_index % 10 != 0 and hover_rect_index > 9 and gridRects[bomb] == gridRects[hover_rect_index - 10 - 1] #top left
        or hover_rect_index > 9 and gridRects[bomb] == gridRects[hover_rect_index - 10] #top
        or int(str(hover_rect_index)[-1]) == 0 and hover_rect_index > 9 and gridRects[bomb] == gridRects[hover_rect_index - 10 + 1] or int(str(hover_rect_index)[-1]) % 9 != 0 and hover_rect_index > 9 and gridRects[bomb] == gridRects[hover_rect_index - 10 + 1] #top right
        or int(str(hover_rect_index)[-1]) == 0 and gridRects[bomb] == gridRects[hover_rect_index + 1] or int(str(hover_rect_index)[-1]) % 9 != 0 and gridRects[bomb] == gridRects[hover_rect_index + 1] #right
        or int(str(hover_rect_index)[-1]) == 0 and hover_rect_index < 90 and gridRects[bomb] == gridRects[hover_rect_index + 10 + 1] or int(str(hover_rect_index)[-1]) % 9 != 0 and hover_rect_index < 90 and gridRects[bomb] == gridRects[hover_rect_index + 10 + 1] #bottom right
        or hover_rect_index < 90 and gridRects[bomb] == gridRects[hover_rect_index + 10] #bottom
        or hover_rect_index % 10 != 0 and hover_rect_index < 90 and gridRects[bomb] == gridRects[hover_rect_index + 10 - 1]): #bottom left)
        create_bomb()
        return
    grid_bombs.append(gridRects[bomb])


def reveal_grid_box(rect):
    if rect: #if not clicking but got sent command, use this
        global hover_rect
        hover_rect = rect
    
    for rect in marked_bombs: #if trying to reveal flag pos, just remove flag
            if rect == hover_rect:
                marked_bombs.remove(hover_rect)
                send_info()
                return

    if hover_rect:
        if first_reveal:
            create_bombs()
            fill_bomb_numbers()
            reveal_visible_grid(hover_rect)
            send_info()
            return

        for rect in grid_bombs:
            if rect == hover_rect:
                global hit_bomb
                hit_bomb = True
                send_info()
                return

        reveal_visible_grid(hover_rect)
        if len(revealed_grid) == len(gridRects) - BOMBCOUNT:
            global no_bombs
            no_bombs = True
        send_info()


def send_info():
    command_file = open("command_files/flask_command.txt","w") #send command
    command_file.write(str(bomb_number_grid))
    command_file.write("\n")
    command_file.write(str(revealed_grid))
    command_file.write("\n")
    command_file.write(str(gridRects))
    command_file.write("\n")
    command_file.write(str(marked_bombs))
    command_file.write("\n")
    command_file.write(str(no_bombs) + " " + str(hit_bomb))
    command_file.close()


def fill_bomb_numbers():
    for rect_index in range(len(gridRects)):
        bombs_nearby = 0
        rect_is_bomb = False

        for bomb in grid_bombs: #check if bomb and quit checking the rest if so
            if bomb == gridRects[rect_index]:
                bombs_nearby += 9
                rect_is_bomb = True
                break

        if rect_is_bomb == False:
            if rect_index % 10 != 0: #left
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index - 1]:
                        bombs_nearby += 1
                        break
            if rect_index % 10 != 0 and rect_index > 9: #top left
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index - 10 - 1]:
                        bombs_nearby += 1
                        break
            if rect_index > 9: #top
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index - 10]:
                        bombs_nearby += 1
                        break
            if int(str(rect_index)[-1]) == 0 and rect_index > 9 or int(str(rect_index)[-1]) % 9 != 0 and rect_index > 9: #top right
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index - 10 + 1]:
                        bombs_nearby += 1
                        break
            if int(str(rect_index)[-1]) == 0 or int(str(rect_index)[-1]) % 9 != 0: #right
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index + 1]:
                        bombs_nearby += 1
                        break
            if int(str(rect_index)[-1]) == 0 and rect_index < 90 or int(str(rect_index)[-1]) % 9 != 0 and rect_index < 90: #bottom right
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index + 10 + 1]:
                        bombs_nearby += 1
                        break
            if rect_index < 90: #bottom
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index + 10]:
                        bombs_nearby += 1
                        break
            if rect_index % 10 != 0 and rect_index < 90: #bottom left
                for bomb in grid_bombs:
                    if bomb == gridRects[rect_index + 10 - 1]:
                        bombs_nearby += 1
                        break

        bomb_number_grid.append(bombs_nearby)

    # show all bombs ↓↓↓
    # for i in range(10):
    #     for j in range(10):
    #         if j == 9:
    #             print(bomb_number_grid[j + i * 10])
    #         else:
    #             print(bomb_number_grid[j + i * 10], end = ' ')
    
    
def reveal_visible_grid(clicked_rect):
    if revealed_grid.count(clicked_rect) == 0: # if not allready exists add it to list
        revealed_grid.append(clicked_rect)

    rect_index = gridRects.index(clicked_rect)

    if bomb_number_grid[rect_index] == 0: #if gridRect is empty, check around...

        if rect_index % 10 != 0: #left
            if bomb_number_grid[rect_index - 1] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index - 1]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index - 1]) # reveal gridbox
                    if bomb_number_grid[rect_index - 1] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index - 1])

        if rect_index % 10 != 0 and rect_index > 9: #top left
            if bomb_number_grid[rect_index - 10 - 1] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index - 10 - 1]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index - 10 - 1]) # reveal gridbox
                    if bomb_number_grid[rect_index - 10 - 1] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index - 10 - 1])
        
        if rect_index > 9: #top
            if bomb_number_grid[rect_index - 10] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index - 10]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index - 10]) # reveal gridbox
                    if bomb_number_grid[rect_index - 10] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index - 10])
        
        if int(str(rect_index)[-1]) == 0 and rect_index > 9 or int(str(rect_index)[-1]) % 9 != 0 and rect_index > 9: #top right
            if bomb_number_grid[rect_index - 10 + 1] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index - 10 + 1]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index - 10 + 1]) # reveal gridbox
                    if bomb_number_grid[rect_index - 10 + 1] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index - 10 + 1])
        
        if int(str(rect_index)[-1]) == 0 or int(str(rect_index)[-1]) % 9 != 0: #right
            if bomb_number_grid[rect_index + 1] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index + 1]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index + 1]) # reveal gridbox
                    if bomb_number_grid[rect_index + 1] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index + 1])
        
        if int(str(rect_index)[-1]) == 0 and rect_index < 90 or int(str(rect_index)[-1]) % 9 != 0 and rect_index < 90: #bottom right
            if bomb_number_grid[rect_index + 10 + 1] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index + 10 + 1]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index + 10 + 1]) # reveal gridbox
                    if bomb_number_grid[rect_index + 10 + 1] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index + 10 + 1])
        
        if rect_index < 90: #bottom
            if bomb_number_grid[rect_index + 10] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index + 10]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index + 10]) # reveal gridbox
                    if bomb_number_grid[rect_index + 10] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index + 10])
        
        if rect_index % 10 != 0 and rect_index < 90: #bottom left
            if bomb_number_grid[rect_index + 10 - 1] != 9: # if not bomb
                if revealed_grid.count(gridRects[rect_index + 10 - 1]) == 0: # check if allready revealed
                    revealed_grid.append(gridRects[rect_index + 10 - 1]) # reveal gridbox
                    if bomb_number_grid[rect_index + 10 - 1] == 0: # if empty run reveal again
                        reveal_visible_grid(gridRects[rect_index + 10 - 1])
    


def main():
    running = True
    create_grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if hit_bomb == False and no_bombs == False:
                if event.type == pygame.USEREVENT: 
                    global second_count #updating timer
                    second_count += 1
                    if second_count % 10 == 0:
                        global second_count_surface
                        second_count_surface = font.render(str(int(second_count / 10)), False, "white")

                    flag_command = False
                    command_file = open("command_files/pygame_command.txt","r") #get command from command file
                    command = command_file.readline()
                    if command == "flag\n":
                        flag_command = True
                        command = command_file.readline()
                    command_file.close()

                    if command != "": #use command if there is one
                        command_file = open("command_files/pygame_command.txt","w") #clear command file
                        command_file.close()

                        if flag_command:
                            mark_bomb(gridRects[int(command)])
                        else:
                            reveal_grid_box(gridRects[int(command)])


                if event.type == pygame.MOUSEMOTION: #check for hover
                    updateHover()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        reveal_grid_box(None)
                    if event.button == 3:
                        mark_bomb(None)
        
        clock.tick(60)
        draw()
    
    pygame.quit()


if __name__ == "__main__":
    main()

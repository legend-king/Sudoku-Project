import pygame
import random
from sudoku import Sudoku
from tkinter import *
from tkinter import messagebox
from pygame import mixer
from tkinter import filedialog
import os

Tk().wm_withdraw()

restart = True
pygame.init()
win = pygame.display.set_mode((575, 650))
win.fill((255, 255, 255))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
buffer = 5
original_grid_element_color = (52, 31, 151)
background_color = (251, 247, 245)
theme = 1

difficulty = 0

click_sound = mixer.Sound('settings_sound.mp3')
insert_sound = mixer.Sound('game_sound.wav')
mixer.music.load('bgm_song.wav')
mixer.music.play(-1)
music_playing = True
click_check = 0

save_folder_exists = False
for folders in os.listdir():
    if folders == 'Game Saves':
        save_folder_exists = True

if not save_folder_exists:
    os.mkdir('Game Saves')


def str_to_array(strr):
    arr = []
    for i in strr:
        if '0' <= i <= '9':
            arr.append(int(i))

    index = 0
    twodarr = [[0 for y in range(9)] for x in range(9)]

    for p in range(9):
        for q in range(9):
            twodarr[p][q] = arr[index]
            index += 1
    return twodarr


gridl = 1
grid_solutionl = 1
ansl = 1
grid_solution_checkerl = 1
grid_originall = 1


def load_game():
    filename = filedialog.askopenfilename(initialdir=os.getcwd() + '\\Game Saves', title="Select you Soduku Save",
                                          filetypes=(("text files", "*.txt"),))
    if filename:
        sf = open(filename, 'r')
        global gridl, grid_solutionl, ansl, grid_solution_checkerl, grid_originall, restart
        gridl = str_to_array(sf.readline())
        grid_solutionl = str_to_array(sf.readline())
        ansl = str_to_array(sf.readline())
        grid_solution_checkerl = str_to_array(sf.readline())
        grid_originall = str_to_array(sf.readline())
        sf.close()
        restart = True
        screen3(0)


def save_count():
    global save_folder_exists
    save_name = 'save0'
    for save_name in os.listdir('Game Saves'):
        pass
    return int(save_name[4]) + 1


def save_game():
    global save_folder_exists
    save_folder_exists = False
    for folders in os.listdir():
        if folders == 'Game Saves':
            save_folder_exists = True

    if not save_folder_exists:
        os.mkdir('Game Saves')

    if save_folder_exists:
        if not os.listdir('Game Saves'):
            sf = open(os.getcwd() + '\\Game Saves\\save1.txt', 'w')
            sf.write(str(grid) + '\n')
            sf.write(str(grid_solution) + '\n')
            sf.write(str(ans) + '\n')
            sf.write(str(grid_solution_checker) + '\n')
            sf.write(str(grid_original) + '\n')
            sf.close()

        elif os.listdir('Game Saves'):
            save_name = 'save0'
            for save_name in os.listdir('Game Saves'):
                pass
            save_number = int(save_name[4]) + 1
            sf = open(os.getcwd() + '\\Game Saves\\save' + str(save_number) + '.txt', 'w')
            sf.write(str(grid) + '\n')
            sf.write(str(grid_solution) + '\n')
            sf.write(str(ans) + '\n')
            sf.write(str(grid_solution_checker) + '\n')
            sf.write(str(grid_original) + '\n')
            sf.close()


class Button:
    def __init__(self, color, x, y, width, height, text='', fontsize=60, textcolor=(0, 0, 0)):
        self.textcolor = textcolor
        self.fontsize = fontsize
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 2)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.fontsize)
            text = font.render(self.text, 1, self.textcolor)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def redrawButton1():
    easy.draw(win, (0, 0, 0))
    medium.draw(win, (0, 0, 0))
    hard.draw(win, (0, 0, 0))
    load_old_game.draw(win, (0, 0, 0))


easy = Button((0, 255, 0), 180, 50, 200, 100, "Easy")
medium = Button((0, 255, 0), 180, 200, 200, 100, "Medium")
hard = Button((0, 255, 0), 180, 350, 200, 100, "Hard")
load_old_game = Button((0, 255, 0), 75, 500, 430, 100, "Load Existing Game")


def screen1():
    global difficulty, restart, click_check
    run = True
    timer = 0
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    direc = 1
    while run:
        if 0 < c1 < 255:
            if direc:
                c1 += 1
            else:
                c1 -= 1

        elif c1 == 255:
            direc = 0
            c1 -= 1
        elif c1 == 0:
            direc = 1
            c1 += 1
        win.fill((c1, c2, c3))
        redrawButton1()
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.isOver(pos):
                    difficulty = 1
                    restart = True
                    click_sound.play(1)
                    screen2()
                if medium.isOver(pos):
                    restart = True
                    difficulty = 2
                    click_sound.play(1)
                    screen2()
                if hard.isOver(pos):
                    difficulty = 3
                    restart = True
                    click_sound.play(1)
                    screen2()
                if load_old_game.isOver(pos):
                    load_game()
                    restart = True
                    click_check = 0
                    click_sound.play(1)

            if event.type == pygame.MOUSEMOTION:
                if easy.isOver(pos):
                    easy.color = (255, 0, 0)
                else:
                    easy.color = (0, 255, 0)

                if medium.isOver(pos):
                    medium.color = (255, 0, 0)
                else:
                    medium.color = (0, 255, 0)

                if hard.isOver(pos):
                    hard.color = (255, 0, 0)
                else:
                    hard.color = (0, 255, 0)

                if load_old_game.isOver(pos):
                    load_old_game.color = (255, 0, 0)
                else:
                    load_old_game.color = (0, 255, 0)


grid1 = 1
grid_solution = 1
grid = 1
grid_original = 1
ans = 1
grid_solution_checker = 1


def redrawButton2():
    theme1.draw(win, (0, 0, 0))
    theme2.draw(win, (0, 0, 0))
    theme3.draw(win, (0, 0, 0))
    back.draw(win, (0, 0, 0))


theme1 = Button((0, 255, 0), 115, 50, 320, 100, "Light Theme")
theme2 = Button((0, 255, 0), 115, 200, 320, 100, "Dark Theme")
theme3 = Button((0, 255, 0), 115, 350, 320, 100, "Custom Theme")
back = Button((0, 255, 0), 115, 500, 320, 100, "BACK")


def screen2():
    global click_check, theme
    run = True
    timer = 0
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    direc = 1
    while run:
        if 0 < c1 < 255:
            if direc:
                c1 += 1
            else:
                c1 -= 1

        elif c1 == 255:
            direc = 0
            c1 -= 1
        elif c1 == 0:
            direc = 1
            c1 += 1

        win.fill((c1, c2, c3))
        redrawButton2()
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if theme1.isOver(pos):
                    click_sound.play(1)
                    click_check = 0
                    theme = 1
                    screen3()
                if theme2.isOver(pos):
                    click_sound.play(1)
                    click_check = 0
                    theme = 2
                    screen3()
                if theme3.isOver(pos):
                    click_sound.play(1)
                    click_check = 0
                    theme = 3
                    screen3()
                if back.isOver(pos):
                    click_sound.play(1)
                    screen1()

            if event.type == pygame.MOUSEMOTION:
                if theme1.isOver(pos):
                    theme1.color = (255, 0, 0)
                else:
                    theme1.color = (0, 255, 0)

                if theme2.isOver(pos):
                    theme2.color = (255, 0, 0)
                else:
                    theme2.color = (0, 255, 0)

                if theme3.isOver(pos):
                    theme3.color = (255, 0, 0)
                else:
                    theme3.color = (0, 255, 0)

                if back.isOver(pos):
                    back.color = (255, 0, 0)
                else:
                    back.color = (0, 255, 0)


def redrawButton3():
    back1.draw(win, (0, 0, 0))
    sol.draw(win, (0, 0, 0))
    hint.draw(win, (0, 0, 0))
    play_pause.draw(win, (0, 0, 0))
    check_answer.draw(win, (0, 0, 0))
    save_button.draw(win, (0, 0, 0))


back1 = Button((0, 255, 0), 25, 550, 150, 75, "BACK", 40)
sol = Button((0, 255, 0), 200, 550, 150, 75, "Solution", 40)
hint = Button((0, 255, 0), 375, 550, 150, 75, "Hint", 40)
play_pause = Button((0, 255, 0), 50, 10, 120, 30, "Music", 25)
check_answer = Button((0, 255, 0), 380, 10, 120, 30, "Check Answer", 25)
hint_count = 3
number_color = (0, 0, 0)
save_button = Button((0, 255, 0), 215, 10, 120, 30, "Save", 25)


def insert(win, position):
    i, j = position[1], position[0]
    if 9 >= i >= 1 and 9 >= j >= 1:
        insert_sound.play(1)
        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if grid_original[i - 1][j - 1] != 0:
                        return
                    if event.key == 48:
                        ans[i - 1][j - 1] = event.key - 48
                        grid_solution_checker[i - 1][j - 1] = event.key - 48
                        pygame.draw.rect(win, background_color, (
                            position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        pygame.display.update()
                        return
                    if 0 < event.key - 48 < 10:
                        pygame.draw.rect(win, background_color, (
                            position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        value = myfont.render(str(event.key - 48), True, number_color)
                        win.blit(value, (position[0] * 50 + 15, position[1] * 50))
                        ans[i - 1][j - 1] = event.key - 48
                        grid_solution_checker[i - 1][j - 1] = event.key - 48
                        pygame.display.update()
                        return
                    return


def insert1(i, j):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    hint_value = grid_solution[i - 1][j - 1]
    pygame.draw.rect(win, background_color, (
        j * 50 + buffer, i * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
    value = myfont.render(str(hint_value), True, (255, 0, 0))
    win.blit(value, (j * 50 + 15, i * 50))
    ans[i - 1][j - 1] = hint_value
    grid_solution_checker[i - 1][j - 1] = hint_value
    insert_sound.play(1)
    pygame.display.update()


def hint_fun():
    for i in range(9):
        for j in range(9):
            if grid_solution_checker[i][j] == 0:
                insert1(i + 1, j + 1)
                return


def screen3(mode=1):
    global grid_solution_checker, ans, grid_original, grid_solution, grid1, grid, restart, music_playing, \
        click_check, number_color, background_color
    if restart:
        if mode == 0:
            grid = gridl
            grid_solution = grid_solutionl
            ans = ansl
            grid_solution_checker = grid_solution_checkerl
            grid_original = grid_originall

        elif mode == 1:
            if difficulty == 1:
                grid1 = Sudoku(3).difficulty(0.35)
            elif difficulty == 2:
                grid1 = Sudoku(3).difficulty(0.5)
            else:
                grid1 = Sudoku(3).difficulty(0.65)
            grid_solution = grid1.solve().board

            grid = grid1.board
            for i in range(9):
                for j in range(9):
                    if grid[i][j] is None:
                        grid[i][j] = 0
            grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
            ans = [[0 for y in range(9)] for x in range(9)]

            grid_solution_checker = [[grid[x][y] for y in range(9)] for x in range(9)]

    if theme == 1:
        play_pause.textcolor = (0, 0, 0)
        back1.textcolor = (0, 0, 0)
        sol.textcolor = (0, 0, 0)
        hint.textcolor = (0, 0, 0)
        play_pause.textcolor = (0, 0, 0)
        check_answer.textcolor = (0, 0, 0)
        save_button.textcolor = (0, 0, 0)
        number_color = (0, 0, 0)
        background_color = (255, 255, 255)
        bc = (0, 0, 0)
    elif theme == 2:
        play_pause.textcolor = (255, 255, 255)
        background_color = (0, 0, 0)
        back1.textcolor = (255, 255, 255)
        sol.textcolor = (255, 255, 255)
        hint.textcolor = (255, 255, 255)
        play_pause.textcolor = (255, 255, 255)
        check_answer.textcolor = (255, 255, 255)
        save_button.textcolor = (255, 255, 255)
        bc = (255, 255, 255)
        number_color = (255, 255, 255)

    elif theme == 3:
        background_color = (255, 240, 77)
        back1.textcolor = (168, 50, 96)
        sol.textcolor = (168, 50, 96)
        hint.textcolor = (168, 50, 96)
        play_pause.textcolor = (168, 50, 96)
        check_answer.textcolor = (168, 50, 96)
        save_button.textcolor = (168, 50, 96)
        number_color = (0, 0, 0)
        bc = (50, 168, 141)

    global hint_count
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, bc, (50 + 50 * i, 50), (50 + 50 * i, 500), 6)
            pygame.draw.line(win, bc, (50, 50 + 50 * i), (500, 50 + 50 * i), 6)
        else:
            pygame.draw.line(win, bc, (50 + 50 * i, 50), (50 + 50 * i, 500), 3)
            pygame.draw.line(win, bc, (50, 50 + 50 * i), (500, 50 + 50 * i), 3)
    pygame.display.update()

    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < ans[i][j] < 10:
                value = myfont.render(str(ans[i][j]), True, number_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    pygame.display.update()
    run = True
    while run:
        redrawButton3()
        pygame.display.update()
        if grid_solution_checker == grid_solution:
            game_over_screen()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if click_check > 0:
                    insert(win, (pos[0] // 50, pos[1] // 50))
                click_check += 1
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back1.isOver(pos):
                    click_sound.play(1)
                    restart = False
                    screen2()

                if check_answer.isOver(pos):
                    click_check = 0
                    if grid_solution_checker == grid_solution:
                        messagebox.showinfo("Congratulations", "YOUR ANSWER IS CORRECT !")
                    else:
                        messagebox.showinfo("Sorry",
                                            "Your answer is not correct, check your solution properly")

                if play_pause.isOver(pos):
                    click_sound.play(1)
                    if music_playing:
                        mixer.music.pause()
                        music_playing = False
                    else:
                        mixer.music.unpause()
                        music_playing = True

                if save_button.isOver(pos):
                    click_sound.play(1)
                    click_check = 0
                    x = 0
                    for folders in os.listdir():
                        if folders == 'Game Saves':
                            x = 1
                    if x:
                        messagebox.showinfo("Saved", "Your game has been saved successfully in save" +
                                            str(save_count()))
                    else:
                        messagebox.showinfo("Saved", "Your game has been successfully saved in save1")
                    save_game()

                if sol.isOver(pos):
                    click_check = 0
                    click_sound.play(1)
                    confirm = messagebox.askquestion("Confirm", "Are you sure you want to see the solution?")
                    if confirm == "yes":
                        restart = False
                        screen4()

                if hint.isOver(pos):
                    click_check = 0
                    click_sound.play(1)
                    check = True
                    for i in range(9):
                        for j in range(9):
                            if grid_solution_checker[i][j] == 0:
                                check = False
                    if check:
                        messagebox.showinfo("Sorry", "There is no empty place left for showing hint")
                    elif hint_count == 3:
                        confirm = messagebox.askquestion("Confirm", "Are you sure? You can use hint only three times")
                        if confirm == "yes":
                            hint_count -= 1
                            hint_fun()
                    elif hint_count == 2:
                        confirm = messagebox.askquestion("Confirm", "Are you sure? You have only 2 hints left")
                        if confirm == "yes":
                            hint_count -= 1
                            hint_fun()
                    elif hint_count == 1:
                        confirm = messagebox.askquestion("Confirm",
                                                         "This is your last hint. Are you sure you want to use it ?")
                        if confirm == "yes":
                            hint_count -= 1
                            hint_fun()
                    else:
                        messagebox.showinfo("Sorry", "You have already used all your hints")

            if event.type == pygame.MOUSEMOTION:
                if back1.isOver(pos):
                    back1.color = (255, 0, 0)
                else:
                    back1.color = (0, 255, 0)

            if event.type == pygame.MOUSEMOTION:
                if check_answer.isOver(pos):
                    check_answer.color = (255, 0, 0)
                else:
                    check_answer.color = (0, 255, 0)

            if event.type == pygame.MOUSEMOTION:
                if sol.isOver(pos):
                    sol.color = (255, 0, 0)
                else:
                    sol.color = (0, 255, 0)

            if event.type == pygame.MOUSEMOTION:
                if hint.isOver(pos):
                    hint.color = (255, 0, 0)
                else:
                    hint.color = (0, 255, 0)

            if event.type == pygame.MOUSEMOTION:
                if play_pause.isOver(pos):
                    play_pause.color = (255, 0, 0)
                else:
                    play_pause.color = (0, 255, 0)

            if event.type == pygame.MOUSEMOTION:
                if save_button.isOver(pos):
                    save_button.color = (255, 0, 0)
                else:
                    save_button.color = (0, 255, 0)


def redrawButton4():
    back2.draw(win, (0, 0, 0))


back2 = Button((0, 255, 0), 175, 550, 150, 75, "BACK", 40)


def screen4():
    global background_color, click_check, bc
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    if theme == 1:
        background_color = (255, 255, 255)
        back2.textcolor = (0, 0, 0)
        bc = (0, 0, 0)
    elif theme == 2:
        background_color = (0, 0, 0)
        back2.textcolor = (255, 255, 255)
        bc = (255, 255, 255)

    elif theme == 3:
        background_color = (255, 240, 77)
        back2.textcolor = (168, 50, 96)
        bc = (50, 168, 141)
    win.fill(background_color)
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, bc, (50 + 50 * i, 50), (50 + 50 * i, 500), 6)
            pygame.draw.line(win, bc, (50, 50 + 50 * i), (500, 50 + 50 * i), 6)
        else:
            pygame.draw.line(win, bc, (50 + 50 * i, 50), (50 + 50 * i, 500), 3)
            pygame.draw.line(win, bc, (50, 50 + 50 * i), (500, 50 + 50 * i), 3)
    pygame.display.update()

    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid_solution[i][j] < 10:
                value = myfont.render(str(grid_solution[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    pygame.display.update()
    run = True
    while run:
        redrawButton4()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back2.isOver(pos):
                    click_sound.play(1)
                    click_check = 0
                    screen3(3)

            if event.type == pygame.MOUSEMOTION:
                if back2.isOver(pos):
                    back2.color = (255, 0, 0)
                else:
                    back2.color = (0, 255, 0)


exit_game = Button((0, 255, 0), 175, 350, 250, 100, "Exit Game", textcolor=(255, 255, 255))


def game_over_screen():
    win.fill((0, 0, 0))
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    value = myfont.render("You finished the game", True, original_grid_element_color)
    win.blit(value, (150, 650 / 4))
    pygame.display.update()
    waiting = True
    while waiting:
        exit_game.draw(win, (0, 0, 0))
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_game.isOver(pos):
                    click_sound.play(1)
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if exit_game.isOver(pos):
                    exit_game.color = (255, 0, 0)
                else:
                    exit_game.color = (0, 255, 0)


screen1()

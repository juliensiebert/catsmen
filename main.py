#!/usr/bin/python

import sys
import pygame
import menu
import display
import catsmen
import random
import json
import const


def run_game(starting_player):
    """ run the game window
    starting_player = [0,1]
    """
    g = catsmen.Game(w=16,h=11,nb=5,cell_size_px=48,starting_player=starting_player)
    g.run()

    ## Save scores
    win = g.get_winner()

    if win not in [0,1]:
        ## load file
        with open('scores.json','r') as inputfile:
            scores = json.load(inputfile)
        ## update scores
        scores[win]["vic"] += 1
        scores[g.name_p1]["cat"] += g.score_p1
        scores[g.name_p2]["cat"] += g.score_p2
        ## save to file
        with open('scores.json', 'w') as outfile:
            json.dump(scores, outfile)

        ## Display Winner Menu
        pygame.display.set_caption('Hooray %s Wins' %(win))
        gm = display.GameDisplay(screen, ['%s Wins the game' %(win)])
        _ = gm.run()
    elif win == 1:
        ## Display Winner Menu
        pygame.display.set_caption('Nobody Wins??')
        gm = display.GameDisplay(screen, ['Really?? THat shall not be possible'])
        _ = gm.run()

def display_scores():
    """ display scores """
    ## Display Scores
    pygame.display.set_caption('Catsmen Scores')

    ## load file
    with open('scores.json','r') as inputfile:
        scores = json.load(inputfile)

    # setup strings to display
    scores_str = [ "%s\t%d\t%d" %(k,v["vic"],v["cat"]) for k,v in scores.iteritems()]

    gm = display.GameDisplay(screen, scores_str + ['press enter to go back'])
    _ = gm.run()

def reset_scores():
    """ reset scores """
    ## Display confirm menu
    pygame.display.set_caption('Reset Scores ?')
    gm = menu.GameMenu(screen, ['Yes, reset scores!', 'Nope, nope, nope!!'])
    choice = gm.run()

    # run the game if player_choice is not 3 (back)
    if choice == 0:

        ## load file
        with open('scores.json','r') as inputfile:
            scores = json.load(inputfile)

        ## create a backup
        with open('scores.json.bkp', 'w') as outfile:
            json.dump(scores, outfile)

        ## reset scores
        scores = {"P2": {"vic": 0, "cat": 0}, "P1": {"vic": 0, "cat": 0}}

        ## save the file
        with open('scores.json', 'w') as outfile:
            json.dump(scores, outfile)

def choose_color(player):
    """ choose color of the current player
    player in [0,1]
    """
    ## Display confirm menu
    pygame.display.set_caption('Choose color of player %d' %(player+1))
    colors = ['Blue', 'Brown', 'Green', 'Orange', 'Red', 'Taupe', 'Violet', 'Yellow']
    gm = menu.GameMenu(screen, colors)
    chosen_color = gm.run()

    if player == 0:
        const.SPRITE_P1 = 'cat_R_%s.png' %(colors[chosen_color].lower())
    else:
        const.SPRITE_P2 = 'cat_L_%s.png' %(colors[chosen_color].lower())

if __name__ == "__main__":
    pygame.init()

    # Creating the screen
    while 1:

        ## INTRO Screen with menu
        screen = pygame.display.set_mode((640, 480), 0, 32)

        menu_items = ['Start', 'Scores', 'Options', 'Quit']

        pygame.display.set_caption('Catsmen Game Menu')
        gm = menu.GameMenu(screen, menu_items)
        choice = gm.run()

        if menu_items[choice] == 'Start':

            ## Menu choose starting player
            pygame.display.set_caption('Catsmen Player Choice')
            gm = menu.GameMenu(screen, ['Random', 'Player 1 starts', 'Player 2 starts', 'Back'])
            player_choice = gm.run()

            ## setup starting player
            p = -1
            # run the game if player_choice is not 3 (back)
            if player_choice == 0:
                p = random.randint(0,1)
            elif player_choice in [1,2]:
                p = player_choice - 1

            if p in [0,1]:
                run_game(p)

        elif menu_items[choice] == 'Scores':
            display_scores()

        elif menu_items[choice] == 'Options':
            ## Display Options Menu
            pygame.display.set_caption('Catsmen Options')
            options_items = [ 'Color Player 1', 'Color Player 2', 'Reset scores', 'Back']
            gm = menu.GameMenu(screen, options_items)
            option_choice = gm.run()

            if options_items[option_choice] == 'Reset scores':
                reset_scores()
            elif options_items[option_choice] == 'Color Player 1':
                choose_color(0)
            elif options_items[option_choice] == 'Color Player 2':
                choose_color(1)

        elif menu_items[choice] == 'Quit':
            pygame.quit()
        else:
            pygame.quit()

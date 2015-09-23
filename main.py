#!/usr/bin/python

import sys
import pygame
import menu
import display
import catsmen
import random
import json

pygame.init()

if __name__ == "__main__":


    # Creating the screen
    while 1:

        ## INTRO Screen with menu
        screen = pygame.display.set_mode((640, 480), 0, 32)

        menu_items = ['Start', 'Scores', 'Quit']


        pygame.display.set_caption('Catsmen Game Menu')
        gm = menu.GameMenu(screen, menu_items)
        choice = gm.run()

        if menu_items[choice] == 'Start':

            ## Menu choose starting player
            pygame.display.set_caption('Catsmen Player Choice')
            gm = menu.GameMenu(screen, ['Random', 'Player 1 starts', 'Player 2 starts'])
            player_choice = gm.run()

            ## setup starting player
            p = -1
            if player_choice == 0:
                p = random.randint(0,1)
            else:
                p = player_choice - 1
            
            ## Game window
            g = catsmen.Game(w=16,h=11,nb=5,cell_size_px=48,starting_player=p)
            g.run()

            ## Save scores
            win = g.get_winner()
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

        elif menu_items[choice] == 'Scores':
            ## Display Winner Menu
            pygame.display.set_caption('Catsmen Scores')

            ## load file
            with open('scores.json','r') as inputfile:
                scores = json.load(inputfile)

            scores_str = [ "%s\t%d\t%d" %(k,v["vic"],v["cat"]) for k,v in scores.iteritems()]

            gm = display.GameDisplay(screen, scores_str)
            _ = gm.run()

        elif menu_items[choice] == 'Quit':
            pygame.quit()
        else:
            pygame.quit()

#!/usr/bin/python

import sys
import pygame
import menu
import catsmen

pygame.init()

if __name__ == "__main__":


    # Creating the screen
    while 1:
        screen = pygame.display.set_mode((640, 480), 0, 32)

        menu_items = ['Start', 'Options', 'Quit']


        pygame.display.set_caption('Game Menu')
        gm = menu.GameMenu(screen, menu_items)
        choice = gm.run()

        if menu_items[choice] == 'Start':

            g = catsmen.Game(w=16,h=11,nb=5,cell_size_px=48)
            g.run()

            print 'winner',g.get_winner(),'!'

        elif menu_items[choice] == 'Quit':
            pygame.quit()
        else:
            pygame.quit()

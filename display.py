#!/usr/bin/python
import pygame
import eventloop as el
import const

class DisplayItem(pygame.font.Font):
    def __init__(self, text, font=const.FONT, font_size=const.FONT_SIZE,
                 font_color=const.WHITE, (pos_x, pos_y)=(0, 0)):

        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)


class GameDisplay(el.EventLoop):
    def __init__(self, screen, items, bg_color=const.BLACK, font=const.FONT, font_size=const.FONT_SIZE,
                 font_color=const.WHITE):
        ## initiate parent class
        super(GameDisplay, self).__init__()

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            menu_item = DisplayItem(item, font, font_size, font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            # This line includes a bug fix by Ariel (Thanks!)
            # Please check the comments section of pt. 2 for an explanation
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index*2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)


    def run(self):
        while self.loop:
            # Limit frame speed to 50 FPS
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    # Finally check if Enter or Space is pressed
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.loop = False


            # Redraw the background
            self.screen.fill(self.bg_color)
            for item in self.items:
                self.screen.blit(item.label, item.position)
            pygame.display.flip()

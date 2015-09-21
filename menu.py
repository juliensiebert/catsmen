#!/usr/bin/python
import pygame
import eventloop as el
import const

class MenuItem(pygame.font.Font):
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

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)


class GameMenu(el.EventLoop):
    def __init__(self, screen, items, bg_color=const.BLACK, font=const.FONT, font_size=const.FONT_SIZE,
                 font_color=const.WHITE, font_color_selected=const.RED):
        ## initiate parent class
        super(GameMenu, self).__init__()

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.font_color_selected = font_color_selected
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            # This line includes a bug fix by Ariel (Thanks!)
            # Please check the comments section of pt. 2 for an explanation
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index*2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.cur_item = 0
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(self.font_color_selected)

    def set_keyboard_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(self.font_color)

        # Find the chosen item
        if key == pygame.K_UP and \
                self.cur_item > 0:
            self.cur_item -= 1
        elif key == pygame.K_UP and \
                self.cur_item == 0:
            self.cur_item = len(self.items) - 1
        elif key == pygame.K_DOWN and \
                self.cur_item < len(self.items) - 1:
            self.cur_item += 1
        elif key == pygame.K_DOWN and \
                self.cur_item == len(self.items) - 1:
            self.cur_item = 0

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(self.font_color_selected)


    def run(self):
        while self.loop:
            # Limit frame speed to 50 FPS
            self.clock.tick(30)

            mpos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)

                    # Finally check if Enter or Space is pressed
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return self.cur_item

            # Redraw the background
            self.screen.fill(self.bg_color)
            for item in self.items:
                self.screen.blit(item.label, item.position)
            pygame.display.flip()

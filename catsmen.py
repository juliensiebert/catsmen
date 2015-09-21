import pygame
import random
import eventloop as el
import const

class CursorSprite(pygame.sprite.Sprite):
  """ class for cursor sprites """
  def __init__(self, image, x, y, w, h):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(image).convert()
    self.rect = pygame.Rect(x, y, w, h)

  def update(self, x):
    """ change x coordinate. """
    self.rect.x = x


class CardboxSprite(pygame.sprite.Sprite):
  """ class for cardboxes sprites """
  def __init__(self, image, x, y, w, h, ymin, ymax):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(image).convert()
    self.rect = pygame.Rect(x, y, w, h)
    self.ymin = ymin
    self.ymax = ymax

  def update(self, dx, dy):
    """ change y coordinate. Assure that y stays in [y_min,y_max] """
    y = self.rect.y + dy
    if y > self.ymax:
      y = self.ymin
    elif y < self.ymin:
      y = self.ymax
    self.rect.y = y


class CatSprite(pygame.sprite.Sprite):
  """ class for cats sprites """
  def __init__(self, image, x, y, w, h, xmin, xmax, ymin, ymax):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(image).convert()
    self.rect = pygame.Rect(x, y, w, h)
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax

  def update(self, dx, dy):
    """ change y coordinate. Assure that y stays in [y_min,y_max] """
    y = self.rect.y + dy
    x = self.rect.x + dx
    if y > self.ymax:
      y = self.ymin
    elif y < self.ymin:
      y = self.ymax
    self.rect.y = y
    self.rect.x = x


class Grid():
  """ class Grid: al boxes and cats evolve on a grid made of nb_rows * nb_cols cells,
  the player can only move one column (up or down) at a time """
  def __init__(self,nb_rows=10,nb_cols=16,cell_size_px=48,nb_cats=5,x0=48,y0=96):
    """
    nb_rows: number of rows
    nb_cols: number of columns
    cell_size_px: pixel size of each cell
    nb_cats: number of cats for each player
    x0, y0: origins coordinates in pixels
    """
    self.rows = nb_rows
    self.cols = nb_cols
    self.list_cols = []
    self.n = nb_cats
    self.cell_size_px = cell_size_px
    ## grid coordinates
    self.xmin = x0
    self.ymin = y0
    self.xmax = x0 + (nb_cols - 1) * cell_size_px
    self.ymax = y0 + (nb_rows - 1) * cell_size_px
    ## Sprites Groups (see pygame)
    self.sprites = pygame.sprite.Group()
    self.cats_P1 = pygame.sprite.Group()
    self.cats_P2 = pygame.sprite.Group()
    self.cursors = pygame.sprite.Group()
    ## Sprites files
    self.box_path = 'img/cardbox/'
    self.box_filenames = ['box_48px_001.png',
                          'box_48px_002.png',
                          'box_48px_003.png',
                          'box_48px_004.png',
                          'box_48px_005.png',
                          'box_48px_006.png',
                          'box_48px_007.png',
                          'box_48px_008.png',
                          'box_48px_009.png',
                          'box_48px_010.png']
    self.cat_path = 'img/cats/'
    self.cat_filenames = ['catL.png', 'catR.png']
    self.cursor_path = 'img/cursor/'
    self.cursor_filenames = ['cursor48.png']
    self.create_sprites()


  def get_x(self,i):
    """ return x when i = column id"""
    return self.xmin + i * self.cell_size_px


  def get_y(self,j):
    """ return y when i = row id"""
    return self.ymin + j * self.cell_size_px


  def get_cols_P1(self):
    """ returns the columns where P1 cats are """
    return [(cat.rect.x - self.xmin)/self.cell_size_px for cat in self.cats_P1]


  def get_cols_P2(self):
    """ returns the column where P1 cats are """
    return [(cat.rect.x - self.xmin)/self.cell_size_px for cat in self.cats_P2]


  def get_sprites_P1(self):
    """ get sprites of P1 ordered from bottom right to top left """
    cats_list = list(self.cats_P1) ## copy the list
    cats_list.sort(lambda c1,c2:cmp(c1.rect.x,c2.rect.x), reverse=True)
    cats_list.sort(lambda c1,c2:cmp(c1.rect.y,c2.rect.y), reverse=True)
    return cats_list


  def get_sprites_P2(self):
    """ get sprites of P2 ordered from bottom left to top right """
    cats_list = list(self.cats_P2) ## copy the list
    cats_list.sort(lambda c1,c2:cmp(c1.rect.x,c2.rect.x), reverse=False)
    cats_list.sort(lambda c1,c2:cmp(c1.rect.y,c2.rect.y), reverse=True)
    return cats_list


  def get_sprites_at_col(self,index):
    """ get all sprites contained in column index """
    x = self.xmin + (index+0.5) * self.cell_size_px
    return [sprite for sprite in self.sprites.sprites() if sprite.rect.left < x and x < sprite.rect.right]


  def get_sprites_at(self,x,y):
    """ return a list of sprite at a given position """
    return [ sprite for sprite in self.sprites.sprites() if sprite.rect.left <= x and x <= sprite.rect.right and sprite.rect.bottom >= y and y >= sprite.rect.top ]


  def create_sprites(self):
    """ create sprites: cardboxes, cats P1 and cats P2 """
    # list cardboxes coordinates (usefull for cats sprites)
    box_coords = []
    # choose the number of boxes in each column (let at least 2 holes)
    nb_boxes = [random.randint(2, self.rows - 2) for i in range(self.cols/2 - 1)]
    nb_boxes = [2] + nb_boxes + (self.cols % 2) * [random.randint(2, self.rows - 2)] + nb_boxes[-1::-1] + [2]
    assert len(nb_boxes) == self.cols, "%d,%d,%s" %(len(nb_boxes), self.cols, map(str,nb_boxes))
    # iterate over all columns
    for index in range(self.cols):
      # compute x coordinate (left coordinate of Rect)
      x = index * self.cell_size_px
      # nb of blocks to add in this column
      nb_blocks = nb_boxes[index]
      # randomly choose the block images
      list_imgs = [random.choice(self.box_filenames) for i in range(nb_blocks)]
      # randomly choose the blocks rows number (y coordinates)
      list_rows = random.sample(range(self.rows),nb_blocks)
      # extend list of cardboxes coordinates
      box_coords.extend([(index,j) for j in list_rows])
      # add cardboxes sprites
      for i in range(nb_blocks):
        box_sprite = CardboxSprite(image = self.box_path + list_imgs[i],
                                  x = self.xmin + x,
                                  y = self.ymin + list_rows[i] * self.cell_size_px,
                                  w = self.cell_size_px,
                                  h = self.cell_size_px,
                                  ymin = self.ymin,
                                  ymax = self.ymax)
        self.sprites.add(box_sprite)

    # cats coordinates
    all_coords = [(i,j) for i in range(self.cols) for j in range(self.rows)]
    possible_coords = list( set(all_coords) - set(box_coords) )
    possible_coords_P1 = [(i,j) for (i,j) in possible_coords if i < self.cols/2]
    possible_coords_P2 = [(i,j) for (i,j) in possible_coords if i >= self.cols/2]

   # add sprites P1
    for (i,j) in random.sample(possible_coords_P1,self.n):
      cat_sprite = CatSprite(image = self.cat_path + self.cat_filenames[0],
                             x = self.xmin + i * self.cell_size_px,
                             y = self.ymin + j * self.cell_size_px,
                             w = self.cell_size_px,
                             h = self.cell_size_px,
                             xmin = self.xmin,
                             xmax = self.xmax,
                             ymin = self.ymin,
                             ymax = self.ymax)
      self.sprites.add(cat_sprite)
      self.cats_P1.add(cat_sprite)

    # add sprites P2
    for (i,j) in random.sample(possible_coords_P2,self.n):
      cat_sprite = CatSprite(image = self.cat_path + self.cat_filenames[1],
                             x = self.xmin + i * self.cell_size_px,
                             y = self.ymin + j * self.cell_size_px,
                             w = self.cell_size_px,
                             h = self.cell_size_px,
                             xmin = self.xmin,
                             xmax = self.xmax,
                             ymin = self.ymin,
                             ymax = self.ymax)
      self.sprites.add(cat_sprite)
      self.cats_P2.add(cat_sprite)


    cursor = CursorSprite(image = self.cursor_path + self.cursor_filenames[0],
                          x = self.xmin + self.xmax / 2,
                          y = self.ymax + 60,
                          w = 24,
                          h = 24)
    self.cursors.add(cursor)


  def up(self,index):
    """ push column i upward """
    sprites = self.get_sprites_at_col(index)
    map(lambda s: s.update(0,-self.cell_size_px), sprites)


  def down(self,index):
    """ push column i downward """
    sprites = self.get_sprites_at_col(index)
    map(lambda s: s.update(0,self.cell_size_px), sprites)


  def is_cell_down_empty(self,sprite):
    """ Return true if cell down is empty (no sprite)"""
    y = sprite.rect.y
    if y == self.ymax:
      xc,yc = sprite.rect.center
      return len( self.get_sprites_at(xc,self.ymin) ) == 0
    else:
      xc,yc = sprite.rect.center
      return len( self.get_sprites_at(xc,yc+self.cell_size_px) ) == 0


  def is_cell_left_empty(self,sprite):
    """ Return true if cell left is empty (no sprite)"""
    x = sprite.rect.x
    if x == self.xmin:
      return True
    else:
      xc,yc = sprite.rect.center
      return len( self.get_sprites_at(xc-self.cell_size_px,yc) ) == 0


  def is_cell_right_empty(self,sprite):
    """ Return true if cell right is empty (no sprite)"""
    x = sprite.rect.x
    if x == self.xmax:
      return True
    else:
      xc,yc = sprite.rect.center
      return len( self.get_sprites_at(xc+self.cell_size_px,yc) ) == 0



  def get_updatable_sprites_P1(self):
    return [sprite for sprite in self.cats_P1 if self.is_cell_down_empty(sprite) or self.is_cell_right_empty(sprite)]

  def get_updatable_sprites_P2(self):
    return [sprite for sprite in self.cats_P2 if self.is_cell_down_empty(sprite) or self.is_cell_left_empty(sprite)]


class ScoreItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
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

    def update(self,score):
        self.text = score
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)


class Game(el.EventLoop):
  def __init__(self,w,h,nb,cell_size_px,name_p1="P1",name_p2="P2",starting_player=1):

    super(Game, self).__init__()

    self.width = (w+2)*cell_size_px
    self.height = (h+4)*cell_size_px

    self.screen = pygame.display.set_mode((self.width,self.height))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption("Catsmen Game Window")

    #self.create_background()

    self.score_p1 = 0
    self.score_p2 = 0

    self.name_p1 = name_p1
    self.name_p2 = name_p2

    max_len_score = const.FONT_SIZE * (max(len(name_p1),len(name_p2)) + len(str(nb)) + 1)


    self.si_p1 = ScoreItem("%s:%d" %(self.name_p1, self.score_p1),
                            const.FONT,
                            const.FONT_SIZE,
                            const.WHITE,
                            (max_len_score , cell_size_px / 2))
    self.si_p2 = ScoreItem("%s:%d" %(self.name_p2, self.score_p2),
                            const.FONT,
                            const.FONT_SIZE,
                            const.WHITE,
                            (self.width - max_len_score, cell_size_px / 2))

    self.w = w
    self.h = h
    self.nb = nb
    self.grid = Grid(nb_rows = h, nb_cols = w, nb_cats = nb, cell_size_px = cell_size_px)

    self.current_player = starting_player
    self.winner = ''

    self.update_cats()
    self.draw()

    self.update_score()

    if self.current_player == 1:
        self.current_col_id = -1
    else:
        self.current_col_id = 0

    self.last_col = None
    self.cols = self.get_authorized_cols()
    self.update_cursor()

    self.draw()


  def game_over(self):
    """ check if the game is over """
    return (self.score_p1 == self.nb) or (self.score_p2 == self.nb)

  def get_winner(self):
    """ find the winner """
    if self.score_p1 == self.nb and self.score_p2 == self.nb:
      return 'eq'
    elif self.score_p1 == self.nb:
      return self.name_p1
    elif self.score_p2 == self.nb:
      return self.name_p2
    else:
      return 'no one'


  # def choose_starting_player(self):
  #   """ randomly choose between P1 and P2"""
  #   return random.randint(1,2)


  def change_player(self):
    """ change player """
    if self.current_player == 1:
      self.current_player = 2
      self.current_col_id = 0
    else:
      self.current_player = 1
      self.current_col_id = -1

    self.cols = self.get_authorized_cols()
    # self.current_col_id = 0
    # col_index = self.cols[self.current_col_id]
    self.update_cursor()


  #def create_background(self):
    #""" Fill background """
    #self.background = pygame.Surface(self.screen.get_size())
    #self.background = self.background.convert()
    #self.background.fill(pygame.Color("white"))
    #self.screen.blit(self.background, (0,0))

  def draw(self):
    """ Clear the screen and draw all the sprites """
    self.clock.tick(20)
    # Clear the screen
    self.screen.fill((0,0,0))
    # Draw all the spites
    self.grid.sprites.draw(self.screen)
    self.grid.cursors.draw(self.screen)
    # Draw the scores
    self.screen.blit(self.si_p1.label, (self.si_p1.pos_x - self.si_p1.width/2, self.si_p1.pos_y))
    self.screen.blit(self.si_p2.label, (self.si_p2.pos_x - self.si_p2.width/2, self.si_p2.pos_y))
    # Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()
    pygame.display.update()


  def get_authorized_cols(self):
    cols = []
    if self.current_player == 1:
      cols = set(self.grid.get_cols_P1())
    else:
      cols = set(self.grid.get_cols_P2())

    if self.last_col in cols and len(cols) > 1:
      cols = cols - {self.last_col}

    return sorted(list(cols))


  def update_score(self):
    self.si_p1.update("%s:%d" %(self.name_p1, self.score_p1))
    self.si_p2.update("%s:%d" %(self.name_p2, self.score_p2))


  def update_cursor(self):
    """ update the cursor """
    col_index = self.cols[self.current_col_id]
    self.grid.cursors.update(self.grid.get_x(col_index))


  def update_cats(self, i=0):
    """ update the cats, start with P1 if the current player is P1, P2 otherwise """
    ## recursive function, apply it maximum 5 times
    if i < 5:

      ## check which player is currently playing
      if self.current_player == 1:
        # update cats of P1 then cats of P2
        for cat in self.grid.get_sprites_P1():
          self.update_cat_P1(cat)
        for cat in self.grid.get_sprites_P2():
          self.update_cat_P2(cat)
      else:
        # update cats of P2 then cats of P1
        for cat in self.grid.get_sprites_P2():
          self.update_cat_P2(cat)
        for cat in self.grid.get_sprites_P1():
          self.update_cat_P1(cat)

      ## check if some cats needs to be updated
      if len(self.grid.get_updatable_sprites_P1()) > 0 or len(self.grid.get_updatable_sprites_P2()) > 0:
        self.update_cats(i+1)


  def update_cat_P1(self,cat):
    """ update one cat of P1 """
    x = cat.rect.x

    if x == self.grid.xmax:
      # the cat can go out, P1 score + 1
      cat.kill()
      self.score_p1 += 1
      self.draw()

    elif self.grid.is_cell_down_empty(cat):
        # move cat down
        cat.update(0,self.grid.cell_size_px)
        self.draw()
        self.update_cat_P1(cat)

    elif self.grid.is_cell_right_empty(cat):
        # move cat to the right
        cat.update(self.grid.cell_size_px,0)
        self.draw()
        self.update_cat_P1(cat)


  def update_cat_P2(self,cat):
    """ update one cat of P2 """
    x = cat.rect.x
    if x == self.grid.xmin:
      ## the cat can go out, P2 score + 1
      cat.kill()
      self.score_p2 += 1
      self.draw()

    elif self.grid.is_cell_down_empty(cat):
        # move cat down
        cat.update(0,self.grid.cell_size_px)
        self.draw()
        self.update_cat_P2(cat)

    elif self.grid.is_cell_left_empty(cat):
        # move cat to the right
        cat.update(-self.grid.cell_size_px,0)
        self.draw()
        self.update_cat_P2(cat)


  def run(self):
    while self.loop:

      # Limit frame speed to 50 FPS
      self.clock.tick(30)

      # --- Main event loop
      for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
          pygame.quit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.current_col_id = (self.current_col_id - 1) % len(self.get_authorized_cols())
            self.update_cursor()
            self.draw()
          if event.key == pygame.K_RIGHT:
            self.current_col_id = (self.current_col_id + 1) % len(self.get_authorized_cols())
            self.update_cursor()
            self.draw()
          if event.key == pygame.K_UP:
            # update + affichage
            col = self.get_authorized_cols()[self.current_col_id]
            self.grid.up(col)
            self.last_col = col
            self.draw()
            self.update_cats()
            self.update_score()
            # change player
            self.change_player()
            self.draw()
          if event.key == pygame.K_DOWN:
            # update + affichage
            col = self.get_authorized_cols()[self.current_col_id]
            self.grid.down(col)
            self.last_col = col
            self.draw()
            self.update_cats()
            self.update_score()
            # change player
            self.change_player()
            self.draw()

      # --- Game logic should go here
      # --- Drawing code should go here

      self.loop = self.loop and not self.game_over()

import pygame, random, time
import colors

pygame.init()



pygame.display.set_caption("Brick Breaker")
clock=pygame.time.Clock()
bg = pygame.image.load("background.jpg")


"""Screen set up"""
dw=400
dh=400
screen=pygame.display.set_mode([dw,dh])

"""Function to create message box"""
def msg(txt,color,size,x,y):
    font=pygame.font.SysFont("bold",size)
    msgtxt=font.render(txt,True,color)
    msgrect=msgtxt.get_rect()
    msgrect.center=x,y
    screen.blit(msgtxt,msgrect)
    
    """Creates Player class"""
class Player(pygame.sprite.Sprite):               ##### p variable
    def __init__(self,x,y):
        super().__init__()          ##initialize
        self.image=pygame.image.load("p1.png")      #load image
        self.image=pygame.transform.scale(self.image,[70,20])   #scale size
        self.image.set_colorkey(colors.White)
        self.rect=self.image.get_rect()     #take the image of the rectangle
        self.rect.x=x       
        self.rect.y=y
        self.vx=0
        self.vy=0
        
    
    def update(self):

       keys=pygame.key.get_pressed()
       if keys[pygame.K_LEFT]:
           self.vx=-3           #Move left a 3 velocity
       if keys[pygame.K_RIGHT]:
           self.vx=3
       self.rect.x+=self.vx
       if self.rect.right>=dw: ## stops at end
           self.rect.right=dw
       if self.rect.left<=0:    ##zero is farthest left
           self.rect.left=0
"""Sets up the powerup class"""
class Powerup(pygame.sprite.Sprite):
    def __init__(self,p,x,y):
        super().__init__()
        self.image= pygame.image.load("powerup.png")
        self.image=pygame.transform.scale(self.image,[20,20])
        self.image.set_colorkey(colors.White)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.p=p
        self.t_collide=False        #top collide?
        self.b_collide=False        #bottom collide?
        self.vy=1
        
    """Collision detector"""
    def hit_player(self):
        hits=pygame.sprite.spritecollide(self.p,powerup, True)
        if hits:
            return True
        else:
            return False
        """collision response"""
    def update(self):
        self.rect.y+=self.vy
        
        if self.rect.bottom>=dh:
            self.kill()
        elif self.rect.top<=0 :
            self.t_collide=False
        elif self.hit_player():
            self.b_collide=True
            
"""Create Ball Class"""
class Ball(pygame.sprite.Sprite):
    def __init__(self,p,w,c,pu):
        super().__init__()
        self.image=pygame.image.load("b1.png")
        self.image=pygame.transform.scale(self.image,[25,25])
        self.image.set_colorkey(colors.White)
        self.rect=self.image.get_rect()
        self.rect.x=200
        self.rect.y=200
        self.p=p            #set player
        self.pu=pu          #set powerup
        self.w=w            #set
        self.c=c            #set wall
        self.vy=1           #set velocity of ball up and down
        self.vx=1           #set velocity of ball left and right
        self.t_collide=False        #top collide?
        self.b_collide=False        #bottom collide?
        self.score=0
        self.lives=3
        """Makes ball change when powerup is hit"""
        while self.hit_powerup == True:
            self.image=pygame.image.load("lightningball.png")
    """Lives function for ball to cause game over"""
    def Live(self):
        msg("Lives:"+str(self.lives),colors.Red,30,300,10)

    """collision detection"""
    def hit_wall(self):
        hits=pygame.sprite.groupcollide(balls,self.c.walls,False,True)

        if hits:
            return True
        else:
            return False

    def hit_player(self):
        hits=pygame.sprite.spritecollide(self.p, balls,False)
        if hits:
            return True
        else:
            return False

    def hit_powerup(self):
        hits=pygame.sprite.groupcollide(balls, self.pu,False,True)
        if hits:
            return True
        else:
            return False

    def Score(self):
        msg("Score:"+str(self.score),colors.Blue,30,200,10)

    def update(self):
        if self.rect.bottom>=dh:
            self.kill()
            self.lives-=1
            self.hide()
            
        if self.rect.left<=0:
           if self.t_collide:
               self.vx=random.randrange(1,3)
               self.vy=3
               self.t_collide=False
           elif self.b_collide:
               self.vx=random.randrange(1,3)
               self.vy=-3
               self.b_collide=False
        elif self.rect.top<=0:
               self.t_collide=True
               self.vx=random.randrange(-3,3)
               self.vy=3
        elif self.rect.right>=dw:
            if self.t_collide:
                self.vx=random.randrange(-3,-1)
                self.vy=3
                self.t_collide=False
            elif self.b_collide:
                self.vx=random.randrange(-3,-1)
                self.vy=-3
                self.b_collide=False
        elif self.hit_player():
            self.vx=random.randrange(-3,3)
            self.vy=-3
            self.b_collide=True
        elif self.hit_wall():
            self.vx=random.randrange(-3,3)
            self.vy=3
            self.score+=1
            self.t_collide=True
               
        while self.hit_powerup == True:
            if self.rect.left<=0:
               if self.t_collide:
                   self.vx=random.randrange(7,10)
                   self.vy=7
                   self.t_collide=False
               elif self.b_collide:
                   self.vx=random.randrange(7,10)
                   self.vy=-7
                   self.b_collide=False
               elif self.rect.top<=0:
                   self.t_collide=True
                   self.vx=random.randrange(7,5)
                   self.vy=7
               elif self.rect.right>=dw:
                   if self.t_collide:
                       self.vx=random.randrange(7,10)
                       self.vy=7
                       self.t_collide=False
                   elif self.b_collide:
                       self.vx=random.randrange(7,10)
                       self.vy=-7
                       self.b_collide=False
               elif self.hit_player():
                   self.vx=random.randrange(7,10)
                   self.vy=-7
                   self.b_collide=True
               elif self.hit_wall():
                   self.vx=random.randrange(7,10)
                   self.vy=7
                   self.score+=5
                   self.t_collide=True
        self.rect.x+=self.vx
        self.rect.y+=self.vy

"""Create wall class"""
class Walls(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface([40,20])
        self.image.fill(colors.Green)
        self.rect=self.image.get_rect()
        self.rect.x=x*20
        self.rect.y=y*20
##    pygame.display.flip()

"""start up screen"""
def intro():
    screen.fill(colors.White)
    msg("Brick Breaker",colors.Red,40,200,100)
    icon=pygame.image.load("bimg1.png")
    icon=pygame.transform.scale(icon,[200,150])
    screen.blit(icon,[100,130])
    wait=1

    while wait:
        cur=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        if  70+65>cur[0]>70 and 320+40>cur[1]>320:
            pygame.draw.rect(screen,colors.Blue,[70,320,65,40]  )
            if click[0]==1:
                wait=0
        else:
            pygame.draw.rect(screen,colors.Aqua,[70,320,65,40]  )

        msg("Start",colors.Red,30,100,340)

        if 270+60>cur[0]>270 and 320+40>cur[1]>320:
             pygame.draw.rect(screen,colors.Blue,[270,320,60,40])
             if click[0]==1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen,colors.Aqua,[270,320,60,40])

        msg("Exit",colors.Red,30,300,340)
        pygame.display.flip()

"""If space is pressed will pause"""
def pause():
    paused=True
    screen.fill(colors.White)
    msg("Paused",colors.Red,40,200,100)
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    paused=0
        pygame.display.flip()
"""Set Map"""
class Map:
    def __init__(self,map_file):
        self.map_file=map_file
        self.map_data=[]
        self.walls=pygame.sprite.Group()

    def update(self):
        with open(self.map_file,'r+') as f:
          for line in f:
              self.map_data.append(line)
        for row ,tiles in enumerate(self.map_data):
            for col,tile in enumerate(tiles):
                    if tile=='1':
                        self.w=Walls(col,row)
                        self.walls.add(self.w)
                        all_sprites.add(self.walls)
    
    
"""Game event"""
running=True
start=True
level=False
gover=False

while running:
    clock.tick(60)
    screen.blit(bg,[0,0])
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False


        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                pause()
    if start :
        intro()
        start=False
        
        all_sprites=pygame.sprite.Group()
        balls=pygame.sprite.Group()
        walls=pygame.sprite.Group()
        powerup=pygame.sprite.Group()
        p=Player(200,350)
        all_sprites.add(p)
        c=Map("map1.txt")
        c.update()
        pu=Powerup(p,200,300)
        powerup.add(pu)
        all_sprites.add(pu)
        b=Ball(p,c.w,c,pu)
        balls.add(b)
        all_sprites.add(b)
        

    if level:
        level=False
        all_sprites=pygame.sprite.Group()
        balls=pygame.sprite.Group()
        walls=pygame.sprite.Group()
        powerup=pygame.sprite.Group()
        p=Player(200,350)
        all_sprites.add(p)
        c=Map("map.txt")
        c.update()
        pu=Powerup(p,200,300)
        powerup.add(pu)
        all_sprites.add(pu)
        b=Ball(p,c.w,c,pu)
        balls.add(b)
        all_sprites.add(b)
        
        

    if gover:
        gover=False
        all_sprites=pygame.sprite.Group()
        balls=pygame.sprite.Group()
        walls=pygame.sprite.Group()
        powerup=pygame.sprite.Group()
        p=Player(200,350)
        all_sprites.add(p)
        c=Map("map1.txt")
        c.update()
        pu=Powerup(p,200,300)
        powerup.add(pu)
        all_sprites.add(pu)
        b=Ball(p,c.w,c)
        balls.add(b)
        all_sprites.add(b)
    all_sprites.update()
    if len(c.walls.sprites())<=0:
        level=True



    """Game over if lives = 0"""
    screen.fill(colors.White)
    if b.lives==0:
        screen.fill(colors.White)
        msg("Game Over!",colors.Red,40,200,200)
        p.kill()
        b.kill()
        all_sprites.remove(c.walls)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    gover=True

    all_sprites.draw(screen)
    b.Score()
    b.Live()
    pygame.display.flip()




pygame.quit()
quit()

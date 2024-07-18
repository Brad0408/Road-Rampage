import pygame
import pygame.gfxdraw
import random
pygame.font.init()


#DECLARING VARIABLES

WHITE = (255,255,255)
BLACK = (0,0,0)

WIDTH = 1000
HEIGHT = 700

##main page##
bg = pygame.image.load('Mainbg.png')


##instruction page##
instruction_bg = pygame.image.load('Instructionbg.png')


#gamescreen#
game_bg = pygame.image.load('PlayScreen.png')
arrow = pygame.image.load('arrow.png')

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ROAD RAMPAGE")

#game Over screen#
gameOver_bg = pygame.image.load('gameOverScreen.png')

clock = pygame.time.Clock()
fps_menu = 10
clock.tick(60)

startLives = 3

#FUNCTIONS
LClick = 1
#################################################################################################################
def MainMenu():
    status = True
    playerA.lives = startLives
    playerA.score = 0
    while status == True:
        click = False
        #Check for any key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LClick:
                click = True



        mx,my = pygame.mouse.get_pos() #tracking mouse position
        

        #Display all the sprites
        gameDisplay.blit(bg, (0,0))

        press_instruction = pygame.Rect(500,150,340,100)#invisble box around 'instructions'
        pygame.gfxdraw.box(gameDisplay, press_instruction,(0,0,0,0))

        press_play = pygame.Rect(100,150,340,100)#invisble box around 'play'
        pygame.gfxdraw.box(gameDisplay, press_play,(0,0,0,0))

      

        if press_instruction.collidepoint((mx,my)):#loading instructions on click 
            if click == True:
                InstructionMenu()

        if press_play.collidepoint((mx,my)):#loading play on click 
            if click == True:
                gameScreen()


        pygame.display.flip()


#####################################################################################################################

def InstructionMenu():
    status = True

    while status == True:
        click = False
        #Check for any key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LClick:
                click = True
   
        gameDisplay.blit(instruction_bg, (0,0))


        mx,my = pygame.mouse.get_pos()
        
        press_menuarrow = pygame.Rect(0,0,80,80)
        pygame.gfxdraw.box(gameDisplay, press_menuarrow,(0,0,0,0))


        if press_menuarrow.collidepoint((mx,my)):#loading menu on click 
            if click == True:
                MainMenu()


    

        pygame.display.flip()
        clock.tick(fps_menu)
###########################################################################################################################
def gameOver():
    status = True

    while status == True:
        click = False
        #Check for any key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LClick:
                click = True

        gameDisplay.blit(gameOver_bg, (0,0))
        gameDisplay.blit(arrow, (0,0))

        mx,my = pygame.mouse.get_pos()
        
        press_menuarrow = pygame.Rect(0,0,80,80)
        pygame.gfxdraw.box(gameDisplay, press_menuarrow,(0,0,0,0))

        draw_score(gameDisplay, str(playerA.score), 60, WIDTH // 2 ,250)#updating score value on screen

        if press_menuarrow.collidepoint((mx,my)):#loading menu on click 
            if click == True:
                fullGame()


    

        pygame.display.flip()
################################################################################################################################        

def gameScreen():
    status = True

    while status == True:
        click = False
        #Check for any key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LClick:
                click = True

        gameDisplay.blit(game_bg, (0,0))
        gameDisplay.blit(arrow, (0,0))

##        print(playerA.rect.centerx)
##        print(playerA.rect.centery)

        mx,my = pygame.mouse.get_pos()
        
        press_menuarrow = pygame.Rect(0,0,80,80)
        pygame.gfxdraw.box(gameDisplay, press_menuarrow,(0,0,0,0))


        if press_menuarrow.collidepoint((mx,my)):#loading menu on click 
            if click == True:
                fullGame()



        clock.tick(30)
        playerA.update

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] == True:
             playerA.moveLeft(7)
        if keys[pygame.K_d] == True:
            playerA.moveRight(7)
##        if keys[pygame.K_l]:
##            playerA.score += 10000   debug to test player score 

        hits = pygame.sprite.groupcollide(spritesA, spritesB,False,False, pygame.sprite.collide_rect)#checking collision with obstacles
        score_hits = pygame.sprite.groupcollide(spritesC, spritesA,True,False)#checking collisons with coins

        

        for hit in hits:#what happens to the player when hitting an obstacle
            if playerA.canHit == True:
                playerA.hide()
                playerA.lives = playerA.lives - 1

        for score_hit in score_hits:#what happens to the player when hitting a coin
            if score_hit.blue == False:
                playerA.score += 1
            else:
                playerA.score += 5


            newCoin()
            
 
        
            
        if playerA.lives == 0:#game over check
            gameOver()
            playerA.lives = 3#lives are reset after game over


        draw_score(gameDisplay, str(playerA.score), 30, WIDTH - 900,295)#updating score value on screen
        draw_lives(gameDisplay, WIDTH - 100, 5, playerA.lives, player_mini_img)#updating lives values on screen    
                



        spritesA.update()
        spritesB.update()
        spritesC.update()
        spritesA.draw(gameDisplay)
        spritesB.draw(gameDisplay)
        spritesC.draw(gameDisplay)
    
        pygame.display.flip()        #sprites get updated



        
        
        

    
#######################################################################################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self, startLives):
        super().__init__()
        self.image = pygame.image.load('Player.png')
        self.width = self.image.get_width()
        self.width = self.width*2
        self.height = self.image.get_height()
        self.height = self.height*2
        self.lives = startLives
        self.hidden = False
        self.hide_timer =  pygame.time.get_ticks()
        self.score = 0
        self.canHit = True
        

        
        self.image = pygame.transform.scale(self.image,(int(self.width),int(self.height)))

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WIDTH/2)
        self.rect.centery = int(HEIGHT-100)


    def moveRight(self,speed):#move right method
        self.rect.x += speed
        if self.rect.x >= WIDTH-250:
            self.rect.x = 200

    def moveLeft(self,speed):#move left method
        self.rect.x -= speed
        if self.rect.x <= 200:
            self.rect.x = WIDTH-250

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 200)


    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.canHit = False
            self.rect.centerx = WIDTH // 2
            self.rect.centery = HEIGHT - 100
        if pygame.time.get_ticks() - self.hide_timer > 3500:
            self.canHit = True

      


 
 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('obstacle.png')
        self.width = self.image.get_width()
        self.width = self.width*2
        self.height = self.image.get_height()
        self.height = self.height*2

        self.image = pygame.transform.scale(self.image,(int(self.width),int(self.height)))

        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, WIDTH - 250)#random spawing point along x axis
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(10,12)#random speed value of obstacles
        
        
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:#when obstacles reaches the bottom is placed back to the top with a new location and speed
            self.rect.x = random.randrange(200, WIDTH - 250)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(10,12)
        


class Coin(pygame.sprite.Sprite):
    def __init__ (self, blue):
        super().__init__()

        self.blue = blue
        if self.blue == False:
            self.image = pygame.image.load('coin.png')
        else:
            self.image = pygame.image.load('blueCoin.png')
        
        self.width = self.image.get_width()
        self.width = self.width*0.8
        self.height = self.image.get_height()
        self.height = self.height*0.8
        
        self.image = pygame.transform.scale(self.image,(int(self.width),int(self.height)))

        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, WIDTH - 250)#random spawing point along x axis
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(10,12)#random speed value of coins

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:#when obstacles reaches the bottom is placed back to the top with a new location and speed
            self.rect.x = random.randrange(200, WIDTH - 250)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(10,12)




    
#Sprites
        
playerA = Player(startLives)
spritesA = pygame.sprite.Group()
spritesA.add(playerA)


spritesB = pygame.sprite.Group()

for i in range (4):#creating obstacles
    obstacle = Obstacle()
    spritesB.add(obstacle)
    
spritesC = pygame.sprite.Group()#creating coins
for i in range (4):
    coin = Coin(False)
    spritesC.add(coin)

def newCoin():
    randomChance = random.randint(0,8)
    print(randomChance)
    if randomChance == 1:
        c = Coin(True)
    else:
        c = Coin(False)
    spritesC.add(c)



    


font_name = pygame.font.match_font('arial')#creating score values
def draw_score(surf, text, size, x,y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)




player_img = pygame.image.load("Player.png").convert()#creating lives to look like the player
player_mini_img = pygame.transform.scale(player_img,(30,50))
player_mini_img.set_colorkey(BLACK)



def draw_lives(surf, x, y, lives, img):#creating live values 
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x +30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
 






#MAIN PROGRAM
def fullGame():
    gameRunning = True
    while gameRunning == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                



        
        MainMenu()

fullGame()

      







import pygame
import math
import random
from Player import Player
from Bullet import Bullet
from Enemy import Enemy

class SpaceInvaders:

    def __init__(self):
        pygame.init()
        # Level Controller
        self.game_level = 0
        g_level = 0
        # Creating the screen
        self.screen = pygame.display.set_mode((800, 600))
        # Title and icon
        pygame.display.set_caption("Space Cowboy")
        self.icon = pygame.image.load('assets\\spaceship_icon.png')
        pygame.display.set_icon(self.icon)
        # Delete bullet
        self.toBeDeleted = []
        # Background
        self.background = pygame.image.load('assets\\desert.jpg')
        # Score
        self.score = 0
        # Game
        self.liste2 = []
        self.intro_checker = 0
        self.running = True

    def creatingThePlayer(self):
        # Player
        playerImg = pygame.image.load('assets\\jet2.png')
        playerX = 10
        playerY = 10
        playerY_change = 0
        self.player = Player(playerX, playerY, playerImg, playerY_change)

    def creatingTheBullets(self):
        # Bullet
        self.noOfBullets = []
        bulletX = -5
        bulletY = -5
        bulletX_change = 0
        bullet_state = "ready"
        self.bullet = Bullet(0, 0, bullet_state, bulletX_change)

    def setGameSpike(self):
        # Spike
        self.spikeX = random.randint(350, 550)
        self.spikeY = random.randint(200, 600)
        self.spikeX_change = -2
        self.spikeImg = pygame.image.load('assets\\mace.png')
        self.margin_right = 0

    def creatingTheEnemy(self):
        # Enemy
        self.enemy = Enemy()

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            """
            This if block checks:
            -If the user clicks Start at the intro,it will create the stone objects
            -If the user clicks Quit,it will quit the game basicly.
            """
            if (self.intro_checker == 0):
                self.start = self.game_intro()
                if self.start == 1:
                    self.intro_checker = 1
                    # No of enemies
                    self.game_level = 0
                    self.numberOfEnemies = self.game_level_checker()
                elif self.start == 0:
                    self.intro_checker = 0
                    self.running = False
                else:
                    continue
            # If you clicked Start already,then it means we can get to our gameplay.
            if self.start == 1 and self.intro_checker == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.running = False
                        if event.key == pygame.K_UP:
                            self.player.playerY_change = -5
                        if event.key == pygame.K_DOWN:
                            self.player.playerY_change = 5
                        if event.key == pygame.K_SPACE:
                            # To make sure we don't shoot multiple bullets too fast(one by one)
                            if len(self.noOfBullets) != 0:
                                if self.noOfBullets[-1].bulletX - self.player.playerX < 90:
                                    break
                            self.bullet = Bullet(self.bullet.bulletX, self.bullet.bulletY, self.bullet.bullet_state, self.bullet.bulletX_change)
                            self.noOfBullets.append(self.bullet)
                            self.noOfBullets[-1].bulletX = self.player.playerX
                            self.noOfBullets[-1].bulletY = self.player.playerY
                            self.bullet.bulletX_change = 5
                            self.noOfBullets[-1].fire_bullet(self.noOfBullets[-1].bulletX, self.noOfBullets[-1].bulletY,
                                                        self.noOfBullets[-1].bullet_state, self.screen)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                            self.player.playerY_change = 0
                # Player Moves
                self.player.playerY += self.player.playerY_change
                # Checking Boundries to make sure we do not jump out of range
                if self.player.playerY <= 32:
                    self.player.playerY = 32
                elif self.player.playerY >= 536:
                    self.player.playerY = 536
                # Bullet Moves
                self.bullet.bullet_moves(self.noOfBullets, self.screen)
                # Enemy Moves
                self.enemy.enemy_moves(self.numberOfEnemies)
                # Collision between the bullet and the enemy
                self.bulletCollisionWithEnemy()
                # Level Designs
                self.levelDesign()
                # Main Collision between rocks and player
                self.playerCollisionWithEnemy()
                # Display of our stone objects.
                e_c3 = 0
                while e_c3 < len(self.numberOfEnemies):
                    self.numberOfEnemies[e_c3].draw_player(self.numberOfEnemies[e_c3].enemyX, self.numberOfEnemies[e_c3].enemyY,
                                                      self.numberOfEnemies[e_c3].enemyImg, self.screen)
                    e_c3 += 1
                # Display of our ingame objects.
                self.player.draw_player(self.player.playerX, self.player.playerY, self.player.playerImg, self.screen)
                self.draw_score()
                self.level()
                pygame.display.update()

    # This function is intro.It greets the player and ask if the user wants to play or quit.
    def game_intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        largeText = pygame.font.Font('freesansbold.ttf', 32)
        text1 = largeText.render("Welcome to Space Cowboy Game", True, (0, 0, 0))
        self.screen.blit(text1, (150, 200))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 270 + 156 > mouse[0] > 270 and 260 + 32 > mouse[1] > 260:
            pygame.draw.rect(self.screen, (0, 232, 0), (270, 260, 156, 32))
            if click[0] == 1:
                return 1
        else:
            pygame.draw.rect(self.screen, (0, 200, 0), (270, 260, 156, 32))
        if 270 + 156 > mouse[0] > 270 and 310 + 32 > mouse[1] > 310:
            pygame.draw.rect(self.screen, (232, 0, 0), (270, 310, 156, 32))
            if click[0] == 1:
                return 0
        else:
            pygame.draw.rect(self.screen, (200, 0, 0), (270, 310, 156, 32))
        playText = pygame.font.Font('freesansbold.ttf', 24)
        text2 = playText.render("Play", True, (255, 255, 255))
        self.screen.blit(text2, (315, 265))
        quitText = pygame.font.Font('freesansbold.ttf', 24)
        text3 = quitText.render("Quit", True, (255, 255, 255))
        self.screen.blit(text3, (315, 315))
        pygame.display.update()
        return 2

    def levelDesign(self):
        if len(self.numberOfEnemies) == 0 and self.game_level < 3:
            if self.game_level + 1 == 3:  # The end of the game.
                self.congrats()
                self.intro_checker = 0
                self.score = 0
                return
            self.spikeX += self.spikeX_change
            self.draw_spike()
            # If you catch the spike,you level up.
            if self.collision(self.player.playerX, self.player.playerY, self.spikeX, self.spikeY):
                self.spikeX = 900
                self.spikeY = 900
                self.game_level += 1
                self.numberOfEnemies = self.game_level_checker()
                self.spikeX = random.randint(350, 550)
                self.spikeY = random.randint(200, 600)
            # If you miss the spike,then you will have to replay that level.
            elif (self.spikeX < 0):
                self.spikeX = random.randint(350, 550)
                self.spikeY = random.randint(200, 600)
                self.numberOfEnemies = self.game_level_checker()
                self.score = self.score - (len(self.numberOfEnemies) + 5)

    def playerCollisionWithEnemy(self):
        e_c2 = 0
        while e_c2 < len(self.numberOfEnemies):
            if self.mainCollision(self.player.playerX, self.player.playerY, self.numberOfEnemies[e_c2].enemyX,
                                  self.numberOfEnemies[e_c2].enemyY):
                self.noOfBullets.clear()
                self.game_over()
                self.score = 0
                self.intro_checker = 0
            e_c2 += 1

    def bulletCollisionWithEnemy(self):
        e_c = 0
        while e_c < len(self.numberOfEnemies):
            for i in range(len(self.noOfBullets)):
                if (self.collision(self.noOfBullets[i].bulletX, self.noOfBullets[i].bulletY, self.numberOfEnemies[e_c].enemyX,
                              self.numberOfEnemies[e_c].enemyY)):
                    self.numberOfEnemies.pop(e_c)
                    self.toBeDeleted.append(self.noOfBullets[i])
                    self.score += 1
                    e_c = 0
                    break
            e_c += 1
            """
            -If block- below functions as:
            If i hit an stone object,i want to delete that bullet(the one i hit stone with) from my array.
            When collision between them happens,i append that bullet to toBeDeleted.
            And below,if the address of toBeDeleted item equals to one of our bullets',then it will be deleted.
            """
            if len(self.toBeDeleted) != 0 and len(self.noOfBullets) != 0:
                croller = 0
                while croller < len(self.noOfBullets):
                    for j in range(0, len(self.toBeDeleted)):
                        if self.toBeDeleted[j] == self.noOfBullets[croller]:
                            self.noOfBullets.pop(croller)
                    croller += 1
                self.toBeDeleted.clear()

    # Collision between bullets and a stones
    def collision(self,bulletX, bulletY, enemyX, enemyY):
        col = math.sqrt(math.pow(enemyX - (bulletX + 59), 2) + math.pow(enemyY - (bulletY + 25), 2))
        return col < 26


    # This is the congrats window after you complete the game.
    def congrats(self):
        self.screen.blit(self.background, (0, 0))
        c_text = pygame.font.Font('freesansbold.ttf', 32)
        text8 = c_text.render("Congrats! You've won the game!", True, (0, 0, 0))
        self.screen.blit(text8, (210, 260))
        score_text = pygame.font.Font('freesansbold.ttf', 32)
        text1 = score_text.render('Score : ' + str(self.score), True, (0, 0, 0))
        self.screen.blit(text1, (340, 300))
        pygame.display.update()
        pygame.time.wait(4000)

    # Drawing the spike
    def draw_spike(self):
        self.screen.blit(self.spikeImg, (self.spikeX, self.spikeY))

    # This function decides the current level of the game.
    def game_level_checker(self):
        # When level increases,i'm increasing the enemy(stone object) number.
        enemy_number = 0
        if self.game_level == 0:
            enemy_number = 15
        elif self.game_level == 1:
            enemy_number = 20
        elif self.game_level == 2:
            enemy_number = 25
        noOfEnemies = []
        for j in range(enemy_number):
            enemy = Enemy()
            noOfEnemies.append(enemy)
        return noOfEnemies

    # If a stone hits the player,the game will be over.
    def mainCollision(self,playerX, playerY, enemyX, enemyY):
        distance = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
        return distance < 24

    # This is the game over window
    def game_over(self):
        self.screen.blit(self.background, (0, 0))
        over_text = pygame.font.Font('freesansbold.ttf', 24)
        text3 = over_text.render("Game Over", True, (0, 0, 0))
        self.screen.blit(text3, (350, 260))
        score_text = pygame.font.Font('freesansbold.ttf', 32)
        text1 = score_text.render('Score : ' + str(self.score), True, (0, 0, 0))
        self.screen.blit(text1, (340, 300))
        pygame.display.update()
        pygame.time.wait(4000)

    # Drawing the score
    def draw_score(self):
        score_text = pygame.font.Font('freesansbold.ttf', 32)
        text1 = score_text.render('Score : ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(text1, (0, 0))

    # Drawing the current level of the game.
    def level(self):
        self.margin_right = 0
        for i in range(0, self.game_level + 1):
            self.margin_right += 40
            self.screen.blit(self.spikeImg, (160 + self.margin_right, 10))

if __name__ == '__main__':
    mainGame = SpaceInvaders()
    mainGame.creatingTheEnemy()
    mainGame.creatingTheBullets()
    mainGame.creatingThePlayer()
    mainGame.setGameSpike()
    mainGame.run()

import pygame
import math
import random
class Enemy:
    def __init__(self, x=0, y=0):
        self.enemyX = x
        self.enemyY = y
        self.create_enemy()

    def draw_player(self, enemyX, enemyY, enemyImg,screen):
        screen.blit(enemyImg, (enemyX, enemyY))

    def create_enemy(self):
        # Enemy
        self.enemyImg = pygame.image.load('assets\\icon.png')
        self.enemyX = random.randint(832, 882)
        self.enemyY = random.randint(20, 540)
        self.enemyX_change = -6
        if self.enemyY > 0 and self.enemyY < 270:
            # If stone object spawns at the top of screen,we need it to go down.
            self.enemyY_change = -0.45
        else:
            self.enemyY_change = 0.25

    def enemy_moves(self,numberOfEnemies):
        # Enemy Moves
        enemy_counter = 0
        while enemy_counter < len(numberOfEnemies):
            numberOfEnemies[enemy_counter].enemyX += numberOfEnemies[enemy_counter].enemyX_change
            numberOfEnemies[enemy_counter].enemyY += numberOfEnemies[enemy_counter].enemyY_change
            if numberOfEnemies[enemy_counter].enemyX < 0 or numberOfEnemies[enemy_counter].enemyY < 0 or \
                    numberOfEnemies[enemy_counter].enemyY > 568:
                numberOfEnemies[enemy_counter].create_enemy()
            enemy_counter += 1
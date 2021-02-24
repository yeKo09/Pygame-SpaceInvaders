import pygame
class Bullet:
    def __init__(self, x, y, b_state,bx_change):
        self.bulletX = x
        self.bulletY = y
        self.bullet_state = b_state
        self.bulletX_change=bx_change

    def fire_bullet(self, x, y,bullet_state,screen):
        self.bullet_state = "fire"
        pygame.draw.rect(screen, (255, 0, 0), (x + 59, y + 25, 35, 15))

    def bullet_moves(self,noOfBullets,screen):
        # Bullet Moves
        z = 0
        while z < len(noOfBullets):
            if noOfBullets[z].bullet_state == "fire":
                noOfBullets[z].bulletX += self.bulletX_change
                noOfBullets[z].fire_bullet(noOfBullets[z].bulletX, noOfBullets[z].bulletY,
                                           noOfBullets[z].bullet_state, screen)
                if noOfBullets[z].bulletX > 764:
                    """ noOfBullets[z].bulletX = -5
                    noOfBullets[z].bulletY = -5
                    noOfBullets[z].bullet_state = "ready" """
                    noOfBullets.pop(z)
            z += 1
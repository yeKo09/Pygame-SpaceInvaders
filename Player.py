class Player:
    def __init__(self, x, y, img,pY_change):
        self.playerX = x
        self.playerY = y
        self.playerImg = img
        self.playerY_change=pY_change

    def draw_player(self, playerX, playerY, playerImg,screen):
        screen.blit(playerImg, (playerX, playerY))
import pygame

#Initialize Window Details
(width, height) = (1080, 720) #Self-explanatory
background_colour = (24,25,26)
#background_colour = (36,0x19,0x26)
#background_colour = (0x242526)  #Just testing to see what works
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Hassam & Zaeem\'s Chess Bot')

#Tweaj these depending on aesthetic
offsetX = width / 64 
offsetY = height / 64
whiteSquare = 0xEEEED2
blackSquare = 0x769656


#Fill board
for i in range(8):
    for j in range(8):
        #Lol the things i do to avoid an if statement
        pygame.draw.rect(screen, (whiteSquare-blackSquare) * ((i + j + 1) % 2) + blackSquare, pygame.Rect(64 *  i + offsetX , 64 * j + offsetY, 64, 64))


pygame.display.flip() #Updates display, i think 

#Run the window (Game Loop)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
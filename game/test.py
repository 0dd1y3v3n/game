#imports libraries ready for use
import pygame
import math

#this initiates pygame and creates a window called "game_display"
pygame.init()
game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption('test')
#the clock is created for use later
clock = pygame.time.Clock()
#the condition for the while loop is set to true
playing = True

#a while loop is created for running the code
while playing:
	#this is some code that will detect is the user selscts the quit button and exits while loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
	#this code fills in the screen with white and then draws a circle and a selection of lines
	gameDisplay.fill((255,255,255))
	pygame.draw.circle(gameDisplay, (0,0,0), (400, 300), 100, 2)
	for a in range(360):
		pygame.draw.line(gameDisplay, (0,0,0), (400,300), ,2)
	#this will then update the window with the new drawings
	pygame.display.update()
	#here i am setting the refresh rate to 100 frames per second
	clock.tick(100)
#here i am quiting pygame and the window when the users exits the loop
pygame.quit()
quit()
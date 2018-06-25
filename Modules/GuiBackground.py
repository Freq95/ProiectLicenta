import pygame
from time import sleep


def access_grant_GUI():
    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([400, 400])

    # This sets the name of the window
    pygame.display.set_caption('Acces Permis')

    clock = pygame.time.Clock()

    # Before the loop, load the sounds:

    # Set positions of graphics
    background_position = [0, 0]

    # Load and set up graphics.
    background_image = pygame.image.load("D:\\GitLocalRepo\\ProiectLicenta_git\\Documentatie\\App\\AccesPermis.png").convert()
    player_image = pygame.image.load("D:\\GitLocalRepo\\ProiectLicenta_git\\Documentatie\\App\\AccesPermis.png").convert()
    # player_image.set_colorkey(BLACK)

    # Copy image to screen:
    screen.blit(background_image, background_position)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.

    # Copy image to screen:
    # screen.blit(player_image, [x, y])

    pygame.display.flip()
    sleep(3.5)
    pygame.quit()


import sys, pygame
pygame.init()

size = width, height = 1600, 900
speed = [2, 3]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png").convert()  # convert works on pixel format, not file format. If convert isn't used, SDL converts on-the-fly each blit, which is silly.
scaledball = pygame.transform.scale(ball, (20, 20))

ballrect = scaledball.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]

	screen.fill(black)
	screen.blit(scaledball, ballrect)
	pygame.display.update() # try specifying pygame.display.update(ballrect) to draw some fun stuff!
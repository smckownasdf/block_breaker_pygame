import sys, pygame

# Static Variables
screen_size = width, height = 1600, 900
ball_speed = [400, 600]
black = 0, 0, 0

class Ball(object):
	def __init__(self, speed, screen):
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = speed
		self.screen = screen

	def move(self, screen_rect, dt):
		self.rect = self.rect.move(self.speed[0]*dt, self.speed[1]*dt)
		if self.rect.left < 0 or self.rect.right > screen_rect.right:
			self.speed[0] = -self.speed[0]
		if self.rect.top < 0 or self.rect.bottom > screen_rect.bottom:
			self.speed[1] = -self.speed[1]

	def draw(self, surface):
		surface.blit(self.image, self.rect)

class App(object):
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()
		self.fps = 120
		self.done = False
		self.keys = pygame.key.get_pressed()
		self.ball = Ball(ball_speed, self.screen)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
				self.keys = pygame.key.get_pressed()

	def render(self):
		self.screen.fill(black)
		self.ball.draw(self.screen)
		pygame.display.update()

	def update(self, dt):
		self.ball.move(self.screen_rect, dt)

	def main_loop(self):
		dt = 0
		self.clock.tick(self.fps)
		while not self.done:
			self.event_loop()
			self.update(dt)
			self.render()
			dt = self.clock.tick(self.fps)/1000.0

def main():
	pygame.init()
	pygame.display.set_mode(screen_size)
	App().main_loop()
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()

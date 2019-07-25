import sys, pygame

# Static Variables
screen_size = width, height = 1600, 900
ball_speed = [400, 600]
black = (0, 0, 0, 255)
transparent = (0, 0, 0, 0)
paddle_color = pygame.Color(154, 100, 220, a=200)

paddle_move_dict = {pygame.K_LEFT	: [-1, 0],
					pygame.K_RIGHT	: [ 1, 0]}

class Ball(object):
	def __init__(self, speed, screen):
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = speed
		self.screen = screen

	def move(self, screen_rect, dt):
		self.rect = self.rect.move(self.speed[0]*dt, self.speed[1]*dt)
		if self.rect.left < 0 or self.rect.right > screen_rect.right:
			self.speed[0] = -self.speed[0] - 5
		if self.rect.top < 0:
			self.speed[1] = -self.speed[1] + 5
		self.lost_ball(screen_rect)

	def lost_ball(self, screen_rect):
		if self.rect.top > screen_rect.bottom:
			self.rect.top = 0

	def draw(self, surface):
		surface.blit(self.image, self.rect)

class Paddle(object):
	size = (150, 20)
	def __init__(self, posx, posy):
		self.image = self.create_paddle()
		self.rect = self.image.get_rect(center=(posx, posy))
		self.true_pos = list(self.rect.center)
		self.move_speed = 20

	def create_paddle(self):
		image = pygame.Surface(Paddle.size).convert_alpha()
		image.fill(transparent)
		img_rect = image.get_rect()
		pygame.draw.rect(image, paddle_color, img_rect)
		return image

	def update(self, pressedkeys, screen_rect, dt):
		if pressedkeys[pygame.K_LEFT]:
			if self.rect.left > 0:
				self.true_pos[0] -= self.move_speed
		if pressedkeys[pygame.K_RIGHT]:
			if self.rect.right < screen_rect.right:
				self.true_pos[0] += self.move_speed
		self.rect.center = self.true_pos

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
		self.paddle_offset = 30
		self.paddle = Paddle(self.screen_rect.centerx, self.screen_rect.bottom - self.paddle_offset)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
				self.keys = pygame.key.get_pressed()

	def paddle_hit(self):
		if pygame.sprite.collide_rect(self.paddle, self.ball):
			self.ball.speed[1] = -self.ball.speed[1] - 5

	def render(self):
		self.screen.fill(black)
		self.ball.draw(self.screen)
		self.paddle.draw(self.screen)
		pygame.display.update()

	def update(self, dt):
		self.ball.move(self.screen_rect, dt)
		self.paddle.update(self.keys, self.screen_rect, dt)

	def main_loop(self):
		dt = 0
		self.clock.tick(self.fps)
		while not self.done:
			self.event_loop()
			self.update(dt)
			self.render()
			self.paddle_hit()
			dt = self.clock.tick(self.fps)/1000.0

def main():
	pygame.init()
	pygame.display.set_mode(screen_size)
	App().main_loop()
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()

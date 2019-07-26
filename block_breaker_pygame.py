import sys, pygame

# Static Variables
screen_size = width, height = 1600, 900
ball_speed = [400, 600]
black = (0, 0, 0, 255)
transparent = (0, 0, 0, 0)

class Ball(object):
	def __init__(self, speed, screen):
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = speed
		self.screen = screen

	def bouncex(self):
		if self.speed[0] >= 0:
			self.speed[0] = -self.speed[0]
		else:
			self.speed[0] = -self.speed[0]

	def bouncey(self):
		if self.speed[1] >= 0:
			self.speed[1] = -self.speed[1]
		else:
			self.speed[1] = -self.speed[1]

	def bounce(self, collider):
		if self.rect.colliderect(collider):
			if self.speed[1] >= 0: # ball is moving up
				if self.speed[0] >= 0: # ball is moving right
					# vertical distance between objects is less than horizontal distance
					if abs(collider.rect.bottom - self.rect.top) <= abs(collider.rect.left - self.rect.right):
						self.bouncey()
						self.rect.bottom = collider.rect.top
					else: # horizontal distance less than vertical distance
						self.bouncex()
						self.rect.right = collider.rect.left
				else: # ball is moving up and left
					# vert collision closer than horizontal
					if abs(collider.rect.bottom - self.rect.top) <= abs(collider.rect.right - self.rect.left):
						self.bouncey()
						self.rect.bottom = collider.rect.top
					else:
						self.bouncex()
						self.rect.left = collider.rect.right
			else: # ball is moving down
				if self.speed[0] >= 0: # if ball is moving right
					# if the difference between  - ball.rect.top) >= (block.rect.left - ball.rect.right):
					if abs(collider.rect.top - self.rect.bottom) <= abs(collider.rect.left - self.rect.right):
						# self.ball.speed
						self.bouncey()
						self.rect.top = collider.rect.bottom
					else:
						self.bouncex()
						self.rect.right = collider.rect.left
				else: # ball is moving down and left
					if abs(collider.rect.top - self.rect.bottom) <= abs(collider.rect.right - self.rect.left):
						self.bouncey()
						self.rect.top = collider.rect.bottom
					else:
						self.bouncex()
						self.rect.left = collider.rect.right


	def move(self, screen_rect, dt):
		self.rect = self.rect.move(self.speed[0]*dt, self.speed[1]*dt)
		if self.rect.left < 0:
			self.bouncex()
			self.rect.left = 0
		elif self.rect.right > screen_rect.right:
			self.bouncex()
			self.rect.right = screen_rect.right
		if self.rect.top < 0:
			self.bouncey()
			self.rect.top = 0
		self.lost_ball(screen_rect)

	def lost_ball(self, screen_rect):
		if self.rect.top > screen_rect.bottom:
			self.rect.top = 0

	def draw(self, surface):
		surface.blit(self.image, self.rect)

class Paddle(object):
	size = (150, 20)
	paddle_color = pygame.Color(154, 100, 220, a=200)
	def __init__(self, posx, posy):
		self.image = self.create_paddle()
		self.rect = self.image.get_rect(center=(posx, posy))
		self.true_pos = list(self.rect.center)
		self.move_speed = 20

	def create_paddle(self):
		image = pygame.Surface(Paddle.size).convert_alpha()
		image.fill(transparent)
		img_rect = image.get_rect()
		pygame.draw.rect(image, Paddle.paddle_color, img_rect)
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

class Block(object):
	size = (350, 80)
	block_color = pygame.Color(220,114,42,a=200)
	one_hit = 1
	def __init__(self, posx, posy, hitmax):
		self.image = self.create_block()
		self.rect = self.image.get_rect(center=(posx, posy))
		self.hit_count = 0
		self.hit_max = hitmax

	def create_block(self):
		image = pygame.Surface(Block.size).convert_alpha()
		image.fill(transparent)
		img_rect = image.get_rect()
		pygame.draw.rect(image, Block.block_color, img_rect)
		return image

	def draw(self, surface):
		surface.blit(self.image, self.rect)

	def destroy(self, hitmax):
		pass

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
		self.block = Block(500, 100, Block.one_hit)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
				self.keys = pygame.key.get_pressed()

	def render(self):
		self.screen.fill(black)
		self.ball.draw(self.screen)
		self.paddle.draw(self.screen)
		self.block.draw(self.screen)
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
			self.ball.bounce(self.block)
			self.ball.bounce(self.paddle)
			dt = self.clock.tick(self.fps)/1000.0

def main():
	pygame.init()
	pygame.display.set_mode(screen_size)
	App().main_loop()
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()

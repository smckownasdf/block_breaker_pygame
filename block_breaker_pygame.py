import sys, pygame

# Static Variables
screen_size = width, height = 1600, 900
ball_speed = [400, 600]
transparent = (0, 0, 0, 0)

class Ball(pygame.sprite.Sprite):
	def __init__(self, speed, screen):
		pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = speed
		self.screen = screen
		self.corner_threshhold = 1.5

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
			if collider.__class__.__name__ == "Block":
				collider.hit()
			if self.speed[1] >= 0: # ball is moving down
				if self.speed[0] >= 0: # ball is moving right
					# Corner hit
					if abs(abs(self.rect.bottom - collider.rect.top) - abs(self.rect.right - collider.rect.left)) <= self.corner_threshhold:
						pass
					# Contact is more vertical than horizontal 
					elif abs(self.rect.bottom - collider.rect.top) <= abs(self.rect.right - collider.rect.left):
						self.bouncey()
						self.rect.bottom = collider.rect.top
					# Contact is more horizontal than vertical
					else:
						self.bouncex()
						self.rect.right = collider.rect.left
				else: # ball is moving down and left
					# Corner hit
					if abs(abs(self.rect.bottom - collider.rect.top) - abs(self.rect.left - collider.rect.right)) <= self.corner_threshhold:
						pass
					# Contact more vertical than horizontal
					elif abs(self.rect.bottom - collider.rect.top) <= abs(self.rect.left - collider.rect.right):
						self.bouncey()
						self.rect.bottom = collider.rect.top
					# Contact more horizontal than vertical
					else:
						self.bouncex()
						self.rect.left = collider.rect.right
			else: # ball is moving up
				if self.speed[0] >= 0: # ball is moving right
					# Corner hit
					if abs(abs(self.rect.top - collider.rect.bottom) - abs(self.rect.right - collider.rect.left)) <= self.corner_threshhold:
						pass
					# More vertical than horizontal
					elif abs(self.rect.bottom - collider.rect.top) <= abs(self.rect.right - collider.rect.left):
						self.bouncey()
						self.rect.top = collider.rect.bottom
					# More horizontal than vertical
					else:
						self.bouncex()
						self.rect.right = collider.rect.left
				else: # ball is moving up and left
					# Corner hit
					if abs(abs(self.rect.top - collider.rect.bottom) - abs(self.rect.left - collider.rect.right)) <= self.corner_threshhold:
						pass
					# More vertical than horizontal
					elif abs(self.rect.top - collider.rect.bottom) <= abs(self.rect.left - collider.rect.right):
						self.bouncey()
						self.rect.top = collider.rect.bottom
					# More horizontal than vertical
					else:
						self.bouncex()
						self.rect.left = collider.rect.right

	def update(self):
		self.rect = self.rect.move(self.speed[0]*App.dt, self.speed[1]*App.dt)

	def screen_edges(self, screen_rect):
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

class Paddle(pygame.sprite.Sprite):
	size = (150, 20)
	paddle_color = pygame.Color(154, 100, 220, a=200)
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self)
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

	def update(self):
		self.rect.center = self.true_pos
		if App.pressed_left:
			self.true_pos[0] -= self.move_speed
		if App.pressed_right:
			self.true_pos[0] += self.move_speed

class Block(pygame.sprite.Sprite):
	size = (350, 80)
	block_color = pygame.Color(220,114,42,a=200)
	one_hit = 1
	two_hit = 2
	three_hit = 3
	def __init__(self, posx, posy, hitmax):
		pygame.sprite.Sprite.__init__(self)  # Call sprite initializer
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

	def hit(self):
		self.hit_count += 1
		print(self.hit_count)
		self.destroy()

	def destroy(self):
		if self.hit_count == self.hit_max:
			self.kill()
			print("killed?")


class App(object):
	pressed_left = False
	pressed_right = False
	dt = 0
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
		self.block = Block(500, 100, Block.three_hit)
		self.all_sprites = pygame.sprite.RenderPlain((self.ball, self.block, self.paddle))
		self.background = self.create_background()

	def create_background(self):
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((50,50,50))
		return self.background


	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					App.pressed_left = True
				if event.key == pygame.K_RIGHT:
					App.pressed_right = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					App.pressed_left = False
				elif event.key == pygame.K_RIGHT:
					App.pressed_right = False

	def contain_paddle(self): # Should probably be in Paddle, but I didn't want to bother connecting screen_rect to Paddle class
		if self.paddle.rect.left <= 0:
			App.pressed_left = False
		elif self.paddle.rect.right >= self.screen_rect.right:
			App.pressed_right = False

	def bounce(self):
		if self.block in self.all_sprites:
			self.ball.bounce(self.block)
		self.ball.bounce(self.paddle)		

	def update(self):
		self.bounce()
		self.all_sprites.update()
		self.contain_paddle()
		self.screen.blit(self.background, (0,0))
		self.all_sprites.draw(self.screen)
		pygame.display.flip()

	def main_loop(self):
		self.clock.tick(self.fps)
		while not self.done:
			self.event_loop()
			self.update()
			self.ball.screen_edges(self.screen_rect) # Again, like in App.contain_paddle()...Didn't want to pass screen_rect to ball, but probably should
			App.dt = self.clock.tick(self.fps)/1000.0

def main():
	pygame.init()
	pygame.display.set_mode(screen_size)
	pygame.display.set_caption('Pygame Block Breaker')
	App().main_loop()
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()

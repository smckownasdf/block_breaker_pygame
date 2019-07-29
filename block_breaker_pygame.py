import sys, pygame

# Global Variables
screen_size = width, height = 1600, 800
ball_speed = [400, 600]
transparent = (0, 0, 0, 0)
pixelx = 64
pixely = 32

class Ball(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = ball_speed
		self.screen = pygame.display.get_surface()
		self.corner_threshhold = 1.5
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()

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
		self.screen_edges()

	def screen_edges(self):
		if self.rect.left < 0:
			self.bouncex()
			self.rect.left = 0
		elif self.rect.right > self.screen_rect.right:
			self.bouncex()
			self.rect.right = self.screen_rect.right
		if self.rect.top < 0:
			self.bouncey()
			self.rect.top = 0
		self.lost_ball(self.screen_rect)

	def lost_ball(self, screen_rect):
		if self.rect.top > screen_rect.bottom:
			self.rect.top = 0

class Paddle(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.size = (150, 20)
		self.paddle_color = pygame.Color(154, 100, 220, a=200)
		self.image = self.create_paddle()
		self.rect = self.image.get_rect(center=(posx, posy))
		self.true_pos = list(self.rect.center)
		self.move_speed = 20
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()

	def create_paddle(self):
		image = pygame.Surface(self.size).convert_alpha()
		image.fill(transparent)
		img_rect = image.get_rect()
		pygame.draw.rect(image, self.paddle_color, img_rect)
		return image

	def contain_paddle(self): 
		if self.rect.left <= 0:
			App.pressed_left = False
		elif self.rect.right >= self.screen_rect.right:
			App.pressed_right = False

	def update(self):
		self.contain_paddle()
		self.rect.center = self.true_pos
		if App.pressed_left:
			self.true_pos[0] -= self.move_speed
		if App.pressed_right:
			self.true_pos[0] += self.move_speed

class Block(pygame.sprite.Sprite):
	one_hit = 1
	two_hit = 2
	three_hit = 3
	def __init__(self, posx, posy, hitmax):
		pygame.sprite.Sprite.__init__(self)  # Call sprite initializer
		self.hit_count = 0
		self.hit_max = hitmax
		self.size = (62, 30)
		self.block_color = self.determine_color()
		self.image = self.create_block()
		self.rect = self.image.get_rect(center=(posx, posy))

	def determine_color(self):
		if self.hit_max == 1:
			block_color = pygame.Color(220,114,42,a=200)
		elif self.hit_max == 2:
			block_color = pygame.Color(0,0,220,a=200)
		elif self.hit_max == 3:
			block_color = pygame.Color(42,220,114,a=200)
		return block_color

	def create_block(self):
		image = pygame.Surface(self.size).convert_alpha()
		image.fill(transparent)
		img_rect = image.get_rect()
		pygame.draw.rect(image, self.block_color, img_rect)
		return image

	def hit(self):
		self.hit_count += 1
		self.destroy()

	def destroy(self):
		if self.hit_count == self.hit_max:
			self.kill()

class Level(object):
	def __init__(self):
		self.halfcol = pixelx/2
		self.level_layout = None
		self.background = self.create_background()
		self.ball = None
		self.paddles = pygame.sprite.Group()
		self.blocks = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.Group()

	def collision_check(self):
		collisions = pygame.sprite.spritecollide(self.ball, self.all_sprites, False)
		for objects in collisions:
			self.ball.bounce(objects)

	def create_background(self):
		self.background = pygame.Surface(screen_size)
		self.background = self.background.convert()
		self.background.fill((50,50,50))
		return self.background

	def choose_level(self, level=1):
		if level == 1:
			self.level_layout = [ # 26 * 26
				"                          ",
				"                  B       ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"  1111111111111111111111  ",
				"/  111111111111111111111  /",
				"  1111111111111111111111  ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"          P               ",
				"                          ",
			]
		if level == 2:
			self.level_layout = [
				"                          ",
				"                  B       ",
				"                          ",
				"                          ",
				"  2222222222222222222222  ",
				"  2                    2  ",
				"  2                    2  ",
				"  2 111111111111111111 2  ",
				"  2/1111111111111111111/2  ",
				"  2 111111111111111111 2  ",
				"  2                    2  ",
				"  2                    2  ",
				"  2222222222222222222222  ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"                          ",
				"          P               ",
				"                          ",
			]

	def build_level(self):
		x = 0
		y = 0
		for row in self.level_layout:
			for col in row:
				half = False
				if col == "1":
					block = Block(x,y, Block.one_hit)
					self.blocks.add(block)
					self.all_sprites.add(block)
				elif col == "2":
					block = Block(x,y, Block.two_hit)
					self.blocks.add(block)
					self.all_sprites.add(block)
				elif col == "3":
					block = Block(x,y, Block.three_hit)
					self.blocks.add(block)
					self.all_sprites.add(block)
				elif col == "P":
					paddle = Paddle(x,y)
					self.all_sprites.add(paddle)
					self.paddles.add(paddle)
				elif col == "B":
					ball = Ball(x,y)
					self.ball = ball
					self.all_sprites.add(self.ball)
				if col == "/":
					x += self.halfcol
				else: 
					x += pixelx
			y += pixely
			x = 0

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
		self.level = Level()
		self.level.choose_level(2)
		self.level.build_level()

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

	def update(self):
		self.level.all_sprites.update()
		self.level.collision_check()
		self.screen.blit(self.level.background, (0,0))
		self.level.all_sprites.draw(self.screen)
		pygame.display.flip()

	def main_loop(self):
		self.clock.tick(self.fps)
		while not self.done:
			self.event_loop()
			self.update()
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
import sys, pygame
import random

# Global Variables
screen_size = width, height = 1600, 800
transparent = (0, 0, 0, 0)
pixelx = 64
pixely = 32

class Ball(pygame.sprite.Sprite):
	count = 3
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = [400, 600]
		self.corner_threshhold = 1.5
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.spin = 0

	def bouncex(self):
		self.speed[0] = -self.speed[0]
		self.speed[1] = self.speed[1]

	def bouncey(self):
		self.speed[1] = -self.speed[1]
		self.speed[0] = self.speed[0] + self.spin

	def bounce(self, collider):
		if self.rect.colliderect(collider):
			if collider.__class__.__name__ == "Block":
				collider.hit()
			if collider.__class__.__name__ == "Paddle":
				if App.pressed_left:
					self.spin = 100
				elif App.pressed_right:
					self.spin = -100
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
		self.spin = 0

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
		if self.rect.top > screen_rect.bottom + 300:
			Ball.count -= 1
			print(Ball.count)
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
		Display_Score.score += 150
		self.destroy()

	def destroy(self):
		if self.hit_count == self.hit_max:
			self.kill()
			Display_Score.score += 500
			Level.block_count -= 1
			print("Block count: " + str(Level.block_count))

class Level(object):
	block_count = None
	def __init__(self):
		self.halfcol = pixelx/2
		self.level_layout = None
		self.background = self.create_background()
		self.ball = None
		self.paddles = pygame.sprite.Group()
		self.blocks = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.Group()
		self.ui_display = UI_Display()
		self.ball_count = Ball.count
		self.ui_display.display_ball_count()
		self.all_sprites.add(self.ui_display.all_sprites)
		self.display_score = Display_Score()

	def collision_check(self):
		collisions = pygame.sprite.spritecollide(self.ball, self.all_sprites, False)
		for objects in collisions:
			self.ball.bounce(objects)

	def create_background(self):
		self.background = pygame.Surface(screen_size)
		self.background = self.background.convert()
		self.background.fill((0,0,0))
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
				"  2/1111111113111111111/2  ",
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
		Level.block_count = len(self.blocks)

	def clear_level(self):
		self.level_layout = None
		self.ball = None
		self.blocks.empty()
		self.all_sprites.empty()
		self.ball_count = Ball.count
		self.ui_display.display_ball_count()
		self.all_sprites.add(self.ui_display.all_sprites)



class Display_Score(object):
	score = 0
	def __init__(self):
		self.num_value = Display_Score.score
		self.zeroes = ""
		self.zero_str = "0"
		self.str_value = self.num_value_to_text()

	def num_value_to_text(self):
		self.zeroes = ""
		while (len(self.zeroes) + len(str(self.num_value)) < 7):
			self.zeroes += self.zero_str
		self.str_value = self.zeroes + str(self.num_value)
		return self.str_value

	def update(self):
		self.num_value = Display_Score.score
		self.num_value_to_text()

class UI_Display(object):
	def __init__(self):
		self.all_sprites = pygame.sprite.Group()
		self.ball_count = Ball.count
		self.ball1 = Display_Ball(20,20)
		self.ball2 = Display_Ball(45,20)
		self.ball3 = Display_Ball(70,20)
		self.pause_overlay = self.build_pause_overlay()
		self.pause_text = Display_Text(64,"GAME PAUSED", (800, 300))
		self.pause_message = Display_Text(48,'Press "P" to Resume', (800, 500))
		self.blocks_left = Display_Text(32, "Blocks Remaining: " + str(Level.block_count), (800, 600))
		self.display_score = Display_Score()
		self.score_text = self.display_score.str_value
		self.score = Display_Text(32, self.score_text, (1550, 50), True)

	def display_ball_count(self):
		self.all_sprites.add(self.ball1)
		self.all_sprites.add(self.ball2)
		self.all_sprites.add(self.ball3)

	def update(self):
		self.ball_count = Ball.count
		if self.ball_count == 2:
			self.ball3.kill()
		if self.ball_count == 1:
			self.ball2.kill()
		if self.ball_count == 0:
			self.ball1.kill()
		self.display_score.update()
		self.score_text = self.display_score.str_value
		self.score = Display_Text(32, self.score_text, (1550, 50), True)
		self.blocks_left = Display_Text(32, "Blocks Remaining: " + str(Level.block_count), (800, 600))

	def build_display(self):
		self.display_ball_count()

	def build_pause_overlay(self):
		self.pause_overlay = pygame.Surface(screen_size)
		self.pause_overlay.set_alpha(128)
		self.pause_overlay.fill((255,200,200))
		return self.pause_overlay

class Display_Text(object):
	def __init__(self, size, text, center_tuple, is_right=False):
		self.font_size = size
		self.font = self.create_font()
		self.text = text
		self.is_right = is_right
		self.tuple = center_tuple
		self.rendered_text = self.render_font()
		self.text_rect = self.create_text_rect()

	def create_font(self):
		self.font = pygame.font.Font('XeroxSerifWideBold.ttf',self.font_size)
		return self.font

	def create_text_rect(self):
		if self.is_right:
			self.text_rect = self.rendered_text.get_rect(midright=self.tuple)
			return self.text_rect
		else:
			self.text_rect = self.rendered_text.get_rect(center=self.tuple)
			return self.text_rect

	def render_font(self):
		self.rendered_text = self.font.render(self.text, True, (255,255,255))
		return self.rendered_text

class Display_Ball(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect(center=(posx, posy))

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
		self.current_level = 1
		self.level = Level()
		self.level.choose_level(self.current_level)
		self.level.build_level()
		self.level.ui_display.build_display()
		self.paused = False

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				self.pause()
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

	def pause(self):
		self.paused = True
		self.level.ui_display.update()
		self.screen.blit(self.level.ui_display.pause_overlay, (0,0))
		self.screen.blit(self.level.ui_display.pause_text.rendered_text, self.level.ui_display.pause_text.text_rect)	
		self.screen.blit(self.level.ui_display.pause_message.rendered_text, self.level.ui_display.pause_message.text_rect)	
		self.screen.blit(self.level.ui_display.blocks_left.rendered_text, self.level.ui_display.blocks_left.text_rect)

	def paused_event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				self.paused = False

	def update(self):
		if not self.paused:
			self.level.ui_display.update()
			self.level.all_sprites.update()
			self.level.collision_check()
			self.screen.blit(self.level.background, (0,0))
			pygame.draw.rect(self.screen, (0,0,0), self.level.ui_display.score.text_rect)
			self.screen.blit(self.level.ui_display.score.rendered_text, self.level.ui_display.score.text_rect)
			self.level.all_sprites.draw(self.screen)
		pygame.display.flip()

	def main_loop(self):
		self.clock.tick(self.fps)
		while not self.done:
			if self.paused:
				self.paused_event_loop()
			else:
				self.event_loop()
			self.update()
			if Level.block_count == 0:
				Ball.count = 3
				self.level.clear_level()
				self.current_level += 1
				self.level.choose_level(self.current_level)
				self.level.build_level()
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
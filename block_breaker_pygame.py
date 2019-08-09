import sys, pygame
from bblevels import levels as bblevels , bonus_time as bonus_time

# Global Variables
screen_size = width, height = 1600, 800
transparent = (0, 0, 0, 0)
pixelx = 64
pixely = 32

class Ball(pygame.sprite.Sprite):
	count = 3
	lost = False
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
			Ball.lost = True
			self.rect.top = screen_rect.top

class Paddle(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.size = (150, 20)
		self.paddle_color = pygame.Color(154, 100, 220, a=200)
		self.image = self.create_paddle()
		self.rect = self.image.get_rect(center=(posx, posy))
		self.true_pos = list(self.rect.center)
		self.move_speed = 8
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
	count = None
	def __init__(self, posx, posy, hitmax, xl=False, test=False):
		pygame.sprite.Sprite.__init__(self)  # Call sprite initializer
		self.test = test
		self.xl = xl
		self.hit_count = 0
		self.hit_max = hitmax
		self.size = self.determine_size()
		self.block_color = self.determine_color()
		self.image = self.create_block()
		self.rect = self.image.get_rect(center=(posx, posy))

	def determine_size(self):
		if self.xl:
			size = (126, 62)
		elif self.test:
			size = (1280, 30)
		else:
			size = (62, 30)
		return size

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
			Block.count -= 1

class Level(object):
	name = None
	current_time = None
	def __init__(self):
		self.halfcol = pixelx/2
		self.level_layout = None
		self.background = self.create_background()
		self.ball = None
		self.paddle = None
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
		background = pygame.Surface(screen_size)
		background = background.convert()
		background.fill((0,0,0))
		return background

	def choose_level(self, level=1):
		if level == 1:
			Level.name = "level1"
		if level == 2:
			Level.name = "level2"
		if level == 3:
			Level.name = "level3"
		if level > 3:
			raise NotImplementedError
		self.level_layout = bblevels.get(Level.name)

	def build_level(self):
		x = 0
		y = 0
		for row in self.level_layout:
			for col in row:
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
					self.paddle = paddle
					self.all_sprites.add(paddle)
					self.paddles.add(paddle)
				elif col == "B":
					ball = Ball(x,y)
					self.ball = ball
					self.all_sprites.add(self.ball)
				elif col == "T":
					block = Block(x,y, Block.one_hit, xl=False, test=True)
					self.blocks.add(block)
					self.all_sprites.add(block)
				elif col == " ":
					pass
				else:
					pass
				if col == "/":
					x -= self.halfcol
				x += pixelx
			y += pixely
			x = 0
		Block.count = len(self.blocks)

	def clear_level(self):
		self.level_layout = None
		self.ball = None
		self.blocks.empty()
		self.all_sprites.empty()
		self.ball_count = Ball.count
		self.ui_display.display_ball_count()
		self.add_bonus()
		self.ui_display.play_timer.restart_timer()
		self.all_sprites.add(self.ui_display.all_sprites)

	def add_bonus(self):
		time = bonus_time.get(Level.name)
		if self.ui_display.play_timer.current_time < time:
			bonus = int((time - self.ui_display.play_timer.current_time)/300)
			Display_Score.score += bonus

	def update(self):
		Level.current_time = self.ui_display.play_timer.current_time
		self.ui_display.update()
		self.collision_check()
		self.all_sprites.update()

class Start_Menu(object):
	def __init__(self):
		self.title = Display_Text(128,"BLOCK BREAKER", (800, 300), color=(255,50,50))
		self.subtitle = Display_Text(48,"A Clone by Scott McKown, Built Using PyGame", (800, 400), color=(255,80,80))
		self.instructions = Display_Text(32,"Press Spacebar to Begin", (800, 650), color=(30,255,50))
		self.background = self.create_background()
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()

	def create_background(self):
		background = pygame.Surface(screen_size)
		background = background.convert()
		background.fill((0,0,0))
		return background

	def update(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.title.rendered_text, self.title.text_rect)
		self.screen.blit(self.subtitle.rendered_text, self.subtitle.text_rect)
		self.screen.blit(self.instructions.rendered_text, self.instructions.text_rect)
		pygame.display.flip()

class Results_Screen(object):
	def __init__(self):
		self.game_over_title = Display_Text(128,"GAME OVER", (800, 300), color=(255,50,50))
		self.instructions = Display_Text(32,"Press Spacebar to Play Again", (800, 650), color=(30,255,50))
		self.final_score = Display_Text(64,"Final Score: "+str(Display_Score.score), (800, 450)) 
		self.background = self.create_background()
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()

	def create_background(self):
		background = pygame.Surface(screen_size)
		background = background.convert()
		background.fill((0,0,0))
		return background

	def update(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.game_over_title.rendered_text, self.game_over_title.text_rect)
		self.screen.blit(self.final_score.rendered_text, self.final_score.text_rect)
		self.screen.blit(self.instructions.rendered_text, self.instructions.text_rect)
		pygame.display.flip()

class UI_Display(object):
	def __init__(self):
		self.all_sprites = pygame.sprite.Group()
		self.ball_count = Ball.count
		self.ball1 = Display_Ball(20,20)
		self.ball2 = Display_Ball(45,20)
		self.ball3 = Display_Ball(70,20)
		self.pause_overlay = self.build_pause_overlay()
		self.pause_text = Display_Text(128,"GAME PAUSED", (800, 450), color=(255,25,230))
		self.pause_message = Display_Text(48,'Press "P" to Resume', (800, 520), color=(255,25,230))
		self.blocks_left = Display_Text(32, ("Blocks Remaining: " + str(Block.count)), (800, 670), color=(255,230,25))
		self.auto_toggle_off =  Display_Text(24, "Press A to Turn AutoPlay Off", (800,700), color=(255,25,25))
		self.auto_toggle_on = Display_Text(24, "Press A to Turn AutoPlay On", (800,700), color=(25,255,25))
		self.cd1 = Display_Text(128,"1", (800, 400)) #cd = countdown. The fact that I decided to write this comment means I should probably rename the darn variable
		self.cd2 = Display_Text(128,"2", (800, 400))
		self.cd3 = Display_Text(128,"3", (800, 400))
		self.play_timer = Play_Timer()
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
		self.play_timer.update()
		self.update_display_score()
		self.update_blocks_remaining()

	def update_blocks_remaining(self):
		self.blocks_left = Display_Text(32, "Blocks Remaining: " + str(Block.count), (800, 600))

	def update_display_score(self):	
		self.score_text = self.display_score.str_value
		self.score = Display_Text(32, self.score_text, (1550, 50),is_right=True)

	def build_display(self):
		self.display_ball_count()

	def build_pause_overlay(self):
		pause_overlay = pygame.Surface(screen_size)
		pause_overlay.set_alpha(128)
		pause_overlay.fill((255,200,200))
		return pause_overlay

class Display_Text(object):
	def __init__(self, size, text, center_tuple, is_right=False, color=(255,255,255)):
		self.font_size = size
		self.text = text
		self.tuple = center_tuple
		# center tuple becomes mid-right of text object when bool is_right == True
		self.is_right = is_right
		self.color = color
		self.font = self.create_font()
		self.rendered_text = self.render_font()
		self.text_rect = self.create_text_rect()

	def create_font(self):
		font = pygame.font.Font('XeroxSerifWideBold.ttf',self.font_size)
		return font

	def create_text_rect(self):
		if self.is_right:
			text_rect = self.rendered_text.get_rect(midright=self.tuple)
			return text_rect
		else:
			text_rect = self.rendered_text.get_rect(center=self.tuple)
			return text_rect

	def render_font(self):
		rendered_text = self.font.render(self.text, True, self.color)
		return rendered_text

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

class Display_Ball(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
		self.image = pygame.transform.scale(pygame.image.load("ball.png").convert(), (20,20)).convert_alpha()
		self.rect = self.image.get_rect(center=(posx, posy))

class Play_Timer(object):
	def __init__(self):
		self.font_size = 24
		self.font = pygame.font.Font('XeroxSerifWideBold.ttf', self.font_size)
		self.white = (255,255,255)
		self.yellow = (255,255,25)
		self.red = (255,25,25)
		self.rendered_time = None
		self.rect = None
		self.clock = pygame.time.Clock() 
		self.start_ticks = self.clock.get_time()
		self.current_ticks = self.clock.get_time()
		self.current_time = self.clock.get_time()

	def restart_timer(self):
		self.start_ticks = self.clock.get_time()
		self.current_ticks = self.clock.get_time()

	def update_time(self):
		self.current_ticks += self.clock.get_time()
		self.current_time = self.current_ticks - self.start_ticks

	def string_time(self):
		current_minutes = str(int((self.current_time % 600000)/60000)).zfill(2)
		raw_seconds = int((self.current_time % 600000)/1000)
		x = 1
		if raw_seconds >= 60*x:
			raw_seconds = raw_seconds - 60*x
			x += 1
		current_seconds = str(raw_seconds).zfill(2)
		current_decimal = str(int((self.current_time % 1000)/10)).zfill(2)
		return f"{current_minutes}:{current_seconds}:{current_decimal}"

	def pause(self):
		self.start_ticks += self.clock.get_time()

	def build_display(self, color):
		text = self.string_time()
		display_time = Display_Text(self.font_size, text, (1550,100), is_right=True, color=color)
		self.rect = display_time.text_rect
		self.rendered_time = display_time.rendered_text

	def change_color(self):
		timer_goal = bonus_time.get(Level.name)
		if((self.current_time + 30000) < timer_goal):
			color = self.white
		elif(self.current_time > timer_goal):
			color = self.red
		else:
			color = self.yellow
		return color

	def update(self):
		self.update_time()
		self.string_time()
		self.build_display(self.change_color())
		self.clock.tick()

class App(object):
	pressed_left = False
	pressed_right = False
	dt = 0
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()
		self.level = None
		self.start_ticks = pygame.time.get_ticks()
		self.start_menu = Start_Menu()
		self.results_screen = Results_Screen()
		self.fps = 200
		self.current_level = 1
		self.done = False
		self.started = False
		self.finished = False
		self.paused = False
		self.countdown = False
		self.auto_play = False

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

	def paused_event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				self.paused = False
				self.start_countdown()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				if self.auto_play:
					self.auto_play = False
				else:
					self.auto_play = True

	def menu_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.started = True
				self.finished = False
				self.reset_game()
				self.start_game()

	def countdown_counter(self):
		self.static_screen_update()
		self.level.paddle.update()
		seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
		if seconds < 1:
			pass
		elif seconds < 2:
			self.screen.blit(self.level.background, self.level.ui_display.cd3.text_rect, area=self.level.ui_display.cd3.text_rect)
			self.screen.blit(self.level.ui_display.cd3.rendered_text, self.level.ui_display.cd3.text_rect)
		elif 2 <= seconds < 3:
			self.screen.blit(self.level.background, self.level.ui_display.cd2.text_rect, area=self.level.ui_display.cd3.text_rect)
			self.screen.blit(self.level.ui_display.cd2.rendered_text, self.level.ui_display.cd2.text_rect)
		elif 3 <= seconds < 4:
			self.screen.blit(self.level.background, self.level.ui_display.cd1.text_rect, area=self.level.ui_display.cd2.text_rect)
			self.screen.blit(self.level.ui_display.cd1.rendered_text, self.level.ui_display.cd1.text_rect)
		else:
			self.countdown = False

	def start_game(self):
		self.level = Level()
		self.level.choose_level(self.current_level)
		self.level.build_level()
		self.level.ui_display.build_display()
		self.start_countdown()

	def reset_game(self):
		self.level = 1
		Ball.lost = False

	def auto_paddle(self):
		self.level.paddle.rect.centerx = self.level.ball.rect.centerx

	def pause(self):
		self.paused = True
		self.static_screen_update()
		self.screen.blit(self.level.ui_display.pause_overlay, (0,0))
		self.screen.blit(self.level.ui_display.pause_text.rendered_text, self.level.ui_display.pause_text.text_rect)	
		self.screen.blit(self.level.ui_display.pause_message.rendered_text, self.level.ui_display.pause_message.text_rect)	
		self.screen.blit(self.level.ui_display.blocks_left.rendered_text, self.level.ui_display.blocks_left.text_rect)
		if self.auto_play:
			self.screen.blit(self.level.ui_display.auto_toggle_off.rendered_text, self.level.ui_display.auto_toggle_off.text_rect)
		else:
			self.screen.blit(self.level.ui_display.auto_toggle_on.rendered_text, self.level.ui_display.auto_toggle_on.text_rect)

	def start_countdown(self):
		self.start_ticks = pygame.time.get_ticks()
		self.countdown = True
		Ball.lost = False

	def static_screen_update(self):
		self.screen.fill((0,0,0))
		self.level.ui_display.update()
		self.level.all_sprites.draw(self.screen)
		pygame.draw.rect(self.screen, (0,0,0), self.level.ui_display.score.text_rect)
		self.screen.blit(self.level.ui_display.score.rendered_text, self.level.ui_display.score.text_rect)
		pygame.draw.rect(self.screen, (0,0,0), self.level.ui_display.play_timer.rect)
		self.screen.blit(self.level.ui_display.play_timer.rendered_time, self.level.ui_display.play_timer.rect)

	def next_level(self):
		if self.current_level <= len(bblevels):	
			Ball.count = 3
			self.level.clear_level()
			self.current_level += 1
			if self.current_level > 3:
				self.current_level = 1
			self.level.choose_level(self.current_level)
			self.level.build_level()
			self.start_countdown()

	def update(self):
		if not self.paused:
			if not self.countdown:
				self.update_frame()
		pygame.display.flip()

	def update_frame(self):
		self.level.update()
		if self.auto_play:
			self.auto_paddle()
		self.screen.blit(self.level.background, (0,0))
		pygame.draw.rect(self.screen, (0,0,0), self.level.ui_display.score.text_rect)
		self.screen.blit(self.level.ui_display.score.rendered_text, self.level.ui_display.score.text_rect)
		pygame.draw.rect(self.screen, (0,0,0), self.level.ui_display.play_timer.rect)
		self.screen.blit(self.level.ui_display.play_timer.rendered_time, self.level.ui_display.play_timer.rect)
		self.level.all_sprites.draw(self.screen)

	def main_loop(self):
		self.clock.tick(self.fps)
		while not self.done:
			if not self.started:
				self.start_menu.update()
				self.menu_loop()
			elif self.finished:
				self.results_screen.update()
				self.menu_loop()
			else:
				if self.paused:
					self.pause()
					self.countdown = False
					self.paused_event_loop()
					self.level.ui_display.play_timer.pause()
				elif Ball.lost:
					if Ball.count == 0:
						self.results_screen = Results_Screen()
						self.finished = True
					else:
						self.event_loop()
						self.start_countdown()
				elif self.countdown:
					self.paused = False
					self.event_loop()
					self.countdown_counter()
					self.level.ui_display.play_timer.pause()
				else:
					self.event_loop()
				self.update()
				if Block.count == 0:
					self.next_level()
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
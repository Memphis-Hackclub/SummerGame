import arcade
import random
from math import *
import time
grid_width = 20
Sprite_Size = 20
crazyness = 5
seed = 230





def perlin(x, scale):
	x = (x *.006)+seed 
	y = int(abs((sin(2*x) + sin(pi * x*scale)))*scale)+1

	return int(abs((sin(2*x) + sin(pi * x*scale)))*scale)+1




def create_gride(height):
	return [0 for _y in range(height)]

def initialize_grid(grid, x=200):
	""" Randomly set grid locations to on/off based on chance. """
	height = len(grid)
	block_hight = perlin(x, crazyness)
	for row in range(height):
		if row < block_hight:
			grid[row] = 1
		if row == block_hight:
			grid[row] = 2
def grid2sprite(grid, grid_height, x=5, direction = 1):
	wall_list = arcade.SpriteList(use_spatial_hash=True)
	height = len(grid)
	for row in range(height):
			if grid[row]== 1:
				wall = arcade.Sprite("Textures/Tile/dirt.png", scale = Sprite_Size/16)
				wall.center_x = (x*Sprite_Size) + (direction * int(Sprite_Size/2))
				wall.center_y = row * Sprite_Size +(direction * int(Sprite_Size /2))
				
				wall_list.append(wall)
				

			if grid[row] == 2:
				wall = arcade.Sprite("Textures/Tile/grass.png", scale = Sprite_Size/16)
				wall.center_x = (x*Sprite_Size) + (direction * int(Sprite_Size/2))
				wall.center_y = row * Sprite_Size +(direction * int(Sprite_Size /2))

				wall_list.append(wall)
				
	return wall_list

class MyGame(arcade.Window):
	def __init__(self, width, height, title, resizable = False):
		super().__init__(width, height, title, resizable = resizable)
		self.wall_list = []
		self.mouse_cord = (None, None)
		self.width = width
		self.height = height
		self.old_px = 10
		self.new_px = self.old_px
		self.change = 0
		self.player_x = 50
		self.right = False
		self.left = False

		
		arcade.set_background_color(arcade.color.CADET_BLUE)

	def setup(self):
		self.grid_height = int(self.height/Sprite_Size)
		k = 0
		i = 0
		even = True
		while i < grid_width:
			self.grid = create_gride(self.grid_height)
			if even == True:
				print(seed+i)
				initialize_grid(self.grid, x=seed+i)
				self.wall_list.append(grid2sprite(self.grid, self.grid_height, x=int(i)+k))
				even = False
				i += 1
			elif even == False:
				initialize_grid(self.grid, x=seed-i)
				self.wall_list.insert(0,grid2sprite(self.grid, self.grid_height, x=int(-i)+k))
				even = True
				


	def on_draw(self):
		arcade.start_render()
		for i in range(len(self.wall_list)):
			self.wall_list[i].draw()
			arcade.draw_circle_filled(self.player_x, 200, 50 ,arcade.color.RED, 10)


	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.D:
			self.right = True
		if symbol == arcade.key.A:
			self.left = True

	def on_key_release(self, symbol, modifiers):
		if symbol == arcade.key.D:
			self.right = False
		if symbol == arcade.key.A:
			self.left = False

	def on_mouse_press(self, x, y, button, modifiers):
		colume = int(x/Sprite_Size)
		
		
		if button == arcade.MOUSE_BUTTON_LEFT:
	
			block = arcade.get_sprites_at_point((colume*Sprite_Size+(Sprite_Size/2), y), self.wall_list[colume+int(grid_width-1)])
			print(self.wall_list[-1][0].center_x)
	
			
			if len(block) > 0:
	
				self.wall_list[colume+int(grid_width)-1].remove(block[0])
	
			

	def update(self, delta_time):
		if self.right == True:
			self.player_x += 200 * delta_time
		if self.left == True:
			self.player_x -= 200 * delta_time

		if self.player_x + 100 >= self.wall_list[-1][0].center_x:
			self.create_row(1)
		if self.player_x - 100 <= self.wall_list[0][0].center_x:
			self.create_row(-1)
		
		

	def create_row(self, direction):
		y = ((self.wall_list[-1][0].center_x+Sprite_Size)/Sprite_Size)+seed-0.5
		print(y)
		if direction == 1:
			self.wall_list.pop(0)
			newrow = create_gride(self.grid_height)
			initialize_grid(newrow, x= ((self.wall_list[-1][0].center_x+Sprite_Size)/Sprite_Size)+seed-0.5)
			self.wall_list.append(grid2sprite(newrow, self.grid_height, x=self.wall_list[-1][0].center_x/Sprite_Size+0.5))
		if direction == -1:
			self.wall_list.pop(-1)
			newrow = create_gride(self.grid_height)
			initialize_grid(newrow, x=((self.wall_list[0][0].center_x-Sprite_Size)/Sprite_Size)+seed-0.5)
			self.wall_list.insert(0,grid2sprite(newrow, self.grid_height, x=self.wall_list[0][0].center_x/Sprite_Size-1.5))

def main():
	game = MyGame(1270, 700, "Game", resizable=True)
	game.setup()
	arcade.run()

if __name__ == "__main__":
	main()
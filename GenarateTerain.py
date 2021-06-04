import arcade
import random
from math import *
import time

#Terain class
class MyTerain():
	def __init__(self, window_width, window_height):

		self.window_width = window_width
		self.window_height = window_height
		self.world_list_complied = []
		self.world_list_uncomplied = arcade.SpriteList(use_spatial_hash=True)
		self.whole_world = []
		self.world_seed = random.randint(0,9999)*random.randint(0,9999)
		self.sprite_size = 16
		self.grid_height = int(self.window_height/self.sprite_size)
		self.left_bound = 0
		self.right_bound = 0
		#stores the amplatude of each hill
		self.crazyness = 5
		#how streched out are each hills
		self.smoothness = 0.006
		self.render_distence = 20

	#creates a blank list the length of |grid height|
	def create_colume(self, height):
		return [0 for _y in range(height)]

	#takes blank list and uses perlin noise to detirmin how much of the list is dirt
	def initialize_colume(self, grid, x=None):
		#finds the length of the blank list givin 
		height = len(grid)
		#finds noisy number to dirtimin how tall the block colume is going to be 
		block_hight = perlin(x, self.crazyness, self.world_seed, self.smoothness)
		#loops though each y value and matches that with the blocks ID givin a spesfic rule (subject to changes)
		for row in range(height):
			if row < block_hight:
				grid[row] = 1
			if row == block_hight:
				grid[row] = 2

	def trasnform_id_sprite(self, grid, grid_height, x=None):
		world_list_complied =  arcade.SpriteList(use_spatial_hash=True)
		height = len(grid)
		
		for row in range(height):
				if grid[row]== 1:
					block = arcade.Sprite("Textures/Tile/dirt.png", scale = self.sprite_size/16)
					block.center_x = (x*self.sprite_size) + int(self.sprite_size/2)
					block.center_y = row * self.sprite_size + int(self.sprite_size /2)
					world_list_complied.append(block)
				if grid[row] == 2:
					block = arcade.Sprite("Textures/Tile/grass.png", scale = self.sprite_size/16)
					block.center_x = (x*self.sprite_size) + int(self.sprite_size/2)
					block.center_y = row * self.sprite_size + int(self.sprite_size /2)
					world_list_complied.append(block)
		return world_list_complied

	def create_left_row(self):
		grid = self.create_colume(self.grid_height)
		self.initialize_colume(grid, x=(self.world_seed+self.left_bound))
		self.world_list_complied.insert(0, self.trasnform_id_sprite(grid, self.grid_height, x=int(self.left_bound)))
		self.whole_world.insert(0,[self.left_bound,self.trasnform_id_sprite(grid, self.grid_height, x=int(self.left_bound))])
		self.left_bound -= 1 
	def create_right_row(self):
		grid = self.create_colume(self.grid_height)
		self.initialize_colume(grid, x=self.world_seed+self.right_bound)
		self.world_list_complied.append(self.trasnform_id_sprite(grid, self.grid_height, x=int(self.right_bound)))
		self.whole_world.append([self.right_bound,self.trasnform_id_sprite(grid, self.grid_height, x=int(self.right_bound))])
		self.right_bound+=1

	def load_unload_chunks(self, player_x):
		if player_x - (self.render_distence*16) <= (self.left_bound)*self.sprite_size:
			load = self.find_if_already_loaded(self.left_bound)
			
			if load == False:
				self.create_left_row()
			else: 
				self.world_list_complied.insert(0,load)
				self.left_bound -= 1
			self.uncomplie_world_list()
		if player_x + (self.render_distence*16) >= (self.right_bound)*self.sprite_size:
			load = self.find_if_already_loaded(self.right_bound)
			if load == False:
				self.create_right_row()
			else: 
				self.world_list_complied.append(load)
				self.right_bound+=1 
			self.uncomplie_world_list()
		if player_x - (self.render_distence*16) >= (self.left_bound)*self.sprite_size:
			self.world_list_complied.pop(0)
			self.left_bound += 1
			self.uncomplie_world_list()
		if player_x + (self.render_distence*16) <= (self.right_bound)*self.sprite_size:
			self.world_list_complied.pop(-1)
			self.right_bound -= 1
			self.uncomplie_world_list()

	def uncomplie_world_list(self):
		self.world_list_uncomplied = arcade.SpriteList(use_spatial_hash=True)
		for i in range(len(self.world_list_complied)):
			for l in range(len(self.world_list_complied[i])):
				self.world_list_uncomplied.append(self.world_list_complied[i][l])
	def find_if_already_loaded(self, x):
		if len(self.whole_world) > 0:
			left_most_x = self.whole_world[0][0] 
			point_in_list = abs(left_most_x-abs(x)-1)
			if len(self.whole_world) > point_in_list and point_in_list >= 0:
				return self.whole_world[point_in_list][1]
	
		return False		
		
def perlin(x, scale,seed,smoothness):
	x = (x * smoothness)+seed 
	return int(abs((sin(2*x) + sin(pi * x*scale)))*scale)+1
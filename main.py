import arcade
import random
from math import *
import time
from GenarateTerain import MyTerain

class MyGame(arcade.Window):
	def __init__(self, width, height, title, resizable = False):
		super().__init__(width, height, title, resizable = resizable)
		self.MyTerain = MyTerain(width, height)
		self.player_x = 0
		self.player_speed = 300
		self.right = False
		self.left = False
	def on_draw(self):
		arcade.start_render()
		self.worldlist = self.MyTerain.world_list_uncomplied
		self.worldlist.draw()

	def update(self, delta_time):
		self.MyTerain.load_unload_chunks(self.player_x)
		if self.right == True:
			self.player_x += self.player_speed * delta_time
		if self.left == True:
			self.player_x -= self.player_speed * delta_time

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

	

def main():
	game = MyGame(1270, 700, "Game", resizable=True)
	arcade.run()

if __name__ == "__main__":
	main()

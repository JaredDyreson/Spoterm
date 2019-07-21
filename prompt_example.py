#!/usr/bin/env python3.5

# documentation -> https://code-maven.com/interactive-shell-with-cmd-in-python

from cmd import Cmd as c
import spot_utils
import os
from termcolor import colored
import serial
class base_prompt(c):
	prompt = 'spoterm>'
	options = ["albums", "artists", "songs"]
	def do_exit(self, inp):
		base_prompt.prompt = 'spoterm>'
		return True
	def do_cd(self, inp):
		if(inp == ".."):
			base_prompt.prompt = "spoterm>"
			return self.do_exit(inp)
		elif("artist" in inp):
			name_ = os.path.basename(inp)
			artist_sub_cli = artist_prompt(name_)
			artist_sub_cli.cmdloop()

	def default(self, inp):
		if(inp == ":q"):
			return self.do_exit(inp)
		elif(inp == ":qall"):
			quit()
class artist_prompt(base_prompt):
	def __init__(self, artist_sub_prompt_name: str):
		base_prompt.__init__(self)
		base_prompt.prompt = "spoterm/artist/{}>".format(artist_sub_prompt_name)

	def do_ls(self, inp):
		name = os.path.basename(base_prompt.prompt.replace('\\ ', '_').replace('_', ' ').replace('>', ''))
		artist = spot_utils.Artist(name)
		if(inp == "albums"):
			for album in artist.get_albums():
				print(colored(album, 'red'))
	def do_count(self, inp):
		name = os.path.basename(base_prompt.prompt.replace('\\ ', '_').replace('_', ' ').replace('>', ''))
		artist = spot_utils.Artist(name)
		if(inp == "albums"):
			number = artist.get_number_of_albums()
			print("Albums:", colored(number, 'red'))
		elif(inp == "songs"):
			number = artist.get_number_of_songs()
			print("Songs:", colored(number, 'red'))
base_prompt().cmdloop()

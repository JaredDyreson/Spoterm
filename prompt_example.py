#!/usr/bin/env python3.5

# documentation -> https://code-maven.com/interactive-shell-with-cmd-in-python

from cmd import Cmd as c
import spot_utils
import os
from termcolor import colored
import serial
from fave import Favorite

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
	def do_fave(self, inp):
		inp_mod = inp.replace('\\','')
		favorite_handler = Favorite("example.txt")
		favorite_handler.add(inp_mod)
		print("added {} to your favorites".format(inp_mod))
	def do_unfave(self, inp):
		inp_mod = inp.replace('\\', '')
		favorite_handler = Favorite("example.txt")
		favorite_handler.remove(inp_mod)
		print("removed {} from your favorites".format(inp_mod))
	def do_ls(self, inp):
		if(inp == "faves"):
			favorite_handler = Favorite("example.txt")
			favorite_handler.print_contents()
		else:
			print("ls from base_prompt")
	def default(self, inp):
		means_of_escape = [":q", "quit", "Q"]
		if(inp in means_of_escape):
			return self.do_exit(inp)
		elif(inp == ":qall"):
			quit()
class artist_prompt(base_prompt):
	def __init__(self, artist_sub_prompt_name: str):
		base_prompt.__init__(self)
		base_prompt.prompt = "spoterm/artists/{}>".format(artist_sub_prompt_name)

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

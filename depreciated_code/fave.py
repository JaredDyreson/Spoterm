#!/usr/bin/env python3.5

import os
from termcolor import colored

class Favorite():
	def __init__(self, source: str):
		self.source_file_ = source
		self.source_content_ = self.contents_of_source(self.source_file_)
	def contents_of_source(self, source: str):
		if(os.path.exists(self.source_file_)):
			with open(self.source_file_, 'r+') as f:
				return [line.strip() for line in f]
		else:
			with open(source, "w+") as create_new_file:
				create_new_file.close()
			return []
	def add(self, artist: str):
		with open(self.source_file_, 'a+') as appending:
			if(artist not in self.source_content_):
				appending.write("{}\n".format(artist))
				self.source_content_ = self.contents_of_source(self.source_file_)
			else:
				print("{} is already in your favorites".format(colored(artist, 'red')))

	def remove(self, artist: str):
		with open(self.source_file_, 'w') as removing:
			if(artist in self.source_content_):
				self.source_content_.remove(artist)
				removing.truncate()
				for value in self.source_content_:
					removing.write("{}\n".format(value))
			else:
				print("cannot remove {}. Not in source file.".format(artist))
	def print_contents(self):
		with open(self.source_file_, 'r+') as f:
			for line in f:
				print(colored(line.strip(), 'blue'))
	def clean(self):
		with open(self.source_file_, 'w+') as cleaning:
			cleaning.truncate()

#!/usr/bin/env python3.8

from SpotifyPlaylist import SpotifyPlaylist, PlaylistManager
from SpotifyAuthenticator import application, CredentialIngestor
from lexical import lexer
import sys
import traceback
import pdb
from datetime import datetime
import re
import types

from aenum import Enum
import FroggerOutput

class FroggerOperandCodes(Enum, start=0):
    GARBAGE
    LINEFEED
    LIST
    LOAD
    SONGS
    ARTISTS
    GENRES
    EXPORT


def patch(target):
  """
  Dynamically add methods to a Python class during Runtime.
  This can extend the functionality of the class infinitely and only pertains to the current instance
  """
  def check_url(self,url):
      """
      Hey mom look!
      I wrote that regex!
      """
      playlist_regex_string = "https:\/\/open\.spotify\.com\/(playlist|user)\/[a-zA-Z0-9]{22}\?si\=[a-zA-Z0-9]{22}$"
      playlist_regex = re.compile(playlist_regex_string)
      return playlist_regex.match(url)
  target.check_url = types.MethodType(check_url, target)

lexi = lexer(FroggerOperandCodes)
patch(lexi)

src_playlist = None
generate_playlist = False
list_contents = False

load_function_map = {
  lexi.operands.SONGS.value: lambda token: FroggerOutput.list_songs(token)
}


manager = CredentialIngestor.generate_manager("credentials.json")

while(True):
  expression = input(">>> ")
  try:
    for index, token in enumerate(expression.split()):
      operand_code = lexi.individual_token(token)
      if(operand_code == lexi.operands.GARBAGE.value):
        if(generate_playlist and lexi.check_url(token)):
          src_playlist = SpotifyPlaylist.from_url(manager, token)
          print("[+] Successfully loaded: {}".format(src_playlist.name))
        else:
          print("[-] Got garbage operand of {}".format(token))
      elif(operand_code == lexi.operands.LOAD.value):
        generate_playlist = True
      elif(operand_code == lexi.operands.LIST.value):
        list_contents = True
      elif(list_contents and (operand_code in load_function_map.keys())):
        load_function_map[operand_code](src_playlist)
        
  except Exception as error:
    print("[-] Exception has been thrown, aborting....")
    print("[-] Error: {}".format(error))
    _, _, tb = sys.exc_info()
    filename, lineno, funname, line = traceback.extract_tb(tb)[-1]
    print("{}:{}, in {}\n\t{}".format(
        filename, lineno, funname, line
    ))
    pdb.set_trace()

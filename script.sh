#!/usr/bin/env zsh
#
function _perm_err_(){
  echo "[-] You are not root. Stop."
  exit
}

[[ "$(whoami)" != "root" ]] && _perm_err_

# install SpotifyPlaylist

pip install git+https://github.com/JaredDyreson/SpotifyPlaylist.git#egg=httpie

# install SpotifyAuthenticator

git clone "https://github.com/JaredDyreson/SpotifyAuthenticator.git" /tmp/SpotAuth

pip -e /tmp/SpotAuth

#!/usr/bin/env python3.5

import spotify_playlist

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import time

def wait_for_element(driver, element_css_selector: str, delay=20):
	WebDriverWait(driver, delay).until(ec.presence_of_element_located((By.CSS_SELECTOR, element_css_selector)))

url = "https://music.apple.com/us/playlist/rock-hits-2007/pl.3af683127d6b4f21bd5a2f397b044f3b"
headless_ = Options()
headless_.headless = False
driver = webdriver.Firefox(options=headless_)
manager = spotify_playlist.PlaylistManager()

driver.get(url)

wait_for_element(driver, "picture[class='we-artwork ember-view product-artwork product-artwork--bottom-separator product-artwork--captioned we-artwork--fullwidth']")

track_list = driver.find_elements_by_css_selector("div[class='tracklist-item__text we-selectable-item__link-text']")
playlist_name = driver.find_element_by_css_selector("h1[class='product-header__title']").text

print("[+] Playlist is: {}".format(playlist_name))
track_id_list = []

for element in track_list:
	song_name = element.find_element_by_css_selector("span[class='we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target']").text.strip()
	artist_name = element.find_element_by_css_selector("a[class='table__row__link table__row__link--secondary']").text.strip()
	result = manager.search(artist_name, song_name)
	if(result is None):
		print("[-] Could not find {} - {}".format(artist_name, song_name))
	else:
		track_id_list.append(result)
print(track_id_list)
print(len(track_id_list))
quit()
print("[+] New playlist named {} will be created...".format(playlist_name))
new_playlist = spotify_playlist.Playlist(url="", name=playlist_name, list_of_tracks=track_id_list)
if(not manager.is_playlist(playlist_name)):
	print("[+] Playlist does not exist, creating..")
	manager.create_new_playlist(playlist_name)
new_playlist.url = manager.get_playlist_url(playlist_name)
print("[+] Truncating the preexisting playlist....")
manager.truncate_playlist(new_playlist)
print("[+] Appending track ids from new playlist into the Spoitfy one....")
manager.append_to_playlist(new_playlist, new_playlist.track_ids)
print("[+] Check out the new playlist at: {}".format(new_playlist.url))

driver.quit()

#!/usr/bin/env python3.8


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

url = "https://www.at40.com/music/top-songs/"
driver = webdriver.Firefox()
driver.get(url)
wait_for_element(driver, "h1[class='headline']")
manager = spotify_playlist.PlaylistManager()
playlist_name = driver.find_element_by_css_selector("h1[class='headline']").text

for x in range(0, 3):

	driver.find_element_by_css_selector("button[class='station-custom-button large load-more']").click()
	wait_for_element(driver, "button[class='station-custom-button large load-more']")
track_list = driver.find_elements_by_css_selector("li[class='playlist-track-container ondemand-track']")

track_id_list = []

for track in track_list:
	song_name = track.find_element_by_css_selector("a[class='song-title station-custom-link-hover']").text
	artist_name = track.find_element_by_css_selector("a[class='artist-name station-custom-link-hover']").text
	result = manager.search(artist_name, song_name)
	if(result is None):
		print("[-] Could not find {} - {}".format(artist_name, song_name))
	else:
		track_id_list.append(result)
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

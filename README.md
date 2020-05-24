# spotutils

A collection of utilities that communicate and interact with Spotify.

## Clone

Clone a given playlist so you can have a copy for yourself

## Funnel Cake (CLI)

Merge multiple playlists into a larger one

### Features

- Read from STDIN when using the pipe (|) operator
- Read multiple files containing valid Spotify urls
- Read a list of urls from a comma separated list
- Web application version can be found [here](http://funnelcake-env.s29abpc9ge.us-west-1.elasticbeanstalk.com/)

## Example

- From files

```bash
funnel_cake -F url_list_one.txt -F url_list_two.txt -O combined_from_files
```

- From list

```bash
funnel_cake -L "url1,url2,url3" -L "url4,url5" -O combined_from_lists
```



## Spoterm

A Spotify command line client, inspired by [this reddit post](https://www.reddit.com/r/unixporn/comments/cfd64p/oc_new_cli_discord_client_discpp_that_is_purely/)

[Original Link for this project](https://github.com/SeungheonOh/DisCpp)
# Features

- go to particular artist
- list artists:
	- albums
	- song count
	- album count

# External Links

- [Spotipy Documentation](https://spotipy.readthedocs.io/en/latest/#non-authorized-requests)
- [Python Spotify OAuth Flow](https://stackoverflow.com/questions/26726165/python-spotify-oauth-flow)
- [Running Flask Instance in a Thread](https://stackoverflow.com/questions/49469978/properly-terminate-flask-web-app-running-in-a-thread)
- [Spotify Developer Portal](https://developer.spotify.com/)
- [Spotify Developer Documentation](https://developer.spotify.com/documentation/web-api/)
- [Handling Multiple Scopes](https://stackoverflow.com/questions/53218225/using-multiple-scopes-with-spotipy)
- [Get more than Spotipy limit via pagination](https://stackoverflow.com/questions/39086287/spotipy-how-to-read-more-than-100-tracks-from-a-playlist)
- [Adding tracks outside of Spotipy API](https://www.oipapio.com/question-5492713)
- [Getting more precise search results from Spotipy](https://stackoverflow.com/questions/39840319/spotipy-get-track-ids-from-track-names)
- [Interactive Shell Python Documentation](https://code-maven.com/interactive-shell-with-cmd-in-python)
- [Convert dict to json](https://stackoverflow.com/questions/26745519/converting-dictionary-to-json)
- [Get access token via Spotify API](https://stackoverflow.com/questions/39887342/how-can-i-get-an-access-token-spotify-api)
- [Bearer Token Example Python](https://stackoverflow.com/questions/29931671/making-an-api-call-in-python-with-an-api-that-requires-a-bearer-token)
- [Postman Playlist Generator](https://documenter.getpostman.com/view/583/spotify-playlist-generator/2MtDWP?version=latest)
- [Spotify Console](https://developer.spotify.com/console/artists/)
- [Fake REST API for testing](https://jsonplaceholder.typicode.com/)

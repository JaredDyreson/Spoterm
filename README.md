# spotutils

Several different Spotify tools, some web applications and others as command line utilities


## Funnel Cake

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

[Spotipy Documentation](https://spotipy.readthedocs.io/en/latest/#more-examples)

[Interactive Shell Python Documentation](https://code-maven.com/interactive-shell-with-cmd-in-python)

[Convert dict to json](https://stackoverflow.com/questions/26745519/converting-dictionary-to-json)

[Get access token via Spotify API](https://stackoverflow.com/questions/39887342/how-can-i-get-an-access-token-spotify-api)

[Bearer Token Example Python](https://stackoverflow.com/questions/29931671/making-an-api-call-in-python-with-an-api-that-requires-a-bearer-token)

[Postman Playlist Generator](https://documenter.getpostman.com/view/583/spotify-playlist-generator/2MtDWP?version=latest)

[Spotify Console](https://developer.spotify.com/console/artists/)

[Fake REST API for testing](https://jsonplaceholder.typicode.com/)

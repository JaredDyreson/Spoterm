
@app.route('/login')
def login():
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return spotify.authorize(callback=callback)


@app.route('/login/authorized')
def spotify_authorized():
	resp = spotify.authorized_response()
	if resp is None:
		return 'Access denied: reason={0} error={1}'.format(
			request.args['error_reason'],
			request.args['error_description']
		)
	if isinstance(resp, OAuthException):
		return 'Access denied: {0}'.format(resp.message)

	session['oauth_token'] = (resp['access_token'], '')
	me = spotify.get('/me')
	return "Access granted"
#	return redirect(url_for('util'))
@spotify.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')

@app.route('/util', methods=['GET', 'POST'])
def util():
	token = session.get('oauth_token')[0]
	manager = spotify_playlist.PlaylistManager(token=token)
	form = funnel_cake_form()
	if(form.validate_on_submit()):
		url_one = form.url_one.data
		url_two = form.url_two.data
		output_name = form.playlist_output_name.data
		if(expression.match(url_one) and expression.match(url_two)):
			if(url_one == url_two):
				form.url_one.data = ""
				form.url_two.data = ""
				form.playlist_output_name.data = ""

				return render_template('index.html', title='Funnel Cake', form=form)
			playlist_one = spotify_playlist.Playlist(url="{}".format(url_one))
			playlist_two = spotify_playlist.Playlist(url="{}".format(url_two))
			print("[+] Created both playlists")
			if(manager.is_playlist(output_name)):
				destination = spotify_playlist.Playlist(url="{}".format(manager.get_playlist_url(output_name)))
			else:
				destination = spotify_playlist.Playlist.from_playlists(output_name, playlist_one, playlist_two, token)

			print("[+] Created destination")
			manager.truncate_playlist(destination)
			print("[+] Truncating newly created playlist")
			manager.append_to_playlist(destination, destination.track_ids)
			print("[+] Added the contents of playlist one and playlist two")
		else: raise Exception("Malformed urls")

	form.url_one.data = ""
	form.url_two.data = ""
	form.playlist_output_name.data = ""
	return render_template('index.html', title='Funnel Cake', form=form)


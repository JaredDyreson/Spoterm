# Documentation

## Scopes

These are the permissions that you, the end user grant this program.
The term "scope" refers to how much funnel cake can see in your Spotify account.

### playlist-modify-public

This allows for cleaning the newly create playlist. Truncating was a feature introduced in the command line version but has since seen no real use in AWS version (web application).

### user-private-read

Makes sure the playlist being created does not already exist and we need to list the user's playlists for this validation process.

### user-library-modify

Allows for the creation of playlists on a user's account.

### user-read-email and user-read-private

Needed to get the current user's id and account name. This is used to create playlists and to display who has been logged in.

### External Documentation

You can read more about the other types of scopes that can be used [here](https://developer.spotify.com/documentation/general/guides/scopes/).

## 

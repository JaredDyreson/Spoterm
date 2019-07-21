#!/usr/bin/env python3.5

import requests
from pprint import pprint as pp
import json

client_id = "cbecd4d200f8482d910cb1db77d6f10c"
client_secret = "e1f239ec0ee443689d6786fd3f397af1"

grant_type = 'client_credentials'

#Request based on Client Credentials Flow from https://developer.spotify.com/web-api/authorization-guide/

#Request body parameter: grant_type Value: Required. Set it to client_credentials
body_params = {'grant_type' : grant_type}

url='https://accounts.spotify.com/api/token'

response=requests.post(url, data=body_params, auth = (client_id, client_secret)) 
print(response.content)

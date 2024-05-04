import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn import svm

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'a03708bc2ce047e7be073f6430010fb1'
client_secret = '20eb2257e63946f0b028c106e6b6e19a'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

##################################################
name = "ariana grande" 
result = sp.search(name) 
print(result['tracks']['items'][0]['artists'])
##################################################

artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

sp_albums = sp.artist_albums(artist_uri, album_type='album')
name = []
uri = []
for i in sp_albums['items']:
    name.append(i['name'])
    uri.append(i['uri'])

song_name = []
song_uri = []
album = []
count = 0
for j in uri:
    
    tracks = sp.album_tracks(j)   
    for i in tracks['items']:
        album.append(name[count])
        song_name.append(i['name'])
        song_uri.append(i['uri'])
    count+=1
song_name

acoustic = []
dance = []
energy = []
instrumental = []
liveness = []
loudness = []
speech = []
tempo = []
valence = []
popularity = []

#https://python.plainenglish.io/how-similar-my-boyfriend-top-tracks-on-spotify-compare-to-mine-bf754622d4d6

for i in song_uri:
    feat = sp.audio_features(i)[0]
    acoustic.append(feat['acousticness'])
    dance.append(feat['danceability'])
    energy.append(feat['energy'])
    speech.append(feat['speechiness'])
    instrumental.append(feat['instrumentalness'])
    loudness.append(feat['loudness'])
    tempo.append(feat['tempo'])
    liveness.append(feat['liveness'])
    valence.append(feat['valence'])
    popu = sp.track(i)
    popularity.append(popu['popularity'])


ari = pd.DataFrame({'name':song_name,
                    'album':album,
                    'dance':dance,
                    'acoustic':acoustic,
                    'energy':energy,
                    'instrumental':instrumental,
                    'liveness':liveness,
                    'loudness':loudness,
                    'speech':speech,
                    'tempo':tempo,
                    'valence':valence,
                    'popularity':popularity
    
})
print(ari.head())
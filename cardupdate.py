from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch



PLAYLISTS = [    
    ['Hot trong tuần', 'https://open.spotify.com/playlist/37i9dQZF1DX0F4i7Q9pshJ', "PL59eqqQABruN3GyAPiPnQ6Jq-TngWjT-Y"],
    ['Bài hát hàng đầu tại Việt Nam', 'https://open.spotify.com/playlist/37i9dQZEVXbKZyn1mKjmIl', "PL59eqqQABruMSx6VSy1hbkBhG4XwtgSuy"],
    ['Bài hát hàng đầu Toàn cầu', 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF', 'PL59eqqQABruN3GyAPiPnQ6Jq-TngWjT-Y'],
    ['Indie Việt', 'https://open.spotify.com/playlist/37i9dQZF1DWT2oR9BciC32', 'PL59eqqQABruNew5O0cRvomfbU6FI0RGyl'],
    ['Hip-hop Việt', 'https://open.spotify.com/playlist/37i9dQZF1DWYLMi9ZNZUaz', 'PL59eqqQABruM3TLAGthvgW10c1R6omGwq'],
    ['Thiên Hạ Nghe Gì', 'https://open.spotify.com/playlist/37i9dQZF1DWVOaOWiVD1Lf', 'PL59eqqQABruM3TLAGthvgW10c1R6omGwq'],
]





client_credentials_manager = SpotifyClientCredentials(client_id='41a63969895b4054ba7021b92d612409',
                client_secret='f08c343ccb52465484e3a0e1e362e9a8')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




CONTAINER = []
for playlist in PLAYLISTS:
    Name,Link,playlistid = playlist
    playlistcard = []
    count = 0
    PlaylistLink = "http://www.youtube.com/watch_videos?video_ids="
    for i in (sp.playlist_tracks(Link)['items']):
        if count == 50:
            break
        try:
            song = i['track']['name'] + i['track']['artists'][0]['name']
            songdic = (YoutubeSearch(song, max_results=1).to_dict())[0]
            playlistcard.append([songdic['thumbnails'][0],songdic['title'],songdic['channel'],songdic['id']])
            PlaylistLink += songdic['id'] + ','
        except:
            continue
        count += 1

    from urllib.request import urlopen
    req = urlopen(PlaylistLink)
    PlaylistLink = req.geturl()
    print(PlaylistLink)
    PlaylistId = PlaylistLink[PlaylistLink.find('list')+5:]

    CONTAINER.append([Name,playlistcard,playlistid])

import json

json.dump(CONTAINER,open('card.json', 'w'),indent = 6) 

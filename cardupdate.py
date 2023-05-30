from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch

PLAYLISTS = [
    ['Accidental', 'https://open.spotify.com/playlist/0zJ8hC8YJOcHYuk5nMPFm8?si=U6Kyom3XQ32reSuVgl2uhA', "PL59eqqQABruMQOPlUVcVsIid685ZdwDjf"],
    ['TimePass', 'https://open.spotify.com/playlist/6gADLrLFK1kXgEEOsENi1c', "PL59eqqQABruMSx6VSy1hbkBhG4XwtgSuy"],
    ['CHILLS', 'https://open.spotify.com/playlist/3zs3QOLX8bASY5oV2dmEQw', 'PL59eqqQABruN3GyAPiPnQ6Jq-TngWjT-Y'],
    ['Programming & Coding Music', 'https://open.spotify.com/playlist/6vWEpKDjVitlEDrOmLjIAj', 'PL59eqqQABruNew5O0cRvomfbU6FI0RGyl'],
    ['Spanish', 'https://open.spotify.com/playlist/75QJ1JeFaeSm0uH1znWxb0?si=Lt4kd-RARBu2TQz35RAQiQ', 'PL59eqqQABruM3TLAGthvgW10c1R6omGwq']
]


client_credentials_manager = SpotifyClientCredentials(client_id='e5d66c188ef64dd89afa4d13f9555411',
                                                      client_secret='d070988d7bd5479a9e0818fa23839544')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

CONTAINER = []

for playlist in PLAYLISTS:
    Name, Link, playlistid = playlist
    playlistcard = []  # Danh sách chứa thông tin các bài hát trong playlist
    count = 0  
    PlaylistLink = "http://www.youtube.com/watch_videos?video_ids="  # Link để tạo playlist trên YouTube

    # Duyệt qua từng bài hát trong playlist trên Spotify
    for i in (sp.playlist_tracks(Link)['items']):
        if count == 50:
            break
        try:
            song = i['track']['name'] + i['track']['artists'][0]['name']  # Tên bài hát và tên nghệ sĩ
            songdic = (YoutubeSearch(song, max_results=1).to_dict())[0]  # Tìm kiếm thông tin bài hát trên YouTube
            playlistcard.append([songdic['thumbnails'][0], songdic['title'], songdic['channel'], songdic['id']])
            PlaylistLink += songdic['id'] + ','  # Thêm ID của bài hát vào link tạo playlist trên YouTube
        except:
            continue
        count += 1

    # Lấy link tạo playlist trên YouTube
    from urllib.request import urlopen
    req = urlopen(PlaylistLink)
    PlaylistLink = req.geturl()
    print(PlaylistLink)

    # Lấy playlist ID từ link tạo playlist trên YouTube
    PlaylistId = PlaylistLink[PlaylistLink.find('list') + 5:]


    CONTAINER.append([Name, playlistcard, playlistid])

import json

json.dump(CONTAINER, open('card.json', 'w'), indent=6)

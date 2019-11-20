# https://developer.spotify.com/console/get-users-currently-playing-track/?market=ES

from bottle import route, run, request
import spotipy
from spotipy import oauth2
import requests
import time
import re
import html2text
import itertools
from bs4 import BeautifulSoup
from bs4.element import Comment

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '*******'
SPOTIPY_CLIENT_SECRET = '*****'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/'
SCOPE = 'user-read-currently-playing'
CACHE = '.spotipyoauthcache'
song_info = None
SPOTIFY_TOKEN = '*********************'
GENIUS_TOKEN = '******************'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)


@route('/')
def index():
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        getCurrentTrack()
        return results

    else:
        return htmlForLoginButton()


def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton


def getCurrentTrack():
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
               'Authorization': 'Bearer ' + SPOTIFY_TOKEN}
    res = requests.get(url, headers=headers).json()
    # add advertisement
    # print(res)

    playedTrackWbraces = res['item']['name']
    playedTrack = re.sub("[\(\[].*?[\)\]]", "", playedTrackWbraces)
    artistWbraces = res['item']['artists'][0]['name']
    artistName = re.sub("[\(\[].*?[\)\]]", "", artistWbraces)
    # print('Artist ' + artistName)
    # print('Currently Played Track is ' + playedTrack)

    getLyrics(playedTrack, artistName)


def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


def getLyrics(songName, artistName):
    url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    searchUrl = url + '/search'
    data = {'q': songName + ' ' + artistName}
    res = requests.get(searchUrl, data, headers=headers)
    checkIfValueMatchesWithAnyHit(res.json(), songName, artistName)


def checkIfValueMatchesWithAnyHit(data, songName, artistName):
    dataHits = data['response']['hits']
    print(dataHits)
    global song_info
    for x in dataHits:
        trackNameWithBraces = x['result']['title']
        trackNameWithOutBraces = re.sub("[\(\[].*?[\)\]]", "", trackNameWithBraces)
        artistNameWithBraces = x['result']['primary_artist']['name']
        artistNameWithOutBraces = re.sub("[\(\[].*?[\)\]]", "", artistNameWithBraces)
        if artistNameWithOutBraces == artistName:
            song_info = x['result']
            getLyricsUrl(song_info['api_path'])
            print(song_info['api_path'])
            break
        else:
            print('/NA/')


def getLyricsUrl(id):
    url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_TOKEN}
    searchUrl = url + id
    res = requests.get(searchUrl, headers=headers)
    print(res.json()['response']['song']['url'])
    scrapeUrl(res.json()['response']['song']['url'])


def scrapeUrl(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', {'class': 'lyrics'}).text
    print(lyrics)


run(host='', port=8080)

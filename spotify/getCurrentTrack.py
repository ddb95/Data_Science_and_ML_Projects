# https://developer.spotify.com/console/get-users-currently-playing-track/?market=ES

from bottle import route, run, request
import spotipy
from spotipy import oauth2
import requests
import time
import re
import itertools
from bs4 import BeautifulSoup
from bs4.element import Comment

SCOPE = 'user-read-currently-playing'
song_info = None
SPOTIFY_TOKEN = '***********************'
GENIUS_TOKEN = '********************'


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


if __name__ == '__main__':
    getCurrentTrack()

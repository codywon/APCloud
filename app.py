# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, Response, url_for
import json
import requests
import base64
from user_agents import parse
from werkzeug.contrib.cache import SimpleCache
from NEMbox.api import NetEase, geturl_new_api

app = Flask(__name__)
ne = NetEase()


@app.route("/<int:song_id>.lrc")
def lrc(song_id):
    result = ne.song_lyric(song_id)
    if result is None:
        return '[00:00.00]歌曲无歌词'
    return result


@app.route("/<int:song_id>.mp3")
def mp3(song_id):
    url = geturl_new_api({'id': song_id})[0]
    result = redirect(url)
    if result.headers['Location'] == 'None':
        abort(404)
    else:
        return result


@app.route("/<int:playlist_id>")
def player(playlist_id):
    showlrc = request.args.get("showlrc")
    autoplay = request.args.get("autoplay")
    if showlrc is None or showlrc == '1':
        showlrc = '3'  # 使APlayer从指定地址获取歌词
    if autoplay is None:
        autoplay = '1'

    if playlist_id is not None:
        playlist = ne.playlist_detail_full(playlist_id)
        songs_info = []
        name = playlist['name']
        for song in playlist['tracks']:
            try:
                title = song["name"]
                album = song["album"]["name"]
                pic_url = song["album"]["picUrl"]
                artist = song["artists"][0]["name"]
                url = '/' + str(song['id']) + '.mp3'
                lrc = '/' + str(song['id']) + '.lrc'
            except Exception as e:
                continue
            songs_info.append(
                {"url": url, "title": title, "album": album, "pic_url": pic_url, "artist": artist, 'lrc': lrc})
    else:
        abort(404)
        return ''

    return render_template("aplayer.html", name=name, songs_info=songs_info, showlrc=showlrc, autoplay=autoplay)


if __name__ == "__main__":
    app.run()

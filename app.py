# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, Response, url_for
import json
import requests
import base64

from flask import stream_with_context
from user_agents import parse
from werkzeug.contrib.cache import SimpleCache
from NEMbox.api import NetEase, geturl_new_api

app = Flask(__name__)
ne = NetEase()


@app.route("/apcloud/")
def hello():
    return '''<pre>网易云音乐 APlayer
项目地址：https://github.com/vhyme/APCloud
演示效果可以看我的博客(电脑打开)：https://heya.myseu.cn/

Usage:
/歌单ID       显示指定歌单播放器
    参数：
    autoplay     是否自动播放(1=true/0=false)，默认是
    showlrc      是否显示歌词(1=true/0=false)，默认是
/歌曲ID.mp3   重定向到该歌曲直链，若有版权问题则返回空音频
/歌曲ID.lrc   下载该歌曲歌词

本播放器可以自适应窗口或iframe的高度，嵌入到iframe中不会出现
全局滚动条，而是使用APlayer自带的列表滚动条，另外本播放器隐藏
了APlayer的边距、圆角、外阴影、歌词背景等元素，非常方便嵌入到
博客中！

注意：mp3通过https传输的问题已经解决，现在mp3文件将通过本服务
器进行流式转发，若要在你的服务器上部署本项目，请注意流量消耗!
</pre>'''


@app.route("/apcloud/<int:song_id>.lrc")
def lrc(song_id):
    result = ne.song_lyric(song_id)
    if result is None:
        return '[00:00.00]歌曲无歌词'
    return result


@app.route("/apcloud/<int:song_id>.mp3")
def mp3(song_id):
    url = geturl_new_api({'id': song_id})[0]
    result = redirect(url)
    if result.headers['Location'] == 'None':
        return app.send_static_file('empty.mp3')

    def generate():
        r = requests.get(url, stream=True)
        yield r.content

    return Response(stream_with_context(generate()), mimetype='audio/mpeg')


@app.route("/apcloud/<int:playlist_id>")
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
                url = str(song['id']) + '.mp3'
                lrc = str(song['id']) + '.lrc'
            except Exception as e:
                continue
            songs_info.append(
                {"url": url, "title": title, "album": album, "pic_url": pic_url, "artist": artist, 'lrc': lrc})
    else:
        abort(404)
        return ''

    return render_template("aplayer.html", name=name, songs_info=songs_info,
                           showlrc=showlrc, autoplay=autoplay)


if __name__ == "__main__":
    app.run(threaded=True, debug=True)

# APCloud
> 网易云音乐 APlayer

- 项目地址：https://github.com/vhyme/APCloud
- 演示效果可以看我的博客(电脑打开)：https://heya.myseu.cn/

## Usage:
```
/歌单ID       显示指定歌单播放器
    参数：
    autoplay     是否自动播放(1=true/0=false)，默认是
    showlrc      是否显示歌词(1=true/0=false)，默认是
/歌曲ID.mp3   重定向到该歌曲直链，若有版权问题则返回空音频
/歌曲ID.lrc   下载该歌曲歌词
```
本播放器可以自适应窗口或iframe的高度，嵌入到iframe中不会出现
全局滚动条，而是使用APlayer自带的列表滚动条，另外本播放器隐藏
了APlayer的边距、圆角、外阴影、歌词背景等元素，非常方便嵌入到
博客中！
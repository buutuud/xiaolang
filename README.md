# 小浪
支持中文的智能音箱，能够听懂你的命令，通过语音控制一切。

原始代码复制自 http://jasperproject.github.io/ branch：jasper-dev，并做了很多修改，

具体有：

* 原先的 Jasper 只支持最老版本的 raspberry pi，代码在新版 raspberry pi 上跑不通。通过 debug，修改代码，使代码能够在 raspberry pi 3 上正常跑起来。
* 修改了原先的 config 配置格式，jasper-dev 原有两种配置文件格式，现修改为一种。
* 删除了一些中国用不上连不上的 plugin。
* 语音模块保留了 pocketsphinx-stt 和 espeak-tts，如果需要其他模块，请到 jasper-dev 自行添加。
* 增加了 baidu-tts，需要网络。
* 增加了 ifly-tts，需要网络。
* 增加了一个 mp3player，可以由语音控制播放，暂停等等。由这个 player，可以播放音乐，讲故事，放儿歌。


### 更多功能
与智能家居结合


### 问题讨论
提交pr即可

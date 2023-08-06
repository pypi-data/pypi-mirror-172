
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot_plugin_tts_gal

基于nonebot和vits的部分gal角色的语音合成插件

</div>

# 旧版本用户注意

在0.3.0版本再次对代码进行了更改，支持添加部分中文VITS模型，也许可能会报错下面的关键错误，具体解决方案可以看可以查看[Usage.md](https://github.com/dpm12345/nonebot_plugin_tts_gal/blob/master/Usage.md)

# 安装

pip安装

```
pip install nonebot_plugin_tts_gal
```

nb-cli安装

```
nb plugin install nonebot-plugin-tts-gal
```

## 相关依赖

<details>
<summary>ffmpeg的安装</summary> 
**Windows**

在ffmpeg官网[下载](https://github.com/BtbN/FFmpeg-Builds/releases),选择对应的版本，下载后解压，并将位于`bin`目录添加到环境变量中

其他具体细节可自行搜索

**Linux**

Ubuntu下

```
apt-get install ffmpeg
```

或者下载源码安装(具体可搜索相关教程)

</details>

# 配置项

<details>
<summary>auto_delete_voice</summary> 

请在使用的配置文件(.env.*)加入

```
auto_delete_voice = true
```

用于是否自动删除生成的语音文件，如不想删除，可改为

```
auto_delete_voice = false
```

</details>

<details>
<summary>tts_gal</summary> 

该配置项采用python的字典，其中键为元组，值为列表，具体代表含义及设置可以查看[Usage.md](https://github.com/dpm12345/nonebot_plugin_tts_gal/blob/master/Usage.md)

</details>

# 使用

群聊和私聊仅有细微差别，其中下面语句中，`name`为合成语音的角色，`text`为转语音的文本内容(根据配置文件中的`lang`会自动翻译为对应语言)

## 群聊

`@机器人 [name]说[text]`

## 私聊

`[name]说[text]`

例如：宁宁说おはようございます.

**关于此方面自定义问题的可以查看**[Usage.md](https://github.com/dpm12345/nonebot_plugin_tts_gal/blob/master/Usage.md)



# 感谢

+ 部分代码参考自[nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet)
+ **[CjangCjengh](https://github.com/CjangCjengh/)**：g2p转换，适用于日语调形标注的符号文件及分享的[柚子社多人模型](https://github.com/CjangCjengh/TTSModels)
+ **[luoyily](https://github.com/luoyily)**：分享的[ATRI模型](https://pan.baidu.com/s/1_vhOx50OE5R4bE02ZMe9GA?pwd=9jo4)



**其他完整内容请前往github查看**

# 更新日志

**2022.10.21 version 0.3.1：**

修复对配置项`auto_delete_voice`的判断bug

**2022.10.19 version 0.3.0：**

支持添加中文模型，优化相关代码，增添更多提示

**2022.10.7 version 0.2.3:**

适配nonebot2-rc1版本，并添加部分报错信息提醒

**2022.9.28 version 0.2.2:**

添加中文逗号替换成英文逗号

**version 0.2.1:**

将pyopenjtalk依赖更新为0.3.0，使python3.10也能使用

**2022.9.25 version 0.2.0:**

优化修改代码逻辑，支持自行添加vits模型，简单修复了一下有道翻译的翻译问题，启动时自动检测所需文件是否缺失

**2022.9.21 version 0.1.1:**

修改依赖


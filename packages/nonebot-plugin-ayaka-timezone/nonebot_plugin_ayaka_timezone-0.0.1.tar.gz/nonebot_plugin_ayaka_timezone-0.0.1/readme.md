# 时区助手

基于ayaka开发的 时区助手 插件

任何问题请发issue

注意：只适用于群聊！

<b>注意：由于更新pypi的readme.md需要占用版本号，因此其readme.md可能不是最新的，强烈建议读者前往[github仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-timezone)以获取最新版本的帮助</b>


# How to start

## 安装 ayaka

安装 [前置插件](https://github.com/bridgeL/nonebot-plugin-ayaka) 

`poetry add nonebot-plugin-ayaka`


## 安装 本插件

安装 本插件

`poetry add nonebot-plugin-ayaka-timezone`

修改nonebot2  `bot.py` 

```python
nonebot.load_plugin("ayaka_timezone")
```

## 配置

推荐配置（非强制要求）
```
COMMAND_START=["#"]
COMMAND_SEP=[" "]
```

# 指令
指令|参数|功能
-|-|-
tz_add|name, timezone|添加一条时区转换，例如，#tz_add 北京 8，#tz_add 伦敦 0，#tz_add 洛杉矶 -8
tz|name|返回name对应时区的时间，例如 #tz 北京
tz|number|返回对应时区的时间，例如 #tz 8
tz_list|无|查看所有的时区转换



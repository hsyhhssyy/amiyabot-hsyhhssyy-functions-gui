# 增强版管理功能的插件

该插件仅支持兔兔>=v6.1版本，该兔兔版本在本插件发布时尚未发布。

安装了这个插件后，你可以在兔兔控制台的插件管理里，找到本插件，然后即可看到一大堆switch，这些switch可以精确的控制某个特定插件消息处理器的开关。当你想单独禁用某些子功能时。你可以在这里控制这个功能的开关。

![例子](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-hsyhhssyy-functions-gui/master/example.jpg)

每当插件升级时，配置项名称和配置项对应的功能的关系可能会发生变化，因为这里的功能开关，是根据插件作者代码里这个功能的顺序编号的，开发者的代码重新排版，可能会导致所控制的功能发生变化，因此插件每次升级后，你需要重新检查对应的配置项是否还能生效。

该插件只能禁止功能，不能保证功能一定生效，该功能实际是否能生效还取决于系统的功能管理插件，和插件自己的配置。

该插件首次启动后，后续新安装的插件，其各项功能会默认关闭，需要在全局和各个启用了独立配置的频道中启用。

当你不知道搞了什么把插件搞乱了的时候，私聊兔兔并说`重置超级功能开关`，系统将会重置所有频道以及全局配置的默认值，你可以重新配置。

插件才刚刚开发完成，可能会有一些bug，如果实在遇到问题，最差也可以手动删除本插件来解决问题。
未来会添加更多功能，比如想办法区分不同的消息管理器。

> [项目地址:Github](https://github.com/hsyhhssyy/amiyabot-hsyhhssyy-functions-gui/)

> [遇到问题可以在这里反馈(Github)](https://github.com/hsyhhssyy/amiyabot-hsyhhssyy-functions-gui/issues/new/)

> [如果上面的连接无法打开可以在这里反馈(Gitee)](https://gitee.com/hsyhhssyy/amiyabot-plugin-bug-report/issues/new)

> [Logo作者:Sesern老师](https://space.bilibili.com/305550122)

|  版本   | 变更  |
|  ----  | ----  |
| 1.0  | 最初的版本 |
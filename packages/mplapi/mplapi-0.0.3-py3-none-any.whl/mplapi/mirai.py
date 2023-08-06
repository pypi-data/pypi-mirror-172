from mplapi import config
from mplapi import msg

PIN_NUM = 8


class Permission:
    """
    插件的权限类,
    一个插件和一个bot对应该类一个对象,
    默认都为全开放模式,
    BLACK_LIST_MODE 黑名单模式,
    WHITE_LIST_MODE 白名单模式,
    ALL_MODE 全开放模式,
    """
    BLACK_LIST_MODE = 0
    WHITE_LIST_MODE = 1
    ALL_MODE = 2

    @property
    def group_list(self) -> set:
        """
        :return: 群权限列表
        """
        pass

    @property
    def friend_list(self) -> set:
        """
        :return: 好友权限列表
        """
        pass

    @property
    def admin_list(self) -> set:
        """
        :return: 管理员权限列表
        """
        pass

    def set_group_mode(self, mode: int):
        """
        设置群权限模式
        :param mode: Permission类内置的三个模式枚举
        :return:
        """
        pass

    def get_group_mode(self) -> int:
        """
        获取群权限模式
        :return: Permission类内置的三个模式枚举
        """
        pass

    def set_friend_mode(self, mode: int):
        """
        设置好友权限模式
        :param mode: Permission类内置的三个模式枚举
        :return:
        """
        pass

    def get_friend_mode(self) -> int:
        """
        获取好友权限模式
        :return: Permission类内置的三个模式枚举
        """
        pass

    @property
    def PIN(self):
        """
        获取该权限对象的PIN(一个bot和一个插件对应一个PIN，该PIN不会改变) PIN可以用于插件刚启用时认证管理员
        :return:
        """
        pass

    def reset_PIN(self, num=PIN_NUM):
        """
        重置该权限对象的PIN
        :param num: PIN的位数（默认8位）
        :return:
        """
        pass

    def reset_group(self):
        """
        清空群权限列表
        :return:
        """
        pass

    def reset_friend(self):
        """
        清空群好友权限列表
        :return:
        """
        pass

    def reset_admin(self):
        """
        清空管理员权限列表
        :return:
        """
        pass

    def add_group(self, group):
        """
        添加群至群权限列表
        :param group: 群号
        :return:
        """
        pass

    def remove_group(self, group):
        """
        从群权限列表移除群
        :param group: 群号
        :return:
        """
        pass

    def add_admin(self, qq):
        """
        添加管理员至管理员权限列表
        :param qq: qq号
        :return:
        """
        pass

    def remove_admin(self, qq):
        """
        从管理员权限列表移除管理员
        :param qq: qq号
        :return:
        """
        pass

    def has_admin_permission(self, qq) -> bool:
        """
        判断该qq号是否为管理员
        :param qq: qq号
        :return: bool
        """
        pass

    def add_friend(self, qq):
        """
        添加好友至好友权限列表
        :param qq: qq号
        :return:
        """
        pass

    def remove_friend(self, qq):
        """
        从好友权限列表移除好友
        :param qq: qq号
        :return:
        """
        pass

    def has_group_permission(self, group) -> bool:
        """
        判断该群是否有权限(判断规则取决于mode)
        :param group: 群号
        :return: bool
        """
        pass

    def has_friend_permission(self, qq) -> bool:
        """
        判断该好友是否有权限(判断规则取决于mode)
        :param qq: qq号
        :return: bool
        """
        pass


class Bot:
    """
    一个机器人类，通过此此类内维护的方法与mirai进行交互
    """

    @property
    def bot_qq(self) -> int:
        """
        :return: bot qq号
        """
        pass

    @property
    def login_time(self) -> int:
        """
        :return: bot登录时间戳
        """
        pass

    def send_group_msg(self, message: msg.Msg, group):
        """
        发送群消息
        :param message: 消息体,任意继承了Msg类的对象
        :param group: 群号
        :return:
        """
        pass

    def send_friend_msg(self, message: msg.Msg, target):
        """
        发送好友消息
        :param message: 消息体,任意继承了Msg类的对象
        :param target: qq号
        :return:
        """
        pass

    def recall_msg(self, source: msg.SourceMsg):
        """
        撤回消息
        :param source: SourceMsg对象
        :return:
        """
        pass

    def mute(self, group, target, time):
        """
        禁言
        :param group: 群号
        :param target: 禁言对象qq号
        :param time: 禁言时长 秒
        :return:
        """
        pass

    def mute_all(self, group):
        """
        全体禁言
        :param group: 群号
        :return:
        """
        pass

    def un_mute(self, group, target):
        """
        解除禁言
        :param group: 群号
        :param target: 被禁言的qq号
        :return:
        """
        pass

    def un_mute_all(self, group):
        """
        解除全体禁言
        :param group: 群号
        :return:
        """
        pass

    def kick(self, group, target):
        """
        踢出群聊
        :param group: 群号
        :param target: 踢出对象qq号
        :return:
        """
        pass

    def quit(self, group):
        """
        退出群聊
        :param group: 群号
        :return:
        """
        pass

    def get_friend_list(self) -> list:
        """
        获取好友列表
        :return: 好友qq号列表
        """
        pass

    def get_friend_info(self, target) -> config.FriendConfig:
        """
        TODO
        获取好友资料
        :param target: 好友qq号
        :return: 好友资料对象
        """
        pass

    def get_group_list(self) -> list:
        """
        获取群列表
        :return: 已加入的群列表
        """
        pass

    def get_group_info(self, group) -> config.GroupConfig:
        """
        获取群资料
        :param group: 群号
        :return: 群资料对象
        """
        pass

    def get_group_member_list(self, group) -> list[config.GroupMemberConfig]:
        """
        获取群员资料列表
        :param group: 群号
        :return: 群员资料对象列表
        """
        pass

    def get_group_member_info(self, group, target) -> config.GroupMemberConfig:
        """
        TODO
        :param group:
        :param target:
        :return:
        """
        pass

    def set_group_info(self, group, info: config.GroupConfig):
        """
        设置群资料
        :param group: 群号
        :param info: GroupConfig对象
        :return:
        """
        pass

    def set_group_member_info(self, group, target, info: config.GroupMemberConfig):
        """
        设置群成员资料
        :param group: 群号
        :param target: 群成员qq号
        :param info: GroupMemberConfig对象
        :return:
        """
        pass

    def register_plugin(self, py_plugin):
        """
        注册插件到bot
        :param py_plugin: PyPlugin对象
        :return:
        """
        pass

    def set_plugin_permission(self, plugin_name: str, permission: Permission):
        """
        为插件设置权限
        :param plugin_name: 插件名
        :param permission: Permission对象
        :return:
        """
        pass

    def get_plugin_permission(self, plugin_name: str) -> Permission:
        """
        获取插件的权限对象
        :param plugin_name: 插件名
        :return: Permission对象
        """
        pass

    def get_register_plugin_list(self) -> list:
        """
        获取bot内已注册的插件对象列表
        :return: Pyplugin对象列表
        """
        pass

    def add_plugin_task(self, task):
        """
        添加一个插件任务
        :param task: PluginTask对象
        :return:
        """
        pass

    def get_plugin_task(self, plugin_name) -> list:
        """
        获取插件未被执行且未超时的任务列表
        :param plugin_name: 插件名
        :return: PluginTask对象列表
        """
        pass

    def remove_plugin_task(self, task):
        """
        移除一个插件任务
        :param task: PluginTask对象
        :return:
        """
        pass

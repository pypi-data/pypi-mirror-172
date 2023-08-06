import sqlite3
from abc import ABCMeta
from abc import abstractmethod

from mplapi import msg
from mplapi import MPLLoggerHandler
from mplapi.mirai import Bot


def catch_async_exception(func):
    """
    MPL默认无视插件中异步方法的异常，若你希望MPL捕获，请在任意实现了PluginExceptionCatcher接口的异步方法中添加此装饰器
    :param func: 任意继承了PluginExceptionCatcher类的异步方法
    :return:
    """

    pass


class PluginExceptionCatcher(metaclass=ABCMeta):
    """
    实现该接口，使得@catch_async_exception装饰器可以捕获类中异步方法抛出的异常
    该类为抽象类，请实现被@abstractmethod标记的抽象方法
    """

    @abstractmethod
    def handle_exception(self, e: BaseException):
        """
        处理异常
        :param e: 捕获的异常
        :return:
        """
        pass


class PyPlugin(PluginExceptionCatcher, metaclass=ABCMeta):
    """
    插件类，MPL通过实例化该类来加载插件，且只会实例化一次
    该类为抽象类，请实现被@abstractmethod标记的抽象方法
    plugin_name 插件名(将由MPL自动设置)
    """

    def handle_exception(self, e: BaseException):
        pass

    @abstractmethod
    @property
    def version(self) -> tuple[int, int, int]:
        """
        插件的版本号，采用x.y.z规范
        :return:(x,y,z)
        """
        pass

    def get_plugin_name(self) -> str:
        """
        获取插件名
        :return:
        """
        pass

    @abstractmethod
    def on_create(self):
        """
        插件启动时调用该方法
        :return:
        """
        pass

    @abstractmethod
    async def on_login(self, bot: Bot):
        """
        bot登录时调用该方法
        :param bot: bot对象
        :return:
        """
        pass

    @abstractmethod
    async def on_logout(self, bot: Bot):
        """
        bot登出时调用该方法
        :param bot: bot对象
        :return:
        """
        pass

    def get_logger(self) -> MPLLoggerHandler:
        """
        获取日志对象
        :return:日志对象
        """
        pass

    def get_database(self, db_name='database') -> sqlite3.Connection:
        """
        获取数据库连接对象
        :param db_name: 数据库名字(无后缀)
        :return: sqlite3数据库连接对象
        """
        pass

    def get_config(self, conf_name='plugin') -> dict:
        """
        获取配置文件
        :param conf_name: 配置文件名
        :return: 自定义配置
        """
        pass

    def set_config(self, conf: dict, conf_name='plugin'):
        """
        设置配置文件
        :param conf: 自定义配置
        :param conf_name: 配置文件名
        :return:
        """
        pass

    def get_files_path(self) -> str:
        """
        获取文件保存目录(最后带分隔符'/')
        :return: 文件保存目录
        """
        pass

    @abstractmethod
    async def get_group_msg(self, bot: Bot, source: msg.Source, message: msg.MsgChain):
        """
        处理群消息
        :param bot: Bot对象
        :param source: 一个有发送者信息的集合
        :param message: 消息链
        :return:
        """
        pass

    @abstractmethod
    async def get_friend_msg(self, bot: Bot, source: msg.Source, message: msg.MsgChain):
        """
        处理好友消息
        :param bot: Bot对象
        :param source: 一个有发送者信息的集合
        :param message: 消息链
        :return:
        """
        pass

    @abstractmethod
    async def get_admin_msg(self, bot: Bot, source: msg.Source, message: msg.MsgChain):
        """
        处理插件管理员的消息
        :param bot: Bot对象
        :param source: 一个有发送者信息的集合
        :param message: 消息链
        :return:
        """
        pass


class PluginTask(PluginExceptionCatcher):
    """
    插件任务类，通过实例化该类来创建一个插件任务来提交至Bot
    该类为抽象类，请实现被@abstractmethod标记的抽象方法
    plugin_instance PyPlugin对象
    """

    def handle_exception(self, e: BaseException):
        pass

    def __init__(self, plugin: PyPlugin):
        self.plugin_instance = plugin

    def set_timeout(self, timeout: int):
        """
        设置任务超时时间(即一定时间内任务没有执行，任务将会被释放),不设置为永不超时
        :param timeout: 超时时间 秒
        :return:
        """
        pass

    @abstractmethod
    def is_task_target(self, group, target) -> bool:
        """
        任务是否执行的判别规则
        :param group: 群号(若不是群聊，此项传入的值为None)
        :param target: 发送者QQ号
        :return: 判别结果
        """
        pass

    @abstractmethod
    async def execute_task(self, bot: Bot, source: msg.Source, message: msg.MsgChain):
        """
        执行的任务体，在判别结果为True时调用该方法
        :param bot: Bot对象
        :param source: 一个有发送者信息的集合
        :param message: 消息链
        :return:
        """
        pass

    @abstractmethod
    async def on_timeout(self, bot: Bot):
        """
        任务超时被释放时调用该方法
        :param bot: Bot对象
        :return:
        """
        pass


class GroupTask(PluginTask, metaclass=ABCMeta):
    """
    插件的群任务类
    该类为抽象类，请实现被@abstractmethod标记的抽象方法
    group 任务目标群号
    target 任务目标qq号
    """

    def __init__(self, group, plugin: PyPlugin, target=None):
        """

        :param group: 需要执行任务的群号
        :param plugin: PyPlugin对象
        :param target: 需要执行任务的QQ号，不传入或为None时将判定为任意群友
        """
        super().__init__(plugin)
        self.group = group
        self.target = target

    def is_task_target(self, group, target) -> bool:
        pass


class FriendTask(PluginTask, metaclass=ABCMeta):
    """
    插件的好友任务类
    该类为抽象类，请实现被@abstractmethod标记的抽象方法
    target 任务目标qq号
    """

    def __init__(self, target, plugin: PyPlugin):
        """
        
        :param target: 需要执行任务的QQ号
        :param plugin: PyPlugin对象
        """
        super().__init__(plugin)
        self.target = target

    def is_task_target(self, group, target) -> bool:
        pass

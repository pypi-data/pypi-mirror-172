import logging


class MPLLoggerHandler:
    """
    MPL的日志类
    """
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def set_stream_level(self, level):
        """
        设置输出到控制台的日志等级
        :param level: 类中的5个枚举
        :return:
        """
        pass

    def set_file_level(self, level):
        """
        设置输出到文件的日志等级
        :param level: 类中的5个枚举
        :return:
        """
        pass

    def debug(self, msg: str):
        """
        输出debug信息
        :param msg: 信息
        :return:
        """
        pass

    def info(self, msg: str):
        """
        输出info信息
        :param msg: 信息
        :return:
        """
        pass

    def warning(self, msg: str):
        """
        输出warning信息
        :param msg: 信息
        :return:
        """
        pass

    def error(self, msg: str):
        """
        输出error信息
        :param msg: 信息
        :return:
        """
        pass

    def critical(self, msg: str):
        """
        输出critical信息
        :param msg: 信息
        :return:
        """
        pass

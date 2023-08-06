from abc import ABCMeta
from abc import abstractmethod


class Config(metaclass=ABCMeta):
    """
    资料信息集合
    """

    @abstractmethod
    def serialize(self):
        """
        序列化方法
        :return:
        """
        return {}

    def __str__(self):
        return str(self.serialize())


class FriendConfig(Config):
    """
    好友资料信息集合
    """

    def __init__(self):
        self.nickname = None
        self.email = None
        self.age = None
        self.level = None
        self.sign = None
        self.sex = None

    def serialize(self):
        return {
            'nickname': self.nickname,
            'email': self.email,
            'age': self.age,
            'level': self.level,
            'sign': self.sign,
            'sex': self.sex
        }


class GroupConfig(Config):
    """
    群资料信息集合
    """

    def __init__(self):
        self.name = None
        self.announcement = None
        self.confess_talk = None
        self.allow_member_invite = None
        self.auto_approve = None
        self.anonymous_chat = None

    def serialize(self):
        return {
            'name': self.name,
            'announcement': self.announcement,
            'confessTalk': self.confess_talk,
            'allowMemberInvite': self.allow_member_invite,
            'autoApprove': self.auto_approve,
            'anonymousChat': self.anonymous_chat
        }


class GroupMemberConfig(Config):
    """
    群成员资料信息集合
    """

    def __init__(self):
        self.id = None
        self.member_name = None
        self.special_title = None
        self.permission = None
        self.join_timestamp = None
        self.last_speak_timestamp = None
        self.mute_time_remaining = None

    def serialize(self):
        return {
            'name': self.member_name,
            'specialTitle': self.special_title
        }

from abc import ABCMeta
from abc import abstractmethod


class Msg(metaclass=ABCMeta):
    """
    Msg消息对象,任意可被发送的消息或者接收的消息都是该类的子类
    """
    @abstractmethod
    def serialize(self) -> dict:
        """
        序列化Msg
        :return: 序列化结果
        """
        pass

    def __str__(self):
        return str(self.serialize())


class SourceMsg(Msg):
    """
    SourceMsg类
    存在于接收的消息链中，作为唯一标识
    """

    def __init__(self, id, time):
        self.id = id
        self.time = time

    def serialize(self):
        return {'type': 'Source', 'id': self.id, 'time': self.time}


class PlainMsg(Msg):
    """
    PlainMsg类
    文字消息
    """

    def __init__(self, text):
        self.text = text

    def serialize(self):
        return {'type': 'Plain', 'text': self.text}


class ImageMsg(Msg):
    """
    ImageMsg类
    图片消息
    """
    URL = 'url'
    BASE64 = 'base64'
    PATH = 'path'
    __info = {URL: None, BASE64: None, PATH: None}

    def __init__(self, info, type):
        """

        :param info: 图片的来源
        :param type: ImageMsg中的三个枚举(URL,BASE64,绝对路径PATH)
        """
        self.__info[type] = info

    def get_url(self):
        """
        获取图片消息的图片URL，接收的图片消息仅有URL
        :return: URL
        """
        return self.__info[self.URL]

    def get_base64(self):
        """
        获取图片消息的图片BASE64字符串
        :return: BASE64
        """
        return self.__info[self.BASE64]

    def get_path(self):
        """
        获取图片消息的图片PATH
        :return: PATH
        """
        return self.__info[self.PATH]

    def serialize(self):
        temp = {'type': 'Image'}
        temp.update(self.__info)
        return temp


class FlashImageMsg(ImageMsg):
    """
    FlashImageMsg类
    闪照消息，继承于ImageMsg
    """

    def __init__(self, info, type):
        super().__init__(info, type)

    def serialize(self):
        temp = {'type': 'FlashImage'}
        temp.update(self.__info)
        return temp


class VoiceMsg(Msg):
    """
    VoiceMsg类
    语音消息
    """
    URL = 'url'
    BASE64 = 'base64'
    PATH = 'path'
    length = None
    __info = {URL: None, BASE64: None, PATH: None}

    def __init__(self, info, type):
        """

        :param info: 语音的来源
        :param type: VoiceMsg中的三个枚举(URL,BASE64,绝对路径PATH)
        """
        self.__info[type] = info

    def get_url(self):
        """
        获取语音消息的语音URL，接收的语音消息仅有URL
        :return: URL
        """
        return self.__info[self.URL]

    def get_base64(self):
        """
        获取语音消息的语音BASE64字符串
        :return: BASE64
        """
        return self.__info[self.BASE64]

    def get_path(self):
        """
        获取语音消息的语音PATH
        :return: PATH
        """
        return self.__info[self.PATH]

    def get_length(self):
        """
        获取语音消息的语音长度 秒
        :return: 长度
        """
        return self.length

    def serialize(self):
        temp = {'type': 'Voice', 'length': self.length}
        temp.update(self.__info)
        return temp


class AtMsg(Msg):
    """
    AtMsg类
    @某人
    """
    display = ''

    def __init__(self, target):
        """

        :param target: 艾特的对象qq号
        """
        self.target = target

    def serialize(self):
        return {'type': 'At', 'target': self.target, 'display': self.display}


class AtAllMsg(Msg):
    """
    AtAllMsg类
    艾特全体成员消息
    """

    def serialize(self):
        return {'type': 'AtAll'}


class QuoteMsg(Msg):
    """
    QuoteMsg类
    回复消息
    """

    def __init__(self, id, sender, target, origin_msg_chain, group=0):
        """

        :param id: 回复的源消息ID(SourceMsg对象中的id字段)
        :param sender: 发送者qq号
        :param target: 回复对象qq号
        :param origin_msg_chain: 回复的源消息链
        :param group: 回复的群号(好友消息时为0)
        """
        self.id = id
        self.sender = sender
        self.target = target
        self.origin_msg_Chain = origin_msg_chain
        self.group = group

    def serialize(self):
        origin_ser = []
        for i in self.origin_msg_Chain:
            origin_ser.append(i.serialize())
        return {
            'type': 'Quote',
            'id': self.id,
            'groupId': self.group,
            'senderId': self.sender,
            'targetId': self.target,
            'origin': origin_ser
        }


class ForwardMsg(Msg):
    """
    ForwardMsg类
    转发消息
    """
    __node_list = []

    class MsgNode(Msg):
        def __init__(self, sender, time, sender_name, msg_chain, id=0):
            """

            :param sender: 发送者qq
            :param time: 时间戳
            :param sender_name: 发送者昵称
            :param msg_chain: 消息链
            :param id: 引用的消息id，可不填
            """
            self.__node_list = []
            self.sender = sender
            self.time = time
            self.sender_name = sender_name
            self.msg_chain = msg_chain
            self.id = id

        def serialize(self):
            msg_chain_ser = []
            for i in self.msg_chain:
                msg_chain_ser.append(i.serialize())
            return {
                'senderId': self.sender,
                'time': self.time,
                'senderName': self.sender_name,
                'messageChain': msg_chain_ser,
                'messageId': self.id
            }

    def __len__(self):
        return self.__node_list.__len__()

    def add_node(self, msg_node: MsgNode):
        """
        给转发消息添加一个消息节点
        :param msg_node: 消息节点MsgNode对象
        :return:
        """
        self.__node_list.append(msg_node)

    def pop_node(self, index: int):
        """
        根据索引从转发消息移除一个消息节点
        :param index: 索引
        :return:
        """
        self.__node_list.pop(index)

    def remove_node(self, msg_node: MsgNode):
        """
        从转发消息移除一个消息节点
        :param msg_node: 消息节点MsgNode对象
        :return:
        """
        self.__node_list.remove(msg_node)

    def __iter__(self):
        return self.__node_list.__iter__()

    def __getitem__(self, item):
        return self.__node_list.__getitem__(item)

    def serialize(self):
        node_list_ser = []
        for i in self.__node_list:
            node_list_ser.append(i.serialize())
        return {'type': 'Forward', 'nodeList': node_list_ser}


class FaceMsg(Msg):
    """
    FaceMsg类
    表情消息(指QQ的内置表情)
    """

    def __init__(self, id, name):
        """

        :param id: 表情id
        :param name: 表情名字
        """
        self.id = id
        self.name = name

    def serialize(self):
        return {'type': 'Face', 'faceId': self.id, 'name': self.name}


class PokeMsg(Msg):
    """
    PokeMsg类
    类戳一戳消息
    """
    POKE = "Poke"
    SHOW_LOVE = "ShowLove"
    LIKE = "Like"
    HEART_BROKEN = "Heartbroken"
    SIX = "SixSixSix"
    FANG_DA_ZHAO = "FangDaZhao"

    def __init__(self, type):
        """

        :param type: PokeMsg中的6个枚举
        """
        self.type = type

    def serialize(self):
        return {'type': 'Poke', 'name': self.type}


class AppMsg(Msg):
    """
    AppMsg类
    小程序消息或卡片式消息
    """

    def __init__(self, content):
        """

        :param content:App消息的content
        """
        self.content = content

    def serialize(self):
        return {'type': 'App', 'content': self.content}


class MsgChain(Msg):
    """
    消息链类
    """
    __chain = []

    def __init__(self):
        self.__chain = []

    def __iter__(self):
        return self.__chain.__iter__()

    def __getitem__(self, item):
        return self.__chain.__getitem__(item)

    def __len__(self):
        return self.__chain.__len__()

    def add_msg(self, msg: Msg):
        """
        往消息链中增加消息
        :param msg: 任意继承Msg类的消息对象
        :return:
        """
        self.__chain.append(msg)

    def remove_msg(self, msg: Msg):
        """
        从消息链中移除消息
        :param msg: 任意继承Msg类的消息对象
        :return:
        """
        if msg in self.__chain:
            self.__chain.remove(msg)

    def pop_msg(self, index: int):
        """
        根据索引从消息链中移除消息
        :param index: 索引
        :return:
        """
        self.__chain.pop(index)

    def serialize(self):
        chain_se = []
        for i in self.__chain:
            chain_se.append(i.serialize())
        return chain_se

    def get_source(self) -> SourceMsg:
        """
        获取消息SourceMsg对象
        :return: SourceMsg对象
        """
        for i in self.__chain:
            if type(i) is SourceMsg:
                return i

    def get_plain_msg(self) -> list[PlainMsg]:
        """
        获取该消息链所有的Plain消息对象列表
        :return: PlainMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is PlainMsg:
                temp.append(i)
        return temp

    def get_image_msg(self) -> list[ImageMsg]:
        """
        获取该消息链所有的Image消息对象列表
        :return: ImageMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is ImageMsg:
                temp.append(i)
        return temp

    def get_quote_msg(self) -> list[QuoteMsg]:
        """
        获取该消息链所有的Quote消息对象列表
        :return: QuoteMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is QuoteMsg:
                temp.append(i)
        return temp

    def get_voice_msg(self) -> list[VoiceMsg]:
        """
        获取该消息链所有的Voice消息对象列表
        :return: VoiceMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is VoiceMsg:
                temp.append(i)
        return temp

    def get_at_msg(self) -> list[AtMsg]:
        """
        获取该消息链所有的At消息对象列表
        :return: AtMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is AtMsg:
                temp.append(i)
        return temp

    def get_at_all_msg(self) -> list[AtAllMsg]:
        """
        获取该消息链所有的AtAll消息对象列表
        :return: AtAllMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is AtAllMsg:
                temp.append(i)
        return temp

    def get_face_msg(self) -> list[FaceMsg]:
        """
        获取该消息链所有的Face消息对象列表
        :return: FaceMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is FaceMsg:
                temp.append(i)
        return temp

    def get_flash_image_msg(self) -> list[FlashImageMsg]:
        """
        获取该消息链所有的FlashImage消息对象列表
        :return: FlashImageMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is FlashImageMsg:
                temp.append(i)
        return temp

    def get_poke_msg(self) -> list[PokeMsg]:
        """
        获取该消息链所有的Poke消息对象列表
        :return: PokeMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is PokeMsg:
                temp.append(i)
        return temp

    def get_forward_msg(self) -> list[ForwardMsg]:
        """
        获取该消息链所有的Forward消息对象列表
        :return: ForwardMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is ForwardMsg:
                temp.append(i)
        return temp

    def get_app_msg(self) -> list[AppMsg]:
        """
        获取该消息链所有的App消息对象列表
        :return: AppMsg对象列表
        """
        temp = []
        for i in self.__chain:
            if type(i) is AppMsg:
                temp.append(i)
        return temp


class Source:
    """
    消息发送者对象集合
    """
    def __init__(self, source_msg: SourceMsg, sender: int, group: int = 0):
        """

        :param source_msg: SourceMsg对象
        :param sender: 发送者qq
        :param group: 群号(非群聊时此值为0)
        """
        self.sender = sender
        self.group = group
        self.source_msg = source_msg




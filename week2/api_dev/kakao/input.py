from abc import ABC, abstractmethod
import json

from .customerror import InvalidPayloadError


class ParentPayload(ABC):
    @classmethod
    @abstractmethod
    def from_json(cls, json_payload: str): ...

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_payload: dict): ...


class Param(ParentPayload):
    def __init__(
            self,
            origin: str,
            value: str | dict,
            groupName: str = '',
            **kwargs):
        self.origin = origin
        self.value = value
        self.groupName = groupName
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_json(cls, detail_param_json: str):
        detail_param_dict = json.loads(detail_param_json)
        return cls.from_dict(detail_param_dict)

    @classmethod
    def from_dict(cls, detail_param_dict: dict):
        # value가 딕셔너리 타입이면, 이를 **kwargs로 전달
        additional_params = detail_param_dict['value'] if isinstance(
            detail_param_dict.get('value'), dict) else {}
        try:
            origin = detail_param_dict['origin']
            value = detail_param_dict['value']
            group_name = detail_param_dict['groupName']
            return cls(
                origin=origin,
                value=value,
                groupName=group_name,
                **additional_params
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "Param 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class Params(ParentPayload):
    def __init__(self, **kwargs: dict[str, Param]):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_json(cls, action_json: str):
        params_dict = json.loads(action_json)
        return cls.from_dict(params_dict)

    @classmethod
    def from_dict(cls, action_dict: dict):
        params = {
            key: value
            for key, value in action_dict.get("params", {}).items()
        }
        return cls(**params)


class Action(ParentPayload):
    def __init__(
            self,
            id: str,
            name: str,
            params: Params,
            detailParams: dict,
            clientExtra: dict):
        self.id = id
        self.name = name
        self.params = params
        self.detailParams = detailParams
        self.clientExtra = clientExtra

    @classmethod
    def from_json(cls, action_json: str):
        action_dict = json.loads(action_json)
        return cls.from_dict(action_dict)

    @classmethod
    @classmethod
    def from_dict(cls, action_dict: dict):
        try:
            id = action_dict['id']
            name = action_dict['name']
            params = Params.from_dict(action_dict)
            detail_params = action_dict.get('detailParams', {})
            client_extra = action_dict.get('clientExtra', {})
            return cls(
                id=id,
                name=name,
                params=params,
                detailParams=detail_params,
                clientExtra=client_extra
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "Action 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class Bot(ParentPayload):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, bot_json: str):
        bot_dict = json.loads(bot_json)
        return cls.from_dict(bot_dict)

    @classmethod
    def from_dict(cls, bot_dict: dict):
        try:
            id = bot_dict['id']
            name = bot_dict['name']
            return cls(
                id=id,
                name=name
            )
        except KeyError as err:
            raise InvalidPayloadError("Bot 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class IntentExtra(ParentPayload):
    def __init__(self, reason: dict, knowledge: dict | None = None):
        self.reason = reason
        self.knowledge = knowledge

    @classmethod
    def from_json(cls, intent_extra_json: str):
        intent_extra_dict = json.loads(intent_extra_json)
        return cls.from_dict(intent_extra_dict)

    @classmethod
    def from_dict(cls, intent_extra_dict: dict):
        try:
            reason = intent_extra_dict.get('reason')
            knowledge = intent_extra_dict.get('knowledge')
            return cls(
                reason=reason,
                knowledge=knowledge
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "IntentExtra 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class Intent(ParentPayload):
    def __init__(
            self,
            id: str,
            name: str,
            extra: dict):
        self.id = id
        self.name = name
        self.extra = extra

    @classmethod
    def from_json(cls, intent_json: str):
        intent_dict = json.loads(intent_json)
        return cls.from_dict(intent_dict)

    @classmethod
    def from_dict(cls, intent_dict: dict):
        try:
            id = intent_dict.get('id', '')
            name = intent_dict.get('name', '')
            extra = IntentExtra.from_dict(intent_dict.get('extra', {}))
            return cls(
                id=id,
                name=name,
                extra=extra
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "Intent 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class User(ParentPayload):
    def __init__(
            self,
            id: str,
            type: str,
            properties: dict = {}):

        self.id = id
        self.type = type
        self.properties = properties

    @classmethod
    def from_json(cls, user_request_json: str):
        user_request_dict = json.loads(user_request_json)
        return cls.from_dict(user_request_dict)

    @classmethod
    def from_dict(cls, user_request_dict: dict):
        try:
            id = user_request_dict['id']
            type = user_request_dict['type']
            properties = user_request_dict.get('properties', {})
            return cls(
                id=id,
                type=type,
                properties=properties
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "User 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class UserRequest(ParentPayload):
    def __init__(
            self,
            timezone: str,
            block: dict,
            utterance: str,
            lang: str,
            user: User,
            params: dict):
        self.timezone = timezone
        self.block = block
        self.utterance = utterance
        self.lang = lang
        self.user = user
        self.params = params

    @classmethod
    def from_json(cls, user_request_json: str):
        user_request_dict = json.loads(user_request_json)
        return cls.from_dict(user_request_dict)

    @classmethod
    def from_dict(cls, user_request_dict: dict):
        try:
            timezone = user_request_dict['timezone']
            block = user_request_dict['block']
            utterance = user_request_dict['utterance']
            lang = user_request_dict['lang']
            user = User.from_dict(user_request_dict['user'])
            params = user_request_dict['params']
            return cls(
                timezone=timezone,
                block=block,
                utterance=utterance,
                lang=lang,
                user=user,
                params=params
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "UserRequest 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


class Payload(ParentPayload):
    def __init__(
            self,
            intent: Intent,
            user_request: dict,
            bot: Bot,
            action: Action):
        self.intent = intent
        self.user_request = user_request
        self.bot = bot
        self.action = action

    @classmethod
    def from_json(cls, payload_json: str) -> 'Payload':
        payload_dict = json.loads(payload_json)
        return cls.from_dict(payload_dict)

    @classmethod
    def from_dict(cls, payload_dict: dict) -> 'Payload':
        try:
            intent = {}
            user_request = {}
            bot = Bot.from_dict(payload_dict['bot'])
            action = Action.from_dict(payload_dict['action'])
            return cls(
                intent=intent,
                user_request=user_request,
                bot=bot,
                action=action
            )
        except KeyError as err:
            raise InvalidPayloadError(
                "Payload 객체를 생성하기 위한 키가 존재하지 않습니다.") from err


if __name__ == "__main__":
    data = {
        "bot": {
            "id": "5e0d180affa74800014bd33d",
            "name": "산돌이"
        },
        "action": {
            "name": "jp1j2gy39h",
            "clientExtra": None,
            "params": {
                "store_name": "산돌 분식",
                "lunch_menu": "떡볶이, 순대, 튀김",
                "dinner_list": "짜장면, 짬뽕국, 탕수육"
            },
            "id": "bwjfe6fxc96ngv9ra6dddzah"
        }
    }

    payload = Payload.from_dict(data)
    print(payload.bot.id)

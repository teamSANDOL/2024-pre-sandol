
from abc import abstractmethod, ABC
from enum import Enum

from .validatiion import validate_str, validate_type
from .customerror import InvalidActionError, InvalidTypeError, InvalidLinkError


class Common(ABC):
    """
    카카오톡 응답 형태의 객체를 생성하는 추상 클래스

    Attributes:
        response_content_obj (dict): 카카오톡 응답 형태의 객체

    Raises:
        NotImplementedError: render 메서드가 구현되지 않았을 때
    """

    def __init__(self):
        self.response_content_obj = {}

    @staticmethod
    def create_dict_with_non_none_values(base: dict | None = None, **kwargs):
        if base is None:
            base = {}
        base.update({k: v for k, v in kwargs.items() if v is not None})
        return base

    @abstractmethod
    def render(self): ...
    @abstractmethod
    def validate(self): ...


class Action(Enum):
    WEBLINK = 'webLink'
    MESSAGE = 'message'
    PHONE = 'phone'
    BLOCK = 'block'


class Button(Common):
    """
    카카오톡 응답 형태 Button의 객체를 생성하는 클래스

    Attributes:
        text (str): 버튼의 텍스트
        buttons (list): 버튼의 리스트

    Raises:
        ValueError: text가 문자열이 아닌 경우
    """

    def __init__(
            self,
            label: str,
            action: str | Action,
            webLinkUrl: str | None = None,
            messageText: str | None = None,
            phoneNumber: str | None = None,
            blockId: str | None = None,
            extra: dict | None = None):

        self.label = label
        self.action = self.process_action(action)
        self.webLinkUrl = webLinkUrl
        self.messageText = messageText
        self.phoneNumber = phoneNumber
        self.blockId = blockId
        self.extra = extra

        self.action_field_map = {
            Action.WEBLINK: "webLinkUrl",
            Action.MESSAGE: "messageText",
            Action.PHONE: "phoneNumber",
            Action.BLOCK: "blockId"
        }

    def process_action(self, action: str | Action) -> Action:
        """ 문자열 또는 Action 열거형 인스턴스를 Action 열거형으로 변환합니다. """
        validate_type((str, Action), action, disallow_none=True,
                      exception_type=InvalidActionError)

        if isinstance(action, str):
            try:
                return Action[action.upper()]
            except KeyError as exc:
                raise InvalidActionError(
                    f"유효하지 않은 action 값: {action}") from exc

        return action

    def validate(self):
        validate_str(self.label)

        field_to_validate = getattr(self, self.action_field_map[self.action])
        validate_str(field_to_validate)

    def render(self) -> dict:
        self.validate()
        self.response_content_obj = {
            'label': self.label,
            'action': self.action.value,
        }

        self.response_content_obj[self.action.value] = getattr(
            self, self.action_field_map[self.action])

        if self.extra is not None:
            self.response_content_obj.update(self.extra)

        return self.response_content_obj


class Buttons(Common):
    def __init__(
            self,
            buttons: list[Button] | None = None,
            max_buttons: int = 3):
        self._buttons = buttons or []
        self.max_buttons = max_buttons

    def validate(self):
        if len(self._buttons) > self.max_buttons:
            raise InvalidTypeError("버튼은 최대 3개까지 가능합니다.")
        if False in [isinstance(button, Button) for button in self._buttons]:
            raise InvalidTypeError("self._buttons는 Button으로 이루어져야 합니다.")

    def add_button(self, button: Button):
        if len(self._buttons) > self.max_buttons:
            raise InvalidTypeError("버튼은 최대 3개까지 가능합니다.")

        validate_type(Button, button, disallow_none=True)
        self._buttons.append(button)

    def delete_button(self, button: Button):
        if button not in self._buttons:
            raise ValueError("해당 버튼이 존재하지 않습니다.")
        self._buttons.remove(button)

    def render(self) -> list:
        self.validate()
        return [button.render() for button in self._buttons]


class Link(Common):
    def __init__(
            self,
            web: str | None = None,
            pc: str | None = None,
            mobile: str | None = None):
        self.web = web
        self.pc = pc
        self.mobile = mobile

    def validate(self):
        if self.web is None and self.pc is None and self.mobile is None:
            raise InvalidLinkError("Link는 최소 하나의 링크를 가져야 합니다.")
        validate_str(self.web, self.pc, self.mobile)

    def render(self) -> dict:
        self.validate()
        return self.create_dict_with_non_none_values(
            web=self.web,
            pc=self.pc,
            mobile=self.mobile,
        )


class Thumbnail(Common):
    def __init__(
            self,
            image_url: str,
            link: Link | None = None,
            fixedRatio: bool = False):
        self.image_url = image_url
        self.link = link
        self.fixedRatio = fixedRatio

    def validate(self):
        validate_str(self.image_url)

    def render(self) -> dict:
        self.validate()
        self.response_content_obj = {
            'imageUrl': self.image_url,
            'fixedRatio': self.fixedRatio,
        }
        self.create_dict_with_non_none_values(
            base=self.response_content_obj,
            link=self.link.render() if self.link is not None else None
        )
        return self.response_content_obj


class Thumbnails(Common):
    def __init__(
            self,
            thumbnails: list[Thumbnail],
            max_thumbnails: int = 1):
        self._thubnails = thumbnails
        self.max_thumbnails = max_thumbnails

    def validate(self):
        if len(self._thubnails) > self.max_thumbnails:
            raise InvalidTypeError("버튼은 최대 3개까지 가능합니다.")
        for thumbnail in self._thubnails:
            validate_type(Thumbnail, thumbnail)

    def add_button(self, thumbnail: Thumbnail):
        if len(self._thubnails) > self.max_thumbnails:
            raise InvalidTypeError("버튼은 최대 3개까지 가능합니다.")

        validate_type(thumbnail, Thumbnail)
        self._thubnails.append(thumbnail)

    def delete_button(self, thumbnail: Thumbnail):
        if thumbnail not in self._thubnails:
            raise ValueError("해당 버튼이 존재하지 않습니다.")
        self._thubnails.remove(thumbnail)

    def render(self) -> list:
        self.validate()
        return [thumbnail.render() for thumbnail in self._thubnails]


class Profile(Common):
    def __init__(self, nickname: str, image_url: str | None = None):
        self.nickname = nickname
        self.image_url = image_url

    def validate(self):
        validate_str(self.nickname, self.image_url)

    def render(self):
        return self.create_dict_with_non_none_values(
            nickname=self.nickname,
            imageUrl=self.image_url)


class ListItem(Common):
    def __init__(
            self,
            title: str,
            description: str | None = None,
            imageUrl: str | None = None,
            link: Link | None = None,
            action: str | Action | None = None,
            block_id: str | None = None,
            message_text: str | None = None,
            extra: dict | None = None):
        self.title = title
        self.description = description
        self.imageUrl = imageUrl
        self.link = link
        self.action = action
        self.block_id = block_id
        self.message_text = message_text
        self.extra = extra

    def validate(self):
        validate_str(
            self.title, self.description, self.imageUrl,
            self.block_id, self.message_text)
        validate_type(Link, self.link)

    def render(self):
        self.validate()
        self.response_content_obj = {
            'title': self.title,
            'description': self.description,
            'imageUrl': self.imageUrl,
        }

        self.create_dict_with_non_none_values(
            base=self.response_content_obj,
            link=self.link.render() if self.link is not None else None,
            action=self.action,
            blockId=self.block_id,
            messageText=self.message_text,
        )
        return self.response_content_obj


class ListItems(Common):
    def __init__(
            self,
            list_items: list[ListItem] | None = None,
            max_list_items: int = 5):
        self._list_items = list_items
        self.max_list_items = max_list_items

    def validate(self):
        if len(self._list_items) > self.max_list_items:
            raise ValueError(
                f"버튼이 최대 {self.max_list_items}개까지 가능하도록 제한되어 있습니다.")
        validate_type(ListItem, *self._list_items)

    def add_list_item(self, list_item: ListItem):
        if len(self._list_items) > self.max_list_items:
            raise ValueError(
                f"버튼이 최대 {self.max_list_items}개까지 가능하도록 제한되어 있습니다.")
        validate_type(ListItem, list_item)
        self._list_items.append(list_item)

    def delete_list_item(self, list_item: ListItem):
        if list_item not in self._list_items:
            raise ValueError("해당 ListItem이 존재하지 않습니다.")
        self._list_items.remove(list_item)

    def render(self):
        self.validate()
        return [list_item.render() for list_item in self._list_items]


if __name__ == "__main__":
    button = Button(
        label="구경하기",
        action="webLink",
        webLinkUrl="https://sio2.pe.kr/login",
        messageText=None
    )
    print(button.render())

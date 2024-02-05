
import json
from abc import ABC, abstractmethod

from .validatiion import validate_str, validate_type
from .common import Buttons, ListItem, ListItems, Profile
from .common import Thumbnail, Thumbnails
from . import itemcard


class ParentResponse(ABC):
    """
    카카오톡 응답 형태의 객체를 생성하는 추상 클래스

    Attributes:
        response_content_obj (dict): 카카오톡 응답 형태의 객체

    Raises:
        NotImplementedError: render 메서드가 구현되지 않았을 때
    """

    def __init__(self):
        self.response_content_obj = {}

    @abstractmethod
    def render(self): ...

    @abstractmethod
    def validate(self): ...

    def generate_response_body(self) -> dict:
        self.render()
        return {
            'version': '2.0',
            'template': {
                'outputs': [self.response_content_obj]
            }
        }

    @staticmethod
    def create_dict_with_non_none_values(
            base: dict | None = None, **kwargs):
        if base is None:
            base = {}
        base.update({k: v for k, v in kwargs.items() if v is not None})
        return base

    def get_dict(self, rendering: bool = True) -> dict:
        """
            응답의 사전 표현을 반환합니다.

            rendering이 True인 경우, generate_response_body()를 사용하여 응답 본문을 생성하고,
            rendering이 False인 경우, response_content_obj를 사용하여 응답 본문을 생성합니다.

            Args:
                rendering: 응답 본문을 렌더링할지 여부를 나타내는 불리언 값입니다. 기본값은 True입니다.

            Returns:
                dict: 응답의 딕셔너리 표현입니다.
        """
        if rendering:
            return self.generate_response_body()
        else:
            return self.response_content_obj

    def get_json(self, rendering=True, **kwargs):
        """
        응답 본문을 생성하여 JSON 형식의 문자열로 반환합니다.

        rendering이 True인 경우, generate_response_body()를 사용하여 응답 본문을 생성하고,
        rendering이 False인 경우, response_content_obj를 사용하여 응답 본문을 생성합니다.

        Args:
            rendering: 응답 본문을 렌더링할지 여부를 나타내는 불리언 값입니다. 기본값은 True입니다.
            **kwargs: json.dumps() 함수에 전달되는 추가적인 인자들입니다.

        Returns:
            생성된 응답 본문을 JSON 형식의 문자열로 반환합니다.
        """
        if rendering:
            return json.dumps(
                self.generate_response_body(), ensure_ascii=True, indent=4, **kwargs
            )
        else:
            return json.dumps(
                self.response_content_obj, ensure_ascii=True, indent=4, **kwargs
            )


class SimpleTextResponse(ParentResponse):
    """
    카카오톡 응답 형태 SimpleText의 객체를 생성하는 클래스

    Attributes:
        text (str): 응답할 텍스트

    Raises:
        ValueError: text가 문자열이 아닌 경우
    """

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def validate(self):
        return validate_str(self.text)

    def render(self):
        self.validate()
        self.response_content_obj = {
            'simpleText': {
                'text': self.text,
            },
        }
        return self.response_content_obj


class SimpleImageResponse(ParentResponse):
    """
    카카오톡 응답 형태 SimpleImage의 객체를 생성하는 클래스

    Attributes:
        image_url (str): 이미지의 URL
        alt_text (str): 대체 텍스트

    Raises:
        ValueError: image_url, alt_text가 문자열이 아닌 경우
    """

    def __init__(self, image_url: str, alt_text: str):
        super().__init__()
        self.image_url = image_url
        self.alt_text = alt_text

    def validate(self):
        return validate_str(self.image_url, self.alt_text)

    def render(self):
        validate_str(self.image_url, self.alt_text)
        self.response_content_obj = {
            "SimpleImage": {
                "imageUrl": self.image_url,
                "altText": self.alt_text
            }
        }


class ParentCard(ParentResponse, ABC):
    """
    부모 카드 클래스입니다.

    Attributes:
        buttons (Buttons): 버튼 객체입니다.
    """

    def __init__(self, buttons: Buttons | None = None):
        super().__init__()
        self.buttons = buttons

    def set_buttons(self, buttons: Buttons):
        """
        버튼을 설정합니다.

        Parameters:
            buttons (Buttons): 설정할 버튼 객체
        """
        self.buttons = buttons

    def validate(self):
        if self.buttons is not None:
            validate_type(self.buttons, Buttons)

    @abstractmethod
    def render(self): ...


class BasicCard(ParentCard):
    """
    카카오톡 응답 형태 BasicCard의 객체를 생성하는 클래스

    Args:
        thumbnail (Thumbnail): 썸네일 이미지 정보
        title (str | None optional): 카드 제목. Defaults to None.
        description (str | None optional): 카드 설명. Defaults to None.
        buttons (Buttons | None optional): 카드 버튼 정보. Defaults to None.
        forwardable (bool, optional): 카드 전달 가능 여부. Defaults to False.
    """

    def __init__(
            self,
            thumbnail: Thumbnail,
            title: str | None = None,
            description: str | None = None,
            buttons: Buttons | None = None,
            forwardable: bool = False):
        super().__init__(buttons=buttons)
        self.thumbnail = thumbnail
        self.title = title
        self.description = description
        self.forwardable = forwardable

    def validate(self):
        super().validate()
        validate_str(self.title, self.description)

    def render(self):
        self.validate()
        self.response_content_obj = {
            "thumbnail": self.thumbnail.render(),
            "forwardable": self.forwardable
        }
        # create_dict_with_non_none_values 메소드는 ParentCard에 정의되어야 함
        self.create_dict_with_non_none_values(
            base=self.response_content_obj,
            title=self.title,
            description=self.description,
            buttons=self.buttons.render() if self.buttons else None
        )
        self.response_content_obj = {"basicCard": self.response_content_obj}


class CommerceCard(ParentCard):
    def __init__(
        self,
        price: int,
        thumbnails: Thumbnails,
        title: str | None = None,
        description: str | None = None,
        buttons: Buttons | None = None,
        profile: Profile | None = None,
        currency: str | None = None,
        discount: str | None = None,
        discount_rate: str | None = None,
        discount_price: str | None = None,
    ):
        super().__init__(buttons=buttons)
        self.price = price
        self.thumbnails = thumbnails
        self.title = title
        self.description = description
        self.currency = currency
        self.discount = discount
        self.discount_rate = discount_rate
        self.discount_price = discount_price
        self.profile = profile

    def validate(self):
        super().validate()

    def render(self):
        self.validate()
        self.response_content_obj = {
            "commerceCard": {
                "price": self.price,
                "thumbnails": self.thumbnails.render(),
            }
        }
        self.create_dict_with_non_none_values(
            base=self.response_content_obj["commerceCard"],
            title=self.title,
            description=self.description,
            currency=self.currency,
            discount=self.discount,
            discountRate=self.discount_rate,
            discountPrice=self.discount_price,
            profile=self.profile.render() if self.profile else None,
            buttons=self.buttons.render() if self.buttons else None,
        )


class ListCard(ParentCard):
    def __init__(
            self,
            header: ListItem,
            items: ListItems,
            buttons: Buttons | None = None,):
        super().__init__(buttons=buttons)
        self.header = header
        self.items = items

    def validate(self):
        super().validate()
        validate_type(self.header, ListItem)
        validate_type(self.items, ListItems)

    def render(self):
        self.validate()
        self.response_content_obj = {
            "listCard": {
                "header": self.header.render(),
                "items": self.items.render(),
            }
        }
        self.create_dict_with_non_none_values(
            base=self.response_content_obj["listCard"],
            buttons=self.buttons.render() if self.buttons else None,
        )


class ItemCard(ParentCard):
    def __init__(
            self,
            itemList: itemcard.Item,
            thumbnail: itemcard.Thumbnail | None = None,
            head: itemcard.Head | None = None,
            profile: itemcard.Profile | None = None,
            image_title: itemcard.ImageTitle | None = None,
            item_list: itemcard.ItemList | None = None,
            item_list_alignment: str | None = None,
            item_list_summary: itemcard.ItemListSummary | None = None,
            title: str | None = None,
            description: str | None = None,
            buttons: Buttons | None = None,
            buttonLayout: str | None = None):
        super().__init__(buttons=buttons)
        self.itemList = itemList
        self.thumbnail = thumbnail
        self.head = head
        self.profile = profile
        self.image_title = image_title
        self.item_list = item_list
        self.item_list_alignment = item_list_alignment
        self.item_list_summary = item_list_summary
        self.title = title
        self.description = description
        self.buttonLayout = buttonLayout

    def validate(self):
        super().validate()
        validate_type(self.itemList, itemcard.Item, disallow_none=True)
        validate_type(self.thumbnail, itemcard.Thumbnail)
        validate_type(self.head, itemcard.Head)
        validate_type(self.profile, itemcard.Profile)
        validate_type(self.image_title, itemcard.ImageTitle)
        validate_type(self.item_list, itemcard.ItemList)
        validate_type(self.item_list_summary, itemcard.ItemListSummary)
        validate_str(self.title, self.description, self.buttonLayout)

    def render(self):
        self.validate()
        self.response_content_obj = {
            "itemCard": {
                "itemList": self.itemList.render(),
                "thumbnail": self.thumbnail.render(),
                "head": self.head.render(),
                "profile": self.profile.render(),
                "imageTitle": self.image_title.render(),
                "itemList": self.item_list.render(),
                "itemListAlignment": self.item_list_alignment,
                "itemListSummary": self.item_list_summary.render(),
                "title": self.title,
                "description": self.description,
                "buttonLayout": self.buttonLayout,
            }
        }
        self.create_dict_with_non_none_values(
            base=self.response_content_obj["itemCard"],
            buttons=self.buttons.render() if self.buttons else None,
        )


if __name__ == "__main__":
    # 사용 예시
    simple_text_response = SimpleTextResponse("이것은 간단한 텍스트 메시지입니다.")
    print(simple_text_response.get_dict(rendering=True))

from .common import Common, Link
from .validatiion import validate_str, validate_int, validate_type


class Thumbnail(Common):
    def __init__(
            self,
            imageUrl: str,
            wdith: int | None = None,
            height: int | None = None,
            link: Link | None = None):
        self.imageUrl = imageUrl
        self.width = wdith
        self.height = height
        self.link = link

    def validate(self):
        validate_str(self.imageUrl, disallow_none=True)
        validate_int(self.width, self.height)


class Head(Common):
    def __init__(self, title: str):
        self.title = title

    def validate(self):
        validate_str(self.title)

    def render(self):
        self.validate()
        return {'title': self.title}


class ImageTitle(Common):
    def __init__(
            self,
            title: str,
            description: str | None = None,
            imageUrl: str | None = None):
        self.title = title
        self.description = description
        self.imageUrl = imageUrl

    def validate(self):
        validate_str(self.title, disallow_none=True)
        validate_str(self.description)

    def render(self):
        self.validate()
        return self.create_dict_with_non_none_values(
            title=self.title,
            description=self.description,
            imageUrl=self.imageUrl
        )


class Item(Common):
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def validate(self):
        validate_str(self.title, self.description, disallow_none=True)

    def render(self):
        self.validate()
        return self.create_dict_with_non_none_values(
            title=self.title,
            description=self.description
        )


class ItemList(Common):
    def __init__(self, item_list: list[Item] | None = None):
        self._item_list = item_list

    def validate(self):
        validate_type(Item, *self._item_list, disallow_none=True)

    def add_item_list(self, item_list: Item):
        self._item_list.append(item_list)

    def render(self):
        self.validate()
        return [item.render() for item in self._item_list]


class ItemListSummary(Item):
    ...


class Profile(Common):
    def __init__(
            self,
            title: str,
            image_url: str | None = None,
            width: int | None = None,
            height: int | None = None):
        self.title = title
        self.image_url = image_url
        self.width = width
        self.height = height

    def validate(self):
        validate_str(self.title, disallow_none=True)
        validate_str(self.image_url)
        validate_int(self.width, self.height)

    def render(self):
        self.validate()
        return self.create_dict_with_non_none_values(
            title=self.title,
            imageUrl=self.image_url,
            width=self.width,
            height=self.height
        )

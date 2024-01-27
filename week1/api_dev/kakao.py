"""
This module provides the Kakao package.
"""

import json
from abc import ABC, abstractmethod


class ParentTemplateClass(ABC):
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

    def generate_response_body(self) -> dict:
        self.render()
        return {
            'version': '2.0',
            'template': {
                'outputs': [self.response_content_obj]
            }
        }

    def get_json(self, rendering: bool = True) -> str:
        if rendering:
            return json.dumps(
                self.generate_response_body(), ensure_ascii=True
                )
        else:
            return json.dumps(
                self.response_content_obj, ensure_ascii=True
                )

    def get_dict(self, rendering: bool = True) -> dict:
        if rendering:
            return self.generate_response_body()
        else:
            return self.response_content_obj


class SimpleTextTemplate(ParentTemplateClass):
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

    def render(self):
        # 유효성 검사
        if not isinstance(self.text, str):
            raise ValueError("text는 문자열이어야 합니다.")

        # 카카오톡 응답 형태의 객체 생성
        self.response_content_obj = {
                    'simpleText': {
                        'text': self.text,
                    },
                }
        return self.response_content_obj


class SimpleImageTemplate(ParentTemplateClass):
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

    def render(self):
        # 유효성 검사
        if (not isinstance(self.image_url, str) or
                not isinstance(self.alt_text, str)):
            raise ValueError("image_url, alt_text는 문자열이어야 합니다.")

        # 카카오톡 응답 형태의 객체 생성
        self.response_content_obj = {
            "SimpleImage": {
                "imageUrl": self.image_url,
                "altText": self.alt_text
            }
        }


if __name__ == "__main__":
    # 사용 예시
    simple_text_response = SimpleTextTemplate("이것은 간단한 텍스트 메시지입니다.")
    print(simple_text_response.get_dict(rendering=True))

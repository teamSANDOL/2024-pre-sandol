import requests # type: ignore # noqa
import os
from typing import Any, Union
from flask import Flask, jsonify
import json

from utility.result_wrapper import add_text_element  # type: ignore # noqa 
from utility.frozen_json import FacadeJSON  # type: ignore # noqa
from kakao import SimpleTextTemplate  # type: ignore

app = Flask(__name__)


class DataRetrievalError(Exception):
    """
    데이터를 받아오지 못했을 때 발생하는 에러

    Attributes:
        message (str): 에러 메시지
    """
    def __init__(self, message="[Error] 데이터를 받아오지 못했습니다."):
        super().__init__(message)

    def __dict__(self):
        return {"error": self.args[0]}

    @property
    def to_dict(self):
        return self.__dict__()


@app.route('/')
def root():
    return "error"


@app.route('/subway', methods=['GET', 'POST'])
def subway_info():
    """
    지하철 도착 정보를 반환하는 API

    SimpleTextTemplate을 이용하여 카카오톡 응답 형태의 객체 생성
    """
    try:
        content = __load_json(PATH)
        if content['status'] not in ["success", "200", 200,]:
            raise DataRetrievalError()
        alt_text = subway_info_handler(content)
        return_content = SimpleTextTemplate(text=alt_text)
        return jsonify(return_content.get_dict())

    except FileNotFoundError:
        return_content = DataRetrievalError().to_dict  # 추후 세부 에러 메시지 추가
        return jsonify(return_content, 500)

    except DataRetrievalError as e:
        return_content = e.to_dict  # 추후 세부 에러 메시지 추가
        return jsonify(return_content, 500)

    except Exception:
        return_content = DataRetrievalError().to_dict  # 추후 세부 에러 메시지 추가
        return jsonify(return_content, 500)


def subway_info_handler(content: dict[str, Union[dict, str]]) -> str:
    """
    지하철 도착 정보를 처리하는 함수

    Args:
        content (dict): 지하철 도착 정보가 담긴 dict
    Returns:
        alt_text (str): 카카오톡응답을 위한 문자열
    """
    base_text = "현재 정왕역의 열차 도착 정보를 알려드릴게요!"
    result: Union[dict[Any, Any], str, None] = content.get("resul")
    if isinstance(result, dict):
        info_text: list[str] = [f"[{k}] : {v[0]}" for k, v in result.items()]
        info_text.insert(0, base_text)
        alt_text = "\n".join(info_text)
    else:
        raise DataRetrievalError()
    return alt_text


PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "resource",
    "SubwayArrival.json"
)


def __load_json(path) -> dict:
    with open(path, "r", encoding="UTF-8") as f:  # cp949 에러 방지용 encoding 추가
        raw = json.load(f)

    return raw


if __name__ == "__main__":
    app.run()

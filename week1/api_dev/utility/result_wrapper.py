from .frozen_json import FacadeJSON


def add_text_element(body, content):
    base_block = {
        "simpleText": {"text": content}
    }
    body = FacadeJSON(body)
    body.add(base_block)
    return body.to_json()


def generate_response_body():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
            ]
        }
    }

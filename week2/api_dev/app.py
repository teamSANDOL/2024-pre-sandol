import os
import json
import sys

from flask import Flask, jsonify, request

from .kakao import Payload, SimpleTextResponse
# from .ref import main

bot_id_dict: dict = {
    "산돌 분식": "5e0d180affa74800014bd33d",
    "한공 푸드": "3c0f223affa74800024ac31c",
    "티노 샌드위치": "s2134a85n8021d1w87it3c3h",
}

menu_dict: dict = {
    "store": [
    ],
}

app = Flask(__name__)


@app.route('/updateMenu', methods=["POST"])
def update_menu():
    req = request.get_json()
    try:
        # Facade Pattern
        payload: Payload = Payload.from_dict(req)
        bot_id = payload.bot.id
        params = payload.action.params

        store_name: str = params.store_name
        launch_menus: str = params.lunch_menu
        dinner_lists: str = params.dinner_menu

        if bot_id == bot_id_dict[store_name]:
            target_store: None | dict = None
            stores: list = menu_dict["store"]

            for store in stores:
                if store["name"] == store_name:
                    target_store = store
                    break

            if target_store is None:
                target_store = {
                    "name": store_name,
                    "menu": {
                        "lunch": [],
                        "dinner": [],
                    }
                }
                stores.append(target_store)

            store_menu: dict[str, list[str]] = target_store["menu"]
            store_menu["lunch"] = [
                menu.strip() for menu in launch_menus.split(",")]
            store_menu["dinner"] = [
                menu.strip() for menu in dinner_lists.split(",")]
            basepath = os.path.dirname(os.path.abspath(__file__))
            menupath = os.path.join(basepath, "repo", "menu.json")
            with open(menupath, "w", encoding="UTF-8",) as f:
                json.dump(menu_dict, f, ensure_ascii=False, indent=4)
        else:
            raise ValueError("유효하지 않은 bot id입니다.")
        return jsonify(
            {"response": SimpleTextResponse("성공적으로 저장하였습니다.").get_dict()}
        )
    except Exception as e:
        return jsonify(
            {"response": SimpleTextResponse(
                f"[ERROR] 에러가 발생했습니다. {e}").get_dict()}
        )


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
    app.run(host='0.0.0.0', port=port, debug=True)

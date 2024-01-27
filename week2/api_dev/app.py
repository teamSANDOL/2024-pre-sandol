from flask import Flask, request, jsonify
# from .ref import main

app = Flask(__name__)


@app.route('/updateMenu', methods=["POST"])
def update_menu():
    # req = request.get_json()
    # return main.run(req)
    return None


if __name__ == "__main__":
    app.run()

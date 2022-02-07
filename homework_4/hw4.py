from flask import Flask, request
from time import strftime
from typing import Dict, Tuple, Any, Union
from werkzeug.datastructures import CombinedMultiDict
from random import choice


app = Flask(__name__)


@app.route("/whoami")
def whoami() -> str:
    """
    Provides information about the client
    :return: string with information
    """
    blank: Dict[str, str] = {}
    undefined: str = "undefined"
    client_name, client_ip, server_time = request.user_agent.browser, request.remote_addr, strftime("%H:%M:%S")
    blank["browser"] = client_name.capitalize() if client_name else undefined
    blank["ip"] = client_ip if client_ip else undefined
    blank["time"] = server_time
    return f"<div>Browser: {blank['browser']}<br>IP address: {blank['ip']}<br>Time Server: {blank['time']}</div>"


@app.route("/source_code")
def source_code() -> str:
    """
    Shows the source code of the current file
    :return: contents of this file
    """
    script_file_name: str = __file__.split("/")[-1]
    with open(script_file_name, "r") as f:
        yourself_data = f.read()
    return f"<pre>{yourself_data}</pre>"


@app.route("/random")
def random_sequence() -> str:
    """
    Generates a string of random English characters,
    special characters and numbers, depending on the settings

    string to test (insert end url): ?length=42&specials=1&digits=0

    :return: string of random chars or an empty string
    """
    result: str = ""
    data_work: Dict[str, str] = {
        "alphabet": "abcdefghijklmnopqrstuvwxyz",
        "special_chars": '!"№;%:?*()_+',
        "numbers": "0123456789"
    }
    reserved_keys: Tuple[str, str, str] = ("length", "specials", "digits")
    request_data: CombinedMultiDict = request.values
    if request_data:
        def get_value(key: str) -> int:
            if request_data.get(key):
                value: Union[str, Any] = request_data.get(key)
                if value.isdigit():
                    return int(value)
            return 0

        def get_settings() -> dict:
            settings: Dict[str, int] = {}
            for current_key in request_data:  # type: ignore
                if current_key in reserved_keys:
                    settings[current_key] = get_value(current_key)
            return settings
        sequence_settings = get_settings()

        def build_sequence() -> str:
            length: int = sequence_settings.get(reserved_keys[0], 0)
            if 1 <= length <= 100:
                sequence_string, spirit_string = "", ""
                specials: int = sequence_settings.get(reserved_keys[1], 0)
                digits: int = sequence_settings.get(reserved_keys[2], 0)
                spirit_string += data_work["alphabet"]
                if specials:
                    spirit_string += data_work["special_chars"]
                if digits:
                    spirit_string += data_work["numbers"]
                for _ in range(length):
                    sequence_string += choice(spirit_string)
                return sequence_string
            else:
                return ""
        result = build_sequence()
    return f"<div>{result}</div>"


if __name__ == "__main__":
    app.run(debug=True)

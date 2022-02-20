from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from typing import Tuple, Dict, Union, Any
from random import choice


def random_sequence(request) -> HttpResponse:
    """
    Generates a string of random English characters,
    special characters and numbers, depending on the settings

    string to test (insert end url): ?length=42&specials=1&digits=0
    :param request: contains metadata about the request
    :return: views as an instance of a class HttpResponse
    """
    result: str = ""
    if request.GET:
        request_data: QueryDict = request.GET
        reserved_keys: Tuple[str, str, str] = ("length", "specials", "digits")
        data_work: Dict[str, str] = {
            "alphabet": "abcdefghijklmnopqrstuvwxyz",
            "special_chars": '!"№;%:?*()_+',
            "numbers": "0123456789"
        }

        def get_value(key: str) -> int:
            if request_data.get(key):
                value: Union[str, Any] = request_data.get(key)
                if value.isdigit():
                    return int(value)
            return 0

        def get_settings() -> dict:
            settings: Dict[str, int] = {}
            for current_key in request_data:
                if current_key in reserved_keys:
                    settings[current_key] = get_value(current_key)
            return settings

        sequence_settings = get_settings()
        print(sequence_settings)

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

    return HttpResponse(f'<b>{result}</b>')

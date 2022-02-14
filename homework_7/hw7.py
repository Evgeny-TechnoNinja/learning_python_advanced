from flask import Flask, request
from time import strftime
from typing import Dict, Tuple, Any, Union
from werkzeug.datastructures import CombinedMultiDict
from random import choice
import assets


app = Flask(__name__)
NAVIGATION: Dict[str, str] = assets.navigation("Main", "/", "Who am I", "/whoami", "Source code", "/source_code",
                                               "Randomness", "/random")
LOADING_STYLES: Dict[str, str] = {
    "style_navigation": NAVIGATION["nav_style"],
    "style_section": assets.section_style(),
    "style_description": assets.description_style(),
    "style_wrap": assets.wrap_style(),
    "style_pre": assets.pre_style(),
    "style_form": assets.form_style(),
    "style_big_text": assets.big_txt()
}
COMMON_STYLES: str = f"""
    <style>
        {LOADING_STYLES["style_navigation"]}
        {LOADING_STYLES["style_section"]}
        {LOADING_STYLES["style_description"]}
        {LOADING_STYLES["style_wrap"]}
    </style>
"""


@app.route("/whoami")
def whoami() -> str:
    """
    Provides information about the client
    :return: string as html markup
    """
    blank: Dict[str, str] = {}
    undefined: str = "undefined"
    client_name, client_ip, server_time = request.user_agent.browser, request.remote_addr, strftime("%H:%M:%S")
    blank["browser"] = client_name.capitalize() if client_name else undefined
    blank["ip"] = client_ip if client_ip else undefined
    blank["time"] = server_time

    data_page = {
        "title": "Homework 7 Whoami",
        "heading": "Data about you",
        "navigation": NAVIGATION["nav"]
    }
    head_insert: str = f"""
            <title>{data_page["title"]}</title>
            {COMMON_STYLES}
        """
    head: str = assets.head(head_insert)
    return f"""
    <!doctype html>
    <html lang="en">
        {head}
        <body>
        <header class="header">
            {data_page["navigation"]}
        </header>
        <section class="section">
            <div class="container">
                <div class="wrap">
                    <div class="description">
                        <h2>{data_page["heading"]}</h2>
                        <div>Your browser: <b>{blank["browser"]}</b><div>
                        <div>Your IP address: <b>{blank["ip"]}</b><div>
                        <div>Time to receive: <b>{blank["time"]}</b><div>
                    </div>
                </div>
            </div>
        </section>
      </body>
    </html>
    """


@app.route("/source_code")
def source_code() -> str:
    """
    Shows the source code of the current file
    :return: contents of this file
    """
    script_file_name: str = __file__.split("/")[-1]
    with open(script_file_name, "r") as f:
        yourself_data = f.read()
    yourself_data = yourself_data.replace("<", "&lt;").replace(">", "&gt")

    data_page: Dict[str, str] = {
        "title": "Homework 7 source code",
        "heading": "Source Code",
        "description": "Look into the soul of the program",
        "navigation": NAVIGATION["nav"],
    }
    head_insert: str = f"""
                <title>{data_page["title"]}</title>
                {COMMON_STYLES}
                <style>{LOADING_STYLES["style_pre"]}</style>
            """
    head: str = assets.head(head_insert)

    return f"""
    <!doctype html>
    <html lang="en">
        {head}
        <body>
        <header class="header">
            {data_page["navigation"]}
        </header>
        <section class="section">
            <div class="container">
                <div class="wrap">
                    <div class="description">
                        <h2>{data_page["heading"]}</h2>
                        <div>{data_page["description"]}<div>
                        <hr>
                        <pre>{yourself_data}</pre>
                    </div>
                </div>
            </div>
        </section>
      </body>
    </html>
    """


@app.route("/random", methods=["GET"])
def random_sequence() -> str:
    """
    Generates a string of random English characters,
    special characters and numbers, depending on the settings

    string to test (insert end url): ?length=42&specials=1&digits=0

    :return: string as html markup
    """
    result: str = ""
    data_work: Dict[str, str] = {
        "alphabet": "abcdefghijklmnopqrstuvwxyz",
        "special_chars": '!"№;%:?*()_+',
        "numbers": "0123456789"
    }
    reserved_keys: Tuple[str, str, str] = ("length", "specials", "digits")
    request_data: CombinedMultiDict = request.values

    data_page: Dict[str, str] = {
        "title": "Homework 7 Random",
        "heading": "Random sequence",
        "description": "Fill in the fields correctly:",
        "navigation": NAVIGATION["nav"],
        "result": "Result"
    }
    head_insert: str = f"""
            <title>{data_page["title"]}</title>
            {COMMON_STYLES}
            <style>
                {LOADING_STYLES["style_form"]}
                {LOADING_STYLES["style_big_text"]}
            </style>
        """
    head: str = assets.head(head_insert)

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

    return f"""
    <!doctype html>
    <html lang="en">
        {head}
        <body>
        <header class="header">
            {data_page["navigation"]}
        </header>
        <section class="section">
            <div class="container">
                <div class="wrap">
                    <div class="description">
                        <h1>{data_page["heading"]}</h1>
                        <div>{data_page["description"]}<div>
                        <form>
                            <label for="len">Length (1 - 100):</label>
                            <input type="number" id="len" name="length" max="100" min="1" value="{request.values.get("length", 48)}"> 
                            <label for="specials">Specials (0 - 1):</label>
                            <input type="number" id="specials" name="specials" max="1" min="0" value="{request.values.get("specials", 0)}">
                            <label for="digits">Digits (0 - 1):</label>
                            <input type="number" id="digits" name="digits" max="1" min="0" value="{request.values.get("digits", 0)}">
                            <input type="submit" value="Generates" class="btn btn-primary">
                        </form>
                        <hr>
                        <h3>{data_page["result"]}</h3>
                        <div><b class="big-txt">{result}</b></div>
                    </div>
                </div>
            </div>
        </section>
      </body>
    </html>
    """ # noqa


@app.route("/")
def index():
    """
    Main page
    :return: string as html markup
    """
    data_page: Dict[str, str] = {
        "title": "Homework 7",
        "heading": "Welcome to see my homework 7",
        "description": "You can see how much I tried here. You might like. Walk through the menu.",
        "navigation": NAVIGATION["nav"]
    }
    head_insert: str = f"""
        <title>{data_page["title"]}</title>
        {COMMON_STYLES}
    """
    head: str = assets.head(head_insert)

    return f"""
<!doctype html>
<html lang="en">
    {head}
    <body>
    <header class="header">
        {data_page["navigation"]}
    </header>
    <section class="section">
        <div class="container">
            <div class="wrap">
                <div class="description">
                    <h1>{data_page["heading"]}</h1>
                    <div>{data_page["description"]}<div>
                    <img width="300" height="300" alt="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAlgAAAJYCAMAAACJuGjuAAADAFBMVEWPj4/syafUzccxLS5LQTvV0c7ewqb63L6AaVa8r6LGsZxmW1TSuqRyY1i7trJza2YODAq6oYm2noft49lsVD3t3MxAQECojHKrm466ubnEq5UcGRoAAACso5ybgmzevJtoYV+sp6TdtI2roJW6sasQEBCqlIC8rJxMSUrGt6vKqoxdUEOemZYgHBzJpICAgICPgHOQi4iem5nv6+jCoH9YS0OQh4JlVUmOhHrGu7EpKCi1knEYFRadjoG2lnjpuo3i186elo+uq6gHBgaNc12DfXuOe2yafmTFs6R/eHGNd2SBcWWbhXO+u7iCeXRMRkNfXFl/fHlaU09vaGFPSEHBmHFYRzswKSeNcFbptoVaV1jIx8cvKCLx8fGRj5BLPTSnhGRyW0nOonh2c3Q9My7crH8/Ozytq6vW1dXk4+NlUUK0jmp/ZU+ael2DgYJoZWafnZ3++/iRj4/97+L40Kn3xJP+9/H74Mb859T98+msq6v3yJr52Lfv7+/4zKLj4+NgYGD7483Pz8+/v7/51LD869uEgYKenZ0+MCMgICDf39+fn58wMDC5kGlwcHB7YEYuJBqvr69/f3/ntINQUFAfGBJcSDWaeFiKbE/XqHsaFxhNPCzInHL638X748wWExTx7erQro1ZT0nw6eM+NzWphGB9cGPg08bv4dR0Z14UERLgy7jrwpyPf3PTwbF1cG3j39zHv7mdkYju2cbEp43Ppn/Py8jt0rjcsIbu5+Ht1b+dkIPQqoZfWFGrn5apkHne19F+dGqciXrUxbg+NCri29XCnHjszrDcy7uel5HduJWql4g/ODHhz7+elIrHw8A/PDleTDuPiIHUyb/RtpyCdWzdz8KQg3pyYFC3pZW8qJSoiGvMu6vgx7HRspXr0718ZE1QTElPQDNWRTnLonuDgYFtXEzIx8iIh4fs18TOw7pmZWY3LCLqvpTOx8HNv7Lcx7SAbl58aFTMuKTf29jr0Lbv5dtpZ2iciHS6mHe2moC5lHEjHyD////2wIz///8nzITxAAABAHRSTlP///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AU/cHJQAAU8tJREFUeJztfWmMZMlxHsWiPLZEkWtYXLKlpiyCGqANebEEJFKQtfC1OizINiTBVV1dparunr57eqZ7Znru2dlzdrnLPbjmTYqUbFGmSEmURUu2IcOwReuwBMHHHws+ftgwbMP2D0OAoR9G1ZTrZb68r8h8me+ofh8gcafrHZkZ34uIjIyMfMusRYsEeEvVDWixmGiJ1SIJWmK1SIKWWC2SoCVWiyRoidUiCVpitUiCllgtkqAlVoskaInVIglaYrVIgpZYLZKgJVaLJGiJ1SIJWmK1SIKWWC2SoCWWC6PhcOlqhsHuRMZgcPXOsOoG1hMtsTQYXt0aKCRyoDO42lKMQ0sshuFVbzppCLa1VHU/aoGWWHMsHRcnlITBS6Oqe1UtzjaxRi9F0FEWvHh2reOZJdZwy82LXq/f73YfEuys0f9c63a7/X6/14Owa7/qvlaBs0isfTunen3GJSh2un0rx3bvVN3psnHWiHVHjRkQrAcQSoGNYFer7nyZOEvEumrWUTvFKSVgw0SvM0OuM0KspRWDoDcjaCkTdvrbuld2zoRZPAPEMpHqMCGnGNb6q5p3Hz9d9aikxqIT60Utp7YvlcEphu7hmVNcC00s7exv/WK5pCJYO1Lb8mLVI5QOi0ssHau2KyKVhVxbVY9TIiwosXQTwJLNnwk7illcSG4tIrGGHYVUh7HjCcWwITv0i8etxSOWagL7VfNIhx050rVg/taCEWtfYdVG1QyyYFNq6yIl3CwUsWTParViXx2AI7HFKwuTbLNAxJIzYOqsq3hIeuulqscxDhaFWE9LDnst/SoT1sSJ4u4iqK3FINZQZFVvzS3MmuGCOE9svre1CMS6I9Kq/o6VHqJJbPoksfnEEml1WDU9iqArdGVQ9cgWQtOJ9d5G+utmCN5Wk52tZhPrPbwYVusVXQ/FBt+nTmOp1WRifRMvgu2qCREP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">
                </div>
            </div>
        </div>
    </section>
  </body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

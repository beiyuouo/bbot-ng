import re

temp_dict = {}
lower2original = {}


def format_list(data) -> str:
    msg = ""
    itr = 0
    temp_dict.clear()

    for item in data['status']:
        itr += 1
        msg += f" [{itr}] {item[6:-5]} -> {data['status'][item]}\n"
        temp_dict[str(itr)] = item[6:-5]
        lower2original[item[6:-5].lower()] = item[6:-5]

    return msg


def get_url_middle(url: str) -> str:
    url = url.replace("www.", "")
    url = url.split('.')[0]
    return url


def get_url_abbr(url: str) -> str:
    url = get_url_middle(url)
    url = url[:min(len(url), 3)]
    return url

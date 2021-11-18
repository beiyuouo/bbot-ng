import re


def format_list(data) -> str:
    msg = ""

    ssr_list = data['info']['ssr']
    msg = "ssr:\n"
    for ssr_url in ssr_list:
        msg += f" {get_url_abbr(ssr_url)} -> {ssr_list[ssr_url]}\n"

    v2_list = data['info']['v2ray']
    msg += "v2ray:\n"
    for v2_url in v2_list:
        msg += f" {get_url_abbr(v2_url)} -> {v2_list[v2_url]}\n"

    return msg


def get_url_middle(url: str) -> str:
    url = url.replace("www.", "")
    url = url.split('.')[0]
    return url


def get_url_abbr(url: str) -> str:
    url = get_url_middle(url)
    url = url[:min(len(url), 3)]
    return url

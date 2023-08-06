from sphinxcli.defaults import LIST_SEPARATOR


def str_to_list(text: str) -> list[str]:
    if LIST_SEPARATOR in text:
        return text.split(LIST_SEPARATOR)

    return [text]

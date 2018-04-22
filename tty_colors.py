"""Colored tty output helpers."""


def _treat_input(text):
    if isinstance(text, str):
        return text

    if isinstance(text, tuple) or isinstance(text, list):
        return " - ".join([str(x) for x in text])

    return str(text)


def success(*text, bold=False):
    return _b1(_treat_input(text))


def warning(text, bold=False):
    return _w1(_treat_input(text))


def danger(*text, bold=False):
    return _d1(_treat_input(text))


def neutral_bland(text, bold=False):
    return _n1(_treat_input(text))


def _b1(ss):
    return "\033[1m\033[96m%s\033[0m" % (ss)


def _w1(ss):
    return "\033[1m\033[93m%s\033[0m" % (ss)


def _d1(ss):
    return "\033[1m\033[91m%s\033[0m" % (ss)


def _n1(ss):
    return "\033[1m\033[92m%s\033[0m" % (ss)

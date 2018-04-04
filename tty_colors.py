def success(text, bold=False):
    return text


def warning(text, bold=False):
    return text


def neutral_bland(text, bold=False):
    return text


def _b1(ss):
    return "\033[1m\033[96m%s\033[0m --" % (ss)


def _w1(ss):
    return "\033[1m\033[93m%s\033[0m --" % (ss)


def _d1(ss):
    return "\033[1m\033[91m%s\033[0m --" % (ss)


def _n1(ss):
    return "\033[1m\033[92m%s\033[0m --" % (ss)

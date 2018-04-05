import os
import json
from datetime import datetime

BASE_ST = ".data"


def check_and_config(imp="wiki"):
    tm = datetime.now().strftime("%m%dT%H%M%S")
    imp_st = os.path.join(BASE_ST, imp)
    partials_st = os.path.join(imp_st, "partials")
    raws_st = os.path.join(imp_st, "raws")

    if not os.path.isdir(imp_st):
        os.mkdir(imp_st)
        os.mkdir(partials_st)
        os.mkdir(raws_st)

    run_st = os.path.join(partials_st, tm)
    if not os.path.isdir(run_st):
        os.mkdir(run_st)

    return raws_st, run_st


def _prepare_rfilename(raws_path, title):
    rfilename = "%s.json" % (title.replace("/", "_"))
    rfilename = os.path.join(raws_path, rfilename)
    if len(rfilename) > 256:
        rfilename = "%s.json" % rfilename.split("''")[0]

    return rfilename


def fetch_from_raws(raws_path, title):
    rfilename = _prepare_rfilename(raws_path, title)

    if not os.path.isfile(rfilename):
        return None

    fh = open(rfilename, "r")
    text = fh.read()
    fh.close()

    return json.loads(text)


def store_raw(raws_path, title, content):
    rfilename = _prepare_rfilename(raws_path, title)
    fh = open(rfilename, "w")
    fh.write(content)
    fh.flush()
    fh.close()


def store_partial(partials_path, title, content):
    rfilename = _prepare_rfilename(partials_path, title)
    fh = open(rfilename, "w")
    fh.write(content)
    fh.flush()
    fh.close()

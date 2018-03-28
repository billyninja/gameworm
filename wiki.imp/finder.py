import json
import requests
from SERIES_DB import WIKIPEDIA_SERIES_DB

# GOLDMINE!!!

print("TODO-MINE: https://en.wikipedia.org/wiki/Lists_of_video_games")
print("TODO-MINE: https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions|extracts&rvprop=content&exintro&explaintext&titles=Lists_of_video_games")

print(len(WIKIPEDIA_SERIES_DB))


BASE_URL = "https://en.wikipedia.org/w/api.php?format=json&action=query"
BASE_PARAMS = "&prop=revisions&rvprop=content&rvsection=0&titles=%s"
BASE_FETCH_URL = "%s%s" % (BASE_URL, BASE_PARAMS)


def fetch(titles):
    furl = BASE_FETCH_URL % (titles)
    print(furl)
    return json.loads(requests.get(furl).text)


def parse_results(res):
    hit = False
    redir = set()
    for pid, v in res["query"]["pages"].items():
        if int(pid) < 0:
            continue
        elif "#REDIRECT" in v["revisions"][0]['*'] or "#redirect" in v["revisions"][0]['*']:
            redir.add(v["revisions"][0]['*'].split("[[", 1)[1].split("]]")[0])

        infobox_spl = v["revisions"][0]['*'].split("{{Infobox", 1)
        if len(infobox_spl) == 1:
            continue

        info_comps = infobox_spl[1].split("\n|")
        for ic in info_comps:
            if "video game" in ic.lower():
                hit = True
            if "=" in ic:
                field, values = ic.strip().split("=", 1)
                vals = [x.strip().rstrip(",") for x in values.lower().replace("<br />", "<br/>").replace("<br>", "<br/>").split("<br/>")]
                print(field.strip(), ", ".join(vals))
            else:
                print(">> ", ic.strip())

    return hit, redir


def fetch_and_parse(titles):
    resp = fetch(titles)
    return parse_results(resp)


def wiki_normalize(title):
    return title


def generate_attemps(title):
    title = wiki_normalize(title)
    shortned = set()
    shortned.add(title.split(" - ")[0])
    shortned.add(title.split(":")[0])
    shortned.add(title.split(":")[0].split(" - ")[0])
    pre_finals = sorted(list(set([title] + list(shortned))), key=lambda x: len(x))
    for idx, fn in enumerate(pre_finals):
        if len(fn) < 32 and (len(fn.split(" ")) < 4):
            fn += " (video game)"
            pre_finals = pre_finals[:idx] + [fn] + pre_finals[idx:]

    return pre_finals


class HS:
    MISS = 0
    HIT = 1
    AMBIG = 2


if __name__ == "__main__":

    titles = ["The Walking Dead: Season Two - A Telltale Games Series",
              "The Walking Dead: Season Two Episode 5 - No Going Back",
              "Metal Gear Solid 4: Guns of The Patriots",
              "Lure of the Temptress",
              "Burst Error: Eve the First",
              "Sol Moonarage",   # super obscure, jpn only (dont have an article)
              "1942",
              "Hello Kitty Collection: Miracle Fashion Maker",
              "robocop",
              "Enchanter",
              "Universe",
              "Commando"]

    for tt in titles:
        titles = "|".join(generate_attemps(tt))
        hit, redir = fetch_and_parse(titles)
        if not hit and redir:
            titles = "|".join(list(redir))
            hit, redir = fetch_and_parse(titles)
        print(tt, hit)

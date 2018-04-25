"""structured organization of world release regions."""
import re

REGION_TREE = {
    "WW": {
        "aliases": ["worldwide", "world-wide", "int", "global"],
        "sub": {
            "NA": {
                "aliases": ["north-america"],
                "sub": {
                    "US": {"aliases": ["united-states", "usa"], "sub": {}},
                    "CA": {"aliases": ["canada", "can"], "sub": {}},
                }
            },
            "SA": {
                "aliases": ["south-america"],
                "sub": {
                    "BR": {"aliases": ["bra", "brasil", "brazil"], "sub": {}},
                    "AR": {"aliases": ["arg", "argentina"], "sub": {}},
                    "MX": {"aliases": ["mex", "mexico"], "sub": {}},
                }
            },
            "EU": {
                "aliases": ["europe", "pal", "eur"],
                "sub": {
                    "GR": {"aliases": ["germany", "ger", "de", "deu"], "sub": {}},
                    "PL": {"aliases": ["pol", "poland"], "sub": {}},
                    "FR": {"aliases": ["fra", "france"], "sub": {}},
                    "UK": {"aliases": ["gb", "united-kingdom", "great-britain", "england", "en"], "sub": {}},
                    "ES": {"aliases": ["spain", "esp"], "sub": {}},
                    "IT": {"aliases": ["ita", "italy"], "sub": {}},
                    "CZ": {"aliases": ["cze", "czech-republic"], "sub": {}},
                    "AS": {"aliases": ["austria", "aut"], "sub": {}},
                    "RS": {"aliases": ["russia", "rus"], "sub": {}},
                    "FI": {"aliases": ["fin", "finland"], "sub": {}},
                    "PT": {"aliases": ["prt", "portugal"], "sub": {}},
                    "IL": {"aliases": ["isr", "israel"], "sub": {}},
                    "SE": {"aliases": ["swe", "sweden"], "sub": {}},
                }
            },
            "AS": {
                "aliases": ["asia", "sea", "australasia"],
                "sub": {
                    "TK": {"aliases": ["tur", "turkey"], "sub": {}},
                    "JP": {"aliases": ["japan", "jpn"], "sub": {}},
                    "KR": {"aliases": ["south-korea", "korea", "kor", "ko", "sk", "rok"], "sub": {}},
                    "CH": {"aliases": ["chn", "china"], "sub": {}},
                    "HK": {"aliases": ["hkg", "hong-kong"], "sub": {}},
                    "TL": {"aliases": ["thailand", "tha"], "sub": {}},
                    "TW": {"aliases": ["taiwan", "twn"], "sub": {}},
                    "IN": {"aliases": ["ind", "india"], "sub": {}},
                    "KP": {"aliases": ["prk", "north-korea"], "sub": {}},
                }
            },
            "OC": {
                "aliases": ["oceania", "australasia"],
                "sub": {
                    "AU": {"aliases": ["aus", "australia"], "sub": {}},
                    "NZ": {"aliases": ["nzl", "new zealand"], "sub": {}},
                }
            },
            "AF": {
                "aliases": ["africa"],
                "sub": {
                    "SA": {"aliases": ["south-africa"], "sub": {}},
                }
            }
        }
    },
    "sub": {},
    "aliases": [],
}


slug = re.compile("\s|_")


def search_region_tree(inp, curr_key=None, curr_node=None):
    inp_u = inp.upper()
    inp_l = slug.sub("-", inp).lower()

    if not curr_node or not curr_key:
        curr_key = "WW"
        curr_node = REGION_TREE["WW"]

    if inp_u == curr_key:
        return curr_key

    if inp_l in curr_node.get("aliases", []):
        return curr_key

    for k, sb in curr_node["sub"].items():
        out = search_region_tree(inp, k, sb)
        if out:
            return out

    return None

if __name__ == "__main__":
    print(search_region_tree("BRA"))
    print(search_region_tree("united STATES"))
    print(search_region_tree("united KINGDOM"))

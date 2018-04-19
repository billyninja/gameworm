"""Core methods for find-data extraction/parsing."""
import re
from datetime import date

markup_rm = re.compile(",\s\[\[[0-9]{4}\sin\svideo\sgaming\||titlestyle")
markup_sep1 = re.compile("({{collapsible list\s?\|\s?(title=\s?[\w+\s,]+)?|<[^<]+?>|{{\s?[A-Za-z]+\s?\||'''|''|\]\]|}}|\s?=\s?[a-z\-\s]+:.+(\;|\|))", flags=re.I)
markup_sep2 = re.compile("\s?§\s?\|?§?\s?")
remove_date_commas = re.compile(
    "(\s[0-9]{1,2})?(Jan(uary)?|Feb(ruary)?|Mar(ch)|Apr(il)|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember))(\s[0-9]{1,2})?(?P<comma>\s?\,)"
)
special_date_pattern = re.compile(
    "((start|release)\s?date|dts|§)\|?([0-9]{4})\|([0-9]{1,2})\|([0-9]{1,2})")


def _repl_dt_comma(mo):
    if mo.group("comma"):
        span = mo.span()
        return mo.string[span[0]:span[1] - 1]


def _repl_special_dt(mo):
    span = mo.span()
    parts = mo.string[span[0] + 1:span[1] - 1].split("|")
    dt = date(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) >= 2 else 1)

    return dt.strftime("|%B %d %Y")


def prenorm(inp):
    inp = markup_rm.sub(' ', inp)
    inp = markup_sep1.sub("§", inp)
    inp = markup_sep2.sub("§", inp)
    inp = markup_sep2.sub("§", inp)
    inp = inp.strip("§")
    inp = remove_date_commas.sub(_repl_dt_comma, inp)
    inp = special_date_pattern.sub(_repl_special_dt, inp)

    return inp

'§PlayStation 2§JP|§2015|08|24§|NA|September 19, 2006|EU|February 9, 2007|AUS|February 14, 2007§Wii§NA|April 15, 2008|AUS|June 12, 2008|EU|June 13, 2008|JP|October 15, 2009§PlayStation 3§NA|October 30, 2012|PAL|October 31, 2012|JP|November 1, 2012§Microsoft Windows§WW|December 12, 2017|JP|December 13, 2017§PlayStation 4, Xbox One§WW|December 12, 2017|JP|December 21, 2017§Nintendo Switch§WW|mid-2018§'

if __name__ == "__main__":
    inp = "{{collapsible list|title=March 12, [[2009 in video gaming|2009]]|titlestyle=font-weight:normal;font-size:12px;background:transparent;text-align:left|\n'''Microsoft Windows'''<br>March 12, [[2009 in video gaming|2009]] '''Nintendo DS'''<br>April 4, 2011\n}}"
    inp = prenorm(inp)
    print(inp)

#!/usr/bin/python
from bs4 import BeautifulSoup
import re
import urllib.request

month_name = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]


def parse_ul_tree(el, top_level=True):
    """
    Parse events of a specific theme at a specific date.
    :param el: unordered list containing themes or individual events.
    :return: a list of all links in that element.
    """
    all_links = []
    for ll in el.find_all("li", recursive=False):
        # Each line contains also subordinate ULs,
        # but up to \n is the current line text.
        tt = ll.text.split("\n")[0]
        # remove news agency in parentheses if present (.*? didn't work)
        tt = re.sub(r"\([^(]*\)$", "", tt, count=1)
        links = [[lnks["href"], lnks.text] for lnks
                 in ll.find_all("a", recursive=False)
                 if lnks["href"][:6] == "/wiki/"]
        all_links.extend(links)
        for uu in ll.find_all("ul", recursive=False):
            all_links.extend(parse_ul_tree(uu, False))
    return all_links

def parse_month(month=0, year=0):
    """
    Parse a description of events in one month of Wikipedia events.
    It can also be used to parse the current events.
    :return: nothing
    """
    base = "https://en.wikipedia.org/wiki/Portal:Current_events"
    url = base
    if year != 0:
        url = base + month_name[month-1] + '_' + "{0}".format(year)
    with urllib.request.urlopen(url) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        # The div with region role is deep in the body hierarchy.
        # It represents one day.
        for d in soup.find_all("div", role="region"):
            category = ""
            if "id" in d.attrs:
                year, month, day = d["id"].split("_")
                print("{0} {1} {2}".format(day, month, year))
            for t1 in d.find_all(recursive=False):
                if (t1.name == "div" and "class" in t1.attrs
                        and "description" in t1["class"]):
                    for t in t1.find_all(recursive=False):
                        if t.name == "p":
                            # An opening paragraph contains category name
                            category = t.b.contents[0]
                            print(category)
                        if t.name == "ul":
                            # The following unordered list contains events
                            # grouped in themes.
                            # Each theme is one line in the top-level list
                            # Parse those events
                            events = parse_ul_tree(t)
                            print(events)


if (__name__ == "__main__"):
    import sys
    year = 0
    month = 0
    if len(sys.argv) == 3:
        year = sys.argv[1]
        month = sys.argv[2]
    parse_month(month, year)

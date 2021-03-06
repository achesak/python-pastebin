# -*- coding: utf-8 -*-

# python-pastebin
# Wrapper of the pastebin.com API for the Python language.
# Released under the MIT open source license.

# This file adds extra features not supported by the pastebin.com
# API, such as listing recently created pastes, getting info about a
# particular paste, creating a paste from a file, and renaming and
# merging pastes.

# This module also requires BeautifulSoup 4 to work.


# Import urlopen and urlencode.
# Try both for Python 2 and Python 3 compatability.
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import urlopen, URLError, HTTPError
    from urllib import urlencode
# Import BeautifulSoup for parsing HTML.
from bs4 import BeautifulSoup
# Import the main API file for extending its functions.
import pastebin_api


def create_paste_from_file(devkey, filename, name = "", format_ = "", private = 0, expire = "", userkey = ""):
    """Creates a new paste from a file."""
    
    f = open(filename, "r")
    data = f.read()
    f.close()
    
    data = pastebin_api.create_paste(devkey, data, name, format_, private, expire, userkey)
    
    return data


def get_paste_to_file(pastekey, filename):
    """Gets a paste and writes it to a file."""
    
    data = pastebin_api.get_paste(pastekey)
    
    f = open(filename, "w")
    f.write(data)
    f.close()
    
    return data


def list_recent_pastes():
    """Gets a list of recently created pastes."""
    
    response = urlopen("http://pastebin.com/archive")
    html = response.read()
    response.close()
    
    parser = BeautifulSoup(html)
    data = []
        
    # Structure: Body > Table > TR > data stored in TD
    rows = parser.find("body").find("table", {"class": "maintable"}).find_all("tr")
    for i in rows:
        if len(i.find_all("th")) > 0:
            continue
        td = i.find_all("td")
        link = td[0].a
        row = {
            "name": link.string,
            "key": link["href"][1:],
            "format": td[2].a.string,
            "time_created": td[1].string,
            "link": "http://pastebin.com" + link["href"]
        }
        data.append(row)
    
    return data

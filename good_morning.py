#!/usr/bin/python
import os
import json
import time
import requests
from bs4 import BeautifulSoup


def get_dilbert_comic(date="2016-01-01"):
    """
    Fetches Dilbert comic's image URL & topic for the given date
    (Future dates get redirected to latest date's comic, automatically)
    Input -
        date : YYYY-MM-DD format
    Output -
        {
            success : True/False,
            date    : string,
            url     : string,
            title   : string,
            image   : string,
        }
    """
    url = "http://dilbert.com/strip/{0}".format(date)
    comic = {
        'success': False,
        'date': date,
        'url': url,
        'title': '',
        'image': '',
    }

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            # title is empty at times (e.g. 2016-03-20 comic)
            comic['title'] = soup.find(attrs={"property":"og:title"})['content']
            comic['image'] = soup.find(attrs={"property":"og:image"})['content']
            comic['success'] = True
        except (AttributeError, KeyError):
            pass
    return comic


if __name__ == '__main__':
    comic = get_dilbert_comic(date=time.strftime('%Y-%m-%d'))

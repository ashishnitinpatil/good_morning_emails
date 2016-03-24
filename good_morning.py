#!/usr/bin/python
import os
import json
import time
import requests
from utilities import *
from bs4 import BeautifulSoup
from unidecode import unidecode
from pprint import pprint, pformat


# suppress dirty SSL warnings when using requests
try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass


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
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            # title is empty at times (e.g. 2016-03-20 comic)
            comic['title'] = unidecode(soup.find(attrs={"property":"og:title"})['content'])
            comic['image'] = soup.find(attrs={"property":"og:image"})['content']
            comic['success'] = True
        except (AttributeError, KeyError):
            pass
    return comic


def get_QOTD():
    """
    Fetches QOTD from the REST API of Quotes.rest
    Output -
        {
            success    : True/False,
            date       : string,
            quote      : string,
            author     : string,
            background : string,
        }
    """
    qotd = {
        'success' : False,
        'date' : '',
        'quote' : '',
        'author' : '',
        'background' : '',
    }
    response = requests.get("http://quotes.rest/qod.json", verify=False)
    print response.status_code, response.content
    if response.status_code == 200:
        try:
            json_response = response.json()['contents']['quotes'][0]
            for detail in ['date', 'quote', 'author', 'background']:
                qotd[detail] = unidecode(json_response[detail].strip())
            qotd['success'] = True
        except (AttributeError, KeyError, IndexError):
            pass
    return qotd


def generate_qotd_html(qotd={}):
    """Generates part HTML for the qotd supplied"""
    return """
    <h3>Quote of the day -</h3>
    <blockquote>
        <p style="font:Helvetica;font-size:16px;">{0}</p>
        <footer>- <cite>{1}</cite></footer>
    <!-- Attribution to "They Said So" API for the quotes -->
    <span style="z-index:50;font-size:0.9em;"><img src="https://theysaidso.com/branding/theysaidso.png" height="20" width="20" alt="theysaidso.com"/>
        <a href="https://theysaidso.com" title="Powered by quotes from theysaidso.com" style="color: #9fcc25; margin-left: 4px; vertical-align: middle;">theysaidso.com</a>
    </span>
    </blockquote>
    """.format(qotd['quote'], qotd['author'])


def generate_comic_html(comic={}):
    """Generates part HTML for the qotd supplied"""
    return """
    <h3>Dilbert by Scott Adams -</h3>
    <a href="{0}"><img alt="{1} - Dilbert by Scott Adams" src="{2}"></a>
    """.format(comic['url'], comic['title'], comic['image'])


def get_email_html(qotd_html="", comic_html=""):
    """
    Generates beautiful HTML from the qotd & comic supplied
    Also includes some default content like attribution, etc.
    """
    return """<html>
    <head></head>
    <body>
        <p>Good morning! Here's your daily dose of inspiration & some humour :)</p>
        {0}<br>
        {1}<br><br>
        <p>Cheers,<br>Team Finomena</p>
    </body>
    </html>""".format(qotd_html, comic_html)


if __name__ == '__main__':
    print timestamp()
    comic = get_dilbert_comic(date=time.strftime('%Y-%m-%d'))
    pprint(comic)
    comic_html = generate_comic_html(comic) if comic['success'] else ""
    qotd  = get_QOTD()
    pprint(qotd)
    qotd_html = generate_qotd_html(qotd) if qotd['success'] else ""
    if comic['success'] or qotd['success']:
        send_email(
            subject='Good morning!',
            html=get_email_html(qotd_html, comic_html),
            from_id='inspire@finomena.com',
            recipients=['ashish.patil@8finatics.com',],
            debug=True,
        )
    else:
        send_email(
            subject='Good morning email FAILED!',
            html="QOTD - {0}<br><br>Comic - {1}".format(pformat(qotd),pformat(comic)),
            from_id='inspire@finomena.com',
            recipients=['ashish.patil@8finatics.com',],
            debug=True,
        )


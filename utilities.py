#!/usr/bin/python
import os
import json
import time
import requests


def timestamp():
    """Returns YYYY-MM-DD HH:MM:SS formatted UTC timestamp string"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


def get_public_ip():
    """Fetch public IP of hosting server with the help of httpbin API"""
    return json.loads(requests.get('http://httpbin.org/ip').text)['origin']


def send_email(subject="", html="", from_id="", recipients=[], debug=False):
    """Send an email with the given html body & subject line with the help of MAILGUN API"""
    sandbox = os.environ.get('MAILGUN_SANDBOX', '')
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)
    request = requests.post(
        request_url,
        verify=False,
        auth=('api', os.environ.get('MAILGUN_KEY', '')),
        data={
            'from': from_id,
            'to': recipients,
            'subject': subject,
            'html': html,
        },
    )
    if debug:
        print 'Status: {0}'.format(request.status_code)
        print 'Body:   {0}'.format(request.text)
    return True if int(request.status_code) == 200 else False


__all__ = ['timestamp', 'get_public_ip', 'send_email']

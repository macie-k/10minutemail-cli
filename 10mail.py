from unicodedata import ucnhash_CAPI
from urllib import response
import pyperclip
import string
import random
import requests
import time
import os

from argparse import ArgumentParser
from colorama import Fore
from colorama import Style

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
endpoint = 'https://dropmail.me/api/graphql/'
token = ''

def start(interval):
    request = queried_request(session_query())
    if (not request.ok):
        raise Exception('Could not complete request: #' + str(request.status_code))
    
    response = request.json()
    session = response['data']['introduceSession']
    session_id = session['id']

    email = session['addresses'][0]['address']
    pyperclip.copy(email)

    clear()
    success('Your email: ' + email)
    success('Copied to clipboard\n')
    success('Refreshing inbox...')

    while(True):
        mailbox = queried_request(mailbox_query(session_id)).json()
        mails = mailbox['data']['session']['mails']
        if (mails):
            success(f'Mail received:')
            print('-----------------------\n')
            print(mails[0]['text'])
            return
        else:
            time.sleep(interval)

# query for introduction session
def session_query():
    return 'mutation {introduceSession {id, addresses{address}}}'

# query for getting mailbox content
def mailbox_query(id):
    return 'query ($id: ID!){session(id:$id) {mails{downloadUrl, text}}}&variables={"id":"' + id + '"}'

# generation random token
def get_token(chars):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=chars))

def queried_request(body):
    query = '?query=' + body
    return requests.get(endpoint + token + query)

def success(str, as_input=False):
    output = f'{Fore.GREEN}[OK]{Style.RESET_ALL} {str}'
    if as_input:
        input(output)
    else:
        print(output)

def error(str, e='', as_input=False):
    output = f'{Fore.RED}[ERROR]{Style.RESET_ALL} {str}: {e}'
    if as_input:
        input(output)
    else:
        print(output)

parser = ArgumentParser()
parser.add_argument('-i', '--interval', metavar='interval', type=int, nargs=1, help='Refreshing interval (s)')
args = parser.parse_args()

if __name__ == '__main__':
    print(token)
    try:
        token = get_token(8)
        interval = 3
        if(args.interval):
            interval = args.interval[0]

        start(interval)
    except Exception as e:
        error('Exception occured', e, True)
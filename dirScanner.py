#!/bin/env python3
#-*- coding: utf-8 -*-

import concurrent.futures
import argparse
import requests
import logging
import datetime
import time

SESSION = requests.Session()

def banner():
    print('------------------------------------------------------')
    print(f"""{COLOR.INFO}
     _  _      _____
     | (_)    / ____|
   __| |_ _ _| (___   ___ __ _ _ __  _ __   ___ _ __
  / _` | | '__\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | (_| | | |  ____) | (_| (_| | | | | | | |  __/ |
  \__,_|_|_| |_____/ \___\__,_|_| |_|_| |_|\___|_|
                                                   {COLOR.END}""")
    print('------------------------------------------------------')

class COLOR:
    FAIL = '\x1b[1;31m'
    FOUND = '\x1b[1;32m'
    FORB = '\x1b[1;33m'
    INFO = '\x1b[1;34m'
    END =  '\x1b[0m'

def get_date_time(fmt):
    return datetime.datetime.fromtimestamp(time.time()).strftime(fmt)

def get_file_logger(log_filename=None):

    def _get_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    logger = _get_logger()
    filename = log_filename if log_filename else get_date_time('%Y-%m-%d')+'.log'
    fh = logging.FileHandler(filename)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(fh)
    return logger

def make_request(url, proxy=None):
    global SESSION
    r = SESSION.get(url, allow_redirects=False, proxies={'http': proxy, 'https': proxy})
    return r.status_code

def load_dict(file_name):
    with open(file_name) as f:
        for line in iter(f.readline, ''):
            yield line.strip('\n')

def scan(url, wordlist, proxy=None, log_filename=None, verbose_mode=False, timeout=2):
    print(f'{COLOR.INFO} Starting at {get_date_time("%Y-%m-%d %H:%M:%S")} {COLOR.END}')

    logger = get_file_logger(log_filename)
    url = url if url.endswith('/') else url+'/'

    with concurrent.futures.ProcessPoolExecutor() as executor:
        jobs = {executor.submit(make_request, url+line, proxy=proxy): line for line in load_dict(wordlist)}
        for future in concurrent.futures.as_completed(jobs):
            URL = url+jobs[future]
            try:
                status_code = future.result(timeout=timeout)

            except concurrent.futures.TimeoutError:
                print(f'{COLOR.FAIL} [x]Timeout: {URL} {COLOR.END}')

            message = f'[{status_code}] => {URL}'
            if verbose_mode:
                print(f'{COLOR.INFO} [*]{message} {COLOR.END}')
            elif status_code == 404:
                continue
            elif status_code == 403:
                print(f'{COLOR.FORB} [!]{message} {COLOR.END}')
            else:
                print(f'{COLOR.FOUND} [+]{message} {COLOR.END}')

            logger.info(message)

    print(f"{COLOR.INFO} Total requests: {len(jobs)} {COLOR.END}")

def main():
    banner()
    parser = argparse.ArgumentParser(prog="dirScanner", description="Python3.6+ is NEEDED, scan log will store in current direcotry named by date time by default")
    parser.add_argument("url", help="the target you want to scan")
    parser.add_argument("wordlist", help="the dictionary you want to use in this action")
    parser.add_argument("-p", "--proxy", help="proxy address like 'socks5://127.0.0.1:8080'")
    parser.add_argument("-o", "--output", help="where the log you wnat to store")
    parser.add_argument("-v", "--verbose", help="enable verbose mode means show every single request in the action", action='store_true')
    parser.add_argument("-t", "--timeout", help="set timeout value, default is 2 seconds", type=int)
    args = parser.parse_args()

    params = {'url': args.url, 'wordlist': args.wordlist, 'proxy': args.proxy, 'log_filename': args.output, 'verbose_mode': args.verbose}

    start = time.time()

    scan(**params)

    print(f"{COLOR.INFO} Elapsed time: {time.time() - start} seconds {COLOR.END}")

if __name__ == '__main__':
    main()

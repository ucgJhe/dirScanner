### Introduction

use channel concept with multi-thread

### Setup

`git clone https://github.com/ucgJhe/dirScanner`

`pip install -r requirements`

### Usage

`dirScanner.py <URL> <WORDLIST> -p <PROXY> -o <path_to_file> -t <timeout> -n <threads>`

1. default timeout is 2 seconds

2. default threads value is double cpu counts

3. log will be stored in current directory automatically by default.

**Example:**

`dirScanner.py http://localhost/ DICT.txt -p socks5://127.0.0.1:8080 -o log -t 3 -n 20`

### Requirements

1. python version 3.6+
    - requests
    - requests[socks]

2. your own wordlist

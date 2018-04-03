### Introduction

Use concurrent.futures instead of threading to speed up.

### Usage

`dirScanner.py <URL> <WORDLIST> -p <PROXY> -o <path_to_file> -t <timeout> -v`

1. default timeout is 2 seconds

2. log will be stored in current directory automatically by default.

**Example:**
`dirScanner.py http://localhost/ DICT.txt -p socks5://127.0.0.1:8080 -o log -t 3 -v`

### Requirements

1. python version 3.6+
    - requests
    - requests[socks]

2. your own wordlist

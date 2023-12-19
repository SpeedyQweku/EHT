#!/usr/bin/python3

import requests
from sys import argv


def main(domain):
    try:
        url = f"https://web.archive.org/cdx/search/cdx?url={domain}&fl=original&collapse=urlkey"
        response = requests.get(url)
        with open(f"{domain}.txt", "+a") as w:
            for urls in response.text:
                w.write(urls)
    except requests.exceptions.ConnectionError:
        pass


if __name__ == "__main__":
    file_name = argv[1]
    with open(file_name, 'r') as f:
        for domain in f.readlines():
            try:
                main(domain.strip())
                print(f"[>] {domain} - Successful")
            except requests.exceptions.ConnectTimeout:
                print(f"[!] {domain} - Failed, Retry...")
                main(domain.strip())
                print(f"[>] {domain} - Successful")
#!/usr/bin/python3

import httpx
import asyncio
import argparse
from termcolor import colored
from bs4 import BeautifulSoup


async def swagger(url: str):
    swagger_url = []
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            title_tag = soup.title
            if title_tag:
                title = title_tag.text
                print(title)
            if "Swagger" in title or "swagger" in title:
                print(colored("\t[+] Swagger UI Detected At : " + url, "blue"))
                swagger_url.append(url)
            else:
                print(colored("[!] No Swagger UI Detected At : " + url, "red"))
            if "openapi: 3." in response.text or "swagger: 2." in response.text or "Swagger UI" in response.text:
                print(colored("\t[+] Swagger UI Detected At : " + url, "blue"))
                swagger_url.append(url)
            return swagger_url
        else:
            print(colored(f"[!] Status code : {response.status_code} at" + url, "red"))
            pass


def openfile(file="swagger-list.txt"):
    try:
        with open(file, "r") as para:
            for lines in para.readlines():
                yield (lines.strip())
    except Exception as err:
        print(colored(err, "red"))
        exit()


def savefile(filename, result):
    try:
        with open(filename, "a") as outfile:
            for line in result:
                outfile.write(line + "\n")
    except Exception:
        pass


def make_request(url, file):
    try:
        content = openfile()
        if url.endswith("/"):
            for line in content:
                result = asyncio.run(swagger(f"{url}{line}"))
                savefile(file, result)
        else:
            for line in content:
                result = asyncio.run(swagger(f"{url}/{line}"))
                savefile(file, result)
    except KeyboardInterrupt:
        print(colored("\n[!] ctrl + c to exit", "red"))
        exit()
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--url", dest="url", help="Url to scan.", type=str)
    group.add_argument("-f", "--file", dest="file", help="File to scan", type=str)
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Save the result to a file",
        required=True,
        type=str,
    )

    arg = parser.parse_args()

    if arg.url and arg.output and not arg.file:
        if arg.url.startswith("http://") or arg.url.startswith("https://"):
            make_request(arg.url, arg.output)
        else:
            print(colored("[-] Url should start with http:// or https://", "red"))
            exit()

    if arg.file and arg.output and not arg.url:
        urls = openfile(arg.file)
        for url in urls:
            if url.startswith("http://") or url.startswith("https://"):
                make_request(url, arg.output)
            else:
                print(colored("[-] Url should start with http:// or https://", "red"))
                exit()

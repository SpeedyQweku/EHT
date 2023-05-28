#!/usr/bin/python3

import requests
import argparse
from time import sleep
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


class Main:
    def __init__(self):
        self.urls = []
        self.data = []
        self.subdomain = [{"subdomain": "", "directroy": []}]
        self.bingUrl: str = "https://www.bing.com/search?&count=100&q="
        self.googleUrl: str = "https://www.google.com/search?num=100&filter=0&q="
        self.dork: str = "site%3A"
        self.headers = {"User-Agent": generate_user_agent()}

    def get_args(self):
        try:
            parser = argparse.ArgumentParser()
            group = parser.add_mutually_exclusive_group()
            group.add_argument(
                "-G",
                "--google",
                dest="google",
                help="Google search",
                action="store_true",
            )
            group.add_argument(
                "-B", "--bing", dest="bing", help="Bing search", action="store_true"
            )
            parser.add_argument(
                "-d", "--domain", dest="domain", help="Domain to search", type=str
            )
            parser.add_argument(
                "-p",
                "--page",
                dest="page",
                help="How many pages to search (optional) ",
                type=int,
            )
            arg = parser.parse_args()
            if arg.google or arg.bing and arg.domain or arg.page:
                if arg.page:
                    for i in range(1, (arg.page + 1)):
                        if arg.google:
                            self.google(i, arg.domain)
                            sleep(2)
                        if arg.bing:
                            self.bing(i, arg.domain)
                            sleep(2)
                    if arg.google:
                        self.google_subdomains(arg.domain)
                    if arg.bing:
                        self.bing_subdomains(arg.domain)
                else:
                    page = 2
                    for i in range(1, page):
                        if arg.google:
                            self.google(i, arg.domain)
                            sleep(2)
                        if arg.bing:
                            self.bing(i, arg.domain)
                            sleep(2)
                    if arg.google:
                        self.google_subdomains(arg.domain)
                    if arg.bing:
                        self.bing_subdomains(arg.domain)
            else:
                parser.error("Use -h/--help for more info.")
        except TypeError:
            parser.error("Use -h/--help for more info.")

    def bing(self, page, domain):
        target = f"{self.bingUrl}{self.dork}{domain}&first={100*(page-1)+1}"
        try:
            response = requests.get(target, headers=self.headers)
            soup = BeautifulSoup(response.text, "lxml")
            result = soup.findAll("li", class_="b_algo")
            for links in result:
                link = links.find("a")
                self.urls.append(link.get("href").split("/"))
        except Exception as err:
            print(err)

    def google(self, page, domain):
        target = f"{self.googleUrl}{self.dork}{domain}&start={20*(page-1)}"
        try:
            response = requests.get(target)
            print(response.text)
            soup = BeautifulSoup(response.text, "lxml")
            result = soup.findAll("div")
            for links in result:
                link = links.find("a")
                try:
                    if link.get("href").startswith("/url?q=https://"):
                        self.urls.append(link.get("href").split("/"))
                except AttributeError:
                    pass
        except Exception as err:
            print(err)

    def bing_subdomains(self, domain):
        for i in range(len(self.urls)):
            if domain in self.urls[i][2]:
                sub = dict(subdomain=self.urls[i][2], directroy=self.urls[i][3])
                self.data.append(sub)
        for i in range(len(self.data)):
            trip = 0
            for n in range(len(self.subdomain)):
                if self.data[i]["subdomain"] == self.subdomain[n]["subdomain"]:
                    trip = 1
                    break
            if trip == 0:
                subdata = {
                    "subdomain": self.data[i]["subdomain"],
                    "directroy": [self.data[i]["directroy"]],
                }
                self.subdomain.append(subdata)
            elif trip == 1:
                self.subdomain[n]["directroy"].append(self.data[i]["directroy"])
        self.subdomain.pop(0)
        self.output_results()

    def google_subdomains(self, domain):
        for i in range(len(self.urls)):
            if domain in self.urls[i][3]:
                sub = dict(subdomain=self.urls[i][3], directroy=self.urls[i][4])
                self.data.append(sub)
        for i in range(len(self.data)):
            trip = 0
            for n in range(len(self.subdomain)):
                if self.data[i]["subdomain"] == self.subdomain[n]["subdomain"]:
                    trip = 1
                    break
            if trip == 0:
                subdata = {
                    "subdomain": self.data[i]["subdomain"],
                    "directroy": [self.data[i]["directroy"]],
                }
                self.subdomain.append(subdata)
            elif trip == 1:
                self.subdomain[n]["directroy"].append(self.data[i]["directroy"])
        self.subdomain.pop(0)
        self.output_results()

    def output_results(self):
        for i in self.subdomain:
            print(f'\033[1;31m{i["subdomain"]}')
            directroy = set(i["directroy"])
            for dire in directroy:
                print(f"\t\033[1;34m -- {dire}")


if __name__ == "__main__":
    run = Main()
    run.get_args()

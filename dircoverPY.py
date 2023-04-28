#!/usr/bin/python

import requests
import sys
from time import sleep
from bs4 import BeautifulSoup


class Main:
    def __init__(self):
        self.urls = []
        self.data = []
        self.subdomain = [{"subdomain": "", "directroy": []}]
        self.bingUrl: str = "https://www.bing.com/search?&count=100&q="
        self.googleUrl: str = "https://www.google.com/search?num=100&filter=0&q="
        self.dork: str = "site%3A"

    def bing(self, page, domain):
        target = f"{self.bingUrl}{self.dork}{domain}&first={100*(page-1)+1}"
        try:
            response = requests.get(target)
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
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(
                "dircoverPY.py\n\tUsage: python3 dircoverPY.py -h\
                \n\tUsage: python3 dircoverPY.py -G -d google.com",
                "\n\nOptions:",
            )
            print(
                "\t-G\t\t Using Google Search Engine\n",
                "\t-B\t\t Using Bing Search Engine",
            )
            print("\t-d\t\t Domain\n", "\t-p\t\t Number of pages")
        elif (
            sys.argv[1] == "-G"
            or sys.argv[1] == "-B"
            and sys.argv[2] == "-d"
            or sys.argv[4]
        ):
            try:
                if sys.argv[4]:
                    for i in range(1, int(sys.argv[5])):
                        if sys.argv[1] == "-G":
                            run.google(i, sys.argv[3])
                            run.google_subdomains(sys.argv[3])
                            sleep(2)
                        if sys.argv[1] == "-B":
                            run.bing(i, sys.argv[3])
                            run.bing_subdomains(sys.argv[3])
                            sleep(2)
            except IndexError:
                page = 2
                for i in range(1, page):
                    if sys.argv[1] == "-G":
                        run.google(i, sys.argv[3])
                        run.google_subdomains(sys.argv[3])
                        sleep(2)
                    if sys.argv[1] == "-B":
                        run.bing(i, sys.argv[3])
                        run.bing_subdomains(sys.argv[3])
                        sleep(2)
    except IndexError:
        print("dircoverPY.py\n\tUsage: python3 dircoverPY.py -h")
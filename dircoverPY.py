#!/usr/bin/python

import requests
import optparse
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

    def get_args(self):
        try:
            parser = optparse.OptionParser()
            parser.add_option(
                "-G", "--google", dest="google", help="Google search", action="store_true"
            )
            parser.add_option(
                "-B", "--bing", dest="bing", help="Bing search", action="store_true"
            )
            parser.add_option("-d", "--domain", dest="domain", help="Domain to search")
            parser.add_option(
                "-p",
                "--page",
                dest="page",
                help="How many pages to search [ Default = 1 page ]",
                type=int,
            )
            (options, _) = parser.parse_args()

            if options.google or options.bing and options.domain or options.page:
                if options.page:
                    for i in range(1, (options.page + 1)):
                        if options.google:
                            self.google(i, options.domain)
                            sleep(2)
                        if options.bing:
                            self.bing(i, options.domain)
                            sleep(2)
                    if options.google:
                        self.google_subdomains(options.domain)
                    if options.bing:
                        self.bing_subdomains(options.domain)
                else:
                    page = 2
                    for i in range(1, page):
                        if options.google:
                            self.google(i, options.domain)
                            sleep(2)
                        if options.bing:
                            self.bing(i, options.domain)
                            sleep(2)
                    if options.google:
                        self.google_subdomains(options.domain)
                    if options.bing:
                        self.bing_subdomains(options.domain)
            else:
                parser.error("Use -h/--help for more info.")
        except TypeError:
            parser.error("Use -h/--help for more info.")

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
    run.get_args()

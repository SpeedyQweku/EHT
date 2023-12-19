#!/usr/bin/python3

import requests
import argparse
from os import system
from bs4 import BeautifulSoup


class GsubFinder:
    def rapiddns(self, domain: str):
        url = f"https://rapiddns.io/subdomain/{domain}?full=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("tbody")
        if table is not None:
            rows = table.find_all("tr")
            for row in rows[1:]:
                subdomain = row.find("td").text
                yield subdomain

    def jldc(self, domain: str):
        url = f"https://jldc.me/anubis/subdomains/{domain}"
        response = requests.get(url)
        jsondate = response.json()
        for subdomain in jsondate:
            yield subdomain

    def crtsh(self, domain: str):
        url = f"https://crt.sh/?q={domain}&output=json"
        response = requests.get(url)
        for entry in response.json():
            yield entry["name_value"]

    def securitytrails(self, domain: str, apikey: str):
        url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
        headers = {"accept": "application/json", "apikey": f"{apikey}"}
        response = requests.get(url, headers=headers)
        for subdomain in response.json()["subdomains"]:
            yield f"{subdomain}.{domain}"

    def saving_results(self, domain: str, filename: str, apikey=None):
        with open("data.txt", "a+") as file:
            con = 4
            try:
                jldc_results = self.jldc(domain)
                for value in jldc_results:
                    file.write(value + "\n")
            except requests.RequestException:
                print("\t\033[1;31m[!] Could not get results from jldc.me")
                con -= 1
                pass

            try:
                rapiddns_results = self.rapiddns(domain)
                for value in rapiddns_results:
                    file.write(value + "\n")
            except requests.RequestException:
                print("\t\033[1;31m[!] Could not get results from rapiddns.io")
                con -= 1
                pass

            try:
                crtsh_results = self.crtsh(domain)
                for value in crtsh_results:
                    file.write(value + "\n")
            except requests.RequestException:
                print("\t\033[1;31m[!] Could not get results from crt.sh")
                con -= 1
                pass

            try:
                if apikey is not None:
                    securitytrails_results = self.securitytrails(domain, apikey)
                    for value in securitytrails_results:
                        file.write(value + "\n")
                else:
                    print("\t\033[1;31m[!] No apikey set for securitytrails.com")
                    con -= 1
            except requests.RequestException:
                print(
                    "\t\033[1;31m[!] Could not get results from securitytrails.com, check your apikey or something."  # noqa: E501
                )
                con -= 1
                pass

            if con == 4:
                print(f"\033[1;34m[-] {con}/4 Successfully sites queried!!")
            else:
                print(f"\033[1;34m[-] {con}/4 Successfully sites queried!!")

        try:
            system(f"cat data.txt | sort -u > {filename} && rm data.txt")
        except:  # noqa: E722
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--domain", required=True, type=str, dest="domain", help="domain name"
    )
    parser.add_argument(
        "-o", "--output", required=True, type=str, dest="output", help="output filename"
    )
    parser.add_argument(
        "-k", "--key", type=str, dest="key", help="apikey for securitytrails"
    )
    arg = parser.parse_args()

    run = GsubFinder()
    if arg.domain and arg.output and not arg.key:
        run.saving_results(arg.domain, arg.output)
    if arg.domain and arg.output and arg.key:
        run.saving_results(arg.domain, arg.output, arg.key)

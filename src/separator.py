#!/usr/bin/python3

from sys import argv

with open(argv[1], "r") as rfile:
    for domains in rfile.readlines():
        if domains.startswith("*."):
            with open("wildcard_domain.txt", "a+") as wfile:
                wfile.write(f"{domains.strip()}\n")
        else:
            with open("domain.txt", "a+") as wfile:
                wfile.write(f"{domains.strip()}\n")

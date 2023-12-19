import httpx
import asyncio
import argparse
from sys import exit
from termcolor import colored
from os import path


async def check_domain_status(domain):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            url_http = f"http://{domain}"
            url_https = f"https://{domain}"
            try:
                response_http = await client.get(url_http, timeout=5)
                if response_http.status_code == 200:
                    print(f"Live: {domain}")
                    return True
            except Exception:
                pass
            try:
                response_https = await client.get(url_https, timeout=5)
                if response_https.status_code == 200:
                    print(f"Live: {domain}")
                    return True
            except Exception:
                pass
            print(f"Dead: {domain}")
            return False
    except asyncio.TimeoutError:
        print(f"Timeout: {domain}")
        return False


async def shodan(file, flive):
    print(colored("\n[>>] Checking Dead domains for Live IP\n", "red"))
    dicdata = {}
    with open(f"{file}", "r") as rfile:
        for domain in rfile.readlines():
            try:
                async with httpx.AsyncClient(verify=False) as client:
                    try:
                        url = f"https://api.shodan.io/shodan/host/search?key=aGplIL53fsxry9ljOOMAJOr6U7MLabVP&query=ssl.cert.subject.CN:{domain.strip()}&facets=country"
                        response = await client.get(url, timeout=5)
                    except httpx.ReadTimeout:
                        response = await client.get(url, timeout=10)
                    jdata = response.json()
                    try:
                        if jdata["total"] != 0:
                            for x in jdata["matches"]:
                                dicdata.update({x["ip_str"]: x["hostnames"]})
                            for i in dicdata.keys():
                                if domain.strip() in dicdata[i]:
                                    with open(flive, "+a") as ipfile:
                                        ipfile.write(
                                            f"{i} : {domain.strip()}\n\t{dicdata[i]}\n"
                                        )
                                    print(f"{i} : {domain.strip()}\n\t{dicdata[i]}")
                        else:
                            print(f"{domain.strip()} is fully dead")
                    except KeyError:
                        pass
            except asyncio.TimeoutError:
                ...


async def shodan_live(lfile, dfile, flive):
    print(colored("\n[>>] Checking Live domains for IP & Dead domains\n", "red"))
    dicdata = {}
    with open(f"{lfile}", "r") as rfile:
        for domain in rfile.readlines():
            try:
                async with httpx.AsyncClient(verify=False) as client:
                    try:
                        url = f"https://api.shodan.io/shodan/host/search?key=aGplIL53fsxry9ljOOMAJOr6U7MLabVP&query=ssl.cert.subject.CN:{domain.strip()}&facets=country"
                        response = await client.get(url, timeout=5)
                    except httpx.ReadTimeout:
                        response = await client.get(url, timeout=10)
                    jdata = response.json()
                    try:
                        with open(dfile, "r") as rfile:
                            for ddomain in rfile.readlines():
                                if jdata["total"] != 0:
                                    for x in jdata["matches"]:
                                        dicdata.update({x["ip_str"]: x["hostnames"]})
                                    for i in dicdata.keys():
                                        if ddomain.strip() in dicdata[i]:
                                            with open(flive, "+a") as ipfile:
                                                ipfile.write(
                                                    f"{i} : {ddomain.strip()}\n\t{dicdata[i]}\n"
                                                )
                                            print(
                                                f"{i} : {ddomain.strip()}\n\t{dicdata[i]}"
                                            )
                                else:
                                    print(f"{ddomain.strip()} is fully dead")
                    except KeyError:
                        pass
            except asyncio.TimeoutError:
                ...


async def main(input_file):
    live, dead, live_ip = "live_domains.txt", "dead_domains.txt", "live_ip.txt"
    with open(input_file, "r") as file:
        domains = file.read().splitlines()
    for domain in domains:
        if await check_domain_status(domain):
            with open(live, "a+") as file:
                file.write(domain + "\n")
        else:
            with open(dead, "a+") as file:
                file.write(domain + "\n")
    await shodan(dead, live_ip)
    await shodan_live(live, dead, live_ip)
    if path.exists(live_ip):
        print(
            colored(
                f"[>>] Results Saved In :\n\t{live}\n\t{dead}\n\t{live_ip}",
                "green",
            )
        )
    else:
        print(
            colored(
                "[!] No live Ip Found For The Dead Domains",
                "red",
            )
        )
        print(
            colored(
                f"[>>] Results Saved In :\n\t{live}\n\t{dead}",
                "green",
            )
        )


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-l",
            "--list",
            required=True,
            dest="input_file",
            help="The name of the text file containing domains (e.g., domains.txt)",
        )
        args = parser.parse_args()
        if args.input_file:
            input_file = args.input_file
            asyncio.run(main(input_file))
    except KeyboardInterrupt:
        exit

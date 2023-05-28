#!/usr/bin/python3

import os
import sys
import requests
import argparse


class CRT_SH:
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-d",
            "--domain",
            dest="domain",
            type=str,
            required=True,
            help="target domain.",
        )
        parser.add_argument(
            "-o", "--output", dest="output", type=str, help="output file."
        )
        parser.add_argument(
            "-w",
            "--wildcard",
            dest="wildcard",
            action="store_true",
            help="wildcard subdomains only.",
        )
        parser.add_argument(
            "-s",
            dest="notwildcard",
            action="store_true",
            help="subdomains without wildcard only.",
        )
        return parser.parse_args()

    def offload(self):
        arg = self.parse_args()
        try:
            crt_result, status_code = self.main(arg.domain)

            if status_code != 200:
                print(f"[>] HTTP/HTTPS error code: {status_code}")
                sys.exit()

            else:
                for subdomain in crt_result:
                    with open(".raw_data.txt", "a") as raw:
                        raw.write(subdomain + "\n")
                os.system(
                    "cat .raw_data.txt | sort -u > .sorted_data.txt && rm .raw_data.txt"
                )

                result = []
                with open(".sorted_data.txt", "r") as sorted_data:
                    for line in sorted_data.readlines():
                        result.append(line)

                # For all the subdomains
                if (
                    arg.domain
                    and not arg.wildcard
                    and not arg.output
                    and not arg.notwildcard
                ):
                    for subdomain in result:
                        print(subdomain.strip())

                # For all the subdomains saved in a file
                if (
                    arg.domain
                    and arg.output
                    and not arg.wildcard
                    and not arg.notwildcard
                ):
                    for subdomain in result:
                        with open(f"{arg.output}", "a") as o:
                            o.write(subdomain)
                    print(f"[-] Results saved to {arg.output}")

                # For all the wildcard subdomains saved in a file
                if arg.domain and arg.wildcard and arg.output and not arg.notwildcard:
                    for subdomain in result:
                        if subdomain.startswith("*."):
                            with open(f"{arg.output}", "a") as i:
                                i.write(subdomain)
                    print(f"[-] Results saved to {arg.output}")

                # For all the subdomains without the wildcard subdomains saved in a file
                if arg.domain and arg.notwildcard and arg.output and not arg.wildcard:
                    for subdomain in result:
                        if not subdomain.startswith("*."):
                            with open(f"{arg.output}", "a") as i:
                                i.write(subdomain)
                    print(f"[-] Results saved to {arg.output}")

                # For all the wildcard subdomains
                if (
                    arg.domain
                    and arg.wildcard
                    and not arg.output
                    and not arg.notwildcard
                ):
                    for subdomain in result:
                        if subdomain.startswith("*."):
                            print(subdomain.strip())

                # For all the subdomains without the wildcard subdomains
                if (
                    arg.domain
                    and arg.notwildcard
                    and not arg.output
                    and not arg.wildcard
                ):
                    for subdomain in result:
                        if not subdomain.startswith("*."):
                            print(subdomain.strip())

                os.remove(".sorted_data.txt")
        except Exception as err:
            print(f"[!] Failed : {err}\n\t[!] Try again!!")
            sys.exit()

    def main(self, domain):
        try:
            url = f"https://crt.sh/?q={domain}&output=json"
            response = requests.get(url)
            subdomains = []
            for entry in response.json():
                data = entry["name_value"]
                subdomains.append(data)
            return subdomains, response.status_code
        except Exception as err:
            print(f"[!] Failed : {err}\n\t[!] Try again!!")
            sys.exit()


if __name__ == "__main__":
    run = CRT_SH()
    run.offload()

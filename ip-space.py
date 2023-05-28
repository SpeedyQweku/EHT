import requests
from bs4 import BeautifulSoup
import re
import argparse


class IP_SPACE:
    def get_arg(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-a", "--asn", type=str, dest="asn", required=True, help="input the ASN"
        )
        parser.add_argument(
            "-o", "--output", type=str, dest="output", help="output file"
        )

        arg = parser.parse_args()
        return arg

    def main(self):
        args = self.get_arg()
        try:
            url = f"https://www.radb.net/query?advanced_query=1&keywords={args.asn}&-T+option=&ip_option=&-i=1&-i+option=origin"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            ip_regex = r"([0-9.]+){4}/[0-9]+"
            code_result = soup.find_all("code")
            data = []
            result = set()
            for code_raw in code_result:
                data.append(code_raw.text)
            for raw in data:
                try:
                    raw_data = re.search(ip_regex, raw)
                    result.add(raw_data.group(0))
                except:  # noqa: E722
                    pass
            if len(result) > 0:
                for line in result:
                    print(line)
                    if args.output:
                        with open(args.output, "a") as output_file:
                            output_file.write(line + "\n")
                if args.output:
                    print(f"\n[-] Results saved to {args.output}")
        except Exception as err:
            print(err)


if __name__ == "__main__":
    run = IP_SPACE()
    run.main()

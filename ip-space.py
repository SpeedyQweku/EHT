import requests
from bs4 import BeautifulSoup
import re


def get_unique_ips(asn):
    try:
        url = f"https://www.radb.net/query?advanced_query=1&keywords={asn}&-T+option=&ip_option=&-i=1&-i+option=origin"
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
                with open("result.txt", "a") as f:
                    f.write(line + "\n")
            print("[>] All Done, Sir!")
    except Exception as err:
        print(err)


asn = input("[~] Enter ASN : ")
unique_ips = get_unique_ips(asn)

import re
import requests
import yaml
import argparse
from tqdm import tqdm
from requests.exceptions import RequestException

MAX_RETRIES = 2


def yaml_file(yaml_filename):
    with open(yaml_filename, "r") as file:
        data = yaml.safe_load(file)
    risk = data["risk"]
    rules = data["rules"]

    for rule in rules:
        rule_id = rule["id"]
        reason = rule["reason"]
        detections = rule["detections"]

        try:
            for detection in detections:
                if detection.startswith("RegexSearch"):
                    detection_parts = detection.split(",", 1)
                elif "RegexSearch" in detection:
                    keyword_index = detection.index("RegexSearch")
                    detection_parts = detection[keyword_index:].split(",", 1)
                if len(detection_parts) == 2:
                    if detection_parts[1].strip().startswith('"'):
                        regex = detection_parts[1].strip().split('"', 1)
                    if detection_parts[1].strip().startswith("'"):
                        regex = detection_parts[1].strip().split("'", 1)
                    if len(regex) == 2:
                        if regex[1].endswith('")'):
                            pattern = regex[1].replace('")', "")
                        if regex[1].endswith("')"):
                            pattern = regex[1].replace("')", "")

                result = {
                    "id": rule_id,
                    "risk": risk,
                    "reason": reason,
                    "pattern": pattern,
                }
                yield result
        except UnboundLocalError:
            pass


def check_api_key_patterns(urls, yaml_filename):
    detections = []

    def RegexSearch(pattern, string):
        return re.search(pattern, string)

    rules = yaml_file(yaml_filename)

    with tqdm(
        total=len(urls), ncols=80, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
    ) as pbar:
        for url in urls:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    response = make_http_request(url)
                    break
                except RequestException:
                    retries += 1
                    continue

            else:
                pbar.set_postfix(skip="True")
                pbar.update(1)
                continue

            for rule in rules:
                try:
                    detected_keys = RegexSearch(rule["pattern"], response)
                    if detected_keys:
                        detections.append(
                            {
                                "url": url,
                                "id": rule["id"],
                                "risk": rule["risk"],
                                "reason": rule["reason"],
                                "key": detected_keys.group(0)
                            }
                        )
                except re.error:
                    pass

            pbar.set_postfix(skip="False")
            pbar.update(1)

    return detections


def make_http_request(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def main(filename, yaml_filename):
    with open(filename, "r") as file:
        urls = [line.strip() for line in file.readlines()]

    api_key_detections = check_api_key_patterns(urls, yaml_filename)
    for detection in api_key_detections:
        print(
            f'URL: {detection["url"]}\nAPI Key ID: {detection["id"]}\nRisk: {detection["risk"]}\nReason: {detection["reason"]}\nKey: {detection["key"]}\n'  # noqa: E501
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        dest="url",
        type=str,
        required=True,
        help="file containing the list of URLs",
    )
    parser.add_argument(
        "-y",
        "--yaml",
        dest="yaml",
        type=str,
        required=True,
        help="yaml file containing the rules",
    )

    arg = parser.parse_args()

    if arg.url and arg.yaml:
        main(arg.url, arg.yaml)

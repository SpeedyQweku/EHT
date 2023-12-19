#!/usr/bin/python3

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", dest="wordlist", type=str, required=True, help="your wordlist"
    )
    parser.add_argument(
        "-d", dest="domain", type=str, required=True, help="The * domain"
    )
    parser.add_argument("-o", dest="output", type=str, help="The output file")
    arg = parser.parse_args()

    with open(arg.wordlist, "r") as word_list:
        for line in word_list:
            try:
                subdomain = arg.domain.replace("*", line.strip())
                print(subdomain)
                if arg.output:
                    with open(arg.output, "a") as save_file:
                        save_file.write(subdomain + "\n")
            except:  # noqa: E722
                pass

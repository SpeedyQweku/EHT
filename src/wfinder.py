#!/usr/bin/python3

import argparse


class WFINDER:
    def get_args(self):
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-s",
            "--startwith",
            dest="startwith",
            type=str,
            help="returns the line starting with the specified string.",
        )
        group.add_argument(
            "-e",
            "--endwith",
            dest="endwith",
            type=str,
            help="returns the line ending with the specified string.",
        )
        parser.add_argument(
            "-o", "--output", dest="output", type=str, help="output file."
        )
        parser.add_argument(
            "-f", "--file", dest="file", required=True, type=str, help="input file."
        )

        args = parser.parse_args()
        return args

    def main(self):
        args = self.get_args()

        # Start with
        if args.file and args.startwith or args.output:
            with open(args.file) as input_file:
                for lines in input_file.readlines():
                    try:
                        line = lines.strip()
                        if line.startswith(args.startwith):
                            if args.output:
                                with open(args.output, "a") as output_file:
                                    output_file.write(line + "\n")
                            else:
                                print(line)
                    except Exception as err:
                        print(err)

        # end with
        if args.file and args.endwith or args.output:
            with open(args.file) as input_file:
                for lines in input_file.readlines():
                    try:
                        line = lines.strip()
                        if line.endswith(args.endwith):
                            if args.output:
                                with open(args.output, "a") as output_file:
                                    output_file.write(line + "\n")
                            else:
                                print(line)
                    except Exception as err:
                        print(err)


if __name__ == "__main__":
    run = WFINDER()
    run.main()

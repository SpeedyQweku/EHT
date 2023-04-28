import sys

arg = sys.argv
with open(arg[1]) as f:
    for lines in f.readlines():
        line = lines.strip("\n")
        if line.startswith("https://"):
            with open("HttpsSub", "a") as fws:
                fws.write(line + "\n")
        else:
            with open("HttpSub", "a") as fw:
                fw.write(line + "\n")
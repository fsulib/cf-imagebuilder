import json
import sys

with open(sys.argv[1], "r", encoding="utf8") as infile:
    jsonin = json.load(infile)
    print(json.dumps(jsonin).replace('"','\\"'))
